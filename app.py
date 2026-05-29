"""
Demo Interativa — Multi-Modalidade em Imagem Médica

Versão com máscaras reais de massas mamárias e extração de features morfológicas.

Simulação pedagógica:
- não treina modelos;
- não usa probabilidades clínicas reais;
- não deve ser usada para diagnóstico.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image
from skimage.measure import label, regionprops, perimeter


st.set_page_config(
    page_title="Demo Multimodalidade em Imagem Médica",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# FUNÇÕES PARA MÁSCARAS
# ============================================================

def list_mask_files(mask_dir: Path) -> list[Path]:
    """Lista máscaras disponíveis."""

    if not mask_dir.exists():
        return []

    files = []
    for extension in ["*.png", "*.jpg", "*.jpeg"]:
        files.extend(mask_dir.glob(extension))

    return sorted(files)


def load_mask(mask_path: Path, output_size: int = 128) -> np.ndarray:
    """
    Carrega uma máscara, recorta a região da massa e redimensiona.

    Assume fundo preto e massa em branco/tons claros.
    """

    image = Image.open(mask_path).convert("L")
    mask = np.array(image).astype(float)

    if mask.max() > 0:
        mask = mask / mask.max()

    binary = mask > 0.5

    if not binary.any():
        return np.zeros((output_size, output_size), dtype=bool)

    rows, cols = np.where(binary)
    y_min, y_max = rows.min(), rows.max()
    x_min, x_max = cols.min(), cols.max()

    height = y_max - y_min + 1
    width = x_max - x_min + 1
    margin = int(0.35 * max(height, width))

    y_min = max(0, y_min - margin)
    y_max = min(binary.shape[0], y_max + margin)
    x_min = max(0, x_min - margin)
    x_max = min(binary.shape[1], x_max + margin)

    cropped = binary[y_min:y_max, x_min:x_max]
    cropped_img = Image.fromarray((cropped.astype(np.uint8) * 255))
    cropped_img.thumbnail((output_size, output_size), Image.Resampling.NEAREST)

    canvas = Image.new("L", (output_size, output_size), 0)
    x_offset = (output_size - cropped_img.width) // 2
    y_offset = (output_size - cropped_img.height) // 2
    canvas.paste(cropped_img, (x_offset, y_offset))

    return np.array(canvas) > 127


def create_synthetic_scan_from_mask(
    lesion_mask: np.ndarray,
    seed: int = 0,
    lesion_visible: bool = True,
) -> np.ndarray:
    """
    Cria uma imagem sintética com ruído usando a forma da máscara como lesão.
    """

    rng = np.random.default_rng(seed)
    size = lesion_mask.shape[0]

    img = rng.normal(0.45, 0.08, (size, size))

    yy, xx = np.mgrid[:size, :size]
    organ = (xx - size // 2) ** 2 + (yy - size // 2) ** 2 < (size * 0.36) ** 2
    img[organ] += 0.08

    if lesion_visible and lesion_mask.any():
        img[lesion_mask] += 0.35

    return np.clip(img, 0, 1)


# ============================================================
# FEATURES MORFOLÓGICAS
# ============================================================

def extract_mask_features(mask: np.ndarray) -> dict:
    """
    Extrai features morfológicas simples da máscara.

    Estas features não são usadas como diagnóstico clínico.
    Servem apenas para uma regra pedagógica de classificação.
    """

    if not mask.any():
        return {
            "area_pixels": 0.0,
            "area_ratio": 0.0,
            "perimeter": 0.0,
            "circularity": 0.0,
            "solidity": 0.0,
            "eccentricity": 0.0,
            "major_axis_length": 0.0,
            "minor_axis_length": 0.0,
            "axis_ratio": 0.0,
            "irregularity": 0.0,
        }

    labelled = label(mask)
    regions = regionprops(labelled)

    # Caso existam várias regiões, usar a maior.
    region = max(regions, key=lambda r: r.area)

    area = float(region.area)
    total_area = float(mask.shape[0] * mask.shape[1])
    area_ratio = area / total_area

    perim = float(perimeter(mask, neighborhood=8))

    if perim > 0:
        circularity = float((4 * np.pi * area) / (perim ** 2))
        irregularity = float((perim ** 2) / (4 * np.pi * area))
    else:
        circularity = 0.0
        irregularity = 0.0

    solidity = float(region.solidity)
    eccentricity = float(region.eccentricity)
    major_axis = float(region.major_axis_length)
    minor_axis = float(region.minor_axis_length)

    if minor_axis > 0:
        axis_ratio = major_axis / minor_axis
    else:
        axis_ratio = 0.0

    return {
        "area_pixels": area,
        "area_ratio": area_ratio,
        "perimeter": perim,
        "circularity": circularity,
        "solidity": solidity,
        "eccentricity": eccentricity,
        "major_axis_length": major_axis,
        "minor_axis_length": minor_axis,
        "axis_ratio": axis_ratio,
        "irregularity": irregularity,
    }


def morphology_score(features: dict, lesion_visible: bool) -> float:
    """
    Estimativa simulada baseada nas features morfológicas da máscara.

    Regra pedagógica:
    - menor circularidade aumenta a suspeição;
    - menor solidez aumenta a suspeição;
    - maior excentricidade aumenta a suspeição;
    - maior irregularidade aumenta a suspeição.

    Os pesos são arbitrários e servem apenas para demonstração.
    """

    if not lesion_visible:
        return 0.25

    circularity = features["circularity"]
    solidity = features["solidity"]
    eccentricity = features["eccentricity"]
    irregularity = features["irregularity"]

    # Componentes normalizadas de forma simples.
    low_circularity_component = np.clip(1.0 - circularity, 0.0, 1.0)
    low_solidity_component = np.clip(1.0 - solidity, 0.0, 1.0)
    eccentricity_component = np.clip(eccentricity, 0.0, 1.0)
    irregularity_component = np.clip((irregularity - 1.0) / 2.0, 0.0, 1.0)

    score = (
        0.25
        + 0.25 * low_circularity_component
        + 0.20 * low_solidity_component
        + 0.15 * eccentricity_component
        + 0.15 * irregularity_component
    )

    return float(np.clip(score, 0.01, 0.99))


# ============================================================
# CLASSIFICAÇÃO SIMULADA
# ============================================================

def clinical_only_prediction(
    age_group: str,
    family_history: bool,
    weight_loss: bool,
    previous_cancer: bool,
) -> float:
    """
    Estimativa simulada baseada apenas nos dados clínicos.

    Os pesos são arbitrários e servem apenas para demonstração.
    """

    score = 0.20

    if age_group == "40–59":
        score += 0.10
    elif age_group == "60+":
        score += 0.18

    if family_history:
        score += 0.16

    if weight_loss:
        score += 0.18

    if previous_cancer:
        score += 0.22

    return float(min(score, 0.99))


def multimodal_prediction(image_score: float, clinical_score: float) -> float:
    """
    Estimativa simulada combinando morfologia da máscara e dados clínicos.

    Média ponderada:
    - 60% morfologia da máscara;
    - 40% dados clínicos.
    """

    return float(min((0.60 * image_score) + (0.40 * clinical_score), 0.99))


def classify(score: float, threshold: float = 0.50) -> str:
    """Classificação simplificada."""

    return "Elevada suspeição simulada" if score >= threshold else "Baixa suspeição simulada"


def yes_no(value: bool) -> str:
    """Converte booleanos em Sim/Não."""

    return "Sim" if value else "Não"


def explain_morphology(features: dict) -> str:
    """Explicação curta baseada nas features."""

    circularity = features["circularity"]
    solidity = features["solidity"]
    eccentricity = features["eccentricity"]

    notes = []

    if circularity < 0.60:
        notes.append("a forma é pouco circular")
    else:
        notes.append("a forma é relativamente circular")

    if solidity < 0.85:
        notes.append("a lesão parece ter contorno mais irregular/recortado")
    else:
        notes.append("a lesão parece ter contorno relativamente compacto")

    if eccentricity > 0.75:
        notes.append("a lesão é mais alongada")
    else:
        notes.append("a lesão não é muito alongada")

    return "Com base na máscara, " + ", ".join(notes) + "."


def interpret_results(
    image_score: float,
    clinical_score: float,
    multimodal_score: float,
) -> str:
    """Interpretação pedagógica das três estimativas."""

    if classify(image_score) != classify(multimodal_score):
        return (
            "A combinação multimodal alterou a classificação em relação "
            "ao modelo baseado apenas na morfologia da máscara."
        )

    if classify(clinical_score) != classify(multimodal_score):
        return (
            "A combinação multimodal alterou a classificação em relação "
            "ao modelo baseado apenas nos dados clínicos."
        )

    return (
        "As três estimativas apontam para uma classificação semelhante. "
        "Isto pode acontecer quando as modalidades transmitem sinais compatíveis."
    )


# ============================================================
# INTERFACE
# ============================================================

st.title("Demo Interativa — Multi-Modalidade em Imagem Médica")

st.markdown(
    """
Esta demo usa uma **máscara real de uma massa mamária** para gerar uma imagem
sintética com ruído. A classificação visual é baseada em **features
morfológicas extraídas da máscara**, sem treinar qualquer modelo.

A comparação inclui:

1. **apenas máscara/morfologia**;
2. **apenas dados clínicos**;
3. **máscara/morfologia + dados clínicos**.
"""
)

st.warning(
    "Esta aplicação é apenas uma simulação pedagógica. "
    "Não representa um modelo clínico real, não deve ser usada para diagnóstico "
    "e os valores apresentados não correspondem a probabilidades clínicas reais."
)

MASK_DIR = Path(__file__).parent / "masks"
mask_files = list_mask_files(MASK_DIR)

if not mask_files:
    st.error(
        "Não foram encontradas máscaras na pasta 'masks/'. "
        "Adicione ficheiros .png, .jpg ou .jpeg e volte a correr a app."
    )
    st.stop()

st.sidebar.header("Parâmetros da simulação")

seed = st.sidebar.slider(
    "Semente aleatória",
    min_value=0,
    max_value=100,
    value=2,
    help="Controla a escolha da máscara e o ruído sintético.",
)

rng = np.random.default_rng(seed)
selected_mask = mask_files[int(rng.integers(0, len(mask_files)))]

lesion_visible = st.sidebar.checkbox(
    "Massa visível",
    value=True,
    help="Se desativado, a estimativa visual baixa, simulando ausência de sinal visual.",
)

st.sidebar.subheader("Dados clínicos simulados")

age_group = st.sidebar.selectbox(
    "Grupo etário",
    ["<40", "40–59", "60+"],
    index=1,
)

family_history = st.sidebar.checkbox("Histórico familiar", value=False)
weight_loss = st.sidebar.checkbox("Perda de peso", value=False)
previous_cancer = st.sidebar.checkbox("Histórico pessoal de cancro", value=False)

lesion_mask = load_mask(selected_mask, output_size=128)
features = extract_mask_features(lesion_mask)

img = create_synthetic_scan_from_mask(
    lesion_mask=lesion_mask,
    seed=seed,
    lesion_visible=lesion_visible,
)

image_score = morphology_score(
    features=features,
    lesion_visible=lesion_visible,
)

clinical_score = clinical_only_prediction(
    age_group=age_group,
    family_history=family_history,
    weight_loss=weight_loss,
    previous_cancer=previous_cancer,
)

multimodal_score = multimodal_prediction(
    image_score=image_score,
    clinical_score=clinical_score,
)

col1, col2 = st.columns([1.05, 1.15])

with col1:
    st.subheader("Imagem sintética gerada a partir da máscara")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(img, cmap="gray", vmin=0, vmax=1)
    ax.set_title("Imagem simulada com ruído")
    ax.axis("off")
    st.pyplot(fig, clear_figure=True)

    with st.expander("Ver máscara usada nesta simulação"):
        fig_mask, ax_mask = plt.subplots(figsize=(4, 4))
        ax_mask.imshow(lesion_mask, cmap="gray")
        ax_mask.set_title(selected_mask.name)
        ax_mask.axis("off")
        st.pyplot(fig_mask, clear_figure=True)

with col2:
    st.subheader("Dados clínicos simulados")

    st.markdown(
        f"""
| Variável clínica | Valor |
|---|---:|
| Grupo etário | {age_group} |
| Histórico familiar | {yes_no(family_history)} |
| Perda de peso | {yes_no(weight_loss)} |
| Histórico pessoal de cancro | {yes_no(previous_cancer)} |
"""
    )

    st.subheader("Resultados da classificação simulada")

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric("Máscara/morfologia", f"{image_score:.2f}")
    metric_col1.caption(classify(image_score))

    metric_col2.metric("Dados clínicos", f"{clinical_score:.2f}")
    metric_col2.caption(classify(clinical_score))

    metric_col3.metric("Multimodal", f"{multimodal_score:.2f}")
    metric_col3.caption(classify(multimodal_score))

    st.info(
        interpret_results(
            image_score=image_score,
            clinical_score=clinical_score,
            multimodal_score=multimodal_score,
        )
    )

st.divider()

st.subheader("Features extraídas da máscara")

feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

feature_col1.metric("Área relativa", f"{features['area_ratio']:.3f}")
feature_col2.metric("Circularidade", f"{features['circularity']:.3f}")
feature_col3.metric("Solidez", f"{features['solidity']:.3f}")
feature_col4.metric("Excentricidade", f"{features['eccentricity']:.3f}")

feature_col5, feature_col6, feature_col7, feature_col8 = st.columns(4)

feature_col5.metric("Perímetro", f"{features['perimeter']:.1f}")
feature_col6.metric("Irregularidade", f"{features['irregularity']:.3f}")
feature_col7.metric("Eixo maior", f"{features['major_axis_length']:.1f}")
feature_col8.metric("Razão eixos", f"{features['axis_ratio']:.2f}")

st.caption(explain_morphology(features))

st.divider()

st.subheader("Comparação das três estimativas")

labels = [
    "Máscara/morfologia",
    "Dados clínicos",
    "Multimodal",
]

values = [image_score, clinical_score, multimodal_score]

fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
ax_bar.bar(labels, values)
ax_bar.axhline(0.50, linestyle="--", linewidth=1)
ax_bar.set_ylim(0, 1)
ax_bar.set_ylabel("Estimativa simulada")
ax_bar.set_title("Comparação entre modalidades")
st.pyplot(fig_bar, clear_figure=True)

st.caption("A linha tracejada representa o limiar pedagógico de classificação: 0.50.")

st.divider()

st.subheader("Como interpretar esta demo")

st.markdown(
    """
Nesta versão, a componente visual é baseada em **features morfológicas extraídas
da máscara**. Isto aproxima a demo de uma lógica de análise quantitativa, mas
continua a ser uma simulação.

A classificação baseada na máscara considera, de forma simplificada, que massas
menos circulares, menos sólidas, mais alongadas ou mais irregulares podem
aumentar a suspeição simulada.

A classificação clínica usa fatores clínicos simulados.  
A classificação multimodal combina as duas estimativas.
"""
)

with st.expander("Ver regras simplificadas usadas na simulação"):
    st.markdown(
        """
### Score morfológico

O score começa em 0.25 e pode aumentar com:

```text
menor circularidade
menor solidez
maior excentricidade
maior irregularidade
```

### Score clínico

```text
estimativa_clinica = 0.20
+ idade 40–59: 0.10
+ idade 60+: 0.18
+ histórico familiar: 0.16
+ perda de peso: 0.18
+ histórico pessoal de cancro: 0.22
```

### Score multimodal

```text
estimativa_multimodal = 0.60 × estimativa_morfologica
                     + 0.40 × estimativa_clinica
```

### Classificação

```text
score < 0.50  → Baixa suspeição simulada
score >= 0.50 → Elevada suspeição simulada
```

Estes valores são arbitrários e não têm significado clínico real.
"""
    )

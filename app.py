"""
Demo Interativa — Multi-Modalidade em Imagem Médica

Versão com máscaras reais de massas mamárias.
Simulação pedagógica, sem treino de modelos.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Demo Multimodalidade em Imagem Médica",
    page_icon="🧠",
    layout="wide",
)


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


def image_only_prediction(lesion_visible: bool) -> float:
    """Estimativa simulada baseada apenas na imagem/máscara."""

    return 0.62 if lesion_visible else 0.38


def clinical_only_prediction(
    smoker: bool,
    weight_loss: bool,
    previous_cancer: bool,
) -> float:
    """Estimativa simulada baseada apenas nos dados clínicos."""

    score = 0.25

    if smoker:
        score += 0.18

    if weight_loss:
        score += 0.22

    if previous_cancer:
        score += 0.25

    return min(score, 0.99)


def multimodal_prediction(image_score: float, clinical_score: float) -> float:
    """
    Estimativa simulada combinando imagem/máscara e dados clínicos.

    Média ponderada:
    - 60% imagem/máscara;
    - 40% dados clínicos.
    """

    return min((0.60 * image_score) + (0.40 * clinical_score), 0.99)


def classify(score: float, threshold: float = 0.50) -> str:
    """Classificação simplificada."""

    return "Elevada suspeição simulada" if score >= threshold else "Baixa suspeição simulada"


def yes_no(value: bool) -> str:
    """Converte booleanos em Sim/Não."""

    return "Sim" if value else "Não"


def interpret_results(
    image_score: float,
    clinical_score: float,
    multimodal_score: float,
) -> str:
    """Interpretação pedagógica das três estimativas."""

    if classify(image_score) != classify(multimodal_score):
        return (
            "A combinação multimodal alterou a classificação em relação "
            "ao modelo baseado apenas na imagem/máscara."
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


st.title("Demo Interativa — Multi-Modalidade em Imagem Médica")

st.markdown(
    """
Esta demo usa uma **máscara real de uma massa mamária** para gerar uma imagem
sintética com ruído. A classificação continua a ser simulada, tal como na demo
original.

A comparação inclui:

1. **apenas imagem/máscara**;
2. **apenas dados clínicos**;
3. **imagem/máscara + dados clínicos**.
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
    help="Mantém a lógica da demo original: presença/ausência de alteração visual.",
)

smoker = st.sidebar.checkbox("Fumador/a", value=False)
weight_loss = st.sidebar.checkbox("Perda de peso", value=False)
previous_cancer = st.sidebar.checkbox("Histórico de cancro", value=False)

lesion_mask = load_mask(selected_mask, output_size=128)

img = create_synthetic_scan_from_mask(
    lesion_mask=lesion_mask,
    seed=seed,
    lesion_visible=lesion_visible,
)

image_score = image_only_prediction(lesion_visible)

clinical_score = clinical_only_prediction(
    smoker=smoker,
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
| Fumador/a | {yes_no(smoker)} |
| Perda de peso | {yes_no(weight_loss)} |
| Histórico de cancro | {yes_no(previous_cancer)} |
"""
    )

    st.subheader("Resultados da classificação simulada")

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric("Apenas imagem/máscara", f"{image_score:.2f}")
    metric_col1.caption(classify(image_score))

    metric_col2.metric("Apenas dados clínicos", f"{clinical_score:.2f}")
    metric_col2.caption(classify(clinical_score))

    metric_col3.metric("Imagem/máscara + dados clínicos", f"{multimodal_score:.2f}")
    metric_col3.caption(classify(multimodal_score))

    st.info(
        interpret_results(
            image_score=image_score,
            clinical_score=clinical_score,
            multimodal_score=multimodal_score,
        )
    )

st.divider()

st.subheader("Comparação das três estimativas")

labels = [
    "Apenas imagem/máscara",
    "Apenas dados clínicos",
    "Imagem/máscara + dados clínicos",
]

values = [image_score, clinical_score, multimodal_score]

fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
ax_bar.bar(labels, values)
ax_bar.axhline(0.50, linestyle="--", linewidth=1)
ax_bar.set_ylim(0, 1)
ax_bar.set_ylabel("Estimativa simulada")
ax_bar.set_title("Comparação entre modalidades")
ax_bar.tick_params(axis="x", rotation=15)
st.pyplot(fig_bar, clear_figure=True)

st.caption("A linha tracejada representa o limiar pedagógico de classificação: 0.50.")

st.divider()

st.subheader("Como interpretar esta demo")

st.markdown(
    """
Nesta versão, a componente visual é representada por uma **máscara real de uma
massa mamária**. A máscara é usada apenas para dar uma forma realista à lesão
numa imagem sintética com ruído.

Isto permite manter a simplicidade da demo original, sem treinar modelos e sem
usar imagens clínicas reais completas.

A máscara representa a morfologia da massa, mas não inclui textura, intensidade,
contexto anatómico, margens no tecido envolvente ou outros elementos relevantes
da imagem médica original.

Os valores numéricos são simulados e foram escolhidos apenas para fins
pedagógicos.
"""
)

with st.expander("Ver fórmulas simplificadas usadas na simulação"):
    st.markdown(
        """
### Apenas imagem/máscara

```text
0.62 se a massa estiver visível
0.38 se a massa não estiver visível
```

### Apenas dados clínicos

```text
estimativa_clinica = 0.25
+ 0.18 se fumador/a
+ 0.22 se existir perda de peso
+ 0.25 se existir histórico de cancro
```

### Imagem/máscara + dados clínicos

```text
estimativa_multimodal = 0.60 × estimativa_imagem
                     + 0.40 × estimativa_clinica
```

### Classificação

```text
score < 0.50  → Baixa suspeição simulada
score >= 0.50 → Elevada suspeição simulada
```

Estes valores não têm significado clínico real.
"""
    )

st.divider()

st.subheader("Referências científicas sugeridas")

st.markdown(
    """
- Huang, S. C., Pareek, A., Seyyedi, S., Banerjee, I., & Lungren, M. P. (2020).  
  “Fusion of Medical Imaging and Electronic Health Records Using Deep Learning: A Systematic Review and Implementation Guidelines.”  
  *npj Digital Medicine*, 3, 136.

- Sun, Z., Lin, M., Zhu, Q., Xie, Q., Wang, F., Lu, Z., & Peng, Y. (2023).  
  “A Scoping Review on Multimodal Deep Learning in Biomedical Images and Texts.”  
  *Journal of Biomedical Informatics*, 146, 104482.

- Moor, M., Banerjee, O., Abad, Z. S. H., et al. (2023).  
  “Foundation Models for Generalist Medical Artificial Intelligence.”  
  *Nature*, 616, 259–265.

- Acosta, J. N., Falcone, G. J., Rajpurkar, P., & Topol, E. J. (2022).  
  “Multimodal Biomedical AI.”  
  *Nature Medicine*, 28, 1773–1784.
"""
)

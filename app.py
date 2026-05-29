"""
Demo Interativa — Multi-Modalidade em Imagem Médica

Esta aplicação é uma simulação pedagógica.
Não representa um modelo clínico real e não deve ser usada para diagnóstico.
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Demo Multimodalidade em Imagem Médica",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# FUNÇÕES DA DEMO
# ============================================================

def generate_scan(seed: int = 0, suspicious: bool = False) -> np.ndarray:
    """
    Gera uma imagem médica sintética.

    Parameters
    ----------
    seed:
        Semente para garantir reprodutibilidade.
    suspicious:
        Se True, adiciona uma região circular mais intensa,
        simulando uma possível lesão.

    Returns
    -------
    np.ndarray
        Imagem sintética normalizada entre 0 e 1.
    """

    rng = np.random.default_rng(seed)
    img = rng.normal(0.45, 0.08, (128, 128))

    yy, xx = np.mgrid[:128, :128]

    # Criar uma estrutura circular que representa, de forma simplificada, um órgão.
    organ = (xx - 64) ** 2 + (yy - 64) ** 2 < 45 ** 2
    img[organ] += 0.08

    # Criar uma possível lesão.
    if suspicious:
        lesion = (xx - 80) ** 2 + (yy - 55) ** 2 < 10 ** 2
        img[lesion] += 0.35

    return np.clip(img, 0, 1)


def image_only_prediction(suspicious: bool) -> float:
    """
    Estimativa simulada baseada apenas na imagem.

    Esta função não é um modelo real.
    Os valores foram escolhidos apenas para fins pedagógicos.
    """

    return 0.62 if suspicious else 0.38


def clinical_only_prediction(
    smoker: bool,
    weight_loss: bool,
    previous_cancer: bool,
) -> float:
    """
    Estimativa simulada baseada apenas nos dados clínicos.

    Esta função ignora completamente a imagem.
    Os pesos são arbitrários e servem apenas para demonstração.
    """

    score = 0.25

    if smoker:
        score += 0.18

    if weight_loss:
        score += 0.22

    if previous_cancer:
        score += 0.25

    return min(score, 0.99)


def multimodal_prediction(
    image_score: float,
    clinical_score: float,
) -> float:
    """
    Estimativa simulada combinando imagem e dados clínicos.

    Nesta versão, a estimativa multimodal é uma média ponderada:
    - 60% imagem;
    - 40% dados clínicos.

    Estes pesos são arbitrários e servem apenas para fins pedagógicos.
    """

    score = (0.60 * image_score) + (0.40 * clinical_score)

    return min(score, 0.99)


def classify(score: float, threshold: float = 0.50) -> str:
    """
    Classificação simplificada baseada numa estimativa numérica.
    """

    if score >= threshold:
        return "Elevada suspeição simulada"

    return "Baixa suspeição simulada"


def yes_no(value: bool) -> str:
    """Converte valores booleanos em Sim/Não."""

    return "Sim" if value else "Não"


def interpret_results(
    image_score: float,
    clinical_score: float,
    multimodal_score: float,
) -> str:
    """
    Produz uma interpretação simples das três estimativas.
    """

    scores = {
        "imagem": image_score,
        "dados clínicos": clinical_score,
        "combinação multimodal": multimodal_score,
    }

    highest_source = max(scores, key=scores.get)

    if classify(image_score) != classify(multimodal_score):
        return (
            "A combinação multimodal alterou a classificação em relação "
            "ao modelo baseado apenas na imagem."
        )

    if classify(clinical_score) != classify(multimodal_score):
        return (
            "A combinação multimodal alterou a classificação em relação "
            "ao modelo baseado apenas nos dados clínicos."
        )

    return (
        f"As três estimativas apontam para uma classificação semelhante. "
        f"A estimativa mais elevada veio de: {highest_source}."
    )


# ============================================================
# INTERFACE
# ============================================================

st.title("Demo Interativa — Multi-Modalidade em Imagem Médica")

st.markdown(
    """
Esta demo mostra, de forma simplificada, como diferentes fontes de informação
podem produzir estimativas distintas.

A comparação inclui:

1. **apenas imagem**;
2. **apenas dados clínicos**;
3. **imagem + dados clínicos**.
"""
)

st.warning(
    "Esta aplicação é apenas uma simulação pedagógica. "
    "Não representa um modelo clínico real, não deve ser usada para diagnóstico "
    "e os valores apresentados não correspondem a probabilidades clínicas reais."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Parâmetros da simulação")

suspicious = st.sidebar.checkbox(
    "Lesão visível",
    value=True,
)

smoker = st.sidebar.checkbox(
    "Fumador/a",
    value=False,
)

weight_loss = st.sidebar.checkbox(
    "Perda de peso",
    value=False,
)

previous_cancer = st.sidebar.checkbox(
    "Histórico de cancro",
    value=False,
)

seed = st.sidebar.slider(
    "Semente da imagem sintética",
    min_value=0,
    max_value=100,
    value=2,
    help="Permite gerar variações visuais da imagem sintética.",
)


# ============================================================
# CÁLCULOS
# ============================================================

img = generate_scan(
    seed=seed,
    suspicious=suspicious,
)

image_score = image_only_prediction(suspicious)

clinical_score = clinical_only_prediction(
    smoker=smoker,
    weight_loss=weight_loss,
    previous_cancer=previous_cancer,
)

multimodal_score = multimodal_prediction(
    image_score=image_score,
    clinical_score=clinical_score,
)


# ============================================================
# VISUALIZAÇÃO PRINCIPAL
# ============================================================

col1, col2 = st.columns([1.05, 1.15])

with col1:
    st.subheader("Imagem médica sintética")

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(img, cmap="gray", vmin=0, vmax=1)
    ax.set_title("Imagem simulada")
    ax.axis("off")

    st.pyplot(fig, clear_figure=True)

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

    metric_col1.metric(
        label="Apenas imagem",
        value=f"{image_score:.2f}",
    )
    metric_col1.caption(classify(image_score))

    metric_col2.metric(
        label="Apenas dados clínicos",
        value=f"{clinical_score:.2f}",
    )
    metric_col2.caption(classify(clinical_score))

    metric_col3.metric(
        label="Imagem + dados clínicos",
        value=f"{multimodal_score:.2f}",
    )
    metric_col3.caption(classify(multimodal_score))

    st.info(
        interpret_results(
            image_score=image_score,
            clinical_score=clinical_score,
            multimodal_score=multimodal_score,
        )
    )


# ============================================================
# COMPARAÇÃO VISUAL DOS SCORES
# ============================================================

st.divider()

st.subheader("Comparação das três estimativas")

labels = [
    "Apenas imagem",
    "Apenas dados clínicos",
    "Imagem + dados clínicos",
]

values = [
    image_score,
    clinical_score,
    multimodal_score,
]

fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
ax_bar.bar(labels, values)
ax_bar.axhline(0.50, linestyle="--", linewidth=1)
ax_bar.set_ylim(0, 1)
ax_bar.set_ylabel("Estimativa simulada")
ax_bar.set_title("Comparação entre modalidades")
ax_bar.tick_params(axis="x", rotation=15)

st.pyplot(fig_bar, clear_figure=True)

st.caption(
    "A linha tracejada representa o limiar pedagógico de classificação: 0.50."
)


# ============================================================
# EXPLICAÇÃO PEDAGÓGICA
# ============================================================

st.divider()

st.subheader("Como interpretar esta demo")

st.markdown(
    """
O primeiro valor representa uma estimativa construída apenas a partir da
imagem. O segundo valor representa uma estimativa construída apenas com
dados clínicos simulados. O terceiro valor combina as duas fontes de
informação.

Na prática clínica, uma imagem médica é geralmente interpretada em conjunto
com outros dados: sintomas, idade, antecedentes, análises laboratoriais,
relatórios anteriores ou informação genética. Esta integração de várias
fontes de informação é a base dos modelos multimodais em medicina.

Nesta demo, os pesos atribuídos a cada variável são intencionais e
arbitrários. Servem apenas para tornar visível a ideia de que cada
modalidade pode contribuir de forma diferente para a estimativa final.
"""
)

with st.expander("Ver fórmulas simplificadas usadas na simulação"):
    st.markdown(
        """
### Apenas imagem

```text
0.62 se existir lesão visível
0.38 se não existir lesão visível
```

### Apenas dados clínicos

```text
estimativa_clinica = 0.25
+ 0.18 se fumador/a
+ 0.22 se existir perda de peso
+ 0.25 se existir histórico de cancro
```

### Imagem + dados clínicos

```text
estimativa_multimodal = 0.60 × estimativa_imagem
                     + 0.40 × estimativa_clinica
```

### Classificação

```text
score < 0.50  → Baixa suspeição simulada
score >= 0.50 → Elevada suspeição simulada
```

Mais uma vez: estes valores não têm significado clínico real.
"""
    )


# ============================================================
# REFERÊNCIAS
# ============================================================

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

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


def multimodal_prediction(
    image_score: float,
    smoker: bool,
    weight_loss: bool,
    previous_cancer: bool,
) -> float:
    """
    Estimativa simulada combinando imagem e dados clínicos.

    Esta função não é um modelo real.
    Os pesos atribuídos às variáveis clínicas são arbitrários.
    """

    score = image_score

    if smoker:
        score += 0.12

    if weight_loss:
        score += 0.10

    if previous_cancer:
        score += 0.15

    return min(score, 0.99)


def yes_no(value: bool) -> str:
    """Converte valores booleanos em Sim/Não."""

    return "Sim" if value else "Não"


def interpret_difference(image_score: float, multimodal_score: float) -> str:
    """
    Produz uma interpretação simples da diferença entre as estimativas.
    """

    difference = abs(multimodal_score - image_score)

    if difference > 0.15:
        return (
            "A informação clínica alterou de forma relevante "
            "a estimativa de risco simulada."
        )

    return (
        "Neste exemplo, a imagem teve maior peso na estimativa final simulada."
    )


# ============================================================
# INTERFACE
# ============================================================

st.title("Demo Interativa — Multi-Modalidade em Imagem Médica")

st.markdown(
    """
Esta demo mostra, de forma simplificada, como uma estimativa baseada apenas
numa imagem pode mudar quando são adicionados dados clínicos.

**Mensagem principal:** multi-modalidade significa combinar diferentes tipos
de informação, como imagem médica, texto clínico e dados estruturados.
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

multimodal_score = multimodal_prediction(
    image_score=image_score,
    smoker=smoker,
    weight_loss=weight_loss,
    previous_cancer=previous_cancer,
)

difference = multimodal_score - image_score


# ============================================================
# VISUALIZAÇÃO PRINCIPAL
# ============================================================

col1, col2 = st.columns([1.1, 1])

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

    st.subheader("Estimativas simuladas")

    metric_col1, metric_col2 = st.columns(2)

    metric_col1.metric(
        label="Apenas imagem",
        value=f"{image_score:.2f}",
    )

    metric_col2.metric(
        label="Multimodal",
        value=f"{multimodal_score:.2f}",
        delta=f"{difference:+.2f}",
    )

    st.progress(float(multimodal_score))

    st.info(interpret_difference(image_score, multimodal_score))


# ============================================================
# EXPLICAÇÃO PEDAGÓGICA
# ============================================================

st.divider()

st.subheader("Como interpretar esta demo")

st.markdown(
    """
O primeiro valor representa uma estimativa construída apenas a partir da
imagem. O segundo valor combina essa estimativa com fatores clínicos
simulados.

Na prática clínica, uma imagem médica é geralmente interpretada em conjunto
com outros dados: sintomas, idade, antecedentes, análises laboratoriais,
relatórios anteriores ou informação genética. Esta integração de várias
fontes de informação é a base dos modelos multimodais em medicina.

Nesta demo, os pesos atribuídos a cada variável clínica são intencionais e
arbitrários. Servem apenas para tornar visível a ideia de que o contexto
clínico pode modificar a interpretação de uma imagem.
"""
)

with st.expander("Ver fórmula simplificada usada na simulação"):
    st.markdown(
        """
A estimativa multimodal é calculada assim:

```text
estimativa_multimodal = estimativa_imagem
```

Depois são acrescentados incrementos simulados:

```text
+ 0.12 se fumador/a
+ 0.10 se existir perda de peso
+ 0.15 se existir histórico de cancro
```

O valor final é limitado a 0.99.

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

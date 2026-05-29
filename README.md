# Demo Interativa — Multi-Modalidade em Imagem Médica

Esta aplicação demonstra, de forma pedagógica, o conceito de **multi-modalidade em imagem médica**.

Nesta versão, a imagem sintética usa uma **máscara real de uma massa mamária**. A aplicação escolhe aleatoriamente uma máscara da pasta `masks/`, recorta a região da massa, redimensiona-a e usa a sua forma para criar uma lesão numa imagem sintética com ruído.

O objetivo continua a ser simples:

1. mostrar que a informação visual pode ser ambígua;
2. mostrar que dados clínicos adicionais podem alterar a estimativa;
3. comparar três cenários:
   - apenas imagem/máscara;
   - apenas dados clínicos;
   - imagem/máscara + dados clínicos.

> **Nota importante:** esta aplicação é apenas uma simulação educativa.  
> Não representa um modelo clínico real, não deve ser usada para diagnóstico e os valores apresentados não correspondem a probabilidades clínicas reais.

---

## Estrutura dos ficheiros

```text
multimodal_medical_demo/
├── app.py
├── requirements.txt
├── README.md
└── masks/
    ├── 20587994_mask.png
    ├── 20588046_mask.png
    └── 20587902_mask.png
```

Pode adicionar mais máscaras à pasta `masks/`.

---

## Como instalar

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Instalar os requisitos:

```bash
pip install -r requirements.txt
```

---

## Como correr a aplicação

Na pasta do projeto:

```bash
streamlit run app.py
```

---

## Como adicionar mais máscaras

Coloque os ficheiros de máscara na pasta:

```text
masks/
```

Formatos recomendados:

```text
.png
.jpg
.jpeg
```

As máscaras devem ter fundo preto e a região da massa a branco ou em tons claros.

A aplicação irá:

1. escolher uma máscara da pasta;
2. recortar automaticamente a região da massa;
3. redimensioná-la;
4. inseri-la numa imagem sintética com ruído;
5. calcular classificações simuladas.

---

## O que a aplicação mostra

A aplicação compara três estimativas simuladas:

1. **Apenas imagem/máscara**  
   Usa a presença da massa representada pela máscara.

2. **Apenas dados clínicos**  
   Usa apenas fatores clínicos simulados.

3. **Imagem/máscara + dados clínicos**  
   Combina a estimativa visual com a estimativa clínica.

---

## Limitações da demo

Esta aplicação:

- não treina nenhum modelo de inteligência artificial;
- não usa a imagem médica original, apenas a máscara da massa;
- não estima risco clínico verdadeiro;
- usa pesos arbitrários apenas para fins didáticos;
- não deve ser usada para apoio à decisão clínica.

As máscaras representam apenas a forma da massa. Não incluem textura, intensidade, contexto anatómico, margens no tecido envolvente ou outros elementos importantes da imagem médica real.

---

## Referências científicas sugeridas

- Huang, S. C., Pareek, A., Seyyedi, S., Banerjee, I., & Lungren, M. P. (2020). “Fusion of Medical Imaging and Electronic Health Records Using Deep Learning: A Systematic Review and Implementation Guidelines.” *npj Digital Medicine*, 3, 136.

- Sun, Z., Lin, M., Zhu, Q., Xie, Q., Wang, F., Lu, Z., & Peng, Y. (2023). “A Scoping Review on Multimodal Deep Learning in Biomedical Images and Texts.” *Journal of Biomedical Informatics*, 146, 104482.

- Moor, M., Banerjee, O., Abad, Z. S. H., et al. (2023). “Foundation Models for Generalist Medical Artificial Intelligence.” *Nature*, 616, 259–265.

- Acosta, J. N., Falcone, G. J., Rajpurkar, P., & Topol, E. J. (2022). “Multimodal Biomedical AI.” *Nature Medicine*, 28, 1773–1784.

# Demo Interativa — Multi-Modalidade em Imagem Médica

Esta pequena aplicação demonstra, de forma pedagógica, o conceito de **multi-modalidade em imagem médica**.

O objetivo é mostrar que:

1. Uma imagem médica isolada pode ser ambígua;
2. Dados clínicos adicionais podem alterar uma estimativa de risco;
3. Um modelo multimodal combina diferentes fontes de informação, por exemplo:
   - imagem médica;
   - dados clínicos estruturados;
   - texto clínico;
   - histórico do/a paciente.

> **Nota importante:** esta aplicação é apenas uma simulação educativa.  
> Não representa um modelo clínico real, não deve ser usada para diagnóstico e os valores apresentados não correspondem a probabilidades clínicas reais.

---

## Estrutura dos ficheiros

```text
multimodal_medical_demo/
├── app.py
├── requirements.txt
└── README.md
```

---

## Como instalar

Criar um ambiente virtual, se necessário:

```bash
python -m venv venv
```

Ativar o ambiente virtual:

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

Na pasta do projeto, executar:

```bash
streamlit run app.py
```

Depois, abrir o endereço indicado no terminal, normalmente:

```text
http://localhost:8501
```

---

## O que a aplicação mostra

A aplicação gera uma imagem médica sintética com ruído e uma estrutura circular que representa, de forma simplificada, um órgão.

O utilizador pode ativar ou desativar:

- lesão visível;
- tabagismo;
- perda de peso;
- histórico de cancro.

A aplicação compara duas estimativas:

1. **Modelo apenas com imagem**  
   Usa apenas a presença ou ausência de uma alteração visual na imagem sintética.

2. **Modelo multimodal**  
   Combina a estimativa baseada na imagem com fatores clínicos simulados.

---

## Mensagem pedagógica principal

A imagem médica raramente existe isoladamente na prática clínica.  
A interpretação de uma imagem pode mudar quando se consideram sintomas, antecedentes, fatores de risco e outra informação clínica.

A multi-modalidade procura precisamente integrar diferentes tipos de dados para apoiar uma interpretação mais contextualizada.

---

## Limitações da demo

Esta aplicação:

- não usa dados reais;
- não treina nenhum modelo de inteligência artificial;
- não usa imagens clínicas reais;
- não estima risco clínico verdadeiro;
- usa pesos arbitrários apenas para fins didáticos.

Os valores foram escolhidos para tornar o efeito da informação clínica visível durante a demonstração.

---

## Possíveis usos em aula ou apresentação

Esta demo pode ser usada para introduzir temas como:

- inteligência artificial em saúde;
- imagem médica;
- modelos multimodais;
- integração de dados clínicos;
- apoio à decisão clínica;
- riscos de interpretação baseada apenas numa modalidade de dados.

---

## Referências científicas sugeridas

- Huang, S. C., Pareek, A., Seyyedi, S., Banerjee, I., & Lungren, M. P. (2020). “Fusion of Medical Imaging and Electronic Health Records Using Deep Learning: A Systematic Review and Implementation Guidelines.” *npj Digital Medicine*, 3, 136.

- Sun, Z., Lin, M., Zhu, Q., Xie, Q., Wang, F., Lu, Z., & Peng, Y. (2023). “A Scoping Review on Multimodal Deep Learning in Biomedical Images and Texts.” *Journal of Biomedical Informatics*, 146, 104482.

- Moor, M., Banerjee, O., Abad, Z. S. H., et al. (2023). “Foundation Models for Generalist Medical Artificial Intelligence.” *Nature*, 616, 259–265.

- Acosta, J. N., Falcone, G. J., Rajpurkar, P., & Topol, E. J. (2022). “Multimodal Biomedical AI.” *Nature Medicine*, 28, 1773–1784.

---

## Licença

Este exemplo pode ser usado livremente para fins educativos.

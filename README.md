# Demo Interativa — Multi-Modalidade em Imagem Médica

Esta aplicação demonstra, de forma pedagógica, o conceito de **multi-modalidade em imagem médica**.

Nesta versão, a aplicação usa **máscaras reais de massas mamárias** e extrai automaticamente algumas **features morfológicas** da máscara. A classificação visual usa uma regra simples baseada na forma da lesão.

A classificação é simulada e pedagógica.

---

## Objetivo pedagógico

Mostrar que:

1. uma imagem ou máscara isolada pode ser ambígua;
2. características morfológicas da lesão podem influenciar a estimativa visual;
3. dados clínicos adicionais podem alterar a estimativa;
4. a combinação de imagem/morfologia + dados clínicos é um exemplo simples de multimodalidade.

---

## Features extraídas da máscara

A aplicação calcula automaticamente:

- área relativa da massa;
- perímetro;
- circularidade;
- solidez;
- excentricidade;
- razão entre eixo maior e eixo menor;
- score de irregularidade.

Estas features são usadas para criar uma classificação simulada baseada apenas na morfologia da máscara.

---

## Classificações apresentadas

A aplicação compara três estimativas simuladas:

1. **Apenas máscara / morfologia**  
   Usa features extraídas da máscara.

2. **Apenas dados clínicos**  
   Usa fatores clínicos simulados.

3. **Máscara + dados clínicos**  
   Combina a estimativa morfológica com a estimativa clínica.

---

## Limitações

Esta aplicação:

- não treina nenhum modelo de inteligência artificial;
- não usa imagens médicas originais completas;
- usa apenas máscaras de segmentação;
- não estima risco clínico verdadeiro;
- usa regras arbitrárias apenas para fins didáticos;
- não deve ser usada para apoio à decisão clínica.

As máscaras representam apenas a forma da massa. Não incluem textura, intensidade, contexto anatómico, margens no tecido envolvente ou outros elementos importantes da imagem médica real.

---

## Nota ética e clínica

Esta aplicação serve apenas para ensino.  
Não deve ser interpretada como ferramenta de diagnóstico, triagem ou apoio clínico.

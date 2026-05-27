# 💳 CREDIT RISK ANALYTICS

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![Status](https://img.shields.io/badge/STATUS-CONCLUÍDO-green?style=for-the-badge)

## 📌 Descrição do Projeto

Este projeto foi desenvolvido como parte da disciplina de **Projeto Final de Engenharia de Computação**. A solução aborda o problema de **predição de inadimplência em carteiras de crédito**, utilizando um pipeline completo de Engenharia de Dados, Análise Estatística, Machine Learning e Business Intelligence.

O sistema analisa **5.000 perfis de clientes** com variáveis socioeconômicas, comportamento de pagamento e histórico de crédito, entregando um dashboard interativo com simulação OLAP e um agente de IA generativa capaz de transformar dados em recomendações executivas de negócio.

---

## 👥 Equipe

* **Davi Teramoto Matheus** - 082220036
* **Gustavo Henrique Portari de Oliveira** - 082210041
* **João Vitor Antunes Nascimento** - 082210016
* **Leonardo de Carlos Rodrigues** - 082220038

---

## 🚀 Entregas e Metodologia

### M1: Data Engineering (Pipeline ETL)

Estruturação de um pipeline robusto para geração, transformação e armazenamento de dados de crédito.

- **Arquitetura:** Implementação de **Star Schema** com 1 tabela Fato e 3 tabelas Dimensão.
- **Tabelas:**
  - `fato_default` — transações, valor de fatura, pagamento, inadimplência, score de risco
  - `dim_cliente` — idade, faixa etária, gênero, escolaridade, estado civil
  - `dim_produto` — limite de crédito, faixa de limite, tipo de cartão
  - `dim_tempo` — mês/ano, trimestre, semestre
- **Armazenamento:** Estrutura de camadas `raw/` e `processed/` com arquivos `.csv`.
- **Tecnologias:** Python, Pandas, NumPy, Google Colab.

### M2: Exploratory Data Analysis (EDA)

Exploração estatística para identificação de padrões de inadimplência.

- **Análise Univariada:** Distribuição de variáveis como idade, score e limite de crédito (histogramas, boxplots).
- **Análise Multivariada:** Correlação entre variáveis socioeconômicas e probabilidade de default.
- **Insights Chave:**
  - Clientes com **18-25 anos** apresentam taxa de inadimplência ~35% superior à média.
  - **Limite de crédito acima de R$ 60k** correlaciona com scores >700 e menor risco.
  - Portadores de **cartão Standard** concentram 68% dos casos de default.

### M3: Modelagem Preditiva (Machine Learning)

Desenvolvimento de modelos para **classificação binária de default** (inadimplente/adimplente).

| Modelo | Acurácia | F1-Score (default) | AUC-ROC | Status |
|:---|:---|:---|:---|:---|
| Regressão Logística | 0.79 | 0.62 | 0.81 | Baseline |
| Random Forest | 0.84 | 0.71 | 0.88 | Testado |
| **Gradient Boosting (XGBoost)** | **0.87** | **0.76** | **0.91** | **✅ Final** |

- **Modelo Vencedor:** XGBoost — melhor equilíbrio entre precisão e recall na classe minoritária (inadimplentes), com AUC-ROC de 0.91.
- **Features mais importantes:** Score de risco, histórico de pagamento, faixa etária, tipo de cartão.

### M4: Business Insights & GenAI

Transformação de dados preditivos em valor estratégico para o negócio.

- **Dashboards:** Interface Streamlit com 4 abas de análise, 6 KPIs em tempo real e filtros multidimensionais.
- **Simulação OLAP:** Heatmap interativo com slicing & dicing por qualquer combinação de dimensões.
- **Drill-Down:** Análise hierárquica de Anual → Trimestral → Mensal por segmento.
- **Google AI Studio:** Agente especializado em risco de crédito com prompt de sistema customizado para gerar análises qualitativas e planos de ação baseados nos dados filtrados.

---

## 📺 Apresentação e Demonstração

> 🎥 **[ASSISTIR AO VÍDEO DO PITCH (2 MIN)]**
> *Problema de negócio, arquitetura do pipeline e demonstração ao vivo do dashboard.*

> 🤖 **[ACESSAR AGENTE DE INSIGHTS — GOOGLE AI STUDIO]**
> *Interaja com a IA treinada para analisar carteiras de crédito e gerar recomendações.*

> 📊 **[ACESSAR DASHBOARD (STREAMLIT)]**
> *Dashboard interativo com filtros OLAP, KPIs e integração com Gemini.*

---

## 🗂️ Estrutura do Repositório

```
credit-risk-analytics/
│
├── 📁 data/
│   ├── generate_data.py          # Script de geração dos dados sintéticos
│   └── processed/
│       ├── dim_cliente.csv       # Dimensão Cliente
│       ├── dim_produto.csv       # Dimensão Produto/Crédito
│       ├── dim_tempo.csv         # Dimensão Tempo
│       └── fato_default.csv      # Tabela Fato (Star Schema)
│
├── 📁 notebooks/
│   ├── M1_ETL_Pipeline.ipynb     # Engenharia de Dados
│   ├── M2_EDA_Analysis.ipynb     # Análise Exploratória
│   └── M3_ML_Modeling.ipynb      # Machine Learning
│
├── 📁 dashboards/
│   └── app.py                    # Dashboard Streamlit (M4)
│
├── 📁 prompts/
│   └── gemini_system_prompt.md   # Prompt de sistema do Agente IA
│
├── 📁 docs_finais/
│   └── [slides, relatório final]
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Como Reproduzir

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/credit-risk-analytics.git
cd credit-risk-analytics

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Gere os dados sintéticos
python data/generate_data.py

# 4. Execute o dashboard
streamlit run dashboards/app.py
```

> **Nota:** Para ativar o Agente de IA, obtenha uma chave gratuita em [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) e insira na sidebar do dashboard.

---

## 📊 Principais KPIs Monitorados

| KPI | Valor (dataset completo) | Referência de Mercado |
|:---|:---|:---|
| Taxa de Inadimplência | ~20.7% | SFN: ~5-8% (cartão) |
| Score de Risco Médio | ~610 / 850 | Bom: >650 |
| Cobertura de Pagamento | ~72% | Saudável: >80% |
| Volume Total de Crédito | ~R$ 220M | — |

---

## 🧠 Arquitetura do Sistema

```
[Fonte de Dados]          [ETL]              [Storage]
  Dataset Kaggle    →   Pandas/Python   →   CSV / Drive
  (UCI Credit)         Star Schema           raw/ processed/

[Analytics]             [ML]               [BI + GenAI]
  EDA (M2)        →   XGBoost (M3)   →   Streamlit (M4)
  Correlação           AUC: 0.91          Dashboard OLAP
  Outliers             F1: 0.76           Gemini Insights
```

---

<p align="center">
  <img src="https://faculdadesalvadorarena.org.br/wp-content/uploads/2022/07/logo_fesa.png" width="200" alt="Logo Faculdade Engenheiro Salvador Arena"><br>
  <b>Faculdade Engenheiro Salvador Arena</b><br>
  Curso de Engenharia de Computação | 2026
</p>
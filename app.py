"""
Credit Risk Analytics Dashboard
Faculdade Engenheiro Salvador Arena — Engenharia de Computação
Disciplina: Projeto Final — Entrega M4
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import os

# ── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Customizado ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .main { background-color: #0d1117; }

    .kpi-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: #60a5fa; margin: 0; }
    .kpi-label { font-size: 0.85rem; color: #9ca3af; margin: 0; letter-spacing: 0.05em; }
    .kpi-delta-pos { color: #34d399; font-size: 0.8rem; }
    .kpi-delta-neg { color: #f87171; font-size: 0.8rem; }

    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #e2e8f0;
        border-left: 3px solid #60a5fa; padding-left: 10px;
        margin: 20px 0 10px 0;
    }

    .insight-box {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        color: #e2e8f0;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    div[data-testid="stMetric"] {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ── Carregamento de Dados ─────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    paths = {
        "fato":    os.path.join(base, "data", "processed", "fato_default.csv"),
        "cliente": os.path.join(base, "data", "processed", "dim_cliente.csv"),
        "produto": os.path.join(base, "data", "processed", "dim_produto.csv"),
        "tempo":   os.path.join(base, "data", "processed", "dim_tempo.csv"),
    }
    fato    = pd.read_csv(paths["fato"])
    cliente = pd.read_csv(paths["cliente"])
    produto = pd.read_csv(paths["produto"])
    tempo   = pd.read_csv(paths["tempo"])

    df = (fato
          .merge(cliente, on="id_cliente")
          .merge(produto, on="id_produto")
          .merge(tempo,   on="id_tempo"))
    return df, fato, cliente, produto, tempo


df_full, fato, cliente, produto, tempo = load_data()

# ── Sidebar — Filtros OLAP ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💳 Credit Risk")
    st.markdown("### 🔍 Filtros OLAP")

    anos = sorted(df_full["ano"].unique())
    anos_sel = st.multiselect("Ano", anos, default=anos)

    generos_sel = st.multiselect(
        "Gênero", df_full["genero"].unique(),
        default=list(df_full["genero"].unique())
    )

    escolaridades = sorted(df_full["escolaridade"].unique())
    escolaridade_sel = st.multiselect("Escolaridade", escolaridades, default=escolaridades)

    tipo_cartao_sel = st.multiselect(
        "Tipo de Cartão", df_full["tipo_cartao"].unique(),
        default=list(df_full["tipo_cartao"].unique())
    )

    faixa_etaria_sel = st.multiselect(
        "Faixa Etária", ["18-25","26-35","36-45","46-55","56+"],
        default=["18-25","26-35","36-45","46-55","56+"]
    )

    st.markdown("---")
    st.markdown("### 🤖 API Gemini")
    gemini_key = st.text_input("Chave API Google AI Studio", type="password",
                                placeholder="AIza...")
    st.caption("Obtenha em [aistudio.google.com](https://aistudio.google.com/app/apikey)")


# ── Filtrar DataFrame ─────────────────────────────────────────────────────────
df = df_full[
    df_full["ano"].isin(anos_sel) &
    df_full["genero"].isin(generos_sel) &
    df_full["escolaridade"].isin(escolaridade_sel) &
    df_full["tipo_cartao"].isin(tipo_cartao_sel) &
    df_full["faixa_etaria"].isin(faixa_etaria_sel)
].copy()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_clientes   = len(df)
taxa_inadimplencia = df["inadimplente"].mean()
ticket_medio     = df["valor_fatura"].mean()
score_medio      = df["score_risco"].mean()
cobertura_pag    = (df["valor_pago"] / df["valor_fatura"].replace(0, np.nan)).mean()
volume_credito   = df["limite_credito"].sum()

# ── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#e2e8f0;font-size:2rem;margin-bottom:4px;'>💳 Credit Risk Analytics</h1>"
    "<p style='color:#9ca3af;font-size:0.9rem;margin-top:0;'>Faculdade Engenheiro Salvador Arena "
    "| Projeto Final — M4: Business Intelligence & GenAI</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "👥 Clientes", f"{total_clientes:,}", "base filtrada"),
    (c2, "⚠️ Inadimplência", f"{taxa_inadimplencia:.1%}", "taxa de default"),
    (c3, "💰 Ticket Médio", f"R$ {ticket_medio:,.0f}", "valor médio de fatura"),
    (c4, "📊 Score Médio", f"{score_medio:.0f}", "pontuação de risco"),
    (c5, "✅ Cobertura Pag.", f"{cobertura_pag:.1%}", "pagamento/fatura"),
    (c6, "🏦 Vol. Crédito", f"R$ {volume_credito/1e6:.1f}M", "limite total concedido"),
]
for col, label, value, caption in kpis:
    with col:
        st.metric(label=label, value=value, help=caption)


# ── Aba de Navegação ──────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Visão Geral", "🔬 Análise OLAP", "🗂️ Drill-Down", "🤖 Insights com IA"]
)

DARK_THEME = dict(
    plot_bgcolor="#0d1117", paper_bgcolor="#0d1117",
    font_color="#e2e8f0",
    xaxis=dict(gridcolor="#1f2937", color="#9ca3af"),
    yaxis=dict(gridcolor="#1f2937", color="#9ca3af"),
)
COLORS = px.colors.qualitative.Set2


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Visão Geral
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns(2)

    # Gráfico 1: Inadimplência por Faixa Etária
    with col_a:
        st.markdown("<div class='section-title'>Inadimplência por Faixa Etária</div>",
                    unsafe_allow_html=True)
        agg = (df.groupby("faixa_etaria", observed=True)["inadimplente"]
               .agg(["mean","count"]).reset_index())
        agg.columns = ["faixa_etaria", "taxa", "n"]
        fig = px.bar(agg, x="faixa_etaria", y="taxa",
                     color="taxa", color_continuous_scale="Blues",
                     text=agg["taxa"].apply(lambda x: f"{x:.1%}"),
                     labels={"taxa":"Taxa de Default","faixa_etaria":"Faixa Etária"})
        fig.update_traces(textposition="outside")
        fig.update_coloraxes(showscale=False)
        fig.update_layout(**DARK_THEME, height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico 2: Inadimplência por Tipo de Cartão
    with col_b:
        st.markdown("<div class='section-title'>Distribuição de Default por Cartão</div>",
                    unsafe_allow_html=True)
        agg2 = (df.groupby(["tipo_cartao","inadimplente"])
                .size().reset_index(name="n"))
        agg2["status"] = agg2["inadimplente"].map({0:"Adimplente", 1:"Inadimplente"})
        fig2 = px.bar(agg2, x="tipo_cartao", y="n", color="status",
                      barmode="stack", color_discrete_map={
                          "Adimplente":"#34d399","Inadimplente":"#f87171"},
                      labels={"n":"Clientes","tipo_cartao":"Tipo de Cartão"})
        fig2.update_layout(**DARK_THEME, height=320)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    # Gráfico 3: Evolução Mensal da Taxa de Default
    with col_c:
        st.markdown("<div class='section-title'>Evolução Mensal da Inadimplência</div>",
                    unsafe_allow_html=True)
        monthly = (df.groupby("mes_ano")["inadimplente"]
                   .mean().reset_index().sort_values("mes_ano"))
        fig3 = px.line(monthly, x="mes_ano", y="inadimplente",
                       markers=True, labels={"inadimplente":"Taxa","mes_ano":"Mês"})
        fig3.update_traces(line_color="#60a5fa", marker_color="#f59e0b")
        fig3.update_layout(**DARK_THEME, height=320)
        st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Score de Risco vs Limite de Crédito
    with col_d:
        st.markdown("<div class='section-title'>Score de Risco × Limite de Crédito</div>",
                    unsafe_allow_html=True)
        sample = df.sample(min(800, len(df)), random_state=42)
        fig4 = px.scatter(sample, x="limite_credito", y="score_risco",
                          color="inadimplente",
                          color_discrete_map={0:"#34d399", 1:"#f87171"},
                          opacity=0.6, size_max=6,
                          labels={"limite_credito":"Limite (R$)",
                                  "score_risco":"Score de Risco",
                                  "inadimplente":"Inadimplente"})
        fig4.update_layout(**DARK_THEME, height=320)
        st.plotly_chart(fig4, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Análise OLAP (Slicing & Dicing)
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🔬 Simulação OLAP — Slicing & Dicing")
    st.caption("Cruzamentos multidimensionais para análise de inadimplência.")

    col_x, col_y, col_metric = st.columns(3)
    with col_x:
        dim_x = st.selectbox("Dimensão X (linhas)", ["faixa_etaria","escolaridade",
                                                      "genero","estado_civil","ano"])
    with col_y:
        dim_y = st.selectbox("Dimensão Y (colunas)", ["tipo_cartao","faixa_limite",
                                                       "genero","escolaridade","trimestre"])
    with col_metric:
        metric = st.selectbox("Métrica", ["Taxa de Inadimplência (%)","Score Médio",
                                           "Ticket Médio (R$)","Volume Crédito (R$M)"])

    # Mapeia métrica
    metric_map = {
        "Taxa de Inadimplência (%)": ("inadimplente", "mean"),
        "Score Médio":               ("score_risco",   "mean"),
        "Ticket Médio (R$)":         ("valor_fatura",  "mean"),
        "Volume Crédito (R$M)":      ("limite_credito","sum"),
    }
    col_m, agg_func = metric_map[metric]

    pivot = (df.groupby([dim_x, dim_y], observed=True)[col_m]
             .agg(agg_func).unstack(fill_value=0))

    if "Volume" in metric:
        pivot = pivot / 1e6

    fig_heat = px.imshow(
        pivot, color_continuous_scale="Blues",
        text_auto=".2f",
        labels=dict(x=dim_y.replace("_"," ").title(),
                    y=dim_x.replace("_"," ").title(),
                    color=metric),
        aspect="auto",
    )
    fig_heat.update_layout(**DARK_THEME, height=450)
    st.plotly_chart(fig_heat, use_container_width=True)

    with st.expander("📋 Ver Tabela Pivot"):
        st.dataframe(pivot.style.background_gradient(cmap="Blues"), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Drill-Down
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🗂️ Drill-Down — Do Macro ao Micro")

    drill_nivel = st.radio("Nível de Análise", ["Anual", "Trimestral", "Mensal"],
                            horizontal=True)
    drill_dim   = st.selectbox("Segmentar por", ["escolaridade","faixa_etaria",
                                                   "tipo_cartao","genero"])

    nivel_map = {"Anual":"ano","Trimestral":"trimestre","Mensal":"mes_ano"}
    dim_t = nivel_map[drill_nivel]

    drill_agg = (df.groupby([dim_t, drill_dim], observed=True)["inadimplente"]
                 .mean().reset_index())
    drill_agg.columns = [dim_t, drill_dim, "taxa"]
    drill_agg[dim_t] = drill_agg[dim_t].astype(str)

    fig_drill = px.line(drill_agg, x=dim_t, y="taxa", color=drill_dim,
                        markers=True,
                        labels={"taxa":"Taxa de Default",
                                dim_t: drill_nivel,
                                drill_dim: drill_dim.replace("_"," ").title()})
    fig_drill.update_layout(**DARK_THEME, height=400)
    st.plotly_chart(fig_drill, use_container_width=True)

    st.markdown("#### 📌 KPIs por Segmento")
    seg_kpi = (df.groupby(drill_dim, observed=True)
               .agg(
                   n_clientes=("id_cliente","count"),
                   taxa_default=("inadimplente","mean"),
                   score_medio=("score_risco","mean"),
                   ticket_medio=("valor_fatura","mean"),
               ).reset_index()
               .sort_values("taxa_default", ascending=False))
    seg_kpi["taxa_default"] = seg_kpi["taxa_default"].map("{:.1%}".format)
    seg_kpi["score_medio"]  = seg_kpi["score_medio"].map("{:.0f}".format)
    seg_kpi["ticket_medio"] = seg_kpi["ticket_medio"].map("R$ {:,.0f}".format)
    st.dataframe(seg_kpi, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Insights com IA Generativa
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🤖 Agente de Insights — Google AI Studio (Gemini)")
    st.caption("Cole sua chave API na sidebar para ativar o consultor de IA.")

    # Resumo dos dados para o contexto da IA
    resumo = f"""
RESUMO EXECUTIVO — Credit Risk Analytics
=========================================
Total de Clientes Analisados: {total_clientes:,}
Taxa de Inadimplência:        {taxa_inadimplencia:.2%}
Score de Risco Médio:         {score_medio:.1f} / 850
Ticket Médio de Fatura:       R$ {ticket_medio:,.2f}
Cobertura de Pagamento:       {cobertura_pag:.2%}
Volume Total de Crédito:      R$ {volume_credito:,.0f}

TOP 3 FAIXAS ETÁRIAS COM MAIOR DEFAULT:
{df.groupby('faixa_etaria',observed=True)['inadimplente'].mean()
  .sort_values(ascending=False).head(3)
  .apply(lambda x: f"{x:.1%}").to_string()}

INADIMPLÊNCIA POR TIPO DE CARTÃO:
{df.groupby('tipo_cartao',observed=True)['inadimplente'].mean()
  .sort_values(ascending=False)
  .apply(lambda x: f"{x:.1%}").to_string()}

INADIMPLÊNCIA POR ESCOLARIDADE:
{df.groupby('escolaridade',observed=True)['inadimplente'].mean()
  .sort_values(ascending=False)
  .apply(lambda x: f"{x:.1%}").to_string()}
"""

    st.markdown("**📄 Contexto que será enviado para a IA:**")
    with st.expander("Ver resumo dos dados"):
        st.code(resumo, language="text")

    perguntas_rapidas = [
        "Quais são os 3 maiores riscos identificados nessa carteira de crédito?",
        "Sugira estratégias de retenção para clientes com alto risco de default.",
        "Como a escolaridade impacta o risco de crédito? O que podemos fazer?",
        "Proponha um plano de ação para reduzir a inadimplência em 5 pontos percentuais.",
    ]

    pergunta_sel = st.selectbox("💬 Perguntas rápidas", ["(escolha ou escreva abaixo)"] + perguntas_rapidas)
    pergunta_custom = st.text_area(
        "Ou faça sua própria pergunta:",
        value="" if pergunta_sel == "(escolha ou escreva abaixo)" else pergunta_sel,
        height=80,
        placeholder="Ex: Quais segmentos têm maior potencial de recuperação?"
    )

    if st.button("🚀 Gerar Insight com Gemini", type="primary"):
        if not gemini_key:
            st.warning("⚠️ Insira sua chave de API do Google AI Studio na sidebar!")
        elif not pergunta_custom.strip():
            st.warning("⚠️ Digite uma pergunta antes de gerar o insight.")
        else:
            with st.spinner("Consultando o Agente de IA..."):
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction="""
Você é um consultor sênior de risco de crédito e ciência de dados financeiros com 20 anos de experiência
em instituições bancárias brasileiras. Seu estilo é objetivo, analítico e orientado a resultados.

Ao analisar dados de inadimplência, você sempre:
1. Identifica os principais vetores de risco com evidências quantitativas.
2. Propõe planos de ação SMART (Específicos, Mensuráveis, Alcançáveis, Relevantes, Temporais).
3. Usa linguagem executiva, adequada para apresentações ao conselho de administração.
4. Contextualiza os achados dentro do cenário macroeconômico brasileiro quando relevante.
5. Formata a resposta com seções claras: Diagnóstico, Insights-Chave e Plano de Ação.
"""
                    )
                    prompt = f"{resumo}\n\nPERGUNTA DO USUÁRIO:\n{pergunta_custom}"
                    response = model.generate_content(prompt)
                    st.markdown("**🤖 Resposta do Agente de Insights:**")
                    st.markdown(
                        f"<div class='insight-box'>{response.text}</div>",
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Erro ao chamar a API Gemini: {e}")

    st.markdown("---")
    st.markdown(
        "💡 **Prompt de Sistema usado no Gemini** — "
        "[Ver configuração completa no Google AI Studio](https://aistudio.google.com/app/prompts)"
    )

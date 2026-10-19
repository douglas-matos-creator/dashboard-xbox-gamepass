import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Xbox Game Pass",
    page_icon="🎮",
    layout="wide"
)

# Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('xbox_game_pass.csv')

df = carregar_dados()

# Título
st.title("🎮 Dashboard de Análise de Retenção & Churn - Xbox Game Pass")
st.markdown("Monitorização de engajamento dos jogadores, cancelamentos por plano e dispositivo.")

# Filtros na Barra Lateral
st.sidebar.header("🔍 Filtros")
plano_selecionado = st.sidebar.multiselect(
    "Selecione o Plano:",
    options=df['Plano'].unique(),
    default=df['Plano'].unique()
)

dispositivo_selecionado = st.sidebar.multiselect(
    "Selecione o Dispositivo:",
    options=df['Dispositivo_Principal'].unique(),
    default=df['Dispositivo_Principal'].unique()
)

# Aplicar Filtros
df_filtrado = df[
    (df['Plano'].isin(plano_selecionado)) & 
    (df['Dispositivo_Principal'].isin(dispositivo_selecionado))
]

# Indicadores (KPIs)
st.subheader("📊 Métricas de Desempenho")
col1, col2, col3, col4 = st.columns(4)

total_users = len(df_filtrado)
cancelados = len(df_filtrado[df_filtrado['Status'] == 'Cancelado'])
taxa_churn = (cancelados / total_users * 100) if total_users > 0 else 0
media_horas = df_filtrado['Horas_Jogadas_Mes'].mean() if total_users > 0 else 0

col1.metric("Total de Jogadores", total_users)
col2.metric("Assinaturas Ativas", total_users - cancelados)
col3.metric("Taxa de Churn", f"{taxa_churn:.1f}%")
col4.metric("Média de Horas/Mês", f"{media_horas:.1f} h")

st.markdown("---")

# Gráficos
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("🚨 Taxa de Churn por Plano")
    df_churn_plano = df_filtrado.groupby('Plano')['Status'].value_counts(normalize=True).unstack().get('Cancelado', pd.Series(0, index=df_filtrado['Plano'].unique())) * 100
    fig_plano = px.bar(
        df_churn_plano.reset_index(),
        x='Plano',
        y='Cancelado',
        labels={'Cancelado': 'Churn (%)', 'Plano': 'Plano'},
        color='Cancelado',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_plano, width='stretch')

with col_g2:
    st.subheader("⏱️ Horas Jogadas vs Status da Conta")
    fig_box = px.box(
        df_filtrado,
        x='Status',
        y='Horas_Jogadas_Mes',
        color='Status',
        labels={'Horas_Jogadas_Mes': 'Horas/Mês'},
        color_discrete_map={'Ativo': '#0e7a0d', 'Cancelado': '#d9534f'}
    )
    st.plotly_chart(fig_box, width='stretch')

# Tabela Detalhada
st.subheader("📋 Base de Dados Filtrada")
st.dataframe(df_filtrado, width='stretch')
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import zipfile

# Carregando a imagem do repositório
image_path = "cases_percap.png"
st.image(image_path, use_column_width=True)

st.title("COVID-19 Dashboard")
st.markdown(
    "### Objetivo do Dash: Análise interativa dos dados de COVID-19\nAlunos: Olavo Ferraz(ofn@cesar.school) e Victor Silva(vrss@cesar.school)"
)

zip_path = "COVID-19 Activity.zip"
# Caminho para o arquivo zipado
zip_path = "COVID-19 Activity.zip"

# Abrindo o arquivo zip e lendo o CSV dentro dele
with zipfile.ZipFile(zip_path, "r") as z:
    with z.open("COVID-19 Activity.csv") as f:
        df = pd.read_csv(f, low_memory=False, dtype=str)

df = df.dropna()

# Widgets (Componentes de Entrada do Usuário)
st.sidebar.title("Filtros")
sel_ano = st.sidebar.radio(
    label="Selecione o ano:", options=[2020, 2021, 2022], index=0
)
st.write("Você selecionou:", sel_ano)

jan_1 = datetime.date(sel_ano, 1, 1)
dec_31 = datetime.date(sel_ano, 12, 31)

d = st.date_input(
    "Selecione as datas para análise:",
    (jan_1, datetime.date(sel_ano, 12, 31)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)

# Formatando as datas para exibição
data1 = d[0]
data2 = d[1]
formatted_data1 = data1.strftime("%d/%m/%Y")
formatted_data2 = data2.strftime("%d/%m/%Y")

st.write(f"As datas escolhidas foram: {formatted_data1} até {formatted_data2}")

# Convertendo para o formato YYYY-MM-DD para filtrar o DataFrame
start_date = data1.strftime("%Y-%m-%d")
end_date = data2.strftime("%Y-%m-%d")

# Renomear colunas para português-br
df = df.rename(
    columns={
        "PEOPLE_POSITIVE_CASES_COUNT": "CASOS_POSITIVOS_TOTAL",
        "PEOPLE_POSITIVE_NEW_CASES_COUNT": "NOVOS_CASOS_POSITIVOS",
        "PEOPLE_DEATH_COUNT": "MORTES_TOTAL",
        "PEOPLE_DEATH_NEW_COUNT": "NOVAS_MORTES",
        "REPORT_DATE": "DATA_REPORTE",
        "COUNTY_NAME": "NOME_CONDADO",
        "PROVINCE_STATE_NAME": "NOME_ESTADO",
        "CONTINENT_NAME": "NOME_CONTINENTE",
        "DATA_SOURCE_NAME": "FONTE_DADOS",
        "COUNTY_FIPS_NUMBER": "NUMERO_FIPS_CONDADO",
        "COUNTRY_ALPHA_3_CODE": "CODIGO_PAIS_ALPHA_3",
        "COUNTRY_SHORT_NAME": "NOME_PAIS_CURTO",
        "COUNTRY_ALPHA_2_CODE": "CODIGO_PAIS_ALPHA_2",
    }
)

df["DATA_REPORTE"] = pd.to_datetime(df["DATA_REPORTE"])
filtered_df = df[(df["DATA_REPORTE"] >= start_date) & (df["DATA_REPORTE"] <= end_date)]

# Seleção de condados
unique_counties = df["NOME_CONDADO"].unique()
selected_counties = st.sidebar.multiselect(
    label="Selecione os condados para análise:",
    options=unique_counties.tolist(),
    default=None,
)

# Filtra o DataFrame com base na seleção dos condados
if selected_counties:
    filtered_df = filtered_df[filtered_df["NOME_CONDADO"].isin(selected_counties)]
else:
    st.warning("Por favor, selecione pelo menos um condado para análise.")

# Seleção de eixo X para os gráficos (Data ou Condado)
x_axis_option = st.sidebar.selectbox(
    label="Selecione o eixo X:",
    options=["DATA_REPORTE", "NOME_CONDADO"],
    index=0
)

# Geração dos gráficos com base na seleção dos condados e categorias
if not filtered_df.empty:
    st.write("### Gráfico de Linha - Evolução de Casos Positivos Totais X Condado")
    fig = px.bar(
        filtered_df,
        x=x_axis_option,
        y="CASOS_POSITIVOS_TOTAL",
        color="NOME_CONDADO",
        title="Evolução dos Casos Positivos Totais",
        labels={x_axis_option: "Cidades ou Data", "CASOS_POSITIVOS_TOTAL": "Casos Positivos Totais"},
        barmode='group'
    )
    st.plotly_chart(fig)

    st.write("### Gráfico de Linha - Evolução de Novos Casos Positivos")
    fig = px.bar(
        filtered_df,
        x=x_axis_option,
        y="NOVOS_CASOS_POSITIVOS",
        color="NOME_CONDADO",
        title="Evolução dos Novos Casos Positivos",
        labels={x_axis_option: "Cidades ou Data", "NOVOS_CASOS_POSITIVOS": "Novos Casos Positivos"},
        barmode='group'
    )
    st.plotly_chart(fig)

    st.write("### Gráfico de Linha - Evolução de Mortes Totais")
    fig = px.bar(
        filtered_df,
        x=x_axis_option,
        y="MORTES_TOTAL",
        color="NOME_CONDADO",
        title="Evolução das Mortes Totais",
        labels={x_axis_option: "Cidades ou Data", "MORTES_TOTAL": "Mortes Totais"},
        barmode='group'
    )
    st.plotly_chart(fig)

    st.write("### Gráfico de Linha - Evolução de Novas Mortes")
    fig = px.bar(
        filtered_df,
        x=x_axis_option,
        y="NOVAS_MORTES",
        color="NOME_CONDADO",
        title="Evolução das Novas Mortes",
        labels={x_axis_option: "Cidades ou Data", "NOVAS_MORTES": "Novas Mortes"},
        barmode='group'
    )
    st.plotly_chart(fig)

else:
    st.warning("Não há dados suficientes para exibir os gráficos.")

# Exibindo o DataFrame filtrado
st.write("### Dados Filtrados")
st.write(filtered_df.head())

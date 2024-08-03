import streamlit as st
import pandas as pd
import datetime

st.title("Testee")
st.markdown("Objetivo do Dash")
# Caminho para o arquivo CSV
# 

file_path = 'COVID-19 Activity.csv'
# Ler o arquivo CSV especificando low_memory=False
df = pd.read_csv(file_path, low_memory=False)
# Mostrar o DataFrame na tela com Streamlit

st.title('Mostrar Arquivo CSV com Streamlit')
st.write(df.head())

st.title("Testee")

st.markdown("Objetivo do Dash")

sel_ano = st.radio( label = "Selecione o ano:", 
                   options=[2020,2021,2022], 
                   index=0)

st.write("Você selecionou:",sel_ano)

jan_1 = datetime.date(sel_ano,1,1)
dec_31 = datetime.date(sel_ano,12,31)


d = st.date_input(
    "Selecione as datas para análise:",
    (jan_1,datetime.date(sel_ano,1,7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY"
)


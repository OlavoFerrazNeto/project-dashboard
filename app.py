import streamlit as st
import pandas as pd
from bcb import currency

st.title("Testee")

st.markdown("Objetivo do Dash")

sel_ano = st.radio(
    label = "Selecione o ano:",
    options=["2022","2023","2024"],
    index=None,
)

st.write("Você selecionou:",sel_ano)


print("olavo")
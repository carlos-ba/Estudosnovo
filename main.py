import streamlit as st

st.title("Programa de Concatenação")

# Campos de entrada
primeira_variavel = st.text_input("Digite o primeiro valor:")
segunda_variavel = st.text_input("Digite o segundo valor:")

# Botão para executar
if st.button("Juntar"):
    resultado = primeira_variavel + segunda_variavel
    st.success(f"O resultado da junção é: {resultado}")
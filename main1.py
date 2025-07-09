import streamlit as st
import openai
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da página
st.set_page_config(
    page_title="Diagnóstico Inteligente - Refrigeração",
    page_icon="❄️",
    layout="wide"
)

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def criar_prompt_sistema() -> str:
    return """Você é um técnico especializado em refrigeração com vasta experiência.
    Analise os problemas descritos e forneça:
    1. Diagnóstico provável
    2. Possíveis causas
    3. Sugestões de solução
    4. Recomendações de manutenção preventiva"""


def obter_resposta_gpt(descricao: str) -> Dict[str, Any]:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": criar_prompt_sistema()},
                {"role": "user", "content": descricao}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response
    except Exception as e:
        st.error(f"Erro ao processar a solicitação: {str(e)}")
        return None


def main():
    # Interface do usuário
    st.title("🔧 Diagnóstico Inteligente - Refrigeração")
    st.markdown("### Sistema de Auxílio ao Diagnóstico de Problemas em Refrigeração")

    # Área de entrada
    with st.container():
        descricao = st.text_area(
            "Descreva o problema observado no sistema:",
            height=150,
            placeholder="Ex: O ar condicionado está fazendo barulho e não está gelando..."
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            analisar = st.button("🔍 Analisar", use_container_width=True)

    # Processamento
    if analisar and descricao:
        with st.spinner("Analisando o problema..."):
            response = obter_resposta_gpt(descricao)

            if response:
                st.success("Análise concluída!")
                with st.container():
                    st.markdown("### 📋 Diagnóstico Técnico:")
                    st.markdown(response['choices'][0]['message']['content'])

    elif analisar and not descricao:
        st.warning("Por favor, descreva o problema antes de solicitar a análise.")

    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        <small>Este é um sistema de auxílio. Para problemas graves, consulte sempre um técnico qualificado.</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

import streamlit as st
from openai import OpenAI
from typing import Dict, Any


# Configuração da API OpenAI usando apenas secrets do Streamlit
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



# Configurações da página
st.set_page_config(
    page_title="Diagnóstico Inteligente - Refrigeração",
    page_icon="❄️",
    layout="wide"
)

# Configuração da API OpenAI usando secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



def criar_prompt_sistema() -> str:
    return """Você é um técnico especialista em refrigeração com mais de 20 anos de experiência em diagnóstico e manutenção de sistemas de refrigeração e ar condicionado.

    CONTEXTO TÉCNICO:
    - Você possui conhecimento profundo em sistemas split, janela, self contained, VRF e chillers
    - Você entende completamente sobre ciclos de refrigeração, compressores, condensadores, evaporadores e válvulas de expansão
    - Você domina diagnósticos relacionados a problemas elétricos, mecânicos e de fluido refrigerante

    FORMATO DA ANÁLISE:
    1. Diagnóstico Provável:
       - Liste os problemas mais prováveis em ordem de probabilidade
       - Indique o nível de gravidade (Baixo/Médio/Alto)
       - Estime a urgência do reparo

    2. Causas Detalhadas:
       - Liste todas as possíveis causas
       - Explique a relação entre causa e sintoma
       - Mencione fatores agravantes

    3. Soluções Recomendadas:
       - Providências imediatas que o usuário pode tomar
       - Procedimentos técnicos necessários
       - Estimativa de complexidade do reparo (Simples/Intermediário/Complexo)
       - Indicação se requer técnico especializado

    4. Manutenção Preventiva:
       - Ações específicas para prevenir reincidência
       - Frequência recomendada de manutenções
       - Cuidados diários/semanais/mensais
       - Sinais de alerta para monitorar

    5. Informações de Segurança:
       - Alertas sobre riscos específicos
       - Precauções necessárias
       - Situações que exigem atenção imediata"""


def obter_resposta_gpt(descricao: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": criar_prompt_sistema()},
                {"role": "user", "content": descricao}
            ],
            temperature=0.4,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro ao processar a solicitação: {str(e)}")
        return None


def criar_sidebar():
    with st.sidebar:
        st.header("ℹ️ Informações do Equipamento")

        fabricante = st.text_input("Fabricante do Equipamento:")
        modelo = st.text_input("Modelo:")
        idade = st.number_input("Idade do Equipamento (anos):", min_value=0, max_value=50)

        return {
            "fabricante": fabricante,
            "modelo": modelo,
            "idade": idade
        }


def main():
    st.title("🔧 Diagnóstico Inteligente - Refrigeração")
    st.markdown("### Sistema de Auxílio ao Diagnóstico de Problemas em Refrigeração")

    # Informações do equipamento na sidebar
    info_equipamento = criar_sidebar()

    # Área principal
    col1, col2 = st.columns(2)

    with col1:
        tipo_equipamento = st.selectbox(
            "Tipo de Equipamento:",
            ["Ar Condicionado Split", "Ar Condicionado de Janela",
             "Geladeira/Freezer", "Câmara Frigorífica",
             "Bebedouro", "Sistema VRF", "Chiller"]
        )

        tempo_problema = st.selectbox(
            "Duração do Problema:",
            ["Começou agora", "Alguns dias", "Algumas semanas", "Mais de um mês"]
        )

    with col2:
        manutencao_recente = st.radio(
            "Realizou manutenção recentemente?",
            ["Sim", "Não"]
        )

        if manutencao_recente == "Sim":
            ultima_manutencao = st.date_input("Data da última manutenção:")

    # Área de descrição do problema
    descricao = st.text_area(
        "Descreva detalhadamente o problema observado:",
        height=150,
        placeholder=f"Ex: O {tipo_equipamento.lower()} está apresentando..."
    )

    # Sintomas específicos
    st.subheader("Sintomas Específicos")
    col3, col4, col5 = st.columns(3)

    with col3:
        ruido_anormal = st.checkbox("Ruído Anormal")
        vazamento = st.checkbox("Vazamento")

    with col4:
        baixo_rendimento = st.checkbox("Baixo Rendimento")
        odor_estranho = st.checkbox("Odor Estranho")

    with col5:
        vibracao = st.checkbox("Vibração Excessiva")
        formacao_gelo = st.checkbox("Formação de Gelo")

    # Botão de análise
    if st.button("🔍 Analisar Problema", use_container_width=True):
        if descricao:
            # Preparar contexto completo
            sintomas = []
            if ruido_anormal: sintomas.append("Ruído Anormal")
            if vazamento: sintomas.append("Vazamento")
            if baixo_rendimento: sintomas.append("Baixo Rendimento")
            if odor_estranho: sintomas.append("Odor Estranho")
            if vibracao: sintomas.append("Vibração Excessiva")
            if formacao_gelo: sintomas.append("Formação de Gelo")

            contexto_completo = f"""
            INFORMAÇÕES DO EQUIPAMENTO:
            - Tipo: {tipo_equipamento}
            - Fabricante: {info_equipamento['fabricante']}
            - Modelo: {info_equipamento['modelo']}
            - Idade: {info_equipamento['idade']} anos

            HISTÓRICO DO PROBLEMA:
            - Tempo de ocorrência: {tempo_problema}
            - Manutenção recente: {manutencao_recente}

            SINTOMAS MARCADOS:
            {', '.join(sintomas)}

            DESCRIÇÃO DETALHADA:
            {descricao}
            """

            with st.spinner("Analisando o problema..."):
                response = obter_resposta_gpt(contexto_completo)

                if response:
                    st.success("Análise concluída!")
                    st.markdown("### 📋 Diagnóstico Técnico:")
                    st.markdown(response)
        else:
            st.warning("Por favor, descreva o problema antes de solicitar a análise.")

    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        <small>Este é um sistema de auxílio ao diagnóstico. Para problemas graves, consulte sempre um técnico qualificado.</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
from databricks.sdk import WorkspaceClient
import requests
import os
import time
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv(dotenv_path=".env")

# Lê as variáveis de ambiente
server_hostname = os.getenv("SERVER_HOSTNAME")
tenant_id       = os.getenv("TENANT_ID")
client_id       = os.getenv("CLIENT_ID")
client_secret   = os.getenv("CLIENT_SECRET")
GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID")
GENIE_URL = os.getenv("GENIE_URL")

# Evita conflito com OAuth antigo
os.environ.pop("DATABRICKS_CLIENT_ID", None)
os.environ.pop("DATABRICKS_CLIENT_SECRET", None)

# Funções de formatação
def formatar_numero(valor):
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_moeda(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Configuração da página
st.set_page_config(page_title="Pergunte informações de faturamento!!!")

# Inicializa o histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Layout do título
st.markdown("""
<div style="margin-bottom: 24px;">
    <h4 style="color: #1a1a1a; margin-bottom: 0;">Chatbot de faturamento</h4>
</div>
""", unsafe_allow_html=True)

# Caixa de texto para pergunta
pergunta = st.text_input(
    "Faça uma pergunta para o Chatbot:",
    placeholder=" "
)

# Frase de aviso em letras menores
st.markdown(
    '<div style="font-size: 12px; color: #888; margin-bottom: 16px;">'
    'Conteúdo gerado por IA, podendo conter erros.'
    '</div>',
    unsafe_allow_html=True
)

# Botão de envio
enviar = st.button("Perguntar", key="button1")

# Parâmetros da API
SPACE_ID = GENIE_SPACE_ID
BASE_URL = GENIE_URL

def obter_resposta(pergunta):
    # Cliente unificado do Databricks (Service Principal no Entra ID)
    w = WorkspaceClient(
    host=f"https://{server_hostname}",
    azure_client_id=client_id,
    azure_client_secret=client_secret,
    azure_tenant_id=tenant_id,
    )
    headers = w.config.authenticate()
    # Inicia a conversa
    url_inicio = f"{BASE_URL}/{SPACE_ID}/start-conversation"
    response = requests.post(url_inicio, headers=headers, json={"content": pergunta})
    dados = response.json()
    message_id = dados.get("message_id")
    conversation_id = dados["message"]["conversation_id"]
    # Aguarda a conclusão
    url_status = f"{BASE_URL}/{SPACE_ID}/conversations/{conversation_id}/messages/{message_id}"
    while dados.get("status") != "COMPLETED":
        time.sleep(2)
        response = requests.get(url_status, headers=headers)
        dados = response.json()
    # Obtém o resultado
    url_resultado = f"{url_status}/query-result/"
    response = requests.get(url_resultado, headers=headers)
    return response.json()

def processar_resposta(data):
    resultado = []
    schema = data["statement_response"]["manifest"]["schema"]["columns"]
    linhas = data["statement_response"]["result"]["data_typed_array"]
    for linha in linhas:
        registro = {}
        for i, valor in enumerate(linha["values"]):
            nome_coluna = schema[i]["name"]
            tipo_coluna = schema[i]["type_text"]
            valor_str = valor["str"]
            if tipo_coluna == "BIGINT":
                registro[nome_coluna] = formatar_numero(int(valor_str))
            elif tipo_coluna != "STRING":
                registro[nome_coluna] = formatar_moeda(float(valor_str))
            else:
                registro[nome_coluna] = valor_str
        resultado.append(registro)
    return pd.DataFrame(resultado)

# Processamento da pergunta
try:
    if pergunta.strip() and (enviar or pergunta):
        with st.spinner("Por favor, aguarde..."):
            dados_resposta = obter_resposta(pergunta)
            df_resposta = processar_resposta(dados_resposta)
            # Salva no histórico
            st.session_state.historico.append({
                "pergunta": pergunta,
                "resposta": df_resposta
            })
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

# Exibe histórico
for item in reversed(st.session_state.historico):
    st.markdown(f"**Pergunta:** {item['pergunta']}")
    st.dataframe(item["resposta"].style.hide(axis="index"))
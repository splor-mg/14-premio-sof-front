import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import date

load_dotenv()

st.set_page_config(page_title="Chamada de Fluxo n8n", layout="centered")

st.title("📲 Acionamento de Fluxo – n8n")
st.write("Preencha os dados abaixo. O resultado será enviado para o WhatsApp informado.")

with st.form("formulario_fluxo"):
    data_input = st.date_input("Data:", value=date.today())
    telefone = st.text_input("Número de WhatsApp (com DDD):")

    enviado = st.form_submit_button("Enviar")

if enviado:
    if not telefone:
        st.error("Por favor, preencha o número de telefone.")
        st.stop()

    fluxo_url = os.getenv("FLOW_URL")  # must be /webhook/, NOT /webhook-test
    username = os.getenv("FLOW_USERNAME")
    password = os.getenv("FLOW_PASSWORD")

    payload = {
        "data": str(data_input),
        "telefone": telefone
    }

    try:
        resposta = requests.post(
            fluxo_url,
            json=payload,
            auth=(username, password),     # ← Built-in Basic Auth
            timeout=10
        )

        if resposta.status_code in (200, 201, 202):
            st.success("✅ Fluxo acionado com sucesso!")
            st.info(f"A resposta da pesquisa será enviada para o WhatsApp: **{telefone}**")
        else:
            st.error(f"❌ Erro ao acionar o fluxo. Código: {resposta.status_code}")
            st.write("Resposta do servidor:", resposta.text)

    except requests.exceptions.RequestException as e:
        st.error("❌ Erro de conexão ao chamar o fluxo.")
        st.write(str(e))

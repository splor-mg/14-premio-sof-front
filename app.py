import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import date

load_dotenv()

st.set_page_config(page_title="Chamada de Fluxo n8n", layout="centered")

st.title("📲 Acionamento de Fluxo – n8n")
st.write("Preencha os dados abaixo. O resultado será enviado para o WhatsApp informado.")


data_input = st.date_input("Data:", value=date.today())
telefones_total = st.number_input("Números de telefones:", min_value=0, step=1, key="telefones_total")

telefones = []
for i in range(telefones_total):
    telefone = st.text_input(
        f"Número do {i + 1}° número de WhatsApp (com DDD):",
        placeholder=f"WhatsApp (com DDD)",
        key=f"telefone_{i}"
    )
    telefones.append(telefone)

enviado = st.button("Enviar")

if enviado:
    if not telefone:
        st.error("Por favor, preencha o número de telefone.")
        st.stop()

    fluxo_url = os.getenv("FLOW_URL")
    username = os.getenv("FLOW_USERNAME")
    password = os.getenv("FLOW_PASSWORD")

    payload = {
        "data": str(data_input),
        "telefone": telefones
    }

    try:
        resposta = requests.post(
            fluxo_url,
            json=payload,
            auth=(username, password),
            timeout=10
        )

        if resposta.status_code in (200, 201, 202):
            st.success("✅ Fluxo acionado com sucesso!")
            st.info(f"A resposta da pesquisa será enviada para o(s) WhatsApp(s): **{', '.join(telefones)}**")
        else:
            st.error(f"❌ Erro ao acionar o fluxo. Código: {resposta.status_code}")
            st.write("Resposta do servidor:", resposta.text)

    except requests.exceptions.RequestException as e:
        st.error("❌ Erro de conexão ao chamar o fluxo.")
        st.write(str(e))

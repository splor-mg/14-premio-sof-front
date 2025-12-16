import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import date
from valida_whatsapp import validar_whatsapp

load_dotenv()

def main():
    st.set_page_config(page_title="Feed Alterações Legislativas", layout="centered")

    st.title("📲 Acionamento do Fluxo Feed de Alterações Legislativas (n8n)")

    st.markdown("""
        Este aplicativo foi desenvolvido para acionar o fluxo do Feed de Alterações Legislativas, criado a partir da ferramenta n8n.
        Ele foi criado para atender as regras do 14º Prêmio SOF e demonstrar o funcionamento do mesmo.
        """)

    st.write("Preencha os dados abaixo. O resultado será enviado para o WhatsApp informado assim que o fluxo for finalizado.")
    data_input = st.date_input("Data:", value=date.today(), format="DD/MM/YYYY")
    tipo_diario = st.selectbox(
        "Tipo de Diário Oficial:",
        options=["Edição Normal", "Edição Extraordinária"],
        index=0
    )
    telefone = st.text_input(
            f"Número WhatsApp (somente números, DDD + número):",
            placeholder="Ex: 31987654321 ou 3187654321",
            key="telefone")
    valido, resultado = validar_whatsapp(telefone)
    if telefone and not valido:
        st.error(f"Erro no número de telefone {telefone}: {resultado}")

    enviado = st.button("Enviar")

    if enviado:

        fluxo_url = os.getenv("FLOW_URL")
        username = os.getenv("FLOW_USERNAME")
        password = os.getenv("FLOW_PASSWORD")

        payload = {
            "data": data_input.strftime("%d/%m/%Y"),
            "telefone": [f"55{telefone}",],
            "tipo_diario": "DO1" if tipo_diario == "Edição Normal" else "DOE",
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
                st.info(f"A resposta da pesquisa será enviada para o WhatsApp: 55{telefone}")
                st.info(f"O fluxo pode demorar mais de 30 minutos para ser concluído.")
            else:
                st.error(f"❌ Erro ao acionar o fluxo. Código: {resposta.status_code}")
                st.write("Resposta do servidor:", resposta.text)

        except requests.exceptions.RequestException as e:
            st.error("❌ Erro de conexão ao chamar o fluxo.")
            st.write(str(e))

if __name__ == "__main__":
    main()

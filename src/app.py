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
    data_input = st.date_input("Data:", value=date.today())
    telefones_total = st.number_input("Números de telefones:", min_value=0, step=1, key="telefones_total")

    telefones = []
    for i in range(telefones_total):
        raw = st.text_input(
            f"Número do {i+1}° WhatsApp (somente números, DDD + número):",
            placeholder="Ex: 31987654321 ou 3187654321",
            key=f"telefone_{i}"
        )
        valido, resultado = validar_whatsapp(raw)
        if raw and not valido:
            st.error(f"Erro no número {i+1}: {resultado}")
        telefones.append(raw)

    enviado = st.button("Enviar")

    if enviado:
        if telefones_total == 0:
            st.error("Por favor, informe ao menos um número de whatsapp.")
            st.stop()
        elif any(not telefone.strip() for telefone in telefones):
            st.error("Por favor, preencha todo(s) o(s) número(s) de whatsapp.")
            st.stop()

        telefones_limpos = []
        for idx, raw in enumerate(telefones):
            valido, resultado = validar_whatsapp(raw)
            if not valido:
                st.error(f"Número {idx+1} inválido: {resultado}")
                st.stop()
            else:
                telefones_limpos.append(resultado)

        telefones_para_envio = [f"55{num}" for num in telefones_limpos]

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
                st.info(f"A resposta da pesquisa será enviada para o(s) WhatsApp(s): **{', '.join(telefones_para_envio)}**")
                st.info(f"O fluxo pode demorar mais de 30 minutos para ser concluído.")
            else:
                st.error(f"❌ Erro ao acionar o fluxo. Código: {resposta.status_code}")
                st.write("Resposta do servidor:", resposta.text)

        except requests.exceptions.RequestException as e:
            st.error("❌ Erro de conexão ao chamar o fluxo.")
            st.write(str(e))

if __name__ == "__main__":
    main()

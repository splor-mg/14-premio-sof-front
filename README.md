# 📲 Acionamento do feed de alterações legislativas (n8n) (via Streamlit)

Este é um aplicativo simples em **Streamlit** criado para **acionar o fluxo do [feed de alterações legislativas](https://github.com/splor-mg/feed-legis-workflows) (n8n)** via webhook autenticado.

Este é um protótipo para demonstrar o funcionamento do [feed de alterações legislativas](https://github.com/splor-mg/feed-legis-workflows) no [14º Premio SOF](https://github.com/splor-mg/14-premio-sof).

Para acionar o fluxo, o usuário deverá informar a data da busca e uma lista de números de WhatsApp. A resposta do processo será enviada para os números informados.

## 🚀 Funcionalidades

- Interface web simples usando **Streamlit**.
- Chamada de webhook do **n8n** usando:
    - Autenticação **Basic Auth**.
    - Payload JSON.
- Tratamento de erros com mensagens amigáveis no frontend.

## 📦 Como rodar o projeto localmente

- Clone o repositório:

```sh
git clone git@github.com:splor-mg/14-premio-sof-front.git
cd 14-premio-sof-front
```

- Informe as variáveis de ambiente[^1]:

[^1]: O projeto usa variáveis de ambiente para informar o endpoint do fluxo n8n e as credenciais de autenticação. No repositório há um arquivo `.env-example` com os campos necessários. Basta criar o arquivo `.env` a partir do `.env-example`. Para a demonstração do 14º prêmio SOF, utilizamos [este fluxo n8n](https://dou-feed-legis-demo-n8n.6rngh8.easypanel.host/workflow/7sn2HM02ne0a6hXK) para rodar o feed de alterações legislativas. As credenciais cadastradas podem ser encontradas no primeiro node do fluxo (`Webhook`), no campo "Credential for Basic Auth".

```sh
cp .env-example .env
# Edite o arquivo `.env` com suas configurações reais.
```
Exemplo:

```sh
# .env
FLOW_URL=https://meu-servidor.com/webhook/minha-acao/
FLOW_USERNAME=usuario123
FLOW_PASSWORD=senhaSegura
```

## ▶️ Executando a aplicação

Este projeto utiliza Poetry. Para instalar as dependências[^2] e rodar o servidor localmente:

[^2]: Este projeto use Python `3.13`. caso não tenha esta versão instalada no seu computador, Poetry poderá te ajudar. Use `poetry python install 3.13` para instalar a versão, `poetry env use 3.13` para definir esta versão no seu ambiente virtual e, finalmente, `poetry install` para instalar as dependências.

```bash
poetry install

poetry run task server
# Ou se tiver com ambiente ativado: task server
# Ativar o ambiente virtual: eval $(poetry env activate)
```

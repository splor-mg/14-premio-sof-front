import re

def limpar_numero(raw: str) -> str:
    """Remove tudo que não for dígito."""
    if raw is None:
        return ""
    return re.sub(r"\D", "", raw)

def validar_whatsapp(numero_raw: str):
    """
    Recebe a string do usuário (qualquer coisa), retorna (True, numero_normalizado)
    ou (False, mensagem_de_erro).
    Normalizado: apenas dígitos, sem +55. Ex: '31987654321' ou '3187654321'
    """
    numero = limpar_numero(numero_raw).strip()

    if numero == "":
        return False, "Número vazio."

    if not numero.isdigit():
        return False, "O número deve conter apenas dígitos."

    if len(numero) not in (10, 11):
        return False, "O número deve ter 10 ou 11 dígitos (DDD + número). Ex: 31987654321 ou 3187654321."

    # DDD não pode começar com '0'
    if numero[0] == "0":
        return False, "DDD inválido (não pode começar com 0)."

    # Se tem 11 dígitos, terceiro deve ser '9' (celular)
    if len(numero) == 11 and numero[2] != "9":
        return False, "Formato inválido: números com 11 dígitos devem ter '9' como primeiro dígito do número local."

    # OK
    return True, numero

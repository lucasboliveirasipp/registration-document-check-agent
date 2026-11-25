from enum import Enum

class TipoAssinatura(Enum):
    TITULAR_ATUAL = "Titular Atual"
    TITULAR_NOVO = "Titular Novo"
    SUBSCRITOR_ATUAL = "Subscritor Atual"
    SUBSCRITOR_NOVO = "Subscritor Novo"
    GERENTE = "Gerente"
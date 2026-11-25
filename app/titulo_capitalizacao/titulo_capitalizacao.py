
from .titulo import Titulo
from .subscritor_cap import SubscritorCap
from .titular_cap import TitularCap
from .enums.forma_pagamento import FormaPagamento
from .enums.forma_assinatura import FormaAssinatura
from .enums.tipo_conta import TipoConta
from .enums.tipo_documento import TipoDocumento


class TituloCapitalizacao:
    def __init__(self, opcao: int):
        self.opcao = opcao
        self.titulos: Titulo = []
        
        self.forma_pagamento: FormaPagamento = None
        self.agencia = None
        self.conta = None
        self.tipo_conta: TipoConta = None

        self.subscritor: SubscritorCap = None
        self.tipo_documento_titular: TipoDocumento = None
        self.tipo_documento_subscritor: TipoDocumento = None
        self.titular: TitularCap = None
    
        self.local = None
        self.data = None

        self.forma_assinatura: FormaAssinatura = None
        self.assinaturas = []

    def tipo_alteracao(self):
        if self.opcao == 1:
            return "1. Alteração de Conta e Forma de Pagamento"
        elif self.opcao == 2:
            return "2. Transferência de Subscritor"
        elif self.opcao == 3:
            return "3. Transferência de Titular"
        elif self.opcao == 4:
            return "4. Transferência de Titular e Subscritor"
        


    def __repr__(self): return (f"TituloCapitalizacao(opcao={self.opcao}, titulos={self.titulos}, " f"forma_pagamento={self.forma_pagamento}, agencia={self.agencia}, conta={self.conta}, " f"tipo_conta={self.tipo_conta}, subscritor={self.subscritor}, titular={self.titular}, " f"local={self.local}, data={self.data}, forma_assinatura={self.forma_assinatura}, " f"assinaturas={self.assinaturas})")
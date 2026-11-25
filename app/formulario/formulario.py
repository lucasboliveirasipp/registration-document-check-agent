class Formulario:
    def __init__(self, opcao: int):
        self.opcao = opcao
        self.contratos_titular = []
        self.subscritor = None
        self.titular = None
        self.declaracao = None
        self.nome_subscritor_novo_atual = None
        self.assinatura_subscritor_novo_atual = None
        self.nome_subscritor_antigo = None
        self.assinatura_subscritor_antigo = None
        self.assinatura_procurador = None


    def tipo_alteracao(self):
        if self.opcao == 1:
            return "1. Transferência Agência / Conta, Subscritor e alterar de Não Correntista para Correntista."
        elif self.opcao == 2:
            return "2. Transferência Titular."
        elif self.opcao == 3:
            return "3. Transferência de Subscritor e Titular"
        elif self.opcao == 4:
            return "4. Cancelamento de Autorização de Débito em Conta."

    def novo_atual_subscritor_assinou(self):
        if self.assinatura_subscritor_novo_atual == 'signed':
            return "Assinado"
        else:
            return "Não Assinado"
    
    def antigo_subscritor_assinou(self):
        if self.assinatura_subscritor_antigo == 'signed':
            return "Assinado"
        else:
            return "Não Assinado"

    def __repr__(self):
        return (f"Formulario(opcao={self.opcao},"                
                f"nome_subscritor_novo_atual={self.nome_subscritor_novo_atual}, "
                f"assinatura_subscritor_novo_atual={self.assinatura_subscritor_novo_atual}, "
                f"nome_subscritor_antigo={self.nome_subscritor_antigo}, "
                f"assinatura_subscritor_antigo={self.assinatura_subscritor_antigo}, "
                f"assinatura_procurador={self.assinatura_procurador})")    


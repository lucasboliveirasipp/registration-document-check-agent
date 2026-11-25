class Subscritor:
    def __init__(self, nome: str, cpf_cnpj: str, filial: str, contr: str, codigo_agencia: str, codigo_agencia_dig: str, razao: str, conta: str, conta_dig: str):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj + filial + contr
        self.codigo_agencia = codigo_agencia
        self.codigo_agencia_dig = codigo_agencia_dig
        self.razao = razao
        self.conta = conta
        self.conta_dig = conta_dig

    def __repr__(self):
        return (f"Subscritor(nome='{self.nome}', cpf_cnpj='{self.cpf_cnpj}', "
                f"codigo_agencia='{self.codigo_agencia}', codigo_agencia_dig='{self.codigo_agencia_dig}', "
                f"razao='{self.razao}', conta='{self.conta}', conta_dig='{self.conta_dig}')")
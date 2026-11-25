class Planilha:
    def __init__(self, nome_razao_social: str, cpf_cnpj: str, cep : str, endereco: str, numero: str, complemento: str,
                 bairro: str, cidade: str, estado: str, banco: str, agencia: str,
                 digito_agencia: str, numero_conta: str, digito_conta: str, data_nascimento: str):
        self.nome_razao_social = nome_razao_social
        self.cpf_cnpj = cpf_cnpj
        self.endereco = endereco
        self.cep = cep
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.banco = banco
        self.agencia = agencia
        self.digito_agencia = digito_agencia
        self.numero_conta = numero_conta
        self.digito_conta = digito_conta
        self.data_nascimento = data_nascimento

    def __repr__(self):
        return (f"Planilha(nome_razao_social={self.nome_razao_social!r}, "
                f"cpf_cnpj={self.cpf_cnpj!r}, cep={self.cep!r}, endereco={self.endereco!r}, "
                f"numero={self.numero!r}, complemento={self.complemento!r}, bairro={self.bairro!r}, cidade={self.cidade!r}, "
                f"estado={self.estado!r}, banco={self.banco!r}, agencia={self.agencia!r}, "
                f"digito_agencia={self.digito_agencia!r}, numero_conta={self.numero_conta!r}, "
                f"digito_conta={self.digito_conta!r}, data_nascimento={self.data_nascimento!r})")
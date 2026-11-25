class TitularCap:
    def __init__(self, nome_atual: str, cpf_cnpj_atual: str, grau_parentesco_novo: str, nome_novo: str, cpf_cnpj_novo: str, cep_novo: str, endereco_novo: str, bairro_novo: str, cidade_novo: str, uf_novo: str):
        self.nome_atual = nome_atual
        self.cpf_cnpj_atual = cpf_cnpj_atual
        self.grau_parentesco_novo = grau_parentesco_novo
        self.nome_novo = nome_novo
        self.cpf_cnpj_novo = cpf_cnpj_novo
        self.cep_novo = cep_novo
        self.endereco_novo = endereco_novo
        self.bairro_novo = bairro_novo
        self.cidade_novo = cidade_novo
        self.uf_novo = uf_novo

    def __repr__(self): 
        return (f"TitularCap(nome_atual={self.nome_atual}, cpf_cnpj_atual={self.cpf_cnpj_atual}, " f"grau_parentesco_novo={self.grau_parentesco_novo}, nome_novo={self.nome_novo}, " f"cpf_cnpj_novo={self.cpf_cnpj_novo}, cep_novo={self.cep_novo}, endereco_novo={self.endereco_novo}, " f"bairro_novo={self.bairro_novo}, cidade_novo={self.cidade_novo}, uf_novo={self.uf_novo})")
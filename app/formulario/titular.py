class Titular:
    def __init__(self, cedente: str,
                 cpf_cnpj_cedente: str,
                 filial_cedente: str,
                 contr_cedente: str,
                 nome_razao: str,
                 cpf_cnpj_novo: str,
                 filial_novo: str,
                 contr_novo: str,
                 dt_nasc_const_emp: str,
                 tipo_doc: str,
                 numero_documento: str,
                 orgao_emissor: str,
                 data_emissao: str,
                 endereco_completo: str,
                 bairro: str,
                 cidade: str,
                 uf: str,
                 cep: str,
                 ddd: str,
                 telefone: str,
                 profissao_ativ_principal: str):
        self.cedente = cedente
        self.cpf_cnpj_cedente = cpf_cnpj_cedente + filial_cedente + contr_cedente        
        self.nome_razao = nome_razao
        self.cpf_cnpj_novo = cpf_cnpj_novo + filial_novo + contr_novo
        self.data_nasc_const_emp = dt_nasc_const_emp
        self.tipo_doc = tipo_doc
        self.numero_documento = numero_documento
        self.orgao_emissor = orgao_emissor
        self.data_emissao = data_emissao
        self.endereco_completo = endereco_completo
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.ddd = ddd
        self.telefone = telefone
        self.profissao_ativ_principal = profissao_ativ_principal

    def __repr__(self):
        return (f"Titular(cedente='{self.cedente}', cpf_cnpj_cedente='{self.cpf_cnpj_cedente}', "
                f"nome_razao='{self.nome_razao}', cpf_cnpj_novo='{self.cpf_cnpj_novo}', "
                f"data_nasc_const_emp='{self.data_nasc_const_emp}', tipo_doc='{self.tipo_doc}', "
                f"numero_documento='{self.numero_documento}', orgao_emissor='{self.orgao_emissor}', "
                f"data_emissao='{self.data_emissao}', endereco_completo='{self.endereco_completo}', "
                f"bairro='{self.bairro}', cidade='{self.cidade}', uf='{self.uf}', cep='{self.cep}', "
                f"ddd='{self.ddd}', telefone='{self.telefone}', "
                f"profissao_ativ_principal='{self.profissao_ativ_principal}')")
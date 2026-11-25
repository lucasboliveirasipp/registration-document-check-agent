from .enums.tipo_assinatura import TipoAssinatura

class Assinatura:
    def __init__(self, nome: str, cpf_cnpj: str, assinatura: str, tipo_assinatura: TipoAssinatura):
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.assinatura = assinatura
        self.tipo_assinatura = tipo_assinatura
 
    def __repr__(self):
        return (f"Assinatura(nome='{self.nome}', cpf_cnpj='{self.cpf_cnpj}', "
                f"assinatura='{self.assinatura}', tipo_assinatura='{self.tipo_assinatura}')")
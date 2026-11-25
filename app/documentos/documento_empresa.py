from typing import List

class DocumentoEmpresa:
        def __init__(self, responsaveis, cnpj: str, razao_social: str):
            self.responsaveis = responsaveis            
            self.cnpj = cnpj
            self.razao_social = razao_social

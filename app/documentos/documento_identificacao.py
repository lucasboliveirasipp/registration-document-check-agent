class DocumentoIdentificacao:
        def __init__(self, nome: str, cpf: str, data_nascimento: str):
            self.nome = nome
            self.cpf = cpf
            self.data_nascimento = data_nascimento

        def __repr__(self):
            return (f"DocumentoIdentificacao(nome='{self.nome}', cpf='{self.cpf}', "
            f"data_nascimento='{self.data_nascimento}')")
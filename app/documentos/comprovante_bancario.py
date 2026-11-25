class ComprovanteBancario:
    def __init__(self, nome: str, instituicao: str, agencia: str, conta: str):
        self.nome = nome
        self.instituicao = instituicao        
        self.agencia = agencia
        self.conta = conta        

    def __repr__(self):
        return (f"ComprovanteBancario(nome={self.nome!r}, instituicao={self.instituicao!r}, agencia={self.agencia!r}, conta={self.conta!r})")
class AutenticacaoCartorio:
        def __init__(self, nomes: str, cartorio: str, escrevente: str, codigo_autenticacao: str):
            self.nomes = nomes
            self.cartorio = cartorio
            self.escrevente = escrevente
            self.codigo_autenticacao = codigo_autenticacao

        def __repr__(self):
            return (f"AutenticacaoCartorio(nome='{self.nome_representante}', cpf='{self.cpf_representante}', cnpj='{self.cnpj}', razao_social={self.razao_social})")
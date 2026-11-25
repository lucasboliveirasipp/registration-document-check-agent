class ContratoTitular:
    def __init__(self, n_serie: str, n_serie_dig: str, n_combinacao: str, n_combinacao_dig: str):
        self.n_serie = n_serie
        self.n_serie_dig = n_serie_dig
        self.n_combinacao = n_combinacao
        self.n_combinacao_dig = n_combinacao_dig

    def numero_serie(self):        
        return self.n_serie+"-"+self.n_serie_dig if self.n_serie_dig else self.n_serie

    def numero_combinacao(self):
        return self.n_combinacao+"-"+self.n_combinacao_dig if self.n_combinacao_dig else self.n_combinacao
    
    def __repr__(self):
        return (f"ContratoTitular(n_serie='{self.n_serie}', n_serie_dig='{self.n_serie_dig}', "
                f"n_combinacao='{self.n_combinacao}', n_combinacao_dig='{self.n_combinacao_dig}')")
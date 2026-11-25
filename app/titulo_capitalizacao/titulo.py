class Titulo:
    def __init__(self, quantidade, serie: str, titulo_inicial: str, titulo_final: str):
        self.quantidade = quantidade
        self.serie = serie
        self.titulo_inicial = titulo_inicial
        self.titulo_final = titulo_final
 
    def __repr__(self):
        return (f"Titulo(quantidade='{self.quantidade}', serie='{self.serie}', "
                f"titulo_inicial='{self.titulo_inicial}', titulo_final='{self.titulo_final}')")
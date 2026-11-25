class Declaracao:
    def __init__(self, nome_novo_titular: str,
                 nome_antigo_titular: str,
                 reserva: str,
                 assinatura_novo_titular: str,
                 assinatura_antigo_titular: str
                 ):
        self.nome_novo_titular = nome_novo_titular
        self.nome_antigo_titular = nome_antigo_titular
        self.reserva = reserva
        self.assinatura_novo_titular = assinatura_novo_titular
        self.assinatura_antigo_titular = assinatura_antigo_titular



    def novo_titular_assinou(self):
        if self.assinatura_novo_titular == 'signed':
            return "Assinado"
        else:
            return "Não Assinado"
    
    def antigo_titular_assinou(self):
        if self.assinatura_antigo_titular == 'signed':
            return "Assinado"
        else:
            return "Não Assinado"
        
    def __repr__(self):
            return (f"Declaracao(nome_novo_titular='{self.nome_novo_titular}', "
                    f"nome_antigo_titular='{self.nome_antigo_titular}', "
                    f"reserva='{self.reserva}', "
                    f"assinatura_novo_titular='{self.assinatura_novo_titular}', "
                    f"assinatura_antigo_titular='{self.assinatura_antigo_titular}')")
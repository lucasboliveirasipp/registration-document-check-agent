class ComprovanteEndereco:
        def __init__(self, nome: str, endereco: str, rua: str, numero: str, complemento: str, bairro : str, cidade: str, cep: str):
            def convertNone(a):      
                return "" if a is None else a
            
            self.nome = convertNone(nome)
            self.endereco = convertNone(endereco)
            self.rua = convertNone(rua)
            self.numero = convertNone(numero)
            self.complemento = convertNone(complemento)
            self.bairro = convertNone(bairro)
            self.cidade = convertNone(cidade)
            self.cep = convertNone(cep)              

        def __repr__(self):
            return (f"ComprovanteEndereco(nome={self.nome!r}, endereco={self.endereco!r}, rua={self.rua!r}, "
                f"numero={self.numero!r}, complemento={self.complemento!r}, bairro={self.bairro!r}, "
                f"cidade={self.cidade!r}, cep={self.cep!r})")
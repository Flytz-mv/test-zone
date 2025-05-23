class Unidade:
    def __init__(self, numero, moradores):
        self.numero = numero
        self.moradores = moradores

    def to_dict(self):
        return {
            "numero": self.numero,
            "moradores": self.moradores
        } 
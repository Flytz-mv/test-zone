class Condominio:
    def __init__(self, nome, unidades):
        self.nome = nome
        self.unidades = unidades

    def to_dict(self):
        return {
            "nome": self.nome,
            "unidades": self.unidades
        } 
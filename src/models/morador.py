class Morador:
    def __init__(self, nome, email, condominio, unidade):
        self.nome = nome
        self.email = email
        self.condominio = condominio
        self.unidade = unidade

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "condominio": self.condominio,
            "unidade": self.unidade
        } 
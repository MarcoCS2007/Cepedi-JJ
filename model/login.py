class Login:
    def __init__(self, email, senha, __admin = False, id = None):
        self.email = email
        self.senha = senha
        self.admin = __admin
        self.id = id

    
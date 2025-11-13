class Dojo:

    def __init__(self, id : int, nome: str, cnpj: str, email: str = '', telefone: str = '', endereco: str = '', professor_responsavel: str = ''):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.professor_responsavel = professor_responsavel

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome},\n"
                f"CNPJ: {self.cnpj},\n"
                f"Email: {self.email},\n"
                f"Telefone: {self.telefone},\n"
                f"Endereço: {self.endereco},\n"
                f"Professor responsável: {self.professor_responsavel}")
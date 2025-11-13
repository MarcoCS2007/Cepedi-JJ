from model.categorias import CategoriaFaixa, CategoriaGenero
from model.dojo import Dojo

class Atleta:
    def __init__(self, id: int, nome: str, cpf : str ,dataNasc: str, cat_genero: CategoriaGenero, peso: float, cat_faixa: CategoriaFaixa, dojo: Dojo, email: str = '', telefone: str = ''):
        self.id = id
        self.nome = nome
        self.dataNasc = dataNasc
        self.cpf = cpf
        self.cat_genero = cat_genero
        self.peso = peso
        self.cat_faixa = cat_faixa
        self.email = email
        self.telefone = telefone
        
        self.id_dojo = dojo

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome},\n"
                f"DataNasc: {self.dataNasc},\n"
                f"Categoria de Gênero: {self.cat_genero},\n"
                f"Peso: {self.peso},\n"
                f"Categoria de Faixa: {self.cat_faixa},\n"
                f"Email: {self.email},\n"
                f"Telefone: {self.telefone},\n"
                f"Dojo: {self.id_dojo}")
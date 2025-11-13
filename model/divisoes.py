from model.torneios import Torneios
from model.categorias import CategoriaIdade, CategoriaPeso, CategoriaFaixa, CategoriaGenero

class Divisoes:

    def __init__(self, id : int, torneio : Torneios, categoriaGenero : CategoriaGenero, categoriaIdade : CategoriaIdade, categoriaPeso : CategoriaPeso, categoriaFaixa : CategoriaFaixa):
        self.id = id
        self.torneio = torneio
        self.categoria_genero = categoriaGenero
        self.categoria_idade = categoriaIdade
        self.categoria_peso = categoriaPeso
        self.categoria_faixa = categoriaFaixa

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Torneio: {self.torneio},\n"
                f"Categoria de Gênero: {self.categoria_genero},\n"
                f"Categoria de Idade: {self.categoria_idade},\n"
                f"Categoria de Peso: {self.categoria_peso},\n"
                f"Categoria de Faixa: {self.categoria_faixa}")
class CategoriaIdade:
    def __init__(self, id: int, nome: str):
        self.__id = id
        self.__nome = nome

    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        self.__nome = value
    
    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome}")
    
    
class CategoriaPeso:
    def __init__(self, id: int, nome: str, pesoMax: float):
        self.id = id
        self.nome = nome
        self.pesoMax = pesoMax

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome},\n"
                f"Peso Máximo: {self.pesoMax}")
    

class CategoriaFaixa:
    def __init__(self, id: int, nome: str, ordem: int):
        self.id = id
        self.nome = nome
        self.ordem = ordem

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome},\n"
                f"Ordem: {self.ordem}")

class CategoriaGenero:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome

    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome}")
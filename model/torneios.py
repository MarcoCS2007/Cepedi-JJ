class Torneios:
    def __init__(self, nome: str, data: str, local: str, status: str, organizador: str = None,  id : int = None):
        self.id = id
        self.nome = nome
        self.data = data
        self.local = local
        self.status = status
        self.organizador = organizador
    
    def __str__(self):
        return (f"ID: {self.id},\n"
                f"Nome: {self.nome},\n"
                f"Data: {self.data},\n"
                f"Local: {self.local},\n"
                f"Status: {self.status},\n"
                f"Organizador: {self.organizador}")
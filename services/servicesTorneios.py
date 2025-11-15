from dao.daoTorneios import DaoTorneios
from model.torneios import Torneios
from database.database import Database

class ServicesTorneiosUser:
    
    def __init__(self, database: Database):
        self.dao_torneios = DaoTorneios(database)

    def buscar_torneio_por_id(self, id: int) -> Torneios | None:
        resultado = self.dao_torneios.buscarPorID(id)
        if resultado:
            print (f"Torneio encontrado:\n{resultado}")
            return resultado
        else:
            print("Torneio não encontrado.")
            return None
    
    def buscar_torneio_por_nome(self, nome: str) -> list[Torneios]:
        resultado = self.dao_torneios.buscarPorNome(nome)
        if resultado:
            print(f"Torneios encontrados:")
            for torneio in resultado:
                print(torneio)
                print(30*"-")
            return resultado
        else:
            print("Nenhum torneio encontrado.")
            return []

    def listar_todos_torneios(self) -> list[Torneios]:
        resultado = self.dao_torneios.listarTodos()
        if resultado:
            print("Torneios encontrados:")
            for torneio in resultado:
                print(torneio)
                print(30*"-")
            return resultado
        else:
            print("Nenhum torneio encontrado.")
            return []


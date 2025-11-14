from model.torneios import Torneios
from database.database import Database
import sqlite3

class DaoTorneios:

    def __init__(self, database: Database):
        self.database = database.connect()
        self.cursor = self.database.cursor()

    def salvar(self, torneio: Torneios):

        try:
            if torneio.id is None:
                self.cursor.execute(
                    "INSERT INTO Torneios (nome, date, local, status, organizador) VALUES (?, ?, ?, ?, ?)",
                    (torneio.nome, torneio.data, torneio.local, torneio.status, torneio.organizador)
                )
            else:
                self.cursor.execute(
                    "UPDATE Torneios SET nome = ?, date = ?, local = ?, status = ?, organizador = ? WHERE id = ?",
                    (torneio.nome, torneio.data, torneio.local, torneio.status, torneio.organizador, torneio.id)
                )
            return True
        except Exception as e:
            print(f"Erro ao salvar Torneio: {e}")
            return False
    
    def buscarPorID(self, id: int):

        self.cursor.execute("SELECT * FROM Torneios WHERE id = ?", (id,))
        row = self.cursor.fetchone()

        if row:
            return self.criaRow(row)
        return None
    
    def buscarPorNome(self, nome: str): 

        self.cursor.execute("SELECT * FROM Torneios WHERE nome LIKE ?", (f'%{nome}%',))
        rows = self.cursor.fetchall()
        resultados = []

        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Torneios")
        rows = cur.fetchall()
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def criaRow(self, row: sqlite3.Row):
        
        return Torneios(
            id=row['id'],
            nome=row['nome'],
            data=row['date'],
            local=row['local'],
            status=row['status'],
            organizador=row['organizador']
        )
    
    def deletar(self, id: int): 
        
        try:
            self.cursor.execute("DELETE FROM Torneios WHERE id = ?", (id,))
            return True
        except Exception as e:
            print(f"Erro ao deletar Torneio: {e}")
            return False
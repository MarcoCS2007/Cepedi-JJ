from model.dojo import Dojo
from database.database import Database
import sqlite3

class DojoDAO:

    def __init__(self, database = Database):
        self.db = database.connect()

    def salvar (self, dojo = Dojo):
        cur = self.db.cursor()
        
        try:
            if dojo.id is None:
                cur.execute("INSERT INTO Dojo (nome, cnpj, email, telefone, endereco, professor_responsavel) VALUES (?, ?, ?, ?, ?, ?)",
                            (dojo.nome, dojo.cnpj, dojo.email, dojo.telefone, dojo.endereco, dojo.professor_responsavel))
            else:
                cur.execute("UPDATE Dojo SET nome = ?, cnpj = ?, email = ?, telefone = ?, endereco = ?, professor_responsavel = ? " 
                            "WHERE id = ?",
                            (dojo.nome, dojo.cnpj, dojo.email, dojo.telefone, dojo.endereco, dojo.professor_responsavel, dojo.id))
                
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Dojo: {e}")
            return False 
        
    def buscarPorID(self, id : int):
        cur = self.db.cursor()
        find = cur.execute('SELECT * FROM Dojo WHERE id = ?', (id,))
        row = find.fetchone()

        if row:
            return self.criaRow(row)
        return None
    
    def buscarPorNome(self, nome : str):
        cur = self.db.cursor
        find = cur.execute('SELECT * FROM Dojo WHERE nome LIKE ?', (f'%{nome}%',))
        rows = find.fetchall()
        resultados = []
        
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def buscarPorCNPJ(self, cnpj : str):
        cur = self.db.cursor()
        find = cur.execute('SELECT * FROM Dojo WHERE cnpj = ?', (cnpj,))
        row = find.fetchone()

        if row:
            return self.criaRow(row)
        return None
    
    def listarTodos(self):
        cur = self.db.cursor()
        find = cur.execute('SELECT * FROM Dojo')
        rows = find.fetchall()
        resultados = []
        
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def criaRow(self, row: sqlite3.Row):
        return Dojo(
            id = row['id'],
            nome = row['nome'],
            cnpj = row['CNPJ'],
            email = row['email'],
            telefone = row['telefone'],
            endereco = row['endereco'],
            professor_responsavel = row['professor_responsavel']
        )
    
    def deletar(self, id : int):
        cur = self.db.cursor()
        
        try:
            cur.execute('DELETE FROM Dojo WHERE id = ?', (id,))
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao deletar Dojo: {e}")
            self.db.rollback()
            return False
        
        
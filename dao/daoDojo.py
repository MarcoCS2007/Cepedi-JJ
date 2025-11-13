from model.dojo import Dojo
from database.database import Database

class DojoDAO:

    def __init__(self, database = Database):
        self.db = database.connect()

    def salvar (self, dojo = Dojo):
        cur = self.db.cursor
        
        try:
            if dojo.id is None:
                cur.execute("INSERT INTO Dojo VALUES (?, ?, ?, ?, ?, ?)",
                            (dojo.nome, dojo.cnpj, dojo.email, dojo.telefone, dojo.endereco, dojo.professor_responsavel))
            else:
                cur.execute("UPDADE Dojo SET nome = ?, cnpj = ?, email = ?, telefone = ?, endereco = ?, professor_responsavel ? " 
                            "WHERE id = ?",
                            (dojo.nome, dojo.cnpj, dojo.email, dojo.telefone, dojo.endereco, dojo.professor_responsavel, dojo.id))
                
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Dojo: {e}")
            self.db.rollback() 
            return False
        
    def buscarPorID(self, id : int):
        cur = self.db.cursor
        find = cur.execute('SELET * FROM Dojo WHERE id = ?', (id,))
        row = find.fetchone()

        if row:
            return self.criaRow(row)
        return None
    
    def buscarPorNome(self, nome : str):
        cur = self.db.cursor
        find = cur.execute('SELET * FROM Dojo WHERE nome LIKE ?', (f'%{nome}%',))
        rows = find.fetchall()
        resultados = []
        
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def listarTodos(self):
        cur = self.db.cursor
        find = cur.execute('SELET * FROM Dojo')
        rows = find.fetchall()
        resultados = []
        
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    def criaRow(self, dojo = Dojo):
        return Dojo(
            id = dojo['id'],
            nome = dojo['nome'],
            cnpj = dojo['CNPJ'],
            email = dojo['email'],
            telefone = dojo['telefone'],
            endereco = dojo['endereco'],
            professor_responsavel = dojo['professor_responsavel']
        )
    
    def deletar(self, id : int):
        cur = self.db.cursor
        
        try:
            cur.execute('DELETE FROM Dojo WHERE id = ?', (id,))
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao deletar Dojo: {e}")
            self.db.rollback()
            return False
        
        
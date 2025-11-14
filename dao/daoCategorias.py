import sqlite3 # Adicionado para Type Hinting
from database.database import Database
from model.categorias import CategoriaIdade, CategoriaGenero, CategoriaPeso, CategoriaFaixa

# --- CLASSE 1: CatIdadeDAO ---
class CatIdadeDAO:

    def __init__(self, db: Database):
        # CORREÇÃO: Chamamos o .connect() para obter a conexão
        self.db = db.connect() 

    def salvar(self, categoria: CategoriaIdade):
        cur = self.db.cursor()
        
        try:
            if categoria.id is None:
                cur.execute("""
                    INSERT INTO Categorias_Idade (nome)
                    VALUES (?)
                """, (categoria.nome,))
            else:
                cur.execute("""
                    UPDATE Categorias_Idade SET nome = ?
                    WHERE id = ?
                """, (categoria.nome, categoria.id))
            
            # REMOVIDO: commit() (é autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar CategoriaIdade: {e}")
            # REMOVIDO: rollback() (é autocommit)
            return False

    
    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Idade WHERE id = ?", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Idade WHERE nome LIKE ?", (f"%{nome}%",))
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Idade")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    # CORREÇÃO: Adicionada a dica de tipo
    def criarDeRow(self, row: sqlite3.Row):
        return CategoriaIdade(
            id=row['id'],
            nome=row['nome'],
        )

    def deletar(self, id: int): # Alterado para receber id
        cur = self.db.cursor()
        try:
            cur.execute("""
                DELETE FROM Categorias_Idade
                WHERE id = ?
            """, (id,))
            
            # REMOVIDO: commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar CategoriaIdade: {e}")
            # REMOVIDO: rollback()
            return False
        
# --- CLASSE 2: CatGeneroDAO ---
class CatGeneroDAO:
    
    def __init__(self, db: Database):
        self.db = db.connect() # CORREÇÃO

    def salvar(self, categoria: CategoriaGenero):
        cur = self.db.cursor()
        
        try:
            if categoria.id is None:
                cur.execute("INSERT INTO Categorias_Genero (nome) VALUES (?)", (categoria.nome,))
            else:
                cur.execute("UPDATE Categorias_Genero SET nome = ? WHERE id = ?", (categoria.nome, categoria.id))
            
            # REMOVIDO: commit()
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar CategoriaGenero: {e}")
            return False
        
    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Genero WHERE id = ?", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Genero WHERE nome LIKE ?", (f"%{nome}%",))
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Genero")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row: sqlite3.Row): # CORREÇÃO
        return CategoriaGenero(
            id=row['id'],
            nome=row['nome'],
        )
    
    def deletar(self, id: int): # Alterado para receber id
        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM Categorias_Genero WHERE id = ?", (id,))
            # REMOVIDO: commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar CategoriaGenero: {e}")
            # REMOVIDO: rollback()
            return False
        
# --- CLASSE 3: CatPesoDAO ---
class CatPesoDAO:

    def __init__(self, db: Database):
        self.db = db.connect() # CORREÇÃO

    def salvar(self, categoria: CategoriaPeso):
        cur = self.db.cursor()
        
        try:
            if categoria.id is None:
                cur.execute("""
                    INSERT INTO Categorias_Peso (nome, peso_max_kg)
                    VALUES (?, ?)
                """, (categoria.nome, categoria.pesoMax))
            else:
                cur.execute("""
                    UPDATE Categorias_Peso SET nome = ?, peso_max_kg = ?
                    WHERE id = ?
                """, (categoria.nome, categoria.pesoMax, categoria.id))
            
            # REMOVIDO: commit()
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar CategoriaPeso: {e}")
            return False
        
    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Peso WHERE id = ?", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Peso WHERE nome LIKE ?", (f"%{nome}%",))
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Peso")
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row: sqlite3.Row): # CORREÇÃO
        return CategoriaPeso(
            id=row['id'],
            nome=row['nome'],
            pesoMax=row['peso_max_kg'] # Atenção: coluna no DB é 'peso_max_kg'
        )
    
    def deletar(self, id: int): # Alterado para receber id
        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM Categorias_Peso WHERE id = ?", (id,))
            # REMOVIDO: commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar CategoriaPeso: {e}")
            # REMOVIDO: rollback()
            return False
        
# --- CLASSE 4: CatFaixaDAO ---
class CatFaixaDAO:
    
    def __init__(self, db: Database):
        self.db = db.connect() # CORREÇÃO

    def salvar(self, categoria: CategoriaFaixa):
        cur = self.db.cursor()
        
        try:
            if categoria.id is None:
                cur.execute("""
                    INSERT INTO Categorias_Faixa (nome, ordem)
                    VALUES (?, ?)
                """, (categoria.nome, categoria.ordem))
            else:
                cur.execute("""
                    UPDATE Categorias_Faixa SET nome = ?, ordem = ?
                    WHERE id = ?
                """, (categoria.nome, categoria.ordem, categoria.id))
            
            # REMOVIDO: commit()
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar CategoriaFaixa: {e}")
            return False
        
    def buscarPorId(self, id: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Faixa WHERE id = ?", (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Faixa WHERE nome LIKE ?", (f"%{nome}%",))
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def listarTodas(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Categorias_Faixa ORDER BY ordem") # Adicionado ORDER BY
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado
    
    def criarDeRow(self, row: sqlite3.Row): # CORREÇÃO
        return CategoriaFaixa(
            id=row['id'],
            nome=row['nome'],
            ordem=row['ordem']
        )
    
    def deletar(self, id: int): # Alterado para receber id
        cur = self.db.cursor()
        try:
            cur.execute("DELETE FROM Categorias_Faixa WHERE id = ?", (id,))
            # REMOVIDO: commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar CategoriaFaixa: {e}")
            # REMOVIDO: rollback()
            return False
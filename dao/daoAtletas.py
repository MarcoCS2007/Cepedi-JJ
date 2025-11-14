import sqlite3 # Para o type hint
from model.atletas import Atleta
from database.database import Database

# 1. IMPORT CORRETO: Importe os DAOs que você VAI PRECISAR
from dao.daoDojo import DojoDAO
from dao.daoCategorias import CatGeneroDAO, CatFaixaDAO
# (Você não usou catIdadeDAO nem catPesoDAO no criaRow, então não importei)

class DaoAtletas:

    # 2. __INIT__ CORRIGIDO (Injeção de Dependência)
    def __init__(self, database: Database, dao_dojo: DojoDAO, dao_cat_genero: CatGeneroDAO, dao_cat_faixa: CatFaixaDAO):
        self.database = database.connect()
        # REMOVIDO: self.cursor
        
        # Armazena os DAOs que foram injetados
        self.dao_dojo = dao_dojo
        self.dao_cat_genero = dao_cat_genero
        self.dao_cat_faixa = dao_cat_faixa

    def salvar(self, atleta: Atleta):
        cur = self.database.cursor() # 3. Cursor local
        
        try:
            if atleta.id is None:
                # 4. CORREÇÃO no INSERT (nomes das colunas e .id)
                cur.execute(
                    "INSERT INTO Atletas (nome, cpf, data_nascimento, id_categoria_genero, peso, id_categoria_faixa, id_equipe, email, telefone) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (atleta.nome, atleta.cpf, atleta.dataNasc, 
                     atleta.cat_genero.id, atleta.peso, atleta.cat_faixa.id, 
                     atleta.dojo.id, atleta.email, atleta.telefone)
                )
            else:
                # 4. CORREÇÃO no UPDATE
                cur.execute(
                    "UPDATE Atletas SET nome = ?, cpf = ?, data_nascimento = ?, id_categoria_genero = ?, peso = ?, id_categoria_faixa = ?, id_equipe = ?, email = ?, telefone = ? "
                    "WHERE id = ?",
                    (atleta.nome, atleta.cpf, atleta.dataNasc, 
                     atleta.cat_genero.id, atleta.peso, atleta.cat_faixa.id, 
                     atleta.dojo.id, atleta.email, atleta.telefone, atleta.id)
                )
            
            # 5. REMOVIDO commit()
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Atleta: {e}")
            return False
        
    def buscarPorID(self, id: int):
        cur = self.database.cursor() # 3. Cursor local
        cur.execute("SELECT * FROM Atletas WHERE id = ?", (id,))
        row = cur.fetchone()

        if row:
            return self.criaRow(row)
        return None
    
    def buscarPorNome(self, nome: str):
        cur = self.database.cursor() # 3. Cursor local
        cur.execute("SELECT * FROM Atletas WHERE nome LIKE ?", (f'%{nome}%',))
        rows = cur.fetchall()
        resultados = []

        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados   

    def buscarPorCPF(self, cpf: str):
        cur = self.database.cursor() # 3. Cursor local
        cur.execute("SELECT * FROM Atletas WHERE cpf = ?", (cpf,))
        row = cur.fetchone()

        if row:
            return self.criaRow(row)
        return None 
    
    # ... (outros 'buscar' são iguais, crie o cursor local) ...
    
    def listarTodos(self): 
        cur = self.database.cursor() # 3. Cursor local
        cur.execute("SELECT * FROM Atletas")
        rows = cur.fetchall()
        resultados = []

        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados   
    
    # 6. CRIA ROW (Totalmente Corrigido)
    def criaRow(self, row: sqlite3.Row):
        
        # 7. Usa os DAOs injetados (do self)
        # 8. Usa os nomes de coluna corretos do banco (ex: 'id_equipe')
        dojo = self.dao_dojo.buscarPorID(row['id_equipe'])
        cat_genero = self.dao_cat_genero.buscarPorId(row['id_categoria_genero'])
        cat_faixa = self.dao_cat_faixa.buscarPorId(row['id_categoria_faixa'])

        return Atleta(
            id = row['id'],
            nome = row['nome'],
            cpf = row['cpf'],
            # 9. Mapeia a coluna 'data_nascimento' para o atributo 'dataNasc'
            dataNasc = row['data_nascimento'], 
            cat_genero = cat_genero,
            peso = row['peso'],
            cat_faixa = cat_faixa,
            dojo = dojo,
            email = row['email'],
            telefone = row['telefone']
        )
    
    def deletar(self, id: int):
        cur = self.database.cursor() # 3. Cursor local
        try:
            cur.execute("DELETE FROM Atletas WHERE id = ?", (id,))
            # 5. REMOVIDO commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar Atleta: {e}")
            # 5. REMOVIDO rollback()
            return False
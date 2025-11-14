import sqlite3
from model.lutas import Luta 
from database.database import Database

# 1. Importar os DAOs de quem ele depende
from dao.daoInscricoes import DaoInscricoes
from dao.daoDivisoes import DaoDivisoes

class DaoLutas:

    # 2. __INIT__ (Injeção de Dependência)
    #    Recebe os DAOs que ele usará para o criaRow
    def __init__(self, database: Database, dao_inscricao: DaoInscricoes, dao_divisao: DaoDivisoes):
        self.database = database.connect()
        
        # Armazena os DAOs injetados
        self.dao_inscricao = dao_inscricao
        self.dao_divisao = dao_divisao

    # 3. SALVAR (Mapeia os objetos para seus IDs)
    def salvar(self, luta: Luta):
        cur = self.database.cursor()
        try:
            # Mapeia os objetos (divisao, inscricao1, inscricao2) para seus IDs
            if luta.id is None:
                cur.execute(
                    "INSERT INTO Lutas (id_divisao, participante_1, participante_2, local) "
                    "VALUES (?, ?, ?, ?)",
                    (luta.divisao.id, 
                     luta.inscricao1.id, 
                     luta.inscricao2.id, 
                     luta.local)
                )
            else:
                cur.execute(
                    "UPDATE Lutas SET id_divisao = ?, participante_1 = ?, participante_2 = ?, local = ? "
                    "WHERE id = ?",
                    (luta.divisao.id, 
                     luta.inscricao1.id, 
                     luta.inscricao2.id, 
                     luta.local, 
                     luta.id)
                )
            
            # Sem commit() (autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Luta: {e}")
            # Sem rollback() (autocommit)
            return False
        
    # 4. CRIAROW (Usa a Injeção de Dependência)
    def criaRow(self, row: sqlite3.Row):
        
        # Usa os DAOs (do self) para "re-hidratar" os IDs
        # Atenção: colunas do DB são 'participante_1' e 'participante_2'
        inscricao1 = self.dao_inscricao.buscarPorID(row['participante_1'])
        inscricao2 = self.dao_inscricao.buscarPorID(row['participante_2'])
        divisao = self.dao_divisao.buscarPorID(row['id_divisao'])

        return Luta(
            id=row['id'],
            inscricao1=inscricao1,
            inscricao2=inscricao2,
            divisao=divisao,
            local=row['local']
        )

    # 5. MÉTODOS DE BUSCA (Padrão)

    def buscarPorID(self, id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Lutas WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None
    
    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Lutas")
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    # 6. MÉTODO ÚTIL (Buscar todas as lutas de uma divisão)
    def buscarPorDivisao(self, divisao_id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Lutas WHERE id_divisao = ?", (divisao_id,))
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 7. DELETAR (Padrão)
    def deletar(self, id: int):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM Lutas WHERE id = ?", (id,))
            # Sem commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar Luta: {e}")
            # Sem rollback()
            return False
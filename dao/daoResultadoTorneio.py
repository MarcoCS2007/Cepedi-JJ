import sqlite3
# Assumindo que o arquivo é model/resultado_torneio.py
from model.resultadoTorneio import ResultadoTorneio
from database.database import Database

# 1. Importar os DAOs de quem ele depende
from dao.daoDivisoes import DaoDivisoes
from dao.daoInscricoes import DaoInscricoes

class DaoResultadoTorneio:

    # 2. __INIT__ (Injeção de Dependência)
    def __init__(self, database: Database, dao_divisao: DaoDivisoes, dao_inscricao: DaoInscricoes):
        self.database = database.connect()
        
        # Armazena os DAOs injetados
        self.dao_divisao = dao_divisao
        self.dao_inscricao = dao_inscricao

    # 3. SALVAR (Mapeia os objetos para seus IDs)
    def salvar(self, resultado: ResultadoTorneio):
        cur = self.database.cursor()
        try:
            # Mapeia os objetos (divisao, inscricao) para seus IDs
            if resultado.id is None:
                cur.execute(
                    """INSERT INTO resultado_torneio 
                       (id_divisao, id_inscricao, colocacao) 
                       VALUES (?, ?, ?)""",
                    (resultado.divisao.id, 
                     resultado.inscricao.id, 
                     resultado.colocacao)
                )
            else:
                cur.execute(
                    """UPDATE resultado_torneio SET 
                       id_divisao = ?, id_inscricao = ?, colocacao = ?
                       WHERE id = ?""",
                    (resultado.divisao.id, 
                     resultado.inscricao.id, 
                     resultado.colocacao, 
                     resultado.id)
                )
            
            # Sem commit() (autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar ResultadoTorneio: {e}")
            # Sem rollback() (autocommit)
            return False
        
    # 4. CRIAROW (Usa a Injeção de Dependência)
    def criaRow(self, row: sqlite3.Row):
        
        # Usa os DAOs (do self) para "re-hidratar" os IDs
        divisao = self.dao_divisao.buscarPorID(row['id_divisao'])
        inscricao = self.dao_inscricao.buscarPorID(row['id_inscricao'])

        return ResultadoTorneio(
            id=row['id'],
            divisao=divisao,
            inscricao=inscricao,
            colocacao=row['colocacao']
        )

    # 5. MÉTODOS DE BUSCA (Padrão)

    def buscarPorID(self, id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM resultado_torneio WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None
    
    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM resultado_torneio")
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 6. MÉTODO ÚTIL (Buscar o pódio de uma divisão)
    def buscarPorDivisao(self, divisao_id: int):
        cur = self.database.cursor()
        # Ordena pela colocação (1º, 2º, 3º)
        cur.execute("SELECT * FROM resultado_torneio WHERE id_divisao = ? ORDER BY colocacao", (divisao_id,))
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 7. DELETAR (Padrão)
    def deletar(self, id: int):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM resultado_torneio WHERE id = ?", (id,))
            # Sem commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar ResultadoTorneio: {e}")
            # Sem rollback()
            return False
import sqlite3
# Assumindo que o arquivo é model/resultados_lutas.py
from model.resultadoLutas import ResultadoLuta
from database.database import Database

# 1. Importar os DAOs de quem ele depende
from dao.daoLutas import DaoLutas
from dao.daoInscricoes import DaoInscricoes

class DaoResultados:

    # 2. __INIT__ (Injeção de Dependência)
    def __init__(self, database: Database, dao_luta: DaoLutas, dao_inscricao: DaoInscricoes):
        self.database = database.connect()
        
        # Armazena os DAOs injetados
        self.dao_luta = dao_luta
        self.dao_inscricao = dao_inscricao

    # 3. SALVAR (Mapeia os objetos para seus IDs)
    def salvar(self, resultado: ResultadoLuta):
        cur = self.database.cursor()
        try:
            # Mapeia os objetos (luta, vencedor) para seus IDs
            if resultado.id is None:
                cur.execute(
                    """INSERT INTO Resultados_lutas 
                       (id_luta, vencedor, metodo_vitoria, pontuacao_1, pontuacao_2, 
                       vantagem_1, vantagem_2, punicoes_1, punicoes_2) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (resultado.luta.id, resultado.vencedor.id, resultado.metodo_vitoria,
                     resultado.pontuacao_1, resultado.pontuacao_2,
                     resultado.vantagem_1, resultado.vantagem_2,
                     resultado.punicoes_1, resultado.punicoes_2)
                )
            else:
                cur.execute(
                    """UPDATE Resultados_lutas SET 
                       id_luta = ?, vencedor = ?, metodo_vitoria = ?, pontuacao_1 = ?, 
                       pontuacao_2 = ?, vantagem_1 = ?, vantagem_2 = ?, 
                       punicoes_1 = ?, punicoes_2 = ?
                       WHERE id = ?""",
                    (resultado.luta.id, resultado.vencedor.id, resultado.metodo_vitoria,
                     resultado.pontuacao_1, resultado.pontuacao_2,
                     resultado.vantagem_1, resultado.vantagem_2,
                     resultado.punicoes_1, resultado.punicoes_2,
                     resultado.id)
                )
            
            # Sem commit() (autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar ResultadoLuta: {e}")
            # Sem rollback() (autocommit)
            return False
        
    # 4. CRIAROW (Usa a Injeção de Dependência)
    def criaRow(self, row: sqlite3.Row):
        
        # Usa os DAOs (do self) para "re-hidratar" os IDs
        luta = self.dao_luta.buscarPorID(row['id_luta'])
        vencedor = self.dao_inscricao.buscarPorID(row['vencedor'])

        return ResultadoLuta(
            id=row['id'],
            luta=luta,
            vencedor=vencedor,
            metodo_vitoria=row['metodo_vitoria'],
            pontuacao_1=row['pontuacao_1'],
            pontuacao_2=row['pontuacao_2'],
            vantagem_1=row['vantagem_1'],
            vantagem_2=row['vantagem_2'],
            punicoes_1=row['punicoes_1'],
            punicoes_2=row['punicoes_2']
        )

    # 5. MÉTODOS DE BUSCA (Padrão)

    def buscarPorID(self, id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Resultados_lutas WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None
    
    # Método útil, já que id_luta é UNIQUE
    def buscarPorLutaID(self, luta_id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Resultados_lutas WHERE id_luta = ?", (luta_id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None

    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Resultados_lutas")
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 7. DELETAR (Padrão)
    def deletar(self, id: int):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM Resultados_lutas WHERE id = ?", (id,))
            # Sem commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar ResultadoLuta: {e}")
            # Sem rollback()
            return False
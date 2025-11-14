import sqlite3
from model.inscricoes import Inscricao # Assumindo que o arquivo é model/inscricoes.py
from database.database import Database

# 1. Importar os DAOs de quem ele depende
from dao.daoAtletas import DaoAtletas
from dao.daoDivisoes import DaoDivisoes

class DaoInscricoes:

    # 2. __INIT__ (Injeção de Dependência)
    #    Recebe o Database e os DAOs que ele usará para o criaRow
    def __init__(self, database: Database, dao_atleta: DaoAtletas, dao_divisao: DaoDivisoes):
        self.database = database.connect()
        
        # Armazena os DAOs injetados
        self.dao_atleta = dao_atleta
        self.dao_divisao = dao_divisao

    # 3. SALVAR (Mapeia os objetos para seus IDs)
    def salvar(self, inscricao: Inscricao):
        cur = self.database.cursor()
        try:
            if inscricao.id is None:
                # Mapeia os objetos (atleta, divisao) para seus IDs (id_atleta, id_divisao)
                cur.execute(
                    "INSERT INTO Inscricoes (id_atleta, id_divisao, nis, status_pagamento) "
                    "VALUES (?, ?, ?, ?)",
                    (inscricao.atleta.id, 
                     inscricao.divisao.id, 
                     inscricao.nis, 
                     inscricao.status_pagamento)
                )
            else:
                cur.execute(
                    "UPDATE Inscricoes SET id_atleta = ?, id_divisao = ?, nis = ?, status_pagamento = ? "
                    "WHERE id = ?",
                    (inscricao.atleta.id, 
                     inscricao.divisao.id, 
                     inscricao.nis, 
                     inscricao.status_pagamento, 
                     inscricao.id)
                )
            
            # Sem commit() (autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Inscricao: {e}")
            # Sem rollback() (autocommit)
            return False
        
    # 4. CRIAROW (Usa a Injeção de Dependência)
    def criaRow(self, row: sqlite3.Row):
        
        # Usa os DAOs (do self) para "re-hidratar" os IDs
        atleta = self.dao_atleta.buscarPorID(row['id_atleta'])
        divisao = self.dao_divisao.buscarPorID(row['id_divisao'])

        return Inscricao(
            id=row['id'],
            atleta=atleta,
            divisao=divisao,
            nis=row['nis'],
            status_pagamento=row['status_pagamento']
        )

    # 5. MÉTODOS DE BUSCA (Padrão)

    def buscarPorID(self, id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Inscricoes WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None
    
    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Inscricoes")
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    # 6. MÉTODOS ÚTEIS (Exemplos)

    def buscarPorAtleta(self, atleta_id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Inscricoes WHERE id_atleta = ?", (atleta_id,))
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    def buscarPorDivisao(self, divisao_id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Inscricoes WHERE id_divisao = ?", (divisao_id,))
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 7. DELETAR (Padrão)
    def deletar(self, id: int):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM Inscricoes WHERE id = ?", (id,))
            # Sem commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar Inscricao: {e}")
            # Sem rollback()
            return False
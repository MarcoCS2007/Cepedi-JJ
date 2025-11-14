import sqlite3
from model.divisoes import Divisoes
from database.database import Database

# 1. IMPORTAR TODOS OS DAOS DE QUEM ELE DEPENDE
from dao.daoTorneios import DaoTorneios
from dao.daoCategorias import CatGeneroDAO, CatIdadeDAO, CatPesoDAO, CatFaixaDAO

class DaoDivisoes:

    # 2. __INIT__ (Injeção de Dependência)
    #    Ele precisa receber a conexão E todos os DAOs que ele usa
    def __init__(self, database: Database, 
                 dao_torneio: DaoTorneios, 
                 dao_gen: CatGeneroDAO, 
                 dao_idade: CatIdadeDAO, 
                 dao_peso: CatPesoDAO, 
                 dao_faixa: CatFaixaDAO):
        
        self.database = database.connect()
        
        # Armazena os DAOs injetados para usar no criaRow
        self.dao_torneio = dao_torneio
        self.dao_gen = dao_gen
        self.dao_idade = dao_idade
        self.dao_peso = dao_peso
        self.dao_faixa = dao_faixa

    # 3. SALVAR (Mapeia objetos .id para colunas id_ FOREIGN KEY)
    def salvar(self, divisao: Divisoes):
        cur = self.database.cursor()
        try:
            if divisao.id is None:
                cur.execute(
                    "INSERT INTO Divisoes (id_torneio, id_categoria_genero, id_categoria_idade, id_categoria_peso, id_categoria_faixa) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (divisao.torneio.id, 
                     divisao.categoria_genero.id, 
                     divisao.categoria_idade.id, 
                     divisao.categoria_peso.id, 
                     divisao.categoria_faixa.id)
                )
            else:
                cur.execute(
                    "UPDATE Divisoes SET id_torneio = ?, id_categoria_genero = ?, id_categoria_idade = ?, id_categoria_peso = ?, id_categoria_faixa = ? "
                    "WHERE id = ?",
                    (divisao.torneio.id, 
                     divisao.categoria_genero.id, 
                     divisao.categoria_idade.id, 
                     divisao.categoria_peso.id, 
                     divisao.categoria_faixa.id, 
                     divisao.id)
                )
            
            # Sem commit (autocommit)
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar Divisao: {e}")
            # Sem rollback (autocommit)
            return False
        
    # 4. CRIAROW (Onde a Injeção de Dependência é usada)
    def criaRow(self, row: sqlite3.Row):
        
        # Usa os DAOs armazenados (do self) para buscar os objetos completos
        torneio = self.dao_torneio.buscarPorID(row['id_torneio'])
        cat_gen = self.dao_gen.buscarPorId(row['id_categoria_genero'])
        cat_idade = self.dao_idade.buscarPorId(row['id_categoria_idade'])
        cat_peso = self.dao_peso.buscarPorId(row['id_categoria_peso'])
        cat_faixa = self.dao_faixa.buscarPorId(row['id_categoria_faixa'])

        # Monta o objeto Divisoes com os objetos "re-hidratados"
        return Divisoes(
            id=row['id'],
            torneio=torneio,
            categoriaGenero=cat_gen,
            categoriaIdade=cat_idade,
            categoriaPeso=cat_peso,
            categoriaFaixa=cat_faixa
        )

    # 5. MÉTODOS DE BUSCA (Padrão)

    def buscarPorID(self, id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Divisoes WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return self.criaRow(row)
        return None
    
    def listarTodos(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Divisoes")
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados
    
    # 6. MÉTODO ÚTIL (Buscar todas as divisões de um torneio específico)
    def buscarPorTorneio(self, torneio_id: int):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM Divisoes WHERE id_torneio = ?", (torneio_id,))
        rows = cur.fetchall()
        
        resultados = []
        for row in rows:
            resultados.append(self.criaRow(row))
        return resultados

    # 7. DELETAR (Padrão)
    def deletar(self, id: int):
        cur = self.database.cursor()
        try:
            cur.execute("DELETE FROM Divisoes WHERE id = ?", (id,))
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar Divisao: {e}")
            return False
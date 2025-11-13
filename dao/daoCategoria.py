# 1. Importei a mesma classe de conexão do PessoaDAO
from database.database import Database
from model.categorias import CategoriaIdade 
# (Removi os outros imports não utilizados)

class catIdadeDAO:

    # 2. O 'db' agora é do tipo DatabaseConnection, igual ao PessoaDAO
    def __init__(self, db: Database):
        self.db = db

    def salvar(self, categoria: CategoriaIdade):
        # 3. Criamos um cursor local, assim como em PessoaDAO
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
            

            # 5. Retornamos True (baseado no rowcount) para indicar sucesso, 
            #    um padrão similar ao PessoaDAO.deletar
            return cur.rowcount > 0
        
        except Exception as e:
            print(f"Erro ao salvar CategoriaIdade: {e}")
            # 6. Boa prática: desfazer a operação em caso de erro
            self.db.rollback() 
            return False

    
    def buscarPorId(self, id: int):
        cur = self.db.cursor() # Padrão PessoaDAO
        cur.execute("""
            SELECT *
            FROM Categorias_Idade
            WHERE id = ?
        """, (id,))
        row = cur.fetchone()
        
        if row:
            return self.criarDeRow(row)
        return None

    def buscarPorNome(self, nome: str):
        cur = self.db.cursor() # Padrão PessoaDAO
        # Sintaxe WHERE nome LIKE ? (corrigida da sua primeira versão)
        cur.execute("""
            SELECT *
            FROM Categorias_Idade
            WHERE nome LIKE ?
        """, (f"%{nome}%",)) # Padrão PessoaDAO
        
        rows = cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def listarTodas(self):
        cur = self.db.cursor() # Padrão PessoaDAO
        cur.execute("SELECT * FROM Categorias_Idade")
        # 7. Corrigido para fetchall() (pegar todos, não apenas um)
        rows = cur.fetchall()
        
        resultado = []
        for row in rows:
            resultado.append(self.criarDeRow(row))
        return resultado

    def criarDeRow(self, row):
        # 8. MANTIDO SIMPLES: Ao contrário do PessoaDAO, 
        # CategoriaIdade não tem um objeto "filho" para buscar.
        # Esta função apenas mapeia a 'row' para o objeto.
        
        return CategoriaIdade(
            id=row['id'],
            nome=row['nome'],
        )

    def deletar(self, categoria: CategoriaIdade):
        cur = self.db.cursor() # Padrão PessoaDAO
        try:
            cur.execute("""
                DELETE FROM Categorias_Idade
                WHERE id = ?
            """, (categoria.id,))
            
            # 4. ESSENCIAL: Adicionamos o commit()
            self.db.commit()
            
            # 5. Padrão PessoaDAO.deletar
            return cur.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar CategoriaIdade: {e}")
            # 6. Boa prática: rollback
            self.db.rollback()
            return False
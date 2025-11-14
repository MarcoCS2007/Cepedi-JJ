import sqlite3

class Database:
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name, isolation_level=None)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            return 'Conexsão fechada com sucesso.'
        return 'Nenhuma conexão para fechar.'
    
    def cursor(self):
        if self.conn is None :
            self.connect()
        self.cursor = self.conn.cursor()
        return self.cursor
        
    def createTable(self):
        cur = self.cursor()
        if cur:
            cur.executescript(
                """
            -- Ativa a imposição de chaves estrangeiras (essencial!)
PRAGMA foreign_keys = ON;

-- 1. Tabela de Torneios
CREATE TABLE IF NOT EXISTS Torneios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    date TEXT NOT NULL, -- Usar formato ISO (ex: 'YYYY-MM-DD)
    local TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Aberto' CHECK (status IN ('Aberto', 'Em Andamento', 'Finalizado')),
    organizador TEXT
);

-- 2. Tabela de Dojos/Equipes
CREATE TABLE IF NOT EXISTS Dojo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    CNPJ TEXT UNIQUE, -- TEXT é melhor que CHAR(14) no SQLite
    email TEXT,
    telefone TEXT,
    endereco TEXT,
    professor_responsavel TEXT NOT NULL
);

-- 3. Categorias de Gênero
CREATE TABLE IF NOT EXISTS Categorias_Genero (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE -- Ex: 'Masculino', 'Feminino'
);

-- 4. Categorias de Faixa
CREATE TABLE IF NOT EXISTS Categorias_Faixa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE, -- Ex: 'Branca', 'Azul', 'Roxa', 'Marrom', 'Preta'
    ordem INTEGER NOT NULL UNIQUE -- Ex: 1, 2, 3, 4, 5 (útil para ordenação)
);

-- 5. Tabela de Atletas
CREATE TABLE IF NOT EXISTS Atletas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE, -- TEXT é melhor que CHAR(11)
    data_nascimento TEXT NOT NULL, -- Usar formato ISO (ex: 'YYYY-MM-DD')
    peso REAL NOT NULL,
    id_categoria_genero INTEGER NOT NULL,
    id_categoria_faixa INTEGER NOT NULL,
    email TEXT,
    telefone TEXT,
    id_equipe INTEGER NOT NULL,
    
    FOREIGN KEY(id_categoria_genero) REFERENCES Categorias_Genero(id),
    FOREIGN KEY(id_categoria_faixa) REFERENCES Categorias_Faixa(id),
    FOREIGN KEY(id_equipe) REFERENCES Dojo(id)
);

-- 6. Categorias de Idade
CREATE TABLE IF NOT EXISTS Categorias_Idade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE -- Ex: 'Mirim', 'Infantil', 'Juvenil', 'Adulto', 'Master 1'
);

-- 7. Categorias de Peso
CREATE TABLE IF NOT EXISTS Categorias_Peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE, -- Ex: 'Galo', 'Pluma', 'Pena', 'Leve', 'Absoluto'
    peso_max_kg REAL -- Ex: 57.5, 64.0 (pode ser NULL para 'Absoluto')
);

-- 8. Tabela de Divisões (Categorias do Torneio)
CREATE TABLE IF NOT EXISTS Divisoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_torneio INTEGER NOT NULL,
    id_categoria_genero INTEGER NOT NULL,
    id_categoria_idade INTEGER NOT NULL,
    id_categoria_peso INTEGER NOT NULL,
    id_categoria_faixa INTEGER NOT NULL,
    
    FOREIGN KEY(id_torneio) REFERENCES Torneios(id),
    FOREIGN KEY(id_categoria_genero) REFERENCES Categorias_Genero(id),
    FOREIGN KEY(id_categoria_idade) REFERENCES Categorias_Idade(id),
    FOREIGN KEY(id_categoria_peso) REFERENCES Categorias_Peso(id),
    FOREIGN KEY(id_categoria_faixa) REFERENCES Categorias_Faixa(id),
    
    -- Impede a criação de divisões duplicadas no mesmo torneio
    UNIQUE(id_torneio, id_categoria_genero, id_categoria_idade, id_categoria_peso, id_categoria_faixa)
);

-- 9. Tabela de Inscrições
CREATE TABLE IF NOT EXISTS Inscricoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_atleta INTEGER NOT NULL,
    id_divisao INTEGER NOT NULL,
    nis TEXT, -- Para projetos sociais, etc.
    status_pagamento TEXT NOT NULL DEFAULT 'Pendente' CHECK (status_pagamento IN ('Pendente', 'Pago', 'Isento')),
    
    FOREIGN KEY(id_atleta) REFERENCES Atletas(id),
    FOREIGN KEY(id_divisao) REFERENCES Divisoes(id),
    
    -- Impede inscrição duplicada do mesmo atleta na mesma divisão
    UNIQUE(id_atleta, id_divisao)
);

-- 10. Tabela de Lutas
CREATE TABLE IF NOT EXISTS Lutas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_divisao INTEGER NOT NULL,
    participante_1 INTEGER NOT NULL, -- ID da Inscrição
    participante_2 INTEGER NOT NULL, -- ID da Inscrição
    local TEXT, -- Ex: "Tatame 1"
    
    FOREIGN KEY(id_divisao) REFERENCES Divisoes(id),
    FOREIGN KEY(participante_1) REFERENCES Inscricoes(id),
    FOREIGN KEY(participante_2) REFERENCES Inscricoes(id),

    -- Garante que um participante não lute contra ele mesmo
    CHECK (participante_1 != participante_2)
);

-- 11. Tabela de Resultados das Lutas
CREATE TABLE IF NOT EXISTS Resultados_lutas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_luta INTEGER NOT NULL UNIQUE, -- Cada luta só tem um resultado (1 para 1)
    vencedor INTEGER NOT NULL, -- ID da Inscrição
    pontuacao_1 INTEGER NOT NULL DEFAULT 0,
    pontuacao_2 INTEGER NOT NULL DEFAULT 0,
    vantagem_1 INTEGER NOT NULL DEFAULT 0,
    vantagem_2 INTEGER NOT NULL DEFAULT 0,
    punicoes_1 INTEGER NOT NULL DEFAULT 0,
    punicoes_2 INTEGER NOT NULL DEFAULT 0,
    metodo_vitoria TEXT NOT NULL CHECK (metodo_vitoria IN ('Pontos', 'Finalizacao', 'W.O.', 'Desistencia', 'Desclassificacao')),
    
    FOREIGN KEY(id_luta) REFERENCES Lutas(id),
    FOREIGN KEY(vencedor) REFERENCES Inscricoes(id)
);

-- 12. Tabela de Resultados Finais do Torneio (Pódio)
CREATE TABLE IF NOT EXISTS resultado_torneio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_divisao INTEGER NOT NULL,
    id_inscricao INTEGER NOT NULL,
    colocacao INTEGER NOT NULL, -- 1 (Ouro), 2 (Prata), 3 (Bronze)
    
    FOREIGN KEY(id_divisao) REFERENCES Divisoes(id),
    FOREIGN KEY(id_inscricao) REFERENCES Inscricoes(id),
    
    -- Impede duas pessoas na mesma colocação (ex: dois 1º lugares)
    UNIQUE(id_divisao, colocacao),
    
    -- CORREÇÃO: Impede a mesma inscrição de ter duas colocações
    UNIQUE(id_divisao, id_inscricao)
);

-- 13. Tabela de Login
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL, -- Armazenar HASH, nunca texto plano
    admin TEXT NOT NULL CHECK (admin IN ('Admin', 'Usuario'))
);
            """
            )
   
    def clearTable(self, table_name):
        cur = self.cursor()
        if cur:
            cur.execute(f"DELETE FROM {table_name}")

        
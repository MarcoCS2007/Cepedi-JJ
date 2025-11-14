# Assume-se que os arquivos são 'model/inscricoes.py' e 'model/divisoes.py'
from model import inscricoes 
from model import divisoes

class Luta:

    # CORREÇÃO: Parâmetros reordenados, 'id' no final e 'Divisoes' (plural)
    def __init__(self, inscricao1: inscricoes.Inscricao, inscricao2: inscricoes.Inscricao, 
                 divisao: divisoes.Divisoes, local: str = None, id: int = None):
        self.id = id
        self.inscricao1 = inscricao1
        self.inscricao2 = inscricao2
        self.divisao = divisao
        self.local = local

    def __str__(self):
        # Adicionei o __str__ para seguir o padrão
        return (f"ID: {self.id}\n"
                f"Divisão: {self.divisao.id}\n"
                f"Participante 1: {self.inscricao1.atleta.nome}\n"
                f"Participante 2: {self.inscricao2.atleta.nome}\n"
                f"Local: {self.local}")
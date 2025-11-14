# Assume-se que os arquivos são 'model/divisoes.py' e 'model/inscricoes.py'
from model import divisoes 
from model import inscricoes

class ResultadoTorneio:

    # CORREÇÕES:
    # 1. 'id' movido para o final e com default=None
    # 2. 'divisao' usa 'divisoes.Divisoes' (plural)
    # 3. 'inscricoes' renomeado para 'inscricao' (singular)
    def __init__(self, divisao: divisoes.Divisoes, inscricao: inscricoes.Inscricao, colocacao: int, id: int = None):
        self.id = id
        self.divisao = divisao
        self.inscricao = inscricao # Corrigido para singular
        self.colocacao = colocacao

    def __str__(self):
        # Adicionei o __str__ para seguir o padrão
        return (f"ID: {self.id}\n"
                f"Divisão ID: {self.divisao.id}\n"
                f"Inscrição (Atleta): {self.inscricao.atleta.nome}\n"
                f"Colocação: {self.colocacao}º")
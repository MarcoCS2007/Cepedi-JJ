import inscricoes
import divisoes

class Luta:

    def __init__(self, id_luta, inscricao1: inscricoes.Inscricao, inscricao2: inscricoes.Inscricao, divisao: divisoes.Divisao, local: str = None):
        self.id_luta = id_luta
        self.inscricao1 = inscricao1
        self.inscricao2 = inscricao2
        self.divisao = divisao
        self.local = local
import divisoes
import inscricoes

class ResultadoTorneio:

    def __init__(self, id: int, divisao: divisoes.Divisao, inscricoes: inscricoes.Inscricao, colocacao: int):
        self.id = id
        self.divisao = divisao
        self.inscricoes = inscricoes
        self.colocacao = colocacao
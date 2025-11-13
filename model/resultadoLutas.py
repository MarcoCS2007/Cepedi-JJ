import lutas
import inscricoes

class ResultadoLuta:

    def __init__(self, id: int, luta: lutas.Luta, vencedor: inscricoes.Inscricao, metodo_vitoria: str,
                 pontuacao_1: int = 0, pontuacao_2: int = 0,
                 vantagem_1: int = 0, vantagem_2: int = 0,
                 punicoes_1: int = 0, punicoes_2: int = 0):
        self.id = id
        self.luta = luta
        self.vencedor = vencedor
        self.metodo_vitoria = metodo_vitoria
        self.pontuacao_1 = pontuacao_1
        self.pontuacao_2 = pontuacao_2
        self.vantagem_1 = vantagem_1
        self.vantagem_2 = vantagem_2
        self.punicoes_1 = punicoes_1
        self.punicoes_2 = punicoes_2
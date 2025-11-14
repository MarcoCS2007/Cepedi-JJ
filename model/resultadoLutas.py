from model import lutas 
from model import inscricoes

class ResultadoLuta:

    # CORREÇÃO: 'id' movido para o final e default=None
    def __init__(self, luta: lutas.Luta, vencedor: inscricoes.Inscricao, metodo_vitoria: str,
                 pontuacao_1: int = 0, pontuacao_2: int = 0,
                 vantagem_1: int = 0, vantagem_2: int = 0,
                 punicoes_1: int = 0, punicoes_2: int = 0, id: int = None):
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

    def __str__(self):
        # Adicionei o __str__ para seguir o padrão
        return (f"ID: {self.id}\n"
                f"Luta ID: {self.luta.id}\n"
                f"Vencedor: {self.vencedor.atleta.nome}\n"
                f"Método: {self.metodo_vitoria}")
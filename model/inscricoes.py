import atletas
import divisoes

class Inscricao:

    def __init__(self, id: int, atleta: atletas.Atleta, divisao: divisoes.Divisao, nis: str = '', status_pagamento: str = 'Pendente'):
        self.id = id
        self.atleta = atleta
        self.divisao = divisao
        self.nis = nis
        self.status_pagamento = status_pagamento
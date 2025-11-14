# Assume-se que os arquivos são 'model/atletas.py' e 'model/divisoes.py'
from model import atletas 
from model import divisoes

class Inscricao:

    # CORREÇÃO: 'id' movido para o final e default=None
    # CORREÇÃO: 'divisao' usa 'divisoes.Divisoes' (plural)
    def __init__(self, atleta: atletas.Atleta, divisao: divisoes.Divisoes, nis: str = '', status_pagamento: str = 'Pendente', id: int = None):
        self.id = id
        self.atleta = atleta
        self.divisao = divisao
        self.nis = nis
        self.status_pagamento = status_pagamento

    def __str__(self):
        # Adicionei o __str__ para seguir o padrão
        return (f"ID: {self.id}\n"
                f"Atleta: {self.atleta.nome}\n"
                f"Divisão: {self.divisao.id}\n"
                f"Status Pgto: {self.status_pagamento}")
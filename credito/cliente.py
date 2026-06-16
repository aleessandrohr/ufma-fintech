from dataclasses import dataclass

@dataclass(frozen=True)
class Cliente:
    id: str
    nome: str
    idade: int
    renda_mensal: float
    score: int
    dividas_em_aberto: bool
    atrasos_ultimos_12_meses: int

    def __post_init__(self):
        if not self.id:
            raise ValueError("ID não pode ser vazio")
        if not self.nome:
            raise ValueError("Nome não pode ser vazio")
        if self.idade < 0:
            raise ValueError("Idade não pode ser negativa")
        if self.renda_mensal < 0:
            raise ValueError("Renda mensal não pode ser negativa")
        if not (0 <= self.score <= 1000):
            raise ValueError("Score deve estar entre 0 e 1000")
        if self.atrasos_ultimos_12_meses < 0:
            raise ValueError("Atrasos não podem ser negativos")

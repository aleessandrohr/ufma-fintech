from dataclasses import dataclass

from credit.domain.cliente_domain import Cliente


@dataclass(frozen=True)
class Proposta:
    cliente: Cliente
    valor_solicitado: float
    parcelas: int
    finalidade: str

    def __post_init__(self) -> None:
        if self.valor_solicitado <= 0:
            raise ValueError("Valor solicitado deve ser maior que zero")
        if self.parcelas <= 0:
            raise ValueError("Parcelas devem ser maiores que zero")
        if not self.finalidade:
            raise ValueError("Finalidade não pode ser vazia")

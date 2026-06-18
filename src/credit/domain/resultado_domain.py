from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ResultadoAnalise:
    aprovado: bool
    status: str
    risco: str
    limite_maximo: float
    limite_aprovado: float
    taxa_juros_mensal: float
    motivos: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

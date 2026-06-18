import json
from pathlib import Path
from typing import Any

from credit.domain.cliente_domain import Cliente
from credit.domain.proposta_domain import Proposta


def carregar_propostas(caminho: Path | None = None) -> list[Proposta]:
    """Lê o arquivo JSON e retorna uma lista de propostas."""
    if caminho is None:
        # Resolve o arquivo a partir da raiz do projeto, independentemente do cwd.
        caminho = (
            Path(__file__).resolve().parent.parent.parent
            / "data"
            / "clientes_teste.json"
        )

    with caminho.open("r", encoding="utf-8") as f:
        dados: list[dict[str, Any]] = json.load(f)

    propostas: list[Proposta] = []

    for d in dados:
        cliente = Cliente(
            id=d["id"],
            nome=d["nome"],
            idade=d["idade"],
            renda_mensal=d["renda_mensal"],
            score=d["score"],
            dividas_em_aberto=d["dividas_em_aberto"],
            atrasos_ultimos_12_meses=d["atrasos_ultimos_12_meses"],
        )

        proposta = Proposta(
            cliente=cliente,
            valor_solicitado=d["valor_solicitado"],
            parcelas=d["parcelas"],
            finalidade=d["finalidade"],
        )

        propostas.append(proposta)

    return propostas


def buscar_proposta_por_id(
    id_cliente: str, caminho: Path | None = None
) -> Proposta | None:
    """Busca uma proposta específica pelo ID do cliente."""
    propostas = carregar_propostas(caminho)

    for p in propostas:
        if p.cliente.id == id_cliente:
            return p

    return None

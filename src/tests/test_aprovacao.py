from credit.domain.proposta_domain import Proposta
from credit.repositories.clientes_repository import buscar_proposta_por_id
from credit.services.analise_service import AnaliseRisco


def buscar_proposta_obrigatoria(id_cliente: str) -> Proposta:
    proposta = buscar_proposta_por_id(id_cliente)

    assert proposta is not None

    return proposta


def test_ana001_deve_ser_aprovado() -> None:
    proposta = buscar_proposta_obrigatoria("ANA001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"
    assert resultado.limite_maximo == 24000.0


def test_gab001_deve_ser_aprovado_mesmo_com_divida() -> None:
    proposta = buscar_proposta_obrigatoria("GAB001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"
    # Divida mas score >= 600
    assert any("atende aos critérios" in m for m in resultado.motivos)


def test_hel001_deve_ser_aprovado() -> None:
    proposta = buscar_proposta_obrigatoria("HEL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"

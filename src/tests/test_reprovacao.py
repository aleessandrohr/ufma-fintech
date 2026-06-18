from credit.domain.proposta_domain import Proposta
from credit.repositories.clientes_repository import buscar_proposta_por_id
from credit.services.analise_service import AnaliseRisco


def buscar_proposta_obrigatoria(id_cliente: str) -> Proposta:
    proposta = buscar_proposta_por_id(id_cliente)

    assert proposta is not None

    return proposta


def test_bru001_deve_ser_reprovado_por_idade() -> None:
    proposta = buscar_proposta_obrigatoria("BRU001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    assert any("idade" in m.lower() for m in resultado.motivos)


def test_car001_deve_ser_reprovado_por_renda_baixa() -> None:
    proposta = buscar_proposta_obrigatoria("CAR001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    assert any("renda" in m.lower() for m in resultado.motivos)


def test_dan001_deve_ser_reprovado_por_score_baixo() -> None:
    proposta = buscar_proposta_obrigatoria("DAN001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    assert any("score" in m.lower() for m in resultado.motivos)


def test_eva001_deve_ser_reprovado_por_valor_maior_que_5_vezes_renda() -> None:
    proposta = buscar_proposta_obrigatoria("EVA001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    # Valor solicitado: 20000, Renda: 2500 -> > 5 vezes a renda (12500)
    assert any("5 vezes" in m for m in resultado.motivos)


def test_fel001_deve_ser_reprovado_por_divida_com_score_menor_que_600() -> None:
    proposta = buscar_proposta_obrigatoria("FEL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    assert any(
        "divida" in m.lower() or "dívida" in m.lower() for m in resultado.motivos
    )


def test_ial001_deve_ser_reprovado_por_valor_acima_do_limite_calculado() -> None:
    proposta = buscar_proposta_obrigatoria("IAL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)

    assert resultado.aprovado is False
    assert any("limite" in m.lower() for m in resultado.motivos)

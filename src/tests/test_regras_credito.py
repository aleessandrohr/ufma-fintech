import pytest

from credit.domain.cliente_domain import Cliente
from credit.domain.proposta_domain import Proposta
from credit.services.regras_service import (
    validar_idade,
    validar_parcelas,
    validar_renda,
    validar_score,
    validar_valor_por_renda,
)


@pytest.fixture
def cliente_base() -> Cliente:
    return Cliente("1", "Teste", 30, 3000.0, 600, False, 0)


@pytest.mark.parametrize(
    ("score", "esperado"),
    [
        (800, True),
        (400, True),
        (399, False),
        (0, False),
    ],
)
def test_validar_score(score: int, esperado: bool) -> None:
    cliente = Cliente("1", "Teste", 30, 3000.0, score, False, 0)

    assert validar_score(cliente) is esperado


def test_validar_idade(cliente_base: Cliente) -> None:
    assert validar_idade(cliente_base) is True

    cliente_jovem = Cliente("2", "Jovem", 17, 3000.0, 600, False, 0)

    assert validar_idade(cliente_jovem) is False


def test_validar_renda(cliente_base: Cliente) -> None:
    assert validar_renda(cliente_base) is True

    cliente_baixa_renda = Cliente("3", "Baixa Renda", 30, 1499.0, 600, False, 0)

    assert validar_renda(cliente_baixa_renda) is False


def test_validar_parcelas(cliente_base: Cliente) -> None:
    proposta_valida = Proposta(cliente_base, 1000.0, 12, "teste")

    assert validar_parcelas(proposta_valida) is True

    # O post_init ja bloqueia parcelas <= 0, entao validamos acima do limite.
    proposta_invalida = Proposta(cliente_base, 1000.0, 49, "teste")

    assert validar_parcelas(proposta_invalida) is False


def test_validar_valor_por_renda(cliente_base: Cliente) -> None:
    proposta_valida = Proposta(cliente_base, 15000.0, 12, "teste")

    assert validar_valor_por_renda(proposta_valida) is True

    proposta_invalida = Proposta(cliente_base, 15000.1, 12, "teste")

    assert validar_valor_por_renda(proposta_invalida) is False

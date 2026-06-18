import pytest

from credit.domain.cliente_domain import Cliente
from credit.services.regras_service import calcular_taxa_juros


def test_score_850_sem_divida_deve_gerar_juros_1_ponto_5():
    cliente = Cliente("1", "Teste", 30, 6000.0, 850, False, 0)
    # Limite é 24000. Valor de 5000 não ultrapassa 70% (16800).
    juros = calcular_taxa_juros(cliente, 5000.0, 24000.0)

    assert juros == pytest.approx(1.5)


def test_score_720_com_divida_deve_gerar_juros_3_ponto_5():
    # Base = 2.5
    # Com dívida = +1.0 -> 3.5
    cliente = Cliente("2", "Teste", 30, 5000.0, 720, True, 0)
    juros = calcular_taxa_juros(cliente, 2000.0, 10500.0)

    assert juros == pytest.approx(3.5)


def test_cliente_hel001_deve_ter_juros_3_ponto_0_porque_pediu_mais_que_70_porcento():
    # Score 700 = base 2.5
    # Limite = 3000 * 3 = 9000
    # Pediu 7000 (> 70% de 9000, que é 6300) = +0.5
    # Total = 3.0
    cliente = Cliente("HEL001", "Helena", 29, 3000.0, 700, False, 0)

    juros = calcular_taxa_juros(cliente, 7000.0, 9000.0)

    assert juros == pytest.approx(3.0)


def test_cliente_reprovado_deve_ter_juros_zero():
    # Score < 400
    cliente = Cliente("3", "Teste", 30, 1000.0, 300, False, 0)

    juros = calcular_taxa_juros(cliente, 1000.0, 0.0)

    assert juros == pytest.approx(0.0)

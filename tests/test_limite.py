from credito.regras_credito import calcular_limite_maximo
from credito.cliente import Cliente

def test_score_850_e_renda_6000_deve_gerar_limite_24000():
    cliente = Cliente("1", "Teste", 30, 6000.0, 850, False, 0)
    assert calcular_limite_maximo(cliente) == 24000.0

def test_score_720_e_renda_5000_com_divida_deve_gerar_limite_10500():
    # Base: 5000 * 3 = 15000. Menos 30% = 10500
    cliente = Cliente("2", "Teste", 30, 5000.0, 720, True, 0)
    assert calcular_limite_maximo(cliente) == 10500.0

def test_score_650_e_renda_3000_sem_divida_deve_gerar_limite_6000():
    # Base: 3000 * 2 = 6000
    cliente = Cliente("3", "Teste", 30, 3000.0, 650, False, 0)
    assert calcular_limite_maximo(cliente) == 6000.0

def test_cliente_com_3_atrasos_deve_ter_reducao_adicional_de_20_porcento():
    # Base: 5000 * 3 = 15000
    # Dívida reduz 30% -> 10500
    # Atraso reduz 20% de 10500 -> 8400
    cliente = Cliente("4", "Teste", 30, 5000.0, 720, True, 3)
    assert calcular_limite_maximo(cliente) == 8400.0

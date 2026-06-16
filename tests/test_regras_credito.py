import pytest
from credito.regras_credito import (
    validar_score,
    validar_idade,
    validar_renda,
    validar_parcelas,
    validar_valor_por_renda
)
from credito.cliente import Cliente
from credito.proposta import Proposta

@pytest.fixture
def cliente_base():
    return Cliente("1", "Teste", 30, 3000.0, 600, False, 0)

@pytest.mark.parametrize("score, esperado", [
    (800, True),
    (400, True),
    (399, False),
    (0, False)
])
def test_validar_score(score, esperado):
    cliente = Cliente("1", "Teste", 30, 3000.0, score, False, 0)
    assert validar_score(cliente) is esperado

def test_validar_idade(cliente_base):
    assert validar_idade(cliente_base) is True
    cliente_jovem = Cliente("2", "Jovem", 17, 3000.0, 600, False, 0)
    assert validar_idade(cliente_jovem) is False

def test_validar_renda(cliente_base):
    assert validar_renda(cliente_base) is True
    cliente_baixa_renda = Cliente("3", "Baixa Renda", 30, 1499.0, 600, False, 0)
    assert validar_renda(cliente_baixa_renda) is False

def test_validar_parcelas(cliente_base):
    proposta_valida = Proposta(cliente_base, 1000.0, 12, "teste")
    assert validar_parcelas(proposta_valida) is True
    
    # Testar com parcelas < 1 (não é possível criar a dataclass por causa do post_init, mas vamos mockar se precisar)
    # A dataclass já proíbe parcelas <= 0, então testaremos parcelas acima do limite (48)
    proposta_invalida = Proposta(cliente_base, 1000.0, 49, "teste")
    assert validar_parcelas(proposta_invalida) is False

def test_validar_valor_por_renda(cliente_base):
    # Renda 3000. Max = 15000
    proposta_valida = Proposta(cliente_base, 15000.0, 12, "teste")
    assert validar_valor_por_renda(proposta_valida) is True
    
    proposta_invalida = Proposta(cliente_base, 15000.1, 12, "teste")
    assert validar_valor_por_renda(proposta_invalida) is False

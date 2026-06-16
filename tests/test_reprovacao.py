from credito.analise_risco import AnaliseRisco
from credito.repositorio_clientes import buscar_proposta_por_id

def test_bru001_deve_ser_reprovado_por_idade():
    proposta = buscar_proposta_por_id("BRU001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    assert any("idade" in m.lower() for m in resultado.motivos)

def test_car001_deve_ser_reprovado_por_renda_baixa():
    proposta = buscar_proposta_por_id("CAR001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    assert any("renda" in m.lower() for m in resultado.motivos)

def test_dan001_deve_ser_reprovado_por_score_baixo():
    proposta = buscar_proposta_por_id("DAN001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    assert any("score" in m.lower() for m in resultado.motivos)

def test_eva001_deve_ser_reprovado_por_valor_maior_que_5_vezes_renda():
    proposta = buscar_proposta_por_id("EVA001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    # Valor solicitado: 20000, Renda: 2500 -> > 5 vezes a renda (12500)
    assert any("5 vezes" in m for m in resultado.motivos)

def test_fel001_deve_ser_reprovado_por_divida_com_score_menor_que_600():
    proposta = buscar_proposta_por_id("FEL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    assert any("dívida" in m.lower() for m in resultado.motivos)

def test_ial001_deve_ser_reprovado_por_valor_acima_do_limite_calculado():
    proposta = buscar_proposta_por_id("IAL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is False
    assert any("limite" in m.lower() for m in resultado.motivos)

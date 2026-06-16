from credito.analise_risco import AnaliseRisco
from credito.repositorio_clientes import buscar_proposta_por_id

def test_ana001_deve_ser_aprovado():
    proposta = buscar_proposta_por_id("ANA001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"
    assert resultado.limite_maximo == 24000.0

def test_gab001_deve_ser_aprovado_mesmo_com_divida():
    proposta = buscar_proposta_por_id("GAB001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"
    # Divida mas score >= 600
    assert any("atende aos critérios" in m for m in resultado.motivos)

def test_hel001_deve_ser_aprovado():
    proposta = buscar_proposta_por_id("HEL001")
    analisador = AnaliseRisco()
    resultado = analisador.analisar(proposta)
    
    assert resultado.aprovado is True
    assert resultado.status == "APROVADO"

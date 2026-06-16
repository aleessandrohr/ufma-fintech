from .cliente import Cliente
from .proposta import Proposta

# Constantes de regras de negócio
IDADE_MINIMA = 18
RENDA_MINIMA = 1500.0
SCORE_MINIMO = 400
SCORE_MINIMO_COM_DIVIDA = 600
MAXIMO_PARCELAS = 48
MULTIPLICADOR_MAXIMO_VALOR_RENDA = 5

def validar_idade(cliente: Cliente) -> bool:
    """Verifica se o cliente possui a idade mínima exigida."""
    return cliente.idade >= IDADE_MINIMA

def validar_renda(cliente: Cliente) -> bool:
    """Verifica se o cliente possui a renda mínima exigida."""
    return cliente.renda_mensal >= RENDA_MINIMA

def validar_score(cliente: Cliente) -> bool:
    """Verifica se o cliente possui o score mínimo exigido."""
    return cliente.score >= SCORE_MINIMO

def validar_parcelas(proposta: Proposta) -> bool:
    """Verifica se a quantidade de parcelas solicitada é válida."""
    return 1 <= proposta.parcelas <= MAXIMO_PARCELAS

def validar_valor_por_renda(proposta: Proposta) -> bool:
    """Verifica se o valor solicitado não excede o múltiplo máximo da renda."""
    limite_valor = proposta.cliente.renda_mensal * MULTIPLICADOR_MAXIMO_VALOR_RENDA
    return proposta.valor_solicitado <= limite_valor

def validar_divida_com_score(cliente: Cliente) -> bool:
    """Verifica se cliente com dívida possui score suficiente."""
    if cliente.dividas_em_aberto:
        return cliente.score >= SCORE_MINIMO_COM_DIVIDA
    return True

def calcular_limite_base(cliente: Cliente) -> float:
    """Calcula o limite base de acordo com as faixas de score do cliente."""
    if cliente.score >= 800:
        return cliente.renda_mensal * 4
    elif cliente.score >= 700:
        return cliente.renda_mensal * 3
    elif cliente.score >= 600:
        return cliente.renda_mensal * 2
    elif cliente.score >= 400:
        return cliente.renda_mensal * 1
    return 0.0

def calcular_limite_maximo(cliente: Cliente) -> float:
    """Calcula o limite máximo considerando o limite base e aplicando ajustes por risco."""
    limite = calcular_limite_base(cliente)
    
    # Aplica ajustes em sequência
    if cliente.dividas_em_aberto:
        limite -= limite * 0.30
        
    if cliente.atrasos_ultimos_12_meses >= 3:
        limite -= limite * 0.20
        
    return round(limite, 2)

def calcular_taxa_juros(cliente: Cliente, valor_solicitado: float, limite_maximo: float) -> float:
    """Calcula a taxa de juros base e aplica os devidos ajustes de risco."""
    # Juros base
    if cliente.score >= 800:
        juros = 1.5
    elif cliente.score >= 700:
        juros = 2.5
    elif cliente.score >= 600:
        juros = 3.5
    elif cliente.score >= 400:
        juros = 5.0
    else:
        return 0.0
        
    # Ajustes
    if cliente.dividas_em_aberto:
        juros += 1.0
        
    if cliente.atrasos_ultimos_12_meses >= 3:
        juros += 0.5
        
    if limite_maximo > 0 and valor_solicitado > (limite_maximo * 0.70):
        juros += 0.5
        
    return round(juros, 2)

def classificar_risco(cliente: Cliente, aprovado: bool) -> str:
    """Classifica o nível de risco do cliente com base na sua aprovação e perfil."""
    if not aprovado:
        return "reprovado"
        
    if cliente.score >= 800 and not cliente.dividas_em_aberto and cliente.atrasos_ultimos_12_meses == 0:
        return "baixo"
    elif cliente.score >= 600:
        return "medio"
    else:
        return "alto"

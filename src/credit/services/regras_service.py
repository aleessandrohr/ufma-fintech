from credit.domain.cliente_domain import Cliente
from credit.domain.proposta_domain import Proposta

# Constantes de regras de negócio
IDADE_MINIMA = 18
RENDA_MINIMA = 1500.0
SCORE_MINIMO = 400
SCORE_MINIMO_COM_DIVIDA = 600
MAXIMO_PARCELAS = 48
MULTIPLICADOR_MAXIMO_VALOR_RENDA = 5
LIMIAR_SCORE_EXCELENTE = 800
LIMIAR_SCORE_BOM = 700
LIMIAR_SCORE_REGULAR = 600
LIMIAR_SCORE_BAIXO = 400
MULTIPLICADOR_LIMITE_SCORE_EXCELENTE = 4
MULTIPLICADOR_LIMITE_SCORE_BOM = 3
MULTIPLICADOR_LIMITE_SCORE_REGULAR = 2
MULTIPLICADOR_LIMITE_SCORE_BAIXO = 1
PENALIDADE_DIVIDA = 0.30
PENALIDADE_ATRASOS = 0.20
ATRASOS_MINIMOS_PENALIDADE = 3
TAXA_JUROS_SCORE_EXCELENTE = 1.5
TAXA_JUROS_SCORE_BOM = 2.5
TAXA_JUROS_SCORE_REGULAR = 3.5
TAXA_JUROS_SCORE_BAIXO = 5.0
ACRESCIMO_JUROS_DIVIDA = 1.0
ACRESCIMO_JUROS_ATRASOS = 0.5
PERCENTUAL_SOLICITADO_PARA_ACRESCIMO = 0.70


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
    if cliente.score >= LIMIAR_SCORE_EXCELENTE:
        return cliente.renda_mensal * MULTIPLICADOR_LIMITE_SCORE_EXCELENTE
    elif cliente.score >= LIMIAR_SCORE_BOM:
        return cliente.renda_mensal * MULTIPLICADOR_LIMITE_SCORE_BOM
    elif cliente.score >= LIMIAR_SCORE_REGULAR:
        return cliente.renda_mensal * MULTIPLICADOR_LIMITE_SCORE_REGULAR
    elif cliente.score >= LIMIAR_SCORE_BAIXO:
        return cliente.renda_mensal * MULTIPLICADOR_LIMITE_SCORE_BAIXO

    return 0.0


def calcular_limite_maximo(cliente: Cliente) -> float:
    """
    Calcula o limite máximo considerando o limite base
    e aplicando ajustes por risco.
    """
    limite = calcular_limite_base(cliente)

    # Aplica ajustes em sequência
    if cliente.dividas_em_aberto:
        limite -= limite * PENALIDADE_DIVIDA

    if cliente.atrasos_ultimos_12_meses >= ATRASOS_MINIMOS_PENALIDADE:
        limite -= limite * PENALIDADE_ATRASOS

    return round(limite, 2)


def calcular_taxa_juros(
    cliente: Cliente,
    valor_solicitado: float,
    limite_maximo: float,
) -> float:
    """Calcula a taxa de juros base e aplica os devidos ajustes de risco."""
    # Juros base
    if cliente.score >= LIMIAR_SCORE_EXCELENTE:
        juros = TAXA_JUROS_SCORE_EXCELENTE
    elif cliente.score >= LIMIAR_SCORE_BOM:
        juros = TAXA_JUROS_SCORE_BOM
    elif cliente.score >= LIMIAR_SCORE_REGULAR:
        juros = TAXA_JUROS_SCORE_REGULAR
    elif cliente.score >= LIMIAR_SCORE_BAIXO:
        juros = TAXA_JUROS_SCORE_BAIXO
    else:
        return 0.0

    # Ajustes
    if cliente.dividas_em_aberto:
        juros += ACRESCIMO_JUROS_DIVIDA

    if cliente.atrasos_ultimos_12_meses >= ATRASOS_MINIMOS_PENALIDADE:
        juros += ACRESCIMO_JUROS_ATRASOS

    if limite_maximo > 0 and valor_solicitado > (
        limite_maximo * PERCENTUAL_SOLICITADO_PARA_ACRESCIMO
    ):
        juros += ACRESCIMO_JUROS_ATRASOS

    return round(juros, 2)


def classificar_risco(cliente: Cliente, aprovado: bool) -> str:
    """Classifica o nível de risco do cliente com base na sua aprovação e perfil."""
    if not aprovado:
        return "reprovado"

    if (
        cliente.score >= LIMIAR_SCORE_EXCELENTE
        and not cliente.dividas_em_aberto
        and cliente.atrasos_ultimos_12_meses == 0
    ):
        return "baixo"
    elif cliente.score >= LIMIAR_SCORE_REGULAR:
        return "medio"
    else:
        return "alto"

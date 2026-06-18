from credit.domain.proposta_domain import Proposta
from credit.domain.resultado_domain import ResultadoAnalise
from credit.services.regras_service import (
    IDADE_MINIMA,
    LIMIAR_SCORE_EXCELENTE,
    MAXIMO_PARCELAS,
    MULTIPLICADOR_MAXIMO_VALOR_RENDA,
    RENDA_MINIMA,
    SCORE_MINIMO,
    SCORE_MINIMO_COM_DIVIDA,
    calcular_limite_maximo,
    calcular_taxa_juros,
    classificar_risco,
    validar_divida_com_score,
    validar_idade,
    validar_parcelas,
    validar_renda,
    validar_score,
    validar_valor_por_renda,
)


class AnaliseRisco:
    def analisar(self, proposta: Proposta) -> ResultadoAnalise:
        cliente = proposta.cliente
        motivos: list[str] = []

        # Validar regras automáticas
        if not validar_idade(cliente):
            motivos.append(
                "Cliente reprovado por não atingir a idade mínima de "
                f"{IDADE_MINIMA} anos."
            )

        if not validar_renda(cliente):
            motivos.append(
                "Cliente reprovado por não atingir a renda mínima de "
                f"R$ {RENDA_MINIMA:,.2f}."
            )

        if not validar_score(cliente):
            motivos.append(
                f"Cliente reprovado por score abaixo do mínimo de {SCORE_MINIMO}."
            )

        if not validar_parcelas(proposta):
            motivos.append(
                "Cliente reprovado por quantidade de parcelas inválida "
                f"(deve ser entre 1 e {MAXIMO_PARCELAS})."
            )

        if not validar_valor_por_renda(proposta):
            motivos.append(
                "Cliente reprovado porque o valor solicitado é maior "
                f"que {MULTIPLICADOR_MAXIMO_VALOR_RENDA} vezes a renda mensal."
            )

        if not validar_divida_com_score(cliente):
            motivos.append(
                "Cliente reprovado por ter dívida em aberto "
                f"com score menor que {SCORE_MINIMO_COM_DIVIDA}."
            )

        # Reprovação automática
        if motivos:
            return ResultadoAnalise(
                aprovado=False,
                status="REPROVADO",
                risco="reprovado",
                limite_maximo=0.0,
                limite_aprovado=0.0,
                taxa_juros_mensal=0.0,
                motivos=tuple(motivos),
            )

        # Regras de limite
        limite_maximo = calcular_limite_maximo(cliente)

        # Verificar se valor solicitado cabe no limite
        if proposta.valor_solicitado > limite_maximo:
            motivos.append(
                "Cliente reprovado porque o valor solicitado está acima "
                f"do limite calculado de {limite_maximo}."
            )
            return ResultadoAnalise(
                aprovado=False,
                status="REPROVADO",
                risco="reprovado",
                limite_maximo=limite_maximo,
                limite_aprovado=0.0,
                taxa_juros_mensal=0.0,
                motivos=tuple(motivos),
            )

        # Aprovado
        taxa_juros = calcular_taxa_juros(
            cliente,
            proposta.valor_solicitado,
            limite_maximo,
        )
        risco = classificar_risco(cliente, aprovado=True)

        motivos.append("Cliente atende aos critérios mínimos de idade, renda e score.")

        if cliente.score >= LIMIAR_SCORE_EXCELENTE:
            motivos.append("Score alto permitiu limite base maior.")

        if not cliente.dividas_em_aberto:
            motivos.append("Não há dívidas em aberto.")

        motivos.append("Valor solicitado está dentro do limite calculado.")

        return ResultadoAnalise(
            aprovado=True,
            status="APROVADO",
            risco=risco,
            limite_maximo=limite_maximo,
            limite_aprovado=proposta.valor_solicitado,
            taxa_juros_mensal=taxa_juros,
            motivos=tuple(motivos),
        )

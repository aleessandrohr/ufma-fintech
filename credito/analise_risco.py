from .proposta import Proposta
from .resultado import ResultadoAnalise
from . import regras_credito

class AnaliseRisco:
    def analisar(self, proposta: Proposta) -> ResultadoAnalise:
        cliente = proposta.cliente
        motivos = []
        
        # Validar regras automáticas
        if not regras_credito.validar_idade(cliente):
            motivos.append("Cliente reprovado por não atingir a idade mínima de 18 anos.")
            
        if not regras_credito.validar_renda(cliente):
            motivos.append("Cliente reprovado por não atingir a renda mínima de R$ 1500,00.")
            
        if not regras_credito.validar_score(cliente):
            motivos.append("Cliente reprovado por score abaixo do mínimo de 400.")
            
        if not regras_credito.validar_parcelas(proposta):
            motivos.append("Cliente reprovado por quantidade de parcelas inválida (deve ser entre 1 e 48).")
            
        if not regras_credito.validar_valor_por_renda(proposta):
            motivos.append("Cliente reprovado porque o valor solicitado é maior que 5 vezes a renda mensal.")
            
        if not regras_credito.validar_divida_com_score(cliente):
            motivos.append("Cliente reprovado por ter dívida em aberto com score menor que 600.")
            
        # Reprovação automática
        if motivos:
            return ResultadoAnalise(
                aprovado=False,
                status="REPROVADO",
                risco="reprovado",
                limite_maximo=0.0,
                limite_aprovado=0.0,
                taxa_juros_mensal=0.0,
                motivos=tuple(motivos)
            )
            
        # Regras de limite
        limite_maximo = regras_credito.calcular_limite_maximo(cliente)
        
        # Verificar se valor solicitado cabe no limite
        if proposta.valor_solicitado > limite_maximo:
            motivos.append(f"Cliente reprovado porque o valor solicitado está acima do limite calculado de {limite_maximo}.")
            return ResultadoAnalise(
                aprovado=False,
                status="REPROVADO",
                risco="reprovado",
                limite_maximo=limite_maximo,
                limite_aprovado=0.0,
                taxa_juros_mensal=0.0,
                motivos=tuple(motivos)
            )
            
        # Aprovado
        taxa_juros = regras_credito.calcular_taxa_juros(cliente, proposta.valor_solicitado, limite_maximo)
        risco = regras_credito.classificar_risco(cliente, aprovado=True)
        
        motivos.append("Cliente atende aos critérios mínimos de idade, renda e score.")
        
        if cliente.score >= 800:
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
            motivos=tuple(motivos)
        )

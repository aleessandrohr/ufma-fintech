from credit.domain.proposta_domain import Proposta
from credit.domain.resultado_domain import ResultadoAnalise


def formatar_moeda(valor: float) -> str:
    """Formata float para formato moeda (ex: R$ 5.000,00)."""
    # Formatação simples para pt-BR
    s = f"{valor:,.2f}"
    s = s.replace(",", "v").replace(".", ",").replace("v", ".")

    return f"R$ {s}"


def formatar_percentual(valor: float) -> str:
    """Formata float para percentual (ex: 1.50%)."""
    return f"{valor:.2f}%"


def imprimir_lista_clientes(propostas: list[Proposta]) -> None:
    """Imprime apenas os IDs e nomes dos clientes disponíveis."""
    print("Clientes mockados disponíveis:")

    for p in propostas:
        print(f"- {p.cliente.id}: {p.cliente.nome}")


def imprimir_resultado(proposta: Proposta, resultado: ResultadoAnalise) -> None:
    """Imprime a saída formatada de uma análise."""
    cliente = proposta.cliente

    print("=" * 60)
    print("ANÁLISE DE CRÉDITO")
    print("=" * 60)
    print(f"Cliente: {cliente.nome}")
    print(f"ID: {cliente.id}")
    print(f"Idade: {cliente.idade}")
    print(f"Renda mensal: {formatar_moeda(cliente.renda_mensal)}")
    print(f"Score: {cliente.score}")
    print(f"Dívidas em aberto: {'Sim' if cliente.dividas_em_aberto else 'Não'}")
    print(f"Atrasos nos últimos 12 meses: {cliente.atrasos_ultimos_12_meses}")
    print()
    print(f"Valor solicitado: {formatar_moeda(proposta.valor_solicitado)}")
    print(f"Parcelas: {proposta.parcelas}")
    print(f"Finalidade: {proposta.finalidade}")
    print()
    print(f"Resultado: {resultado.status}")
    print(f"Risco: {resultado.risco}")
    print(f"Limite máximo calculado: {formatar_moeda(resultado.limite_maximo)}")
    print(f"Limite aprovado: {formatar_moeda(resultado.limite_aprovado)}")
    print(f"Taxa de juros mensal: {formatar_percentual(resultado.taxa_juros_mensal)}")
    print()
    print("Motivos:")

    for m in resultado.motivos:
        print(f"- {m}")

    print("=" * 60)


def imprimir_resultados(
    propostas: list[Proposta],
    resultados: list[ResultadoAnalise],
) -> None:
    """Imprime vários resultados de análises."""
    for p, r in zip(propostas, resultados, strict=True):
        imprimir_resultado(p, r)

        print()

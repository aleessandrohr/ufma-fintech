import argparse
import sys

from credit.domain.resultado_domain import ResultadoAnalise
from credit.presentation.terminal_presentation import (
    imprimir_lista_clientes,
    imprimir_resultado,
)
from credit.repositories.clientes_repository import (
    buscar_proposta_por_id,
    carregar_propostas,
)
from credit.services.analise_service import AnaliseRisco


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema de Análise de Crédito Bancário"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista os clientes disponíveis.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Analisa todos os clientes disponíveis.",
    )
    parser.add_argument(
        "--cliente",
        type=str,
        help="Analisa apenas o cliente com o ID especificado.",
    )

    # Se não passou argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    try:
        propostas_todas = carregar_propostas()
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

        sys.exit(1)

    analisador = AnaliseRisco()

    if args.list:
        imprimir_lista_clientes(propostas_todas)

        sys.exit(0)

    if args.all:
        resultados: list[ResultadoAnalise] = []

        for p in propostas_todas:
            resultado = analisador.analisar(p)
            resultados.append(resultado)

        for p, r in zip(propostas_todas, resultados, strict=True):
            imprimir_resultado(p, r)

        sys.exit(0)

    if args.cliente:
        proposta = buscar_proposta_por_id(args.cliente)

        if not proposta:
            print(f"Cliente com ID {args.cliente} não encontrado.")

            imprimir_lista_clientes(propostas_todas)

            sys.exit(1)

        resultado = analisador.analisar(proposta)

        imprimir_resultado(proposta, resultado)

        sys.exit(0)


if __name__ == "__main__":
    main()

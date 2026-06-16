import argparse
import json
import sys
from credito.analise_risco import AnaliseRisco
from credito.repositorio_clientes import carregar_propostas_mock, buscar_proposta_por_id
from credito.terminal import imprimir_lista_clientes, imprimir_resultado

def main():
    parser = argparse.ArgumentParser(description="Sistema de Análise de Crédito Bancário")
    parser.add_argument("--list", action="store_true", help="Lista os clientes mockados disponíveis.")
    parser.add_argument("--all", action="store_true", help="Analisa todos os clientes mockados.")
    parser.add_argument("--cliente", type=str, help="Analisa apenas o cliente com o ID especificado.")
    parser.add_argument("--json", action="store_true", help="Mostra o resultado da análise em formato JSON.")
    
    # Se não passou argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    try:
        propostas_todas = carregar_propostas_mock()
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        sys.exit(1)
        
    analisador = AnaliseRisco()
    
    if args.list:
        imprimir_lista_clientes(propostas_todas)
        sys.exit(0)
        
    if args.all:
        resultados = []
        for p in propostas_todas:
            resultado = analisador.analisar(p)
            resultados.append(resultado)
            
        if args.json:
            saida_json = [r.to_dict() for r in resultados]
            print(json.dumps(saida_json, indent=2, ensure_ascii=False))
        else:
            for p, r in zip(propostas_todas, resultados):
                imprimir_resultado(p, r)
                
    if args.cliente:
        proposta = buscar_proposta_por_id(args.cliente)
        if not proposta:
            print(f"Cliente com ID {args.cliente} não encontrado.")
            imprimir_lista_clientes(propostas_todas)
            sys.exit(1)
            
        resultado = analisador.analisar(proposta)
        if args.json:
            print(json.dumps(resultado.to_dict(), indent=2, ensure_ascii=False))
        else:
            imprimir_resultado(proposta, resultado)

if __name__ == "__main__":
    main()

# Validador de Crédito Bancário

## Objetivo
Sistema acadêmico de análise de crédito bancário para uma fintech fictícia. O sistema avalia clientes com base em suas informações financeiras e histórico, definindo aprovação, limites e taxas de juros.

## Contexto Acadêmico
Projeto desenvolvido com foco em boas práticas de programação em Python, incluindo uso de `dataclasses`, arquitetura limpa, separação de responsabilidades (regras de negócio vs interface), tipagem estática (type hints) e testes automatizados. O código foi projetado para ser simples, legível e de fácil adaptação para outras linguagens e paradigmas acadêmicos como Prolog e Lisp.

## Estrutura de Pastas
```
ufma-fintech/
├── main.py                     # Ponto de entrada CLI
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências (pytest)
├── pytest.ini                  # Configurações do pytest
│
├── data/
│   └── clientes_teste.json     # Base de dados mockada
│
├── credito/
│   ├── __init__.py
│   ├── cliente.py              # Dataclass Cliente
│   ├── proposta.py             # Dataclass Proposta
│   ├── resultado.py            # Dataclass ResultadoAnalise
│   ├── regras_credito.py       # Funções puras de validação e cálculo
│   ├── analise_risco.py        # Orquestração da análise de crédito
│   ├── repositorio_clientes.py # Acesso a dados (JSON)
│   └── terminal.py             # Formatação e saída no terminal
│
└── tests/                      # Suite de testes
    ├── test_aprovacao.py
    ├── test_reprovacao.py
    ├── test_limite.py
    ├── test_juros.py
    └── test_regras_credito.py
```

## Regras de Aprovação e Reprovação
O cliente será reprovado automaticamente se:
- Idade for menor que 18 anos
- Renda mensal for menor que R$ 1.500,00
- Score for menor que 400
- Número de parcelas for menor que 1 ou maior que 48
- Valor solicitado for maior que 5x a renda mensal
- Possuir dívidas em aberto e score menor que 600
- O valor solicitado exceder o limite máximo calculado para o cliente

## Regras de Cálculo de Limite
- Score >= 800: Renda * 4
- Score >= 700: Renda * 3
- Score >= 600: Renda * 2
- Score >= 400: Renda * 1

**Ajustes:**
- Dívidas em aberto: -30%
- 3 ou mais atrasos em 12 meses: -20%

## Regras de Cálculo de Juros
- Score >= 800: 1.5% a.m.
- Score >= 700: 2.5% a.m.
- Score >= 600: 3.5% a.m.
- Score >= 400: 5.0% a.m.

**Ajustes:**
- Dívidas em aberto: +1.0%
- 3 ou mais atrasos em 12 meses: +0.5%
- Solicitou > 70% do limite máximo: +0.5%

## Como Instalar

```bash
# Crie e ative o ambiente virtual
python -m venv .venv

# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## Como Executar pelo Terminal
```bash
python main.py --help
python main.py --list
python main.py --cliente ANA001
python main.py --all
python main.py --cliente ANA001 --json
```

## Como Rodar os Testes
```bash
python -m pytest -v
```

## Decisões de Projeto e Limitações
- Foram utilizadas `@dataclass(frozen=True)` em `Cliente` e `Proposta` para evitar mutação indevida de dados.
- Funções em `regras_credito.py` foram isoladas para facilitar os testes (puras ou semi-puras).
- Arquitetura plugável: fácil de trocar o JSON por um banco de dados SQL atualizando o repositório.
- **Atenção:** Todos os dados aqui presentes são fictícios e usados apenas para fins acadêmicos.

## Uso de IA no desenvolvimento
Este projeto utilizou ferramentas de Inteligência Artificial como apoio no planejamento, estruturação e revisão de código e boas práticas.

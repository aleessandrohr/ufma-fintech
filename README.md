# Validador de Crédito Bancário

## Objetivo

Sistema acadêmico de análise de crédito bancário para uma fintech fictícia. O sistema avalia clientes com base em suas informações financeiras e histórico, definindo aprovação, limites e taxas de juros.

## Contexto Acadêmico

Projeto desenvolvido com foco em boas práticas de programação em Python, incluindo uso de `dataclasses`, arquitetura limpa, separação de responsabilidades (regras de negócio vs interface), tipagem estática (type hints) e testes automatizados. O código foi projetado para ser simples, legível e de fácil adaptação para outras linguagens e paradigmas acadêmicos como Prolog e Lisp.

## Estrutura de Pastas

```
ufma-fintech/
├── README.md                   # Documentação do projeto
├── pyproject.toml              # Configuração central do projeto
├── uv.lock                     # Lockfile do uv
│
├── src/
│   ├── main.py                 # Ponto de entrada CLI
│   ├── data/
│   │   └── clientes_teste.json # Base de dados mockada
│   ├── credit/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── cliente_domain.py   # Dataclass Cliente
│   │   │   ├── proposta_domain.py  # Dataclass Proposta
│   │   │   └── resultado_domain.py # Dataclass ResultadoAnalise
│   │   ├── services/
│   │   │   ├── regras_service.py    # Funcoes puras de validacao e calculo
│   │   │   └── analise_service.py   # Orquestracao da analise de credito
│   │   ├── repositories/
│   │   │   └── clientes_repository.py
│   │   └── presentation/
│   │       └── terminal_presentation.py # Formatação e saída no terminal
│   └── tests/
│       ├── test_aprovacao.py
│       ├── test_reprovacao.py
│       ├── test_limite.py
│       ├── test_juros.py
│       └── test_regras_credito.py
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

- Score >= 800: Renda \* 4
- Score >= 700: Renda \* 3
- Score >= 600: Renda \* 2
- Score >= 400: Renda \* 1

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

## Exemplos de Codigo e Fluxo

O sistema foi separado por responsabilidade para ficar mais facil de entender:

### 1. Ponto de entrada da aplicacao

Em `src/main.py`, a funcao `main()` recebe os argumentos do terminal e decide qual acao executar.

```python
if args.all:
    resultados: list[ResultadoAnalise] = []
    for p in propostas_todas:
        resultado = analisador.analisar(p)
        resultados.append(resultado)

    for p, r in zip(propostas_todas, resultados, strict=True):
        imprimir_resultado(p, r)
```

Esse trecho mostra o fluxo principal:

- carrega todas as propostas
- analisa cada cliente
- imprime o resultado final no terminal

### 2. Modelo de dominio

Em `src/credit/domain/cliente_domain.py`, a classe `Cliente` representa os dados do cliente e valida os campos basicos.

```python
@dataclass(frozen=True)
class Cliente:
    id: str
    nome: str
    idade: int
    renda_mensal: float
    score: int
    dividas_em_aberto: bool
    atrasos_ultimos_12_meses: int
```

Esse modelo evita dados inconsistentes, como idade negativa ou score fora da faixa esperada.

### 3. Regras de negocio

Em `src/credit/services/regras_service.py`, ficam os calculos e validacoes principais.

```python
def calcular_limite_maximo(cliente: Cliente) -> float:
    limite = calcular_limite_base(cliente)

    if cliente.dividas_em_aberto:
        limite -= limite * PENALIDADE_DIVIDA

    if cliente.atrasos_ultimos_12_meses >= ATRASOS_MINIMOS_PENALIDADE:
        limite -= limite * PENALIDADE_ATRASOS

    return round(limite, 2)
```

Esse exemplo mostra como o sistema ajusta o limite conforme o risco do cliente.

### 4. Caso de uso da analise

Em `src/credit/services/analise_service.py`, a classe `AnaliseRisco` coordena todo o processo.

```python
if not validar_score(cliente):
    motivos.append(
        f"Cliente reprovado por score abaixo do minimo de {SCORE_MINIMO}."
    )
```

Aqui o sistema verifica se o cliente cumpre as regras. Se falhar em alguma delas, a proposta e reprovada.

### 5. Acesso a dados

Em `src/credit/repositories/clientes_repository.py`, o sistema le o arquivo JSON e transforma os dados em objetos Python.

```python
with caminho.open("r", encoding="utf-8") as f:
    dados: list[dict[str, Any]] = json.load(f)
```

Esse arquivo isola a leitura de dados, deixando a regra de negocio independente da origem da informacao.

### 6. Apresentacao no terminal

Em `src/credit/presentation/terminal_presentation.py`, o sistema apenas formata e imprime o resultado.

```python
print(f"Resultado: {resultado.status}")
print(f"Limite aprovado: {formatar_moeda(resultado.limite_aprovado)}")
print(f"Taxa de juros mensal: {formatar_percentual(resultado.taxa_juros_mensal)}")
```

Esse modulo nao decide nada. Ele existe apenas para mostrar o resultado de forma legivel.

## Como Instalar

```bash
# Se voce tiver uv instalado:
uv sync --group dev
source .venv/bin/activate
```

Alternativa sem `uv`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install ruff pyright pytest uv
```

## Como Executar pelo Terminal

```bash
python src/main.py --help
python src/main.py --list
python src/main.py --cliente ANA001
python src/main.py --all
```

## Como Rodar com uv

```bash
uv run ruff check .
uv run ruff format .
uv run pyright
uv run pytest
```

## Como Rodar sem uv

```bash
python -m ruff check .
python -m ruff format .
python -m pyright
python -m pytest
```

## Decisões de Projeto e Limitações

- Foram utilizadas `@dataclass(frozen=True)` em `Cliente` e `Proposta` para evitar mutação indevida de dados.
- Funções em `regras_service.py` foram isoladas para facilitar os testes (puras ou semi-puras).
- Arquitetura plugável: fácil de trocar o JSON por um banco de dados SQL atualizando o repositório.
- **Atenção:** Todos os dados aqui presentes são fictícios e usados apenas para fins acadêmicos.

## Versao Prolog

A versao em Prolog fica na pasta `prolog/` e replica a mesma regra de negocio de forma logica, agora separada por responsabilidade.

### Mapeamento Conceitual

- `Cliente` e `Proposta` viram fatos `cliente/10`.
- `regras_service.py` vira predicados de validacao e calculo.
- `analise_service.py` vira o predicado `resultado_cliente/2`.
- `terminal_presentation.py` vira predicados de escrita na tela.

### Estrutura Prolog

```text
prolog/
├── credito_bancario.pl     # Arquivo principal que conecta tudo
├── fatos_credito.pl        # Base de dados ficticia
├── regras_credito.pl       # Validacoes e regras de negocio
└── interface_credito.pl    # Saida formatada no terminal
```

### Exemplo de Uso

Se voce tiver `SWI-Prolog` instalado, pode carregar o arquivo e rodar consultas como estas:

```bash
swipl -q -s prolog/credito_bancario.pl -g run -t halt
swipl -q -s prolog/credito_bancario.pl -g "listar_clientes" -t halt
swipl -q -s prolog/credito_bancario.pl -g "analisar_cliente('ANA001')" -t halt
swipl -q -s prolog/credito_bancario.pl -g "resultado_cliente('ANA001', R), writeln(R)" -t halt
```

### Como Ler o Fluxo

- `fatos_credito.pl` guarda os dados ficticios dos clientes.
- `regras_credito.pl` decide se aprova, reprova, calcula limite e juros.
- `interface_credito.pl` mostra o resultado de forma legivel no terminal.
- `credito_bancario.pl` apenas junta os outros arquivos para facilitar a execucao.

### Exemplo de Regra

```prolog
resultado_cliente(Id, resultado(aprovado, Risco, LimiteMaximo, ValorSolicitado, Juros, Motivos)) :-
    motivos_reprovacao(Id, []),
    limite_maximo(Id, LimiteMaximo),
    cliente(Id, _, _, _, _, _, _, ValorSolicitado, _, _),
    ValorSolicitado =< LimiteMaximo,
    taxa_juros(Id, Juros),
    risco_cliente(Id, aprovado, Risco),
    motivos_aprovacao(Id, Motivos),
    !.
```

Esse predicado resume o fluxo de analise:

- verifica se nao ha motivos automaticos de reprovacao
- calcula o limite maximo
- checa se o valor solicitado cabe no limite
- calcula a taxa de juros
- determina o risco
- retorna todos os motivos da decisao

## Versao LispWorks

A versao em LispWorks fica na pasta `lispworks/` e replica a mesma regra de negocio usando Common Lisp. A organizacao segue o mesmo desenho da versao Prolog: fatos, regras, interface e um arquivo principal para carregar tudo.

### Mapeamento Conceitual

- `Cliente` vira a estrutura `cliente`.
- `ResultadoAnalise` vira a estrutura `resultado`.
- `fatos_credito.pl` vira `fatos_credito.lisp`.
- `regras_credito.pl` vira funcoes puras de validacao, limite, juros, risco e resultado.
- `interface_credito.pl` vira funcoes de exibicao no terminal/Listener.

### Estrutura LispWorks

```text
lispworks/
|-- credito_bancario.lisp   # Arquivo principal que carrega os demais
|-- package.lisp            # Definicao do pacote credito-bancario
|-- fatos_credito.lisp      # Base de dados ficticia
|-- regras_credito.lisp     # Validacoes e regras de negocio
`-- interface_credito.lisp  # Saida formatada no terminal/Listener
```

### Exemplo de Uso

No Listener do LispWorks, carregue o arquivo principal e chame as funcoes exportadas:

```lisp
(load "lispworks/credito_bancario.lisp")
(credito-bancario:run)
(credito-bancario:listar-clientes)
(credito-bancario:analisar-cliente "ANA001")
(credito-bancario:resultado-cliente "ANA001")
```

### Como Ler o Fluxo

- `fatos_credito.lisp` guarda os clientes e propostas em estruturas Common Lisp.
- `regras_credito.lisp` calcula limite, juros, risco e motivos de aprovacao/reprovacao.
- `interface_credito.lisp` apenas imprime os dados de forma legivel.
- `credito_bancario.lisp` centraliza o carregamento para facilitar a execucao no LispWorks.

### Exemplo de Regra

```lisp
(defun limite-maximo (id)
  (let* ((cliente (exigir-cliente id))
         (limite-base (limite-base-cliente cliente))
         (limite-com-divida
           (if (cliente-dividas-em-aberto cliente)
               (- limite-base (* limite-base +penalidade-divida+))
               limite-base))
         (limite-final
           (if (>= (cliente-atrasos-ultimos-12-meses cliente)
                   +atrasos-minimos-penalidade+)
               (- limite-com-divida
                  (* limite-com-divida +penalidade-atrasos+))
               limite-com-divida)))
    (arredondar-2 limite-final)))
```

Essa regra faz o mesmo papel da função de cálculo de limite na versão Python e do predicado `limite_maximo/2` na versão Prolog:

- calcula um limite base a partir do score do cliente
- aplica desconto se houver dívidas em aberto
- aplica desconto se houver atrasos relevantes
- retorna o valor final arredondado

% ---------------------------------------------------------------------------
% Interface: consultas prontas e saida formatada no terminal.
% Esta camada nao decide nada, apenas exibe o resultado da analise.
% ---------------------------------------------------------------------------

listar_clientes :-
    forall(
        cliente(Id, Nome, _, _, _, _, _, _, _, _),
        format('~w - ~w~n', [Id, Nome])
    ).

imprimir_resultado(Id) :-
    resultado_cliente(Id, resultado(Status, Risco, LimiteMaximo, LimiteAprovado, Juros, Motivos)),
    cliente(Id, Nome, Idade, Renda, Score, Dividas, Atrasos, Valor, Parcelas, Finalidade),
    format('~n==============================~n', []),
    format('Cliente: ~w~n', [Nome]),
    format('ID: ~w~n', [Id]),
    format('Idade: ~w~n', [Idade]),
    format('Renda mensal: ~2f~n', [Renda]),
    format('Score: ~w~n', [Score]),
    format('Dividas em aberto: ~w~n', [Dividas]),
    format('Atrasos nos ultimos 12 meses: ~w~n', [Atrasos]),
    format('Valor solicitado: ~2f~n', [Valor]),
    format('Parcelas: ~w~n', [Parcelas]),
    format('Finalidade: ~w~n', [Finalidade]),
    format('Resultado: ~w~n', [Status]),
    format('Risco: ~w~n', [Risco]),
    format('Limite maximo calculado: ~2f~n', [LimiteMaximo]),
    format('Limite aprovado: ~2f~n', [LimiteAprovado]),
    format('Taxa de juros mensal: ~2f~n', [Juros]),
    format('Motivos:~n', []),
    forall(member(Motivo, Motivos), format('- ~w~n', [Motivo])),
    format('==============================~n', []).

analisar_cliente(Id) :-
    imprimir_resultado(Id).

analisar_todos :-
    forall(cliente(Id, _, _, _, _, _, _, _, _, _), imprimir_resultado(Id)).

run :-
    analisar_todos.


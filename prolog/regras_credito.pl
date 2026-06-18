% ---------------------------------------------------------------------------
% Regras: validacao, calculo de limite, juros, risco e resultado.
% Esta camada representa a logica do negocio em Prolog.
% ---------------------------------------------------------------------------

idade_minima(18).
renda_minima(1500.0).
score_minimo(400).
score_minimo_com_divida(600).
maximo_parcelas(48).
multiplicador_maximo_valor_renda(5).

limiar_score_excelente(800).
limiar_score_bom(700).
limiar_score_regular(600).
limiar_score_baixo(400).

multiplicador_limite_score_excelente(4).
multiplicador_limite_score_bom(3).
multiplicador_limite_score_regular(2).
multiplicador_limite_score_baixo(1).

penalidade_divida(0.30).
penalidade_atrasos(0.20).
atrasos_minimos_penalidade(3).

taxa_juros_score_excelente(1.5).
taxa_juros_score_bom(2.5).
taxa_juros_score_regular(3.5).
taxa_juros_score_baixo(5.0).

acrescimo_juros_divida(1.0).
acrescimo_juros_atrasos(0.5).
percentual_solicitado_para_acrescimo(0.70).

idade_valida(Id) :-
    cliente(Id, _, Idade, _, _, _, _, _, _, _),
    idade_minima(Minima),
    Idade >= Minima.

renda_valida(Id) :-
    cliente(Id, _, _, Renda, _, _, _, _, _, _),
    renda_minima(Minima),
    Renda >= Minima.

score_valido(Id) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    score_minimo(Minimo),
    Score >= Minimo.

parcelas_validas(Id) :-
    cliente(Id, _, _, _, _, _, _, _, Parcelas, _),
    maximo_parcelas(Maximo),
    Parcelas >= 1,
    Parcelas =< Maximo.

valor_por_renda_valido(Id) :-
    cliente(Id, _, _, Renda, _, _, _, ValorSolicitado, _, _),
    multiplicador_maximo_valor_renda(Mult),
    ValorSolicitado =< Renda * Mult.

divida_com_score_valida(Id) :-
    cliente(Id, _, _, _, Score, TemDivida, _, _, _, _),
    score_minimo_com_divida(Minimo),
    (   TemDivida = true
    ->  Score >= Minimo
    ;   true
    ).

automaticamente_reprovado(Id) :-
    \+ idade_valida(Id).
automaticamente_reprovado(Id) :-
    \+ renda_valida(Id).
automaticamente_reprovado(Id) :-
    \+ score_valido(Id).
automaticamente_reprovado(Id) :-
    \+ parcelas_validas(Id).
automaticamente_reprovado(Id) :-
    \+ valor_por_renda_valido(Id).
automaticamente_reprovado(Id) :-
    \+ divida_com_score_valida(Id).

motivo_reprovacao(Id, 'Cliente reprovado por nao atingir a idade minima de 18 anos.') :-
    \+ idade_valida(Id).
motivo_reprovacao(Id, 'Cliente reprovado por nao atingir a renda minima de R$ 1500,00.') :-
    \+ renda_valida(Id).
motivo_reprovacao(Id, 'Cliente reprovado por score abaixo do minimo de 400.') :-
    \+ score_valido(Id).
motivo_reprovacao(Id, 'Cliente reprovado por quantidade de parcelas invalida (deve ser entre 1 e 48).') :-
    \+ parcelas_validas(Id).
motivo_reprovacao(Id, 'Cliente reprovado porque o valor solicitado e maior que 5 vezes a renda mensal.') :-
    \+ valor_por_renda_valido(Id).
motivo_reprovacao(Id, 'Cliente reprovado por ter divida em aberto com score menor que 600.') :-
    \+ divida_com_score_valida(Id).

motivos_reprovacao(Id, Motivos) :-
    findall(Motivo, motivo_reprovacao(Id, Motivo), Motivos).

limite_base(Id, Limite) :-
    cliente(Id, _, _, Renda, Score, _, _, _, _, _),
    limiar_score_excelente(Limiar),
    Score >= Limiar,
    multiplicador_limite_score_excelente(Fator),
    Limite is Renda * Fator,
    !.
limite_base(Id, Limite) :-
    cliente(Id, _, _, Renda, Score, _, _, _, _, _),
    limiar_score_bom(Limiar),
    Score >= Limiar,
    multiplicador_limite_score_bom(Fator),
    Limite is Renda * Fator,
    !.
limite_base(Id, Limite) :-
    cliente(Id, _, _, Renda, Score, _, _, _, _, _),
    limiar_score_regular(Limiar),
    Score >= Limiar,
    multiplicador_limite_score_regular(Fator),
    Limite is Renda * Fator,
    !.
limite_base(Id, Limite) :-
    cliente(Id, _, _, Renda, Score, _, _, _, _, _),
    limiar_score_baixo(Limiar),
    Score >= Limiar,
    multiplicador_limite_score_baixo(Fator),
    Limite is Renda * Fator,
    !.
limite_base(_, 0.0).

limite_maximo(Id, LimiteMaximo) :-
    limite_base(Id, LimiteBase),
    cliente(Id, _, _, _, _, TemDivida, Atrasos, _, _, _),
    penalidade_divida(PenDivida),
    penalidade_atrasos(PenAtrasos),
    atrasos_minimos_penalidade(LimAtrasos),
    (   TemDivida = true
    ->  Limite1 is LimiteBase - (LimiteBase * PenDivida)
    ;   Limite1 is LimiteBase
    ),
    (   Atrasos >= LimAtrasos
    ->  Limite2 is Limite1 - (Limite1 * PenAtrasos)
    ;   Limite2 is Limite1
    ),
    LimiteMaximo is round(Limite2 * 100) / 100.

taxa_juros_base(Id, Juros) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_excelente(Limiar),
    Score >= Limiar,
    taxa_juros_score_excelente(Juros),
    !.
taxa_juros_base(Id, Juros) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_bom(Limiar),
    Score >= Limiar,
    taxa_juros_score_bom(Juros),
    !.
taxa_juros_base(Id, Juros) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_regular(Limiar),
    Score >= Limiar,
    taxa_juros_score_regular(Juros),
    !.
taxa_juros_base(Id, Juros) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_baixo(Limiar),
    Score >= Limiar,
    taxa_juros_score_baixo(Juros),
    !.
taxa_juros_base(_, 0.0).

taxa_juros(Id, JurosFinal) :-
    taxa_juros_base(Id, JurosBase),
    cliente(Id, _, _, _, _, TemDivida, Atrasos, ValorSolicitado, _, _),
    limite_maximo(Id, LimiteMaximo),
    acrescimo_juros_divida(AcrescimoDivida),
    acrescimo_juros_atrasos(AcrescimoAtraso),
    percentual_solicitado_para_acrescimo(Percentual),
    atrasos_minimos_penalidade(LimAtrasos),
    (   TemDivida = true
    ->  Juros1 is JurosBase + AcrescimoDivida
    ;   Juros1 is JurosBase
    ),
    (   Atrasos >= LimAtrasos
    ->  Juros2 is Juros1 + AcrescimoAtraso
    ;   Juros2 is Juros1
    ),
    (   LimiteMaximo > 0,
        ValorSolicitado > (LimiteMaximo * Percentual)
    ->  Juros3 is Juros2 + AcrescimoAtraso
    ;   Juros3 is Juros2
    ),
    JurosFinal is round(Juros3 * 100) / 100.

risco_cliente(Id, aprovado, baixo) :-
    cliente(Id, _, _, _, Score, TemDivida, Atrasos, _, _, _),
    limiar_score_excelente(Limiar),
    Score >= Limiar,
    TemDivida = false,
    Atrasos =:= 0,
    !.
risco_cliente(Id, aprovado, medio) :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_regular(Limiar),
    Score >= Limiar,
    !.
risco_cliente(_, aprovado, alto).
risco_cliente(_, reprovado, reprovado).

motivo_aprovacao(Id, 'Cliente atende aos criterios minimos de idade, renda e score.') :-
    idade_valida(Id),
    renda_valida(Id),
    score_valido(Id).
motivo_aprovacao(Id, 'Score alto permitiu limite base maior.') :-
    cliente(Id, _, _, _, Score, _, _, _, _, _),
    limiar_score_excelente(Limiar),
    Score >= Limiar.
motivo_aprovacao(Id, 'Nao ha dividas em aberto.') :-
    cliente(Id, _, _, _, _, TemDivida, _, _, _, _),
    TemDivida = false.
motivo_aprovacao(_, 'Valor solicitado esta dentro do limite calculado.').

motivos_aprovacao(Id, Motivos) :-
    findall(Motivo, motivo_aprovacao(Id, Motivo), Motivos).

resultado_cliente(Id, resultado(reprovado, reprovado, 0.0, 0.0, 0.0, Motivos)) :-
    motivos_reprovacao(Id, Motivos),
    Motivos \= [],
    !.
resultado_cliente(Id, resultado(reprovado, reprovado, LimiteMaximo, 0.0, 0.0, [Motivo])) :-
    motivos_reprovacao(Id, []),
    limite_maximo(Id, LimiteMaximo),
    cliente(Id, _, _, _, _, _, _, ValorSolicitado, _, _),
    ValorSolicitado > LimiteMaximo,
    format(atom(Motivo), 'Cliente reprovado porque o valor solicitado esta acima do limite calculado de ~2f.', [LimiteMaximo]),
    !.
resultado_cliente(Id, resultado(aprovado, Risco, LimiteMaximo, ValorSolicitado, Juros, Motivos)) :-
    motivos_reprovacao(Id, []),
    limite_maximo(Id, LimiteMaximo),
    cliente(Id, _, _, _, _, _, _, ValorSolicitado, _, _),
    ValorSolicitado =< LimiteMaximo,
    taxa_juros(Id, Juros),
    risco_cliente(Id, aprovado, Risco),
    motivos_aprovacao(Id, Motivos),
    !.

aprovado(Id) :-
    resultado_cliente(Id, resultado(aprovado, _, _, _, _, _)).

reprovado(Id) :-
    resultado_cliente(Id, resultado(reprovado, _, _, _, _, _)).


;; Define o pacote publico da aplicacao e as funcoes que podem ser chamadas
;; diretamente pelo Listener do LispWorks.
(defpackage #:credito-bancario
  (:use #:cl)
  (:export
   #:*clientes*
   #:run
   #:listar-clientes
   #:analisar-cliente
   #:analisar-todos
   #:resultado-cliente
   #:aprovado-p
   #:reprovado-p))

(in-package #:cl-user)

;; Arquivo principal: carrega pacote, dados, regras e interface em ordem.
(let ((base (or *load-truename* *default-pathname-defaults*)))
  (load (merge-pathnames "package.lisp" base))
  (load (merge-pathnames "fatos_credito.lisp" base))
  (load (merge-pathnames "regras_credito.lisp" base))
  (load (merge-pathnames "interface_credito.lisp" base)))

(format t "~&Credito bancario carregado. Use (credito-bancario:run).~%")

(in-package #:credito-bancario)

(defun texto-simbolo (simbolo)
  (string-downcase (symbol-name simbolo)))

(defun formatar-moeda (valor)
  (format nil "R$ ~,2f" valor))

(defun texto-status (status)
  (case status
    (:aprovado "APROVADO")
    (:reprovado "REPROVADO")
    (otherwise (string-upcase (texto-simbolo status)))))

(defun texto-dividas (valor)
  (if valor "Sim" "Não"))

(defun listar-clientes ()
  (dolist (cliente *clientes*)
    (format t "~A - ~A~%" (cliente-id cliente) (cliente-nome cliente)))
  (values))

;; Exibe no Listener todos os dados do cliente e o resultado da analise.
(defun imprimir-resultado (id)
  (let ((cliente (buscar-cliente id)))
    (if (null cliente)
        (format t "Cliente nao encontrado: ~A~%" id)
        (let ((resultado (resultado-cliente id)))
          (format t "~%============================================================~%")
          (format t "ANÁLISE DE CRÉDITO~%")
          (format t "============================================================~%")
          (format t "Cliente: ~A~%" (cliente-nome cliente))
          (format t "ID: ~A~%" (cliente-id cliente))
          (format t "Idade: ~A~%" (cliente-idade cliente))
          (format t "Renda mensal: ~A~%" (formatar-moeda (cliente-renda-mensal cliente)))
          (format t "Score: ~A~%" (cliente-score cliente))
          (format t "Dívidas em aberto: ~A~%"
                  (texto-dividas (cliente-dividas-em-aberto cliente)))
          (format t "Atrasos nos ultimos 12 meses: ~A~%"
                  (cliente-atrasos-ultimos-12-meses cliente))
          (format t "~%")
          (format t "Valor solicitado: ~A~%"
                  (formatar-moeda (cliente-valor-solicitado cliente)))
          (format t "Parcelas: ~A~%" (cliente-parcelas cliente))
          (format t "Finalidade: ~A~%" (cliente-finalidade cliente))
          (format t "~%")
          (format t "Resultado: ~A~%"
                  (texto-status (resultado-status resultado)))
          (format t "Risco: ~A~%" (texto-simbolo (resultado-risco resultado)))
          (format t "Limite maximo calculado: ~A~%"
                  (formatar-moeda (resultado-limite-maximo resultado)))
          (format t "Limite aprovado: ~A~%"
                  (formatar-moeda (resultado-limite-aprovado resultado)))
          (format t "Taxa de juros mensal: ~,2f%~%"
                  (resultado-taxa-juros-mensal resultado))
          (format t "Motivos:~%")
          (dolist (motivo (resultado-motivos resultado))
            (format t "- ~A~%" motivo))
          (format t "============================================================~%"))))
  (values))

(defun analisar-cliente (id)
  (imprimir-resultado id))

(defun analisar-todos ()
  (dolist (cliente *clientes*)
    (imprimir-resultado (cliente-id cliente)))
  (values))

(defun run ()
  (analisar-todos)
  (values))

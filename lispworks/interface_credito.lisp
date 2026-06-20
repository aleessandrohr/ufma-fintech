(in-package #:credito-bancario)

(defun texto-simbolo (simbolo)
  (string-downcase (symbol-name simbolo)))

(defun texto-status (status)
  (case status
    (:aprovado "cliente aprovado")
    (:reprovado "cliente reprovado")
    (otherwise (texto-simbolo status))))

(defun texto-dividas (valor)
  (if valor "sim" "nenhuma"))

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
          (format t "~%==============================~%")
          (format t "Cliente: ~A~%" (cliente-nome cliente))
          (format t "ID: ~A~%" (cliente-id cliente))
          (format t "Idade: ~A~%" (cliente-idade cliente))
          (format t "Renda mensal: ~,2f~%" (cliente-renda-mensal cliente))
          (format t "Score: ~A~%" (cliente-score cliente))
          (format t "Dividas em aberto: ~A~%"
                  (texto-dividas (cliente-dividas-em-aberto cliente)))
          (format t "Atrasos nos ultimos 12 meses: ~A~%"
                  (cliente-atrasos-ultimos-12-meses cliente))
          (format t "Valor solicitado: ~,2f~%"
                  (cliente-valor-solicitado cliente))
          (format t "Parcelas: ~A~%" (cliente-parcelas cliente))
          (format t "Finalidade: ~A~%" (cliente-finalidade cliente))
          (format t "Resultado: ~A~%"
                  (texto-status (resultado-status resultado)))
          (format t "Risco: ~A~%" (texto-simbolo (resultado-risco resultado)))
          (format t "Limite maximo calculado: ~,2f~%"
                  (resultado-limite-maximo resultado))
          (format t "Limite aprovado: ~,2f~%"
                  (resultado-limite-aprovado resultado))
          (format t "Taxa de juros mensal: ~,2f~%"
                  (resultado-taxa-juros-mensal resultado))
          (format t "Motivos:~%")
          (dolist (motivo (resultado-motivos resultado))
            (format t "- ~A~%" motivo))
          (format t "==============================~%"))))
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

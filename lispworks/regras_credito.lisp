(in-package #:credito-bancario)

;; Constantes que centralizam os criterios de aprovacao, limite e juros.
(defparameter +idade-minima+ 18)
(defparameter +renda-minima+ 1500.0)
(defparameter +score-minimo+ 400)
(defparameter +score-minimo-com-divida+ 600)
(defparameter +maximo-parcelas+ 48)
(defparameter +multiplicador-maximo-valor-renda+ 5)

(defparameter +limiar-score-excelente+ 800)
(defparameter +limiar-score-bom+ 700)
(defparameter +limiar-score-regular+ 600)
(defparameter +limiar-score-baixo+ 400)

(defparameter +multiplicador-limite-score-excelente+ 4)
(defparameter +multiplicador-limite-score-bom+ 3)
(defparameter +multiplicador-limite-score-regular+ 2)
(defparameter +multiplicador-limite-score-baixo+ 1)

(defparameter +penalidade-divida+ 0.30)
(defparameter +penalidade-atrasos+ 0.20)
(defparameter +atrasos-minimos-penalidade+ 3)

(defparameter +taxa-juros-score-excelente+ 1.5)
(defparameter +taxa-juros-score-bom+ 2.5)
(defparameter +taxa-juros-score-regular+ 3.5)
(defparameter +taxa-juros-score-baixo+ 5.0)

(defparameter +acrescimo-juros-divida+ 1.0)
(defparameter +acrescimo-juros-atrasos+ 0.5)
(defparameter +acrescimo-juros-percentual-limite+ 0.5)
(defparameter +percentual-solicitado-para-acrescimo+ 0.70)

(defun arredondar-2 (valor)
  (/ (float (round (* valor 100.0))) 100.0))

(defun buscar-cliente (id)
  (find id *clientes* :key #'cliente-id :test #'string=))

(defun exigir-cliente (id)
  (or (buscar-cliente id)
      (error "Cliente nao encontrado: ~A" id)))

;; Validacoes minimas exigidas antes de calcular a aprovacao final.
(defun idade-valida-p (cliente)
  (>= (cliente-idade cliente) +idade-minima+))

(defun renda-valida-p (cliente)
  (>= (cliente-renda-mensal cliente) +renda-minima+))

(defun score-valido-p (cliente)
  (>= (cliente-score cliente) +score-minimo+))

(defun parcelas-validas-p (cliente)
  (let ((parcelas (cliente-parcelas cliente)))
    (and (>= parcelas 1)
         (<= parcelas +maximo-parcelas+))))

(defun valor-por-renda-valido-p (cliente)
  (<= (cliente-valor-solicitado cliente)
      (* (cliente-renda-mensal cliente)
         +multiplicador-maximo-valor-renda+)))

(defun divida-com-score-valida-p (cliente)
  (or (not (cliente-dividas-em-aberto cliente))
      (>= (cliente-score cliente) +score-minimo-com-divida+)))

(defun motivo-reprovacao-idade (cliente)
  (unless (idade-valida-p cliente)
    "Cliente reprovado por nao atingir a idade minima de 18 anos."))

(defun motivo-reprovacao-renda (cliente)
  (unless (renda-valida-p cliente)
    "Cliente reprovado por nao atingir a renda minima de R$ 1500,00."))

(defun motivo-reprovacao-score (cliente)
  (unless (score-valido-p cliente)
    "Cliente reprovado por score abaixo do minimo de 400."))

(defun motivo-reprovacao-parcelas (cliente)
  (unless (parcelas-validas-p cliente)
    "Cliente reprovado por quantidade de parcelas invalida (deve ser entre 1 e 48)."))

(defun motivo-reprovacao-valor-renda (cliente)
  (unless (valor-por-renda-valido-p cliente)
    "Cliente reprovado porque o valor solicitado e maior que 5 vezes a renda mensal."))

(defun motivo-reprovacao-divida-score (cliente)
  (unless (divida-com-score-valida-p cliente)
    "Cliente reprovado por ter divida em aberto com score menor que 600."))

(defun motivos-reprovacao (cliente)
  (remove nil
          (list
           (motivo-reprovacao-idade cliente)
           (motivo-reprovacao-renda cliente)
           (motivo-reprovacao-score cliente)
           (motivo-reprovacao-parcelas cliente)
           (motivo-reprovacao-valor-renda cliente)
           (motivo-reprovacao-divida-score cliente))))

(defun automaticamente-reprovado-p (cliente)
  (not (null (motivos-reprovacao cliente))))

;; Calcula o limite maximo com base no score e aplica penalidades de risco.
(defun multiplicador-limite (score)
  (cond
   ((>= score +limiar-score-excelente+)
    +multiplicador-limite-score-excelente+)
   ((>= score +limiar-score-bom+)
    +multiplicador-limite-score-bom+)
   ((>= score +limiar-score-regular+)
    +multiplicador-limite-score-regular+)
   ((>= score +limiar-score-baixo+)
    +multiplicador-limite-score-baixo+)
   (t 0)))

(defun limite-base-cliente (cliente)
  (* (cliente-renda-mensal cliente)
     (multiplicador-limite (cliente-score cliente))))

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

(defun taxa-juros-base-cliente (cliente)
  (let ((score (cliente-score cliente)))
    (cond
     ((>= score +limiar-score-excelente+) +taxa-juros-score-excelente+)
     ((>= score +limiar-score-bom+) +taxa-juros-score-bom+)
     ((>= score +limiar-score-regular+) +taxa-juros-score-regular+)
     ((>= score +limiar-score-baixo+) +taxa-juros-score-baixo+)
     (t 0.0))))

;; Calcula a taxa final somando acrescimos por divida, atrasos e uso alto do limite.
(defun taxa-juros (id)
  (let* ((cliente (exigir-cliente id))
         (limite (limite-maximo id))
         (juros (taxa-juros-base-cliente cliente)))
    (when (cliente-dividas-em-aberto cliente)
      (incf juros +acrescimo-juros-divida+))
    (when (>= (cliente-atrasos-ultimos-12-meses cliente)
              +atrasos-minimos-penalidade+)
      (incf juros +acrescimo-juros-atrasos+))
    (when (and (> limite 0)
               (> (cliente-valor-solicitado cliente)
                  (* limite +percentual-solicitado-para-acrescimo+)))
      (incf juros +acrescimo-juros-percentual-limite+))
    (arredondar-2 juros)))

(defun risco-cliente (cliente status)
  (cond
   ((eq status :reprovado) :reprovado)
   ((and (>= (cliente-score cliente) +limiar-score-excelente+)
         (not (cliente-dividas-em-aberto cliente))
         (= (cliente-atrasos-ultimos-12-meses cliente) 0))
    :baixo)
   ((>= (cliente-score cliente) +limiar-score-regular+)
    :medio)
   (t :alto)))

(defun motivos-aprovacao (cliente)
  (remove nil
          (list
           (when (and (idade-valida-p cliente)
                      (renda-valida-p cliente)
                      (score-valido-p cliente))
             "Cliente atende aos criterios minimos de idade, renda e score.")
           (when (>= (cliente-score cliente) +limiar-score-excelente+)
             "Score alto permitiu limite base maior.")
           (when (not (cliente-dividas-em-aberto cliente))
             "Nao ha dividas em aberto.")
           "Valor solicitado esta dentro do limite calculado.")))

;; Funcao principal das regras: retorna aprovado ou reprovado com limite, juros e motivos.
(defun resultado-cliente (id)
  (let* ((cliente (exigir-cliente id))
         (motivos (motivos-reprovacao cliente)))
    (cond
     (motivos
      (make-resultado
       :status :reprovado
       :risco :reprovado
       :limite-maximo 0.0
       :limite-aprovado 0.0
       :taxa-juros-mensal 0.0
       :motivos motivos))
     (t
      (let ((limite (limite-maximo id))
            (valor-solicitado (cliente-valor-solicitado cliente)))
        (if (> valor-solicitado limite)
            (make-resultado
             :status :reprovado
             :risco :reprovado
             :limite-maximo limite
             :limite-aprovado 0.0
             :taxa-juros-mensal 0.0
             :motivos
             (list
              (format nil
                      "Cliente reprovado porque o valor solicitado esta acima do limite calculado de ~,2f."
                      limite)))
            (make-resultado
             :status :aprovado
             :risco (risco-cliente cliente :aprovado)
             :limite-maximo limite
             :limite-aprovado valor-solicitado
             :taxa-juros-mensal (taxa-juros id)
             :motivos (motivos-aprovacao cliente))))))))

(defun aprovado-p (id)
  (eq (resultado-status (resultado-cliente id)) :aprovado))

(defun reprovado-p (id)
  (eq (resultado-status (resultado-cliente id)) :reprovado))

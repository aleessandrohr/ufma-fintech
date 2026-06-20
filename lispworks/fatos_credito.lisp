(in-package #:credito-bancario)

;; Estrutura que representa os dados cadastrais e financeiros do cliente.
(defstruct cliente
  id
  nome
  idade
  renda-mensal
  score
  dividas-em-aberto
  atrasos-ultimos-12-meses
  valor-solicitado
  parcelas
  finalidade)

;; Estrutura que representa a decisao final da analise de credito.
(defstruct resultado
  status
  risco
  limite-maximo
  limite-aprovado
  taxa-juros-mensal
  motivos)

;; Base ficticia de clientes usada como armazenamento interno em memoria.
(defparameter *clientes*
  (list
   (make-cliente
    :id "ANA001"
    :nome "Ana Souza"
    :idade 28
    :renda-mensal 6000.0
    :score 850
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 5000.0
    :parcelas 12
    :finalidade "emprestimo pessoal")
   (make-cliente
    :id "BRU001"
    :nome "Bruno Lima"
    :idade 17
    :renda-mensal 3000.0
    :score 700
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 1000.0
    :parcelas 12
    :finalidade "curso profissionalizante")
   (make-cliente
    :id "CAR001"
    :nome "Carla Mendes"
    :idade 35
    :renda-mensal 1200.0
    :score 720
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 1000.0
    :parcelas 6
    :finalidade "compra de equipamento")
   (make-cliente
    :id "DAN001"
    :nome "Daniel Rocha"
    :idade 42
    :renda-mensal 4000.0
    :score 350
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 1000.0
    :parcelas 6
    :finalidade "emprestimo pessoal")
   (make-cliente
    :id "EVA001"
    :nome "Eva Martins"
    :idade 30
    :renda-mensal 2500.0
    :score 650
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 20000.0
    :parcelas 24
    :finalidade "reforma residencial")
   (make-cliente
    :id "FEL001"
    :nome "Felipe Alves"
    :idade 32
    :renda-mensal 5000.0
    :score 580
    :dividas-em-aberto t
    :atrasos-ultimos-12-meses 1
    :valor-solicitado 2000.0
    :parcelas 10
    :finalidade "emprestimo pessoal")
   (make-cliente
    :id "GAB001"
    :nome "Gabriela Costa"
    :idade 40
    :renda-mensal 5000.0
    :score 720
    :dividas-em-aberto t
    :atrasos-ultimos-12-meses 1
    :valor-solicitado 2000.0
    :parcelas 10
    :finalidade "capital de giro")
   (make-cliente
    :id "HEL001"
    :nome "Helena Pereira"
    :idade 29
    :renda-mensal 3000.0
    :score 700
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 7000.0
    :parcelas 18
    :finalidade "compra de computador")
   (make-cliente
    :id "IAL001"
    :nome "Ialo Ferreira"
    :idade 30
    :renda-mensal 3000.0
    :score 650
    :dividas-em-aberto nil
    :atrasos-ultimos-12-meses 0
    :valor-solicitado 7000.0
    :parcelas 18
    :finalidade "emprestimo pessoal")))

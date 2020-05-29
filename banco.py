from threading import Thread
import time
import random
import sys

#TESTADO EM PYTHON 3.5

#o programa aceita 3 parametros
#modo de execucao das threads
#quantidade a tranferir
#modo verboso

# banco.py 0 50 v

#executa o codigo com a vulnerabilidade "banco.py 1 50 v"
#executar o codigo corretamente "banco.py 3 10 v"

class Cliente:
    def __init__(self, nome, grana):
        self.nome = nome
        self.grana = grana

    def setGrana(self, grana):
        self.grana=grana

#funcao de tranferencia de dinheiro
def tranferencia(clienteA, dinheiroTransferir, clienteB):
    #converte parametro para int
    dinheiroTransferir = int(dinheiroTransferir)
    dinheiroInicial = clienteA.grana

    if(dinheiroInicial >= dinheiroTransferir):
        #simula o tempo aleatorio para a transferencia
        time.sleep(random.uniform(0, 0.2))
        clienteB.setGrana(clienteB.grana + dinheiroTransferir)
        #simula o tempo aleatorio para a transferencia
        time.sleep(random.uniform(0, 0.2))
        clienteA.setGrana(dinheiroInicial - dinheiroTransferir)
        
        #modo verboso
        if(len(sys.argv) > 3):
            if(sys.argv[3] == 'v'):
                print("Transferencia efetuada com sucesso")
                print(clienteA.nome,":",clienteA.grana,
                '\n'+clienteB.nome,":",clienteB.grana)
    
    else:
        print("Transferencia nao efetuada - saldo insuficiente")

#cria dois clientes
daniel = Cliente("Daniel", 1000)
mateus = Cliente("Mateus", 1000)

#exemplo race condition 
#0 mostra uma tranferencia comum
if(sys.argv[1] == '0'):
    tranferencia(daniel, sys.argv[2], mateus)

#mostra força bruta de tranferencia para forçar race condition
elif(sys.argv[1] == '1'):
    for i in range(100):
        transfereGrana = Thread(target=tranferencia, args=(daniel, sys.argv[2] , mateus,))
        transfereGrana.start()

#mostra força bruta de tranferencia para forçar race condition para gerar dinheiro
elif(sys.argv[1] == '2'):
    for i in range(100):
        transfereGrana = Thread(target=tranferencia, args=(daniel, sys.argv[2] , mateus,))
        transfereGrana.start()
    time.sleep(2)
    for i in range(100):
        transfereGrana = Thread(target=tranferencia, args=(mateus, sys.argv[2] , daniel,))
        transfereGrana.start()

#mostra coreção da execução de maneira a não causar problema
elif(sys.argv[1] == '3'):
    for i in range(100):
        transfereGrana = Thread(target=tranferencia, args=(daniel, sys.argv[2] , mateus,))
        transfereGrana.start()
        transfereGrana.join()

#Espera treads finalizarem
time.sleep(3)

print("##########################")
print(daniel.nome+":",daniel.grana)
print(mateus.nome+":",mateus.grana)
print("##########################")

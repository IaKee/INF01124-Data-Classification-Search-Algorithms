#LABORATORIO 2 - CPD
#Nome: Giordano Souza de Paula
#Cartão UFRGS: 00308054

import math
import random
from timeit import default_timer as timer

recursoes = 0
swaps = 0

def swap(a, b): #Inverte a variavel a pela b
    global swaps
    temp = a
    a = b
    b = temp
    swaps += 1
def termoAleatorio(array, primeiroTermo, ultimoTermo): #Escolhe uma posiçao aleatorio de termo do array
    if abs(ultimoTermo - primeiroTermo) > 1:
        rnd = random.randrange(primeiroTermo, ultimoTermo)
    else:
        rnd = ultimoTermo
    return rnd
def mediana(array, inicio, fim): #Calcula a mediana do array informado
    med = 0
    aux = []
    tamanho = fim - inicio #Tamanho da partição do array informado
    aux.append(array[inicio])
    aux.append(array[fim])
    if tamanho > 2:
        aux.append(array[inicio+(tamanho//2)])
    aux.sort()
    if aux[1] == array[fim]:
        med = fim
    else:
        if aux[1] == array[inicio]:
            med = inicio
        else:
            med = inicio+(tamanho//2)
    return med
def quickSort(array, primeiroTermo, ultimoTermo):
    #Declara que essa função vai modificar variaveis globais
    global recursoes
    global swaps

    if primeiroTermo < ultimoTermo:
        #pontodeQuebra = particionaLomuto(array, primeiroTermo, ultimoTermo, mediana(array, primeiroTermo, ultimoTermo))
        #pontodeQuebra = particionaLomuto(array, primeiroTermo, ultimoTermo, termoAleatorio(array, primeiroTermo, ultimoTermo))

        pontodeQuebra = particionaHoare(array, primeiroTermo, ultimoTermo, termoAleatorio(array, primeiroTermo, ultimoTermo))
        #pontodeQuebra = particionaHoare(array, primeiroTermo, ultimoTermo, mediana(array, primeiroTermo, ultimoTermo))

        recursoes += 1
        quickSort(array, primeiroTermo, int(pontodeQuebra or 0) - 1)
        recursoes += 1
        quickSort(array, int(pontodeQuebra or 0) + 1, ultimoTermo)

def particionaHoare(array, primeiroTermo, ultimoTermo, particionador):
    global swaps
    while primeiroTermo <= ultimoTermo:
        while True:
            primeiroTermo += 1
            if not (primeiroTermo < ultimoTermo and array[primeiroTermo] < particionador): break
        while True:
            ultimoTermo -= 1
            if not (ultimoTermo >= primeiroTermo and array[ultimoTermo] >= particionador): break
        if primeiroTermo < ultimoTermo:
            array[primeiroTermo],array[ultimoTermo] = array[ultimoTermo],array[primeiroTermo]
    if ultimoTermo != 0:
        swaps += 1
        swap(array[primeiroTermo], array[ultimoTermo])
        return ultimoTermo

with open("entrada-quicksort.txt", 'r') as inputFile:
    with open("stats-aleatorio-hoare.txt", 'w') as outputFile:
        for linha in inputFile:
            array = []
            linha = linha.strip()
            linha = linha.rstrip("\n")
            linha = linha.split(" ")
            for i in linha:
                array.append(int(i)) #Soma a

            array.pop(0) #Ignora o primeiro elemento do array (numero de elementos da linha)
            tamanhoLinha = len(array)
            tempoInicio = timer()
            #alg(array, 0, m - 1, met)
            quickSort(array, 0, len(array)-1)
            tempoTot = timer() - tempoInicio

            #Formata a linha lida do arquivo (tirando espaços)
            string = str(tamanhoLinha) + " " + str(array) + "\n"
            #string = string.replace("[", "")
            #string = string.replace("]", "")
            string = string.replace(" ", "")
            outputFile.write("TAMANHO ENTRADA " + str(tamanhoLinha) + "\n")
            outputFile.write("SWAPS #" + str(swaps) + "\n")
            outputFile.write("RECURSOES #" + str(recursoes) + "\n")
            outputFile.write("TEMPO #" + "{:.6f}".format(tempoTot) + "\n") #O tempo foi formatado para ter 6 casas decimais

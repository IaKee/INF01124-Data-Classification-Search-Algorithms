import numpy
import math
import time
stringLida = open('C:/Users/IaKee/Desktop/entrada2.txt', 'r')
w = open('C:/Users/IaKee/Desktop/saida1.txt', 'w')
time_output = open('C:/Users/IaKee/Desktop/saida2.txt', 'w')

def shellSort(stringLida, operador, n, array):
    if(operador == 'SHELL'):
        incrementador = len(stringLida)//2
    elif(operador == 'KNUTH'):
        incrementador = 1
        while (incrementador < len(stringLida)):
            incrementador = (incrementador * 3) + 1
        incrementador = incrementador // 3 #pula o primeiro n sei
    elif(operador == 'CIURA'):
        ciura = [1, 4, 10, 23, 57, 132, 301, 701]

        if(math.floor(len(stringLida)/2) > 701): #Se o incrementador original for maior do que 701....
            while(math.floor(len(stringLida)/2) > ciura[len(ciura)-1]): #enquanto o incrementador calculado for maior do que o ultimo termo da sequencia de ciura
                var = math.floor(ciura[len(ciura)-1]*2.25)
                ciura.append(var)
            incrementador = ciura[len(ciura)-1]

        else: #pega o menor numero possivel do array ciura
            while(math.floor(len(stringLida)/2) < ciura[len(ciura)-1]): #enquanto o incrementador for menor que o ultimo termo do array
                last = ciura[len(ciura)-1]
                ciura.pop() #exclui o ultimo termo
            ciura.append(last)
            incrementador = ciura[len(ciura) - 1]


    while incrementador > 0:

      for startposition in range(incrementador):
        gapInsertionSort(stringLida,startposition,incrementador)

      string = str(n) + " " + str(array)  # insere o primeiro caractere como sendo o tamanho da string
      string = string.replace("[", "")  # Tira '[' ']' e ',' da string
      string = string.replace("]", "")
      # string = string.replace(",", "")

      # Escreve no arquivo de saida
      w.write(string + ' INCR=' + str(incrementador) + "\n")

      if(operador == 'SHELL'):
        incrementador = incrementador // 2 #incremento é calculado como potencias de 2 (shellsort)
      elif(operador == 'KNUTH'):
          incrementador = incrementador//3
      elif(operador == 'CIURA'):
          if(len(ciura) > 1):
            ciura.pop()
            incrementador = ciura[len(ciura)-1]
          else:
              incrementador = 0

def gapInsertionSort(stringLida,start,gap):
    for i in range(start+gap,len(stringLida),gap):

        currentvalue = stringLida[i]
        position = i

        while position>=gap and stringLida[position-gap]>currentvalue:
            stringLida[position]=stringLida[position-gap]
            position = position-gap

        stringLida[position]=currentvalue

def leArquivo():
    flag = 0
    for line in stringLida:
        array = []
        buffer = stringLida.readline()
        buffer = line.rstrip("\n")


        # reading each word
        line = line.strip()
        line = line.rstrip("\n")
        line = line.split(" ")

        for word in line:
            array.append(int(word))

        teste=next((x for x in array if x == 1000), None)
        if(teste != None) and flag == 0:
            print(array)
            flag=1
        primeiro_elem = array.pop(0)
        n = len(array)

        w.write(buffer + 'SEQ=' + 'SHELL' + '\n')  # copia a primeira linha do arquivo de entrada para o arquivo de saida
        #log = math.log(primeiro_elem, 10)
        #log = math.ceil(log)

       # print(primeiro_elem,' -> log: ', log)
        #if(log % 1 == 0): #Se o resto do logaritmo base 10 do tamanho da linha for zero (o numero é potencia de 10)
        firsttime = time.time()
        shellSort(array, 'SHELL', n, array)
        secondtime = time.time()
        time_output.write('SHELL, ' + str(len(array)) + ',' + str(secondtime - firsttime) + '\n')  # escreve o tempo decorrido da operacao no arquivo de saida
        print('SHELL, ' + str(len(array)) + ',' + str(secondtime - firsttime))
        #else:
            #shellSort(array, 'SHELL', n, array)

        w.write(buffer + 'SEQ=' + 'KNUTH' + '\n')  # copia a primeira linha do arquivo de entrada para o arquivo de saida
        log = math.log(primeiro_elem, 10)
        #if (log % 1 == 0):  # Se o resto do logaritmo base 10 do tamanho da linha for zero (o numero é potencia de 10)
        firsttime = time.time()
        shellSort(array, 'KNUTH', n, array)
        secondtime = time.time()
        time_output.write('KNUTH, ' + str(len(array)) + ',' + str(secondtime - firsttime) + '\n')  # escreve o tempo decorrido da operacao no arquivo de saida
        print('KNUTH, ' + str(len(array)) + ',' + str(secondtime - firsttime))
        #else:
        #    shellSort(array, 'KNUTH', n, array)

        w.write(buffer + 'SEQ=' + 'CIURA' + '\n')  # copia a primeira linha do arquivo de entrada para o arquivo de saida
        log = math.log(primeiro_elem, 10)
        #if (log % 1 == 0):  # Se o resto do logaritmo base 10 do tamanho da linha for zero (o numero é potencia de 10)
        firsttime = time.time()
        shellSort(array, 'CIURA', n, array)
        secondtime = time.time()
        time_output.write('CIURA, ' + str(len(array)) + ',' + str(secondtime - firsttime) + '\n')  # escreve o tempo decorrido da operacao no arquivo de saida
        print('CIURA, ' + str(len(array)) + ',' + str(secondtime - firsttime))
        #else:
        #    shellSort(array, 'CIURA', n, array)

leArquivo()

stringLida.close()
w.close()
time_output.close()
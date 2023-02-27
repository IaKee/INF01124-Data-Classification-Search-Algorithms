#Nome: Giordano Souza de Paula
#Cartão UFRGS: 00308054

#Observaçoes:
#-No caso de uma colisão, na inserção de um novo elemento na tabela, o elemento será inserido em uma lista encadeada, na
#chave hash correspondente ao mesmo (o elemento é sempre inserido no final da lista) - conforme proposto no enunciado

colisoes = 0
profundidade = 0

#Classe para operar com uma lista encadeada, no caso de ocorrer uma colisão ao inserir um elemento na tabela
class NodoLista:
    global colisoes
    def __init__(self, string):
        self.string = string #Nome lido do arquivo
        self.proximo = None #Endereço do proximo termo da LSE, se houver

    #Insere o elemento em uma LSE, em caso de colisão
    def encadeia(self, proximo):
        self.proximo = proximo

    #Obtem a variavel string da classe
    def getString(self):
        return self.string

    #Atualiza a variavel string da classe
    def setString(self, string):
        self.string = string

    #Obtem o proximo elemento da LSE, se houver uma colisão
    def getProximo(self):
        return self.proximo

    #Imprime o termo atual e os ligados a esse (em caso de LSE)
    def printR(self):
        print(self.string)
        atual = self.proximo
        while(atual != None):
            print(atual.getString())
            atual = atual.getProximo()
#Classe para operar com uma tabela Hash
class TabelaHash:

    def __init__(self, tamanho):
        self.tamanho = tamanho #Tamanho da tabela hash
        self.lista = [] #String com o nome lido do arquivo
        for i in range(tamanho): #Linha x coluna (tamanho é a qtd de colunas)
            self.lista.append(NodoLista(""))

    #Calcula a chave hash para a string informada
    def hashKey(self, string):
        key = 0
        aux = string.upper()
        for i in range(0, len(aux)):
            key += ord(aux[i]) * (27 ** (len(aux) - i-1))
            #print((len(aux) - i-1))
        return key % self.tamanho

    def insertHash(self, string):
        global colisoes

        chave = self.hashKey(string)
        #print(chave)

        if(self.lista[chave].getString() == ""):
            self.lista[chave].setString(string) #Insere a string, se o espaço estiver disponivel
        else:
            #Se ocorrer uma colisão
            colisoes += 1
            #print("Colisão")
            atual = self.lista[chave]
            while(atual.getProximo() != None):
                atual = atual.getProximo()
            atual.encadeia(NodoLista(string))

    def consulta(self, string):
        acessos = 0
        chave = self.hashKey(string)

        if (self.lista[chave].getString() == string):
            acessos += 1
            return acessos
        else:
            atual = self.lista[chave]
            while (atual.getProximo() != None):
                acessos += 1
                if (atual.getString() == string):
                    return acessos

                atual = atual.getProximo()
            return -1

    #Consulta e retorna a profundidade
    def profundidade(self, string):
        profundidade = 0
        chave = self.hashKey(string)
        atual = self.lista[chave]
        #self.lista[chave].printR()
        while (atual.getProximo() != None):
            profundidade += 1
            atual = atual.getProximo()
        return profundidade

hashKey = 0 #Inicia a chave hash como 0 (nao utilizado)

inputFilePath = "nomes_10000.txt"
inputSearch = "consultas.txt"
inputFile = open(inputFilePath,'r')
searchFile = open(inputSearch, 'r')
tableSize = [503, 2503, 5003, 7507]
Tabela = []
count = 0
totConsultas = 0
maximo = 0

#Para os valores informados em tableSize (exigidos no enunciado do trabalho)
for i in tableSize:
    fileOutput = open("experimento{0}.txt".format(i), "w")
    print("Criando uma tabela hash com o tamanho {0}.".format(i))

    Tabela.append(TabelaHash(i)) #Aloca uma tabela hash com tamanho i

    #Le todos os 10.000 nomes do arquivo de entrada, e vai inserindo na tabela hash
    for line in inputFile:
        line = line.strip() #tira o \n, e espaços antes/depois do nome
        Tabela[len(Tabela)-1].insertHash(line)
        #print(line)

    for line in searchFile:
        line = line.strip()
        consultas = Tabela[len(Tabela)-1].consulta(line)

        if(consultas != -1):
            totConsultas += consultas
            line = line + " {0}\n".format(consultas)
            if (maximo < consultas):
                maximo = consultas
        else:
            handler = Tabela[len(Tabela)-1].profundidade(line)
            line = line + " {0}\n".format(handler + 1) #Imprime o maximo de colisoes dessa consulta, e soma 1 ao total
            #line = line + " o número maximo de colisões + 1.\n"
            totConsultas += handler + 1
            if (maximo < handler + 1):
                maximo = handler + 1
        fileOutput.write(line)

    fileOutput.write("MEDIA {0}\n".format(totConsultas/50))
    fileOutput.write("MAXIMO {0}".format(maximo))

    print("Nomes inseridos na tabela de tamanho {0}, com {1} colisões.".format(i, colisoes))
    inputFile.seek(0, 0)
    searchFile.seek(0, 0)
    fileOutput.close()
    colisoes = 0
    count += 1
    maximo = 0
    totConsultas = 0

inputFile.close()
searchFile.close()
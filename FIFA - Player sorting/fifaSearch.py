import _tkinter
import csv
import math
import sys
from tkinter import *
from tkinter.ttk import *
import time as tm
from random import randint
from unidecode import unidecode

def newline(number):  # pula -number- linhas em branco
    for i in range(number):
        print("")
def openFile(path):
    #print("Abrindo arquivo {0} - de tamanho {1:.2f}Mb...".format(path, os.path.getsize(path) / 1000/1000))
    try:
        return open(path, encoding="utf8")
    except:
        print("Ocorreu um erro ao abrir o arquivo {0}!".format(path))
        return -1
def closeFiles():
    global tabelaPlayers
    global tabelaRatings
    global tabelaTags
    global tabelaMinirating

    try:
        newline(1)
        print("Fechando arquivos...")
        tabelaPlayers.close()
        print("Arquivo {0} fechado.".format(caminhoArquivoPlayers))
        tabelaRatings.close()
        print("Arquivo {0} fechado.".format(caminhoArquivoRatings))
        tabelaTags.close()
        print("Arquivo {0} fechado.".format(caminhoArquivoTags))
    except:
        newline(2)
        print("Ocorreu um erro ao fechar um dos arquivos!!")
        return -1
class player:
    def __init__(self, fifaId, name="", player_positions=""):
        self.fifaId = int(fifaId)  # apenas a raiz vai ter o fifaId
        self.name = name  # nome do jogador
        self.player_positions = player_positions  # posiçoes em que o jogador pode jogar
        self.tags = []  # lista de todas as tags informadas para esse jogador
        self.tagrep = []  # array com o numero de repetiçoes das tags (o tamanho da lista é igual a de tags)
        self.usertags = []  # lista com o ID dos usuários que deram as tags

        self.notaTotal = 0  # nota total desse jogador (soma das ratings recebidas)
        self.numRatings = 0
        self.proximo = []

    def encadeia(self, proximo): # Insere o elemento em uma LSE, caso ja exista um rating para esse fifaId
        self.proximo.append(proximo)  # insere no final da lista

    def getNext(self):
        return self.proximo

    def insertRating_player(self, rating):
        # incrementa o numero de ratings e soma a nota total desse jogador
        self.numRatings += 1
        self.notaTotal += rating
        return True

    def setfifaId(self, fifaId):
        self.fifaId = fifaId

    def getfifaId(self):  # devolve o fifaId da classe
        return self.fifaId

    def setpositions(self, positions):
        self.player_positions = positions

    def getpositions(self):  # devolve o fifaId da classe
        return self.player_positions

    def inserttag(self, tag, userId):
        # assume que o mesmo usuário não pode dar 2 reviews no mesmo jogador
        index = 0
        if(self.tags):  # se a lista nao estiver vazia
            for tagi in self.tags:
                if(tag == tagi):  # se ja for encontrada uma tag igual a inserida
                    self.usertags[index].append(userId)
                    self.tagrep[index] += 1
                    return False
                index += 1
        # se não, insere no final da lista de tags
        self.usertags.append([])  # aloca uma nova lista, de IDs de usuários que aplicaram essa tag
        self.usertags[index].append(userId)
        self.tagrep.append(1)  # inicializa a lista de repetiçoes de tags desse jogador como 1
        self.tags.append(tag)  # insere a tag no final da lista de tags deste jogador
        return True

    def gettags(self):  # devolve o fifaId da classe
        return self.tags

    def gettagrep(self):
        return self.tagrep

    def getusertag(self):
        return self.usertags

    def setname(self, name):
        self.name = name

    def getname(self):  # devolve o fifaId da classe
        return self.name

    def getRatingSum(self):
        return self.notaTotal

    def getReviewsNum(self):
        return self.numRatings

    def getAverage(self):
        return (self.notaTotal/self.numRatings)

    def copy(self):
        return player(self.fifaId, self.name, self.player_positions)
class TabelaHashJogadores:
    def __init__(self, tamanho):
        self.tamanho = tamanho  # o tamanho da tabela hash
        self.lista = [None] * tamanho  # aloca uma lista do tamanho da tabela

    def hashKey(self, fifaId):
        x = int(fifaId) * 2654435761
        return x % self.tamanho

    def insertHash(self, jogador):  #
        key = self.hashKey(jogador.getfifaId())

        if(self.lista[key] == None):  # se a posição do fifaID estiver vazia, preenche
            self.lista[key] = jogador
        else:  # se a posiçao estiver ocupada, encadeia
            self.lista[key].encadeia(jogador.copy())

    def getplayer(self, fifaId=0):  # busca pelo fifaId
        key = self.hashKey(fifaId)
        if(self.lista[key] == None):  # se não for encontrado
            return None
        if(self.lista[key].getfifaId() == fifaId):
            return self.lista[key]
        else:
            for atual in self.lista[key].getNext():
                if (atual.getfifaId() == fifaId):
                    return atual
            return None  # se não for encontrado

    def getplayerIDlist(self):
        # retona uma lista, com t
        lista_ids = []
        count = 0
        for jogador in self.lista:  # para todos o jogadores da tabela hash
            if(jogador != None):  # se não estiver vazio
                count += 1
                lista_ids.append(jogador.getfifaId()) # adiciona na lista
                #print(jogador.getname())
                atual = jogador.getNext()  # recupera a lista de termos encadeados
                for gamer in atual:  # para todos os jogadores que estão encadeados nesse termo
                    lista_ids.append(gamer.getfifaId())  # adiciona na lista
                    count += 1
        return lista_ids
class User:
    def __init__(self, userId):
        self.userId = int(userId)
        self.ratings_fifaId = []
        self.ratings = []
        self.proximo = []

    def encadeia(self, proximo):
        self.proximo.append(proximo)

    def getratings(self):
        return self.ratings

    def getratings_id(self):
        return self.ratings_fifaId

    def getNext(self):
        return self.proximo

    def copy(self):
        return User(self.userId)

    def getuserId(self):
        return self.userId

    def getfifaId(self):
        return self.fifaId

    def insertRating_user(self, rating, fifaId):
        # duas listas são criadas em cada usuário, uma com os jogadores que este avaliou
        # e outra com as notas dadas em cada avaliação. Essas duas listas tem o mesmo
        # tamanho, o outro dado correspondente vai estar na mesma posição
        self.ratings_fifaId.append(fifaId)  # insere a nota no final da lista de ids dos jogadores
        self.ratings.append(rating)  # insere a nota no final da lista de notas
class HashTableUsers:
    def __init__(self, tamanho):
        self.tamanho = tamanho  # o tamanho da tabela hash
        self.lista = [None] * tamanho  # aloca uma lista do tamanho da tabela declarada

    def hashKey(self, userId):
        x = int(userId) * 2654435761
        return x % self.tamanho

    def insertHash(self, user, userId):
        key = self.hashKey(userId)
        if(self.lista[key] == None): #Caso não tenha nenhum usuário nessa posição da tabela hash
            self.lista[key] = user
            return 0
        else:  # Caso ja tenha (colisão)
            if (self.lista[key].getuserId() == userId):  # Caso tenha encontrado o mesmo userId
                return 0  # nao adiciona na tabela
            else:  #Caso o userid seja diferente
                while(atual.getNext() != None):
                    atual = atual.getNext()
                    if (self.lista[key].getuserId() == userId):  # Caso tenha encontrado o mesmo userId
                        return  # nao adiciona na tabela
                self.lista[key].encadeia(user.copy())  # se não, adiciona no final da LSE
                #print("Adicionou")
                return 1

    def getuser(self, userId):
        key = self.hashKey(userId)
        if(self.lista[key] == None):
            return None
        if(self.lista[key].getuserId() == userId):
            return self.lista[key]
        else:
            for atual in self.lista[key].getNext():
                if(atual.getuserId == userId):
                    return atual
            return None  # nao esta na lista
class user_rating:
    def __init__(self, rating=0, fifaID=0):
        self.rating = rating
        self.fifaID = fifaID

    def getrating(self):
        return self.rating
    def getfifaID(self):
        return self.fifaID
class playerwName:
    def __init__(self, name="", fifaID=0):
        self.name=name
        self.fifaID=fifaID

    def getname(self):
        return self.name
    def getfifaID(self):
        return self.fifaID
def printplayer_tags(fifaId):
    jogador = playersTable.getplayer(fifaId)
    if (jogador != None):
        newline(2)
        print("Imprimindo tags do jogador {0} de posiçoes: {1}".format(jogador.getname(), jogador.getpositions()))
        for i in range(0, len(jogador.gettags())):
            print("\t{0} - dada pelos {1} usuarios: {2}".format(jogador.gettags()[i], jogador.gettagrep()[i], jogador.getusertag()[i]))

        print("\tNota media do jogador: {0} em {1} avaliaçoes.".format(jogador.getAverage(), jogador.getReviewsNum()))
    else:
        print("Jogador não encontrado")
def printuser_reviews(userId):
    user = usersTable.getuser(userId)
    if(user != None):
        newline(2)
        print("Imprimindo reviews do usuario {0}:".format(user.getuserId()))
        for i in range(0, len(user.getratings())):
            print("\tDeu nota {0} para o jogador {1} - index {2}".format(user.getratings()[i], user.getratings_id()[i], i))
    else:
        print("Usuário não encontrado")
def startloop():
    global startVar
    startVar.set(1)
def closewindow():
    global windowopen
    windowopen = False
def backwardsbubblesort_usersearch(lista):
    # faz o sort invertido para a nota de um jogador
    for passnum in range(len(lista)-1,0,-1):
        for i in range(passnum):
            if lista[i].getrating()<lista[i+1].getrating():  # se o proximo caractere for maior que o atual
                temp = lista[i]
                lista[i] = lista[i+1]
                lista[i+1] = temp
    return(lista)
class TrieNode:
    # classe de nodos da arvore trie
    def __init__(self):
        self.children = [None] * 27  # inicializa cada nodo com 26 possiveis filhos
        self.fifaID = None  # adiciona o campo fifaID para o nodo da arvore, que vai conter o id do jogador
        self.isEndOfName = False  # se o nodo é o fim de uma palavra
class Trie:
    def __init__(self):
        self.root = self.getNode()  # inicializa a raiz como um nodo
    def getNode(self):
        return TrieNode()  # inicializa um nodo
    def _charToIndex(self, ch):
        if(ch == " " or ch == "'" or ch=="." or ch=="-" or ch == '"'):
            return 26
        else:
            return ord(ch) - ord('a')  # retorna um index
    def insert(self, key, fifaID):
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
        pCrawl.isEndOfName = True
        pCrawl.fifaID = fifaID
    def prefixSearch(self, prefix):
        # retorna todos os fifaIDs encontrados a partir dos prefixos de nomes na TRIE
        found = []
        pCrawl = self.root
        length = len(prefix)
        for level in range(length):
            index = self._charToIndex(prefix[level])
            # print("Index linha 320:", index)
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]

        # a partir desse ponto, faz todos os caminhos possiveis
        isListFilled = True
        children = pCrawl.children
        if(pCrawl.isEndOfName):
            found.append(pCrawl.fifaID)
        while(isListFilled):
            children_list = []
            for i in children:
                if(i != None):  # se houver algum dado
                    if(i.isEndOfName):
                        found.append(i.fifaID)
                    for node in i.children:
                        if(node != None):
                            children_list.append(node)
            children = children_list
            if(len(children) == 0):
                isListFilled = False

        return found  # só pode ser none, ou fifaID - Fim de palavra
def searchName():
    global searchTerm
    if(len(searchTerm.get())==0):
        wText4.configure(text="É necessario ter ao menos um caractere para fazer essa pesquisa!")
        wText4.place(x=25, y=180)
        return -1

    # remove uma possivel mensagem de erro da janela
    #wText4.configure(text="")
    # inicializa uma trie, para armazenar os nomes
    tree = Trie()

    # recupera uma lista com todos os jogadores, da tabela hash
    playerlist = playersTable.getplayerIDlist()

    for j in playerlist:  # para cada jogador da tabela (percorre os fifaIDs)
        jogador = playersTable.getplayer(j)
        tree.insert(unidecode(jogador.getname().lower()), int(j))

    sortedList = tree.prefixSearch(searchTerm.get().lower())
    if(sortedList == False):
        wText4.configure(text="Jogador(es) não encontrado(os)!")
        wText4.place(x=115, y=180)
        return -1
    else:
        searchWindow = Tk()
        searchWindow.resizable(False, False)
        searchWindow.title("Resultado da pesquisa pelo jogador '{0}':".format(searchTerm.get().lower()))

        caixaPesquisa.delete(0, END)  # limpa a caixa de pesquisa

        # inicializa a planilha com o titulo das colunas
        entrylist = []
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=0)
        entrylist[-1].insert(END, "SOFIFA ID")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=2)
        entrylist[-1].insert(END, "POSITIONS")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=3)
        entrylist[-1].insert(END, "COUNT")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=4)
        entrylist[-1].insert(END, "GLOBAL RATING")

        if (len(sortedList) < 20):
            arange = len(sortedList)
        else:
            arange = 20

        # calcula a largura da celula de nome
        newwidth = 0
        for i in range(0, arange):
            jogador = playersTable.getplayer(sortedList[i])
            if (newwidth < len(jogador.getname())):
                newwidth = len(jogador.getname()) + 5

        # inicializa a coluna nome, com a nova largura
        entrylist.append(Entry(searchWindow, width=newwidth, foreground='blue'))
        entrylist[-1].grid(row=0, column=1)
        entrylist[-1].insert(END, "NAME")

        for i in range(0, arange):
            jogador = playersTable.getplayer(sortedList[i])
            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=0)
            entrylist[-1].insert(END, str(jogador.getfifaId()))
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=newwidth))
            entrylist[-1].grid(row=i + 1, column=1)
            entrylist[-1].insert(END, jogador.getname())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=2)
            entrylist[-1].insert(END, jogador.getpositions())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=3)
            if(jogador.getReviewsNum() == 0):
                entrylist[-1].insert(END, "0")
            else:
                entrylist[-1].insert(END, jogador.getAverage())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=4)
            entrylist[-1].insert(END, jogador.getReviewsNum())
            entrylist[-1].configure(state=DISABLED)
        searchWindow.update()
def searchId():
    global searchTerm
    global tabelaRatings
    global usersTable

    if (len(searchTerm.get()) == 0):
        wText4.configure(text="É necessario ter ao menos um caractere para fazer essa pesquisa!")
        wText4.place(x=25, y=180)
        return -1
    if (searchTerm.get().isdecimal()):
        userId = int(searchTerm.get())
        usuario = usersTable.getuser(userId)
        if(usuario != None):
            wText4.configure(text="")  # remove uma possivel mensagem de erro da janela
            ratingList = []
            for i in range(0, len(usuario.getratings())):
                ratingList.append(user_rating(usuario.getratings()[i], usuario.getratings_id()[i]))
            sortedList = backwardsbubblesort_usersearch(ratingList)

            searchWindow = Tk()
            searchWindow.resizable(False, False)
            searchWindow.title("Resultado da pesquisa pelo usuário {0}:".format(searchTerm.get()))

            caixaPesquisa.delete(0, END)

            # inicializa a planilha com o titulo das colunas
            entrylist = []
            entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
            entrylist[-1].grid(row=0, column=0)
            entrylist[-1].insert(END, "SOFIFA ID")
            entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
            entrylist[-1].grid(row=0, column=2)
            entrylist[-1].insert(END, "GLOBAL RATING")
            entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
            entrylist[-1].grid(row=0, column=3)
            entrylist[-1].insert(END, "COUNT")
            entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
            entrylist[-1].grid(row=0, column=4)
            entrylist[-1].insert(END, "RATING")

            if (len(sortedList) < 20):
                arange = len(sortedList)
            else:
                arange = 20

            # calcula a largura da celula de nome
            newwidth = 0
            for i in range(0, arange):
                jogador = playersTable.getplayer(sortedList[i].getfifaID())
                if(newwidth < len(jogador.getname())):
                    newwidth = len(jogador.getname())

            # inicializa a coluna nome, com a nova largura
            entrylist.append(Entry(searchWindow, width=newwidth, foreground='blue'))
            entrylist[-1].grid(row=0, column=1)
            entrylist[-1].insert(END, "NAME")

            for i in range(0, arange):
                entrylist.append(Entry(searchWindow, width=20))
                entrylist[-1].grid(row=i+1,column=4)
                entrylist[-1].insert(END, str(sortedList[i].getrating()))
                entrylist[-1].configure(state=DISABLED)

                entrylist.append(Entry(searchWindow, width=20))
                entrylist[-1].grid(row=i + 1, column=0)
                entrylist[-1].insert(END, str(sortedList[i].getfifaID()))
                entrylist[-1].configure(state=DISABLED)

                # recupera o jogador da tabela hash
                jogador = playersTable.getplayer(sortedList[i].getfifaID())

                entrylist.append(Entry(searchWindow, width=newwidth))
                entrylist[-1].grid(row=i + 1, column=1)
                entrylist[-1].insert(END, jogador.getname())
                entrylist[-1].configure(state=DISABLED)

                entrylist.append(Entry(searchWindow, width=20))
                entrylist[-1].grid(row=i + 1, column=2)
                entrylist[-1].insert(END, jogador.getAverage())
                entrylist[-1].configure(state=DISABLED)

                entrylist.append(Entry(searchWindow, width=20))
                entrylist[-1].grid(row=i + 1, column=3)
                entrylist[-1].insert(END, jogador.getReviewsNum())
                entrylist[-1].configure(state=DISABLED)
            searchWindow.update()


            #for i in sortedList:
                #print(i.getrating(), i.getfifaID())
        else:
            wText4.configure(text="Usuário não encontrado!")
            wText4.place(x=130, y=180)
            return -1
    else:
        wText4.configure(text="O ID dos usuários é formado apenas por números!")
        wText4.place(x=70, y=180)
        return -1
def searchPositions():
    global searchTerm
    global playerlist
    searchString = searchTerm.get()
    lista_input = searchString.split("'")
    lista_input[0] = lista_input[0].replace("top", "")
    lista_input[0] = lista_input[0].replace(" ", "")
    for term in lista_input:
        if (term=="" or term==" "):
            lista_input.remove(term)
    #print(lista_input)

    if (len(lista_input[1]) == 0):
        wText4.configure(text="É necessario ter ao menos um caractere para fazer essa pesquisa!")
        wText4.place(x=25, y=180)
        return -1
    if (lista_input[1].isdecimal()):
        wText4.configure(text="Tag invalida!")
        wText4.place(x=165, y=180)
        return -1

    playerlist = playersTable.getplayerIDlist()  # recupera a lista inteira de "player"

    # percorre a tabela inteira de players
    encontrou = False
    encontrouRelevante = False
    foundList = []
    for j in playerlist:  # para cada jogador...
        jogador = playersTable.getplayer(j)
        encontrou = False
        positions = jogador.getpositions().replace(" ", "")
        positions = positions.split(",")
        for k in range(len(jogador.getpositions())): #Para cada uma das posiçoes...
            for position in positions:
                if(encontrou):
                    break
                if(position.upper() == lista_input[1].upper()):
                    #print(position, jogador.getname())
                    encontrou = True
                    if(jogador.getReviewsNum() > 999):
                        encontrouRelevante = True
                        foundList.append(user_rating(jogador.getAverage(), jogador.getfifaId()))
                        break
    if(encontrouRelevante):
        sortedList = backwardsbubblesort_usersearch(foundList)

        wText4.configure(text="")  # remove uma possivel mensagem de erro da janela
        searchWindow = Tk()
        searchWindow.resizable(False, False)
        if(len(sortedList) < (int(lista_input[0]))):
            searchWindow.title("Resultado da pesquisa entre os {0} melhores da posição {1}:".format(len(sortedList), lista_input[1]))
        else:
            searchWindow.title("Resultado da pesquisa entre os {0} melhores da posição {1}:".format(lista_input[0], lista_input[1]))

        # inicializa a planilha com o titulo das colunas
        entrylist = []
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=0)
        entrylist[-1].insert(END, "SOFIFA ID")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=2)
        entrylist[-1].insert(END, "PLAYER POSITIONS")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=3)
        entrylist[-1].insert(END, "RATING")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=4)
        entrylist[-1].insert(END, "COUNT")

        # calcula a largura da celula de nome
        if (len(sortedList) < int(lista_input[0])):
            arange = len(sortedList)
        else:
            arange = int(lista_input[0])
        newwidth = 0
        for i in range(0, arange):
            jogador = playersTable.getplayer(sortedList[i].getfifaID())
            if (newwidth < len(jogador.getname())):
                newwidth = len(jogador.getname())

            # inicializa a coluna nome, com a nova largura
            entrylist.append(Entry(searchWindow, width=newwidth, foreground='blue'))
            entrylist[-1].grid(row=0, column=1)
            entrylist[-1].insert(END, "NAME")
            caixaPesquisa.delete(0, END)

        for i in range(0, arange):
            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=3)
            entrylist[-1].insert(END, str(sortedList[i].getrating()))
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=0)
            entrylist[-1].insert(END, str(sortedList[i].getfifaID()))
            entrylist[-1].configure(state=DISABLED)

            # recupera o jogador da tabela hash
            jogador = playersTable.getplayer(sortedList[i].getfifaID())

            entrylist.append(Entry(searchWindow, width=newwidth))
            entrylist[-1].grid(row=i + 1, column=1)
            entrylist[-1].insert(END, jogador.getname())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=4)
            entrylist[-1].insert(END, jogador.getReviewsNum())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=2)
            entrylist[-1].insert(END, jogador.getpositions())
            entrylist[-1].configure(state=DISABLED)
    else:
        wText4.configure(text="Nenhum jogador encontrado para essa posição!")
        wText4.place(x=75, y=180)
        return -1
def searchTags():
    global searchTerm
    if (len(searchTerm.get()) == 0):
        wText4.configure(text="É necessario ter ao menos um caractere para fazer essa pesquisa!")
        wText4.place(x=25, y=180)
        return -1
    searchString = searchTerm.get()
    lista_tags = searchString.split("'")
    for tag in lista_tags:
        if (tag=="" or tag==" "):
            lista_tags.remove(tag)

    wText4.configure(text="")  # remove uma possivel mensagem de erro da janela

    playerList = playersTable.getplayerIDlist()
    foundlist = []
    for j in playerList:  # para cada jogador encontrado...
        tagsfound = 0
        allfound = False
        jogador = playersTable.getplayer(j)
        for tag in range(len(jogador.gettags())):  # para cada uma das tags do jogador
            for tagi in range(len(lista_tags)):  # para cada uma das tags solicitadas
                if(lista_tags[tagi] == jogador.gettags()[tag]):
                    #print("ENCONTROU TAG IGUAL", lista_tags[tagi], jogador.gettags()[tag])
                    tagsfound += 1  # encontrou uma tag igual
                if(tagsfound == len(lista_tags)):  # numero de tags igual
                    #print("Todas as tags foram encontradas", jogador.gettags(), lista_tags)
                    #print(jogador.getname())
                    allfound = True
                    if(jogador.getRatingSum()==0):
                        print("Ninguem avaliou esse jogador... Exception")
                    else:
                        foundlist.append(user_rating(jogador.getAverage(), jogador.getfifaId()))
                    break
            if(allfound):
                break
    if(len(foundlist) > 0):
        # a lista é valida, tem jogadores, que serão impressos em uma janela
        wText4.configure(text="")  # remove uma possivel mensagem de erro da janela
        sortedList = backwardsbubblesort_usersearch(foundlist)

        searchWindow = Tk()
        searchWindow.resizable(False, False)
        searchWindow.title("Resultado da pesquisa das tags - {} - odenado por rating:".format(searchTerm.get()))

        # inicializa a planilha com o titulo das colunas
        entrylist = []
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=0)
        entrylist[-1].insert(END, "SOFIFA ID")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=2)
        entrylist[-1].insert(END, "PLAYER POSITIONS")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=3)
        entrylist[-1].insert(END, "RATING")
        entrylist.append(Entry(searchWindow, width=20, foreground='blue'))
        entrylist[-1].grid(row=0, column=4)
        entrylist[-1].insert(END, "COUNT")

        # calcula a largura da celula de nome
        if (len(sortedList) < 25):
            arange = len(sortedList)
        else:
            arange = 25
        newwidth = 0
        for i in range(0, arange):
            jogador = playersTable.getplayer(sortedList[i].getfifaID())
            if (newwidth < len(jogador.getname())):
                newwidth = len(jogador.getname())

            # inicializa a coluna nome, com a nova largura
            entrylist.append(Entry(searchWindow, width=newwidth, foreground='blue'))
            entrylist[-1].grid(row=0, column=1)
            entrylist[-1].insert(END, "NAME")
            caixaPesquisa.delete(0, END)

        for i in range(0, arange):
            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=3)
            entrylist[-1].insert(END, str(sortedList[i].getrating()))
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=0)
            entrylist[-1].insert(END, str(sortedList[i].getfifaID()))
            entrylist[-1].configure(state=DISABLED)

            # recupera o jogador da tabela hash
            jogador = playersTable.getplayer(sortedList[i].getfifaID())

            entrylist.append(Entry(searchWindow, width=newwidth))
            entrylist[-1].grid(row=i + 1, column=1)
            entrylist[-1].insert(END, jogador.getname())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=4)
            entrylist[-1].insert(END, jogador.getReviewsNum())
            entrylist[-1].configure(state=DISABLED)

            entrylist.append(Entry(searchWindow, width=20))
            entrylist[-1].grid(row=i + 1, column=2)
            entrylist[-1].insert(END, jogador.getpositions())
            entrylist[-1].configure(state=DISABLED)
    else:
        wText4.configure(text="Não foi encontrado nenhum jogador para essa(s) tag(s)!")
        wText4.place(x=50, y=180)
if (__name__ == "__main__"):
    # inicializa a janela principal
    mainwindow = Tk()
    mainwindow.resizable(False, False)
    mainwindow.geometry('400x250+1000+300')
    mainwindow.title("Trabalho Final - CPD - FIFA2021 - Players")
    bolaimg = PhotoImage(file="bola.png")
    bolacopy = bolaimg
    mainwindow.call('wm', 'iconphoto', mainwindow._w, bolaimg)
    wText1 = Label(text="text1")
    wText2 = Label(text="text2")
    wText3 = Label(text="text3")
    wText4 = Label(text="text3", foreground="red")
    wText1.pack(side=TOP)
    wText2.pack(side=TOP)
    wText3.pack(side=TOP)
    wText4.pack(side=BOTTOM)
    loadingPercentage = IntVar()
    loadingBar = Progressbar(mainwindow, orient=HORIZONTAL, length=200, mode='determinate', variable=loadingPercentage)

    mainwindow.update()

    # dados sobre o trabalho
    wText1.configure(text="Trabalho Final - LAB 5 - Classificação e Pesquisa de Dados")
    wText2.configure(text="FIFA2021 - Players")
    wText3.configure(text="Aluno: Giordano Souza de Paula - Cartão: 308054")
    wText4.configure(text="Tempo decorrido: 0 segundos")
    startVar = IntVar(0)
    startButton = Button(text="Começar a leitura", command=startloop)
    startButton.pack(expand=True)
    mainwindow.update()

    while(startVar.get() == 0):
        try:
            mainwindow.update()  # atualiza a janela até que o botão de inciar seja pressionado
        except:
            sys.exit()

    wText2.configure(text="")
    wText3.configure(text="")
    startButton.destroy()  # remove o botão de start
    mainwindow.update()

    t0 = tm.perf_counter()  # marcaçao de tempo de incio de execução do programa

    caminhoArquivoPlayers = "players.csv"
    caminhoArquivoRatings = "rating.csv"
    caminhoArquivoTags = "tags.csv"

    tabelaPlayers = openFile(caminhoArquivoPlayers)
    tabelaRatings = openFile(caminhoArquivoRatings)
    tabelaTags = openFile(caminhoArquivoTags)

    wText1.configure(text="Alocando tabela hash de Jogadores...")
    mainwindow.update()
    playersTable = TabelaHashJogadores(24631)  # numero primo mais proximo de 24627,2 sendo 130% de 18944 - que é o numero de jogadores
    wText1.configure(text="Alocando tabela hash de Usuários...")
    mainwindow.update()
    usersTable = HashTableUsers(31444489)  # numero primo mais proximo de 31.444.501 sendo 130% de 24.188.078

    wText1.configure(text="Lendo arquivo {0}...".format(caminhoArquivoPlayers))
    csvPlayers = csv.reader(tabelaPlayers, delimiter=',')
    next(csvPlayers)  # ignora a primeira linha
    wText2.configure(text="Inserindo na tabela Hash com os jogadores lidos do arquivo...")
    loadingBar.pack(expand=True)  # imprime uma barra de carregando, no meio da tela
    mainwindow.update()
    aux = 1893
    counter = 0
    for line in csvPlayers:
        # assume que não existem jogadores duplicados na planilha de entrada
        playersTable.insertHash(player(line[0], line[1], line[2]))  # insere o jogador lido na tabela hash
        # imprime o progresso da inserção
        if(aux==1895):
            aux = 0
            percentage = math.floor(counter / 18944 * 100)
            wText3.configure(text="\tInserindo... {0} de {1} ({2}%)".format(counter, 18944, percentage))
            wText4.configure(text="Tempo decorrido: {:.2} segundos".format(tm.perf_counter() - t0))
            loadingPercentage.set(percentage)
            mainwindow.update()
        aux += 1
        counter += 1
    wText3.configure(text="\tInserindo jogadores... {0} de {1} ({2}%)".format(counter, 18944, math.floor(counter / 18944 * 100)))
    wText1.configure(text="Arquivo {0} lido.".format(caminhoArquivoPlayers))
    mainwindow.update()

    wText1.configure(text="Lendo arquivo {0}...".format(caminhoArquivoRatings))
    csvRatings = csv.reader(tabelaRatings, delimiter=',')
    next(csvRatings)
    wText2.configure(text="Adicionando ratings na tabela Hash de Usuários")
    mainwindow.update()
    counter = 0
    colisoes = 0
    aux = 241880
    for line in csvRatings:  # é necessario manter a rating com o usuário que fez a avaliação
        # atualiza a nota dos jogadores, na tabela hash de jogadores
        jogador = playersTable.getplayer((int(line[1])))  # obtem o jogador que foi avaliado da lista de jogadores
        jogador.insertRating_player(float(line[2]))  # insere a nota dada a nota total do jogador, na classe jogador

        # insere avaliaçoes na tabela hash de usuários
        usersTable.insertHash(User(int(line[0])), int(line[0]))  # insere o usuário na tabela hash, informa o userId
        user = usersTable.getuser(int(line[0]))  # pega o usuário que acabou de ser adicionado
        user.insertRating_user(float(line[2]), int(line[1]))

        # imprime o progresso da inserção
        counter+=1
        aux += 1
        if(aux == 241881):  # imprime o progresso a cada 10% da lista
            aux = 0  # zera o contador, e imprime que ja esta em um uma % multipla de 10
            percentage = math.floor(counter/24188078*100)
            wText3.configure(text="Inserindo avaliações... {0} de {1} avaliações ({2}%)".format(counter, 24188078, percentage))
            wText4.configure(text="Tempo decorrido: {:.3f} segundos".format(tm.perf_counter() - t0))
            loadingPercentage.set(percentage)
            mainwindow.update()
    wText3.configure(text="Inserindo avaliações... {0} de {1} avaliações ({2}%)".format(counter, 24188078,math.floor(counter/24188078*100)))
    wText1.configure(text="Arquivo {0} lido.".format(caminhoArquivoRatings))

    wText1.configure(text="Lendo arquivo {0}...".format(caminhoArquivoTags))
    csvTags = csv.reader(tabelaTags, delimiter=',')
    next(csvTags)
    wText2.configure(text="Adicionando tags aos jogadores na tabela Hash")
    counter = 0
    aux = 3649
    for line in csvTags:  # carrega tags do arquivo e insere na classe de jogadores
        jogador = playersTable.getplayer(int(line[1]))
        jogador.inserttag(line[2], int(line[0]))

        # imprime o progresso da inserção
        counter += 1
        aux += 1
        if(aux == 3650):
            aux = 0
            wText3.configure(text="Inserindo tags... {0} de {1} jogadores ({2}%)".format(counter, 364950, math.floor(counter / 364950 * 100)))
            wText4.configure(text="Tempo decorrido: {:.3f} segundos".format(tm.perf_counter() - t0))
            loadingPercentage.set(percentage)
    wText3.configure(text="Inserindo tags... {0} de {1} jogadores ({2}%)".format(counter, 364950, math.floor(counter / 364950 * 100)))
    wText1.configure(text="Arquivo {0} lido.".format(caminhoArquivoTags))

    # fim da fase 1, de inicialização dos arquivos
    loadingBar.destroy()
    wText4.configure(text="Fim da fase 1, de inicialização das estruturas - em {:.3f} segundos.".format(tm.perf_counter()-t0))
    mainwindow.update()

    # testes de consulta na hash table(jogadores)
    #printplayer_tags(231747)

    # testes de consulta em hash table(usuários)
    #printuser_reviews(52505)

    startVar.set(0)
    startButton = Button(text="Ir para a etapa de pesquisas", command=startloop)
    startButton.pack(expand=True)
    while (startVar.get() == 0):
        try:
            mainwindow.update()  # atualiza a janela até que o botão de inciar seja pressionado
        except:
            sys.exit()

    # inicio da fase 2, loop de pesquisas
    wText4.configure(text="")
    startButton.destroy()
    searchTerm = StringVar()
    caixaPesquisa = Entry(mainwindow, width=40, textvariable=searchTerm)
    caixaPesquisa.pack()

    wText1.configure(text="Fifa 2021 - Players")
    wText2.configure(text="")
    wText3.configure(text="Digite o termo a ser procurado na caixa abaixo")
    wText5 = Label(text="e logo após selecione o tipo de pesquisa")
    wText5.pack(side=TOP)

    searchNameButton = Button(text="Nome de jogador", command=searchName)
    searchNameButton.place(x=43, y=110)
    userIdButton = Button(text="Id de usuário", command=searchId)
    userIdButton.place(x=156, y=110)
    positionButton = Button(text="Top X por posição", command=searchPositions)
    positionButton.place(x=243, y=110)
    tagButton = Button(text="Tags de jogadores", command=searchTags)
    tagButton.place(x=145, y=140)

    exitbutton = Button(text="Sair", command=closewindow)
    exitbutton.place(x=162, y=220)

    windowopen = True
    while(windowopen):
        try:
            mainwindow.update()
        except :
            closeFiles()
            windowopen = False
    if(windowopen):
        mainwindow.destroy()
        closeFiles()  # Fecha os arquivos, que ja foram inseridos em tabelas Hash
# fim
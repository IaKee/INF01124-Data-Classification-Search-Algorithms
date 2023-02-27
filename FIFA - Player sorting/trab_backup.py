import csv
from timeit import default_timer as timer
from tkinter import *

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")

        self.primeiroContainer = Frame(master)      #Contem o Titulo
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)       #Contem a caixa de pesquisa
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)      #Contem os botoes
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)        #Contem a saida do programa
        self.quartoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Caixa de Pesquisa")
        self.titulo["font"] = (self.fontePadrao, "10", "bold")
        self.titulo.pack()

        self.nome = Entry(self.segundoContainer)
        self.nome["font"] = self.fontePadrao
        self.nome.pack(side=LEFT)

        self.autenticar1 = Button(self.terceiroContainer)
        self.autenticar1["text"] = "Title"
        self.autenticar1["font"] = (self.fontePadrao, "12")
        self.autenticar1["width"] = 12
        self.autenticar1["command"] = self.BUTAO1
        self.autenticar1.pack(side = LEFT)

        self.autenticar2 = Button(self.terceiroContainer)
        self.autenticar2["text"] = "User"
        self.autenticar2["font"] = (self.fontePadrao, "12")
        self.autenticar2["width"] = 12
        self.autenticar2["command"] = self.BUTAO2
        self.autenticar2.pack(side = LEFT)

        self.autenticar3 = Button(self.terceiroContainer)
        self.autenticar3["text"] = "Genre"
        self.autenticar3["font"] = (self.fontePadrao, "12")
        self.autenticar3["width"] = 12
        self.autenticar3["command"] = self.BUTAO3
        self.autenticar3.pack(side = LEFT)

        self.autenticar4 = Button(self.terceiroContainer)
        self.autenticar4["text"] = "Tag"
        self.autenticar4["font"] = (self.fontePadrao, "12")
        self.autenticar4["width"] = 12
        self.autenticar4["command"] = self.BUTAO4
        self.autenticar4.pack(side = LEFT)

        #self.resultado = Label(self.quartoContainer, text="Pesquisa ai namiral", font=self.fontePadrao)
        #self.resultado.pack()

    def BUTAO1(self):
        pesquisa = self.nome.get()
        ids = trietitles.find_prefix(trietitles, pesquisa)            #texto contem os id's dos filmes pesquisados

        global listaindices
        listaindices = []
        listaindices.append("Movie Id")
        listaindices.append("Title")
        listaindices.append("Genres")
        listaindices.append("Rating")
        listaindices.append("Count")
        
        global listaprint
        listaprint = []
        for i in range(0,len(ids)):
            dados = tabelahash.busca(ids[i])
            if dados != None:
                listadados=[]
                listadados.append(dados[0])             #Adiciona id
                listadados.append(dados[3])             #Adiciona titulo
                listadados.append(dados[4])             #Adiciona genero
                listadados.append(dados[1])             #Adiciona rating
                listadados.append(dados[2])             #Adiciona count
                listaprint.append(listadados)

        if len(listaprint) >= 0:
            rooti = Tk()
            t=Table(rooti)


    def BUTAO2(self):
        pesquisa = self.nome.get()
        global listaindices
        listaindices = []
        listaindices.append("User_Rating")
        listaindices.append("Title")
        listaindices.append("Global Rating")
        listaindices.append("Count")

        global listaprint
        listaprint = []
        dados = tabelausers.busca(int(pesquisa))#[user, [ID, Avaliação]]
        if dados != None:
            for i in range (1,len(dados)):
                listadados=[]
                listadados.append(dados[i][1])              #User rating
                dadoshash = tabelahash.busca(dados[i][0])   
                listadados.append(dadoshash[3])             #Title
                listadados.append(dadoshash[1])             #Rating global
                listadados.append(dadoshash[2])             #Count
                listaprint.append(listadados)
        if len(listaprint) >= 0:
            rooti = Tk()
            t=Table(rooti)


    def BUTAO3(self):
        resultado = self.nome.get()
        pesquisa = resultado.split()
        ids = triegenres.find_prefix(triegenres, pesquisa[1])  #ids eh uma lista com os ids 
        
        pesquisa[0] = pesquisa[0].replace("top", "")
        #Calcular os top coisa com int(pesquisa[0])
   
        ids = ordenaN(ids,int(pesquisa[0]))
        #print(ids)
        
        global listaindices
        listaindices = []
        listaindices.append("Title")
        listaindices.append("Genres")
        listaindices.append("Rating")
        listaindices.append("Count")

        global listaprint
        listaprint = []
        for i in range(0,len(ids)):
            dados = tabelahash.busca(ids[i][0])
            if dados != None:
                listadados = []
                listadados.append(dados[3])             #Adiciona titulo
                listadados.append(dados[4])             #Adiciona genero
                listadados.append(dados[1])             #Adiciona rating
                listadados.append(dados[2])             #Adiciona count
                listaprint.append(listadados)

        if len(listaprint) >= 0:
            rooti = Tk()
            t=Table(rooti)

    def BUTAO4(self):                                   #Pesquisa por tags, separadas por virgula
        pesquisa = self.nome.get()
        pesquisa = pesquisa.split(",")
        #fazer um for pra  ver cada elemento da string q será dividido por virgulas
        ids = [None]
        idstemp1 = []
        for string in pesquisa:
            idstemp = trietags.find_prefix(trietags, string)        #Coloca os ids da tag desejada em idstemp
            if ids[0] == None:                                         #Se ids estiver vazia, coloca todos os resultados em ids
                ids = idstemp
            else:               #compara os ids e deixa os que estao nas duas
                idstemp1 = []
                for i in range(0,len(ids)):
                    for j in range(0,len(idstemp)):
                        print(ids[i],idstemp[j])
                        if ids[i] == idstemp[j]:
                            idstemp1.append(ids[i])
                ids = idstemp1.copy()
                        
        print(ids)
        global listaindices
        listaindices = []
        listaindices.append("Title")
        listaindices.append("Genres")
        listaindices.append("Rating")
        listaindices.append("Count")

        global listaprint
        listaprint = []
        for i in range(0,len(ids)):
            dados = tabelahash.busca(ids[i])
            if dados != None:
                listadados = []
                listadados.append(dados[3])             #Adiciona titulo
                listadados.append(dados[4])             #Adiciona genero
                listadados.append(dados[1])             #Adiciona rating
                listadados.append(dados[2])             #Adiciona count
                listaprint.append(listadados)

        if len(listaprint) >= 0:
            rooti = Tk()
            t=Table(rooti)

class Table:   
    def __init__(self,root):
        global listaprint
        global listaindices
        column = len(listaindices)
        for i in range(len(listaindices)):                  #Printa os indices
                self.e = Entry(root,          #Entry é editavel ver se tem como mudar
                               font=('Arial',10,'bold'))
                  
                self.e.grid(row=0, column=i)
                self.e.insert(END, listaindices[i])

        # code for creating table
        for i in range(len(listaprint)):
            for j in range(column):
                self.e = Entry(root,          #Entry é editavel ver se tem como mudar
                               font=('Arial',10))
                  
                self.e.grid(row=i+1, column=j)
                self.e.insert(END, listaprint[i][j])

class tabela:
    def __init__(self):
        self.size = 32749 #27011 #22000001 
        self.dados = [None]*self.size            #lista com dados [Id, Media, Quant, Title, Genders]
        self.chave = [-1]*self.size              #chave calculada por duplohash
        self.usado = [False]*self.size

    def busca(self, key):
        chave = key % self.size
        i = 1
        if self.chave[chave] == key and self.usado[chave]:
            return self.dados[chave] #acessa
        while self.chave[chave] != -1 and self.chave[chave] != key and chave <= self.size:
            chave = (key + i * (key % (self.size//2))) % self.size
            i += 1
        if chave <= self.size and self.chave[chave] != -1:
            return self.dados[chave]
        else:
            return None
        #se for, acessa self.dados[key calculado]

    def duplohashing(self, key):
        i = 1
        pos = key % self.size 
        while self.chave[pos] != -1 and pos <= self.size:
            pos = (key + i * (key % (self.size//2))) % self.size
            i += 1
        if pos <= self.size:
            return pos
        return -1
    
    def addinfo(self, key, data):
        pos = self.duplohashing(key)
        self.chave[pos] = key
        self.dados[pos] = data
        self.usado[pos] = True

class tabela_users():
    def __init__(self):
        self.size = 166207 
        self.dados = [None]*self.size                       #lista [user, [ID, Avaliação]]
        self.chave = [-1]*self.size                         #chave calculada por duplohash
        self.usado = [False]*self.size

    def busca(self, key):
        chave = key % self.size
        i = 1
        if self.chave[chave] == key and self.usado[chave]:
            return self.dados[chave] #acessa
        while self.chave[chave] != -1 and self.chave[chave] != key and chave <= self.size:
            chave = (key + i * (key % (self.size//2))) % self.size
            i += 1
        if chave <= self.size and self.chave[chave] != -1:
            return self.dados[chave]
        else:
            return None

    def duplohashing(self, key):
        i = 1
        pos = key % self.size 
        while self.chave[pos] != -1 and pos <= self.size:
            pos = (key + i * (key % (self.size//2))) % self.size
            i += 1
        if pos <= self.size:
            return pos
        return -1
    
    def addinfo(self, key, data):
        pos = self.duplohashing(key)
        self.chave[pos] = key
        self.dados[pos] = data
        self.usado[pos] = True
    
    def addinfo(self, key, data):
        pos = self.duplohashing(key)
        self.chave[pos] = key
        self.dados[pos] = data
        self.usado[pos] = True

class trie():
    
    def __init__(self, char):
        self.char = char
        self.children = []
        # Eh o ultimo caractere da palavra?
        self.fim = -1

    def addword(self, root, title, id):                           
        node = root
        for char in title:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = trie(char)
                node.children.append(new_node)
                node = new_node
        node.fim = id
    

    def find_prefix(self, root, prefix):                #funçao que acha os filmes com o prefixo dado e retorna o id deles
        node = root
        if not root.children:
            return False
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char.lower() == char.lower(): 
                    char_not_found = False
                    node = child
                    break
            if char_not_found:                          #Retorna falso se nao achar
                return 'Não foi encontrado'
        nada = []
        node.print_prefix(node,nada)                #Chama a função que acha os filmes com o prefixo pesquisado
        return nada

    def print_prefix(self, root, lista):
        if root.fim != -1:                          #Achou a palavra é aki q printa as informaçoes
            lista.append(root.fim)
        for i in root.children:
            if root.children != None and i != None:
                root.print_prefix(i, lista)

class trie_tags():
    
    def __init__(self, char):
        self.char = char
        self.children = []
        # Eh o ultimo caractere da palavra?
        self.fim = -1
    def addword(self, root, tag, id):                           
        node = root
        for char in tag:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = trie_tags(char)
                node.children.append(new_node)
                node = new_node
        if node.fim == -1:
            node.fim = []
            node.fim.append(id)
        else:
            flag = False
            for i in range(0, len(node.fim)):
                if node.fim[i] == id:
                    flag = True
            if flag == False:
                node.fim.append(id)

    def find_prefix(self, root, prefix):        #funçao que acha os filmes com o prefixo dado e retorna o id deles
        node = root
        if not root.children:
            return False
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char.lower() == char.lower(): 
                    char_not_found = False
                    node = child
                    break
            if char_not_found:                          #Retorna falso se nao achar
                return 'Não foi encontrado'
        return node.fim

class trie_genres():
    
    def __init__(self, char):
        self.char = char
        self.children = []
        # Eh o ultimo caractere da palavra?
        self.fim = -1

    def addword(self, root, genre, id):                           
        node = root
        for char in genre:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = trie_genres(char)
                node.children.append(new_node)
                node = new_node
        if node.fim == -1:
            node.fim = []
            node.fim.append(id)
        else:
            node.fim.append(id)

    def find_prefix(self, root, prefix):        #funçao que acha os filmes com o prefixo dado e retorna o id deles
        node = root
        if not root.children:
            return False
        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char.lower() == char.lower(): 
                    char_not_found = False
                    node = child
                    break
            if char_not_found:                          #Retorna falso se nao achar
                return 'Não foi encontrado'
        return node.fim

def read_hash():
    with open('rating.csv') as csv_file:
        linha = []
        info = tabela()
        user = tabela_users()
        line = []
        filme = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            pos = info.busca(int(row[1]))
            key = user.busca(int(row[0]))
            if key != None:
                filme.append(int(row[1]))
                filme.append(float(row[2]))
                key.append(filme)
            else:
                line.append(int(row[0]))            # coloca o id do user na lista
                filme.append(int(row[1]))
                filme.append(float(row[2]))
                line.append(filme)                  # coloca o id do filme e a nota do usuario na lista
                user.addinfo(int(row[0]), line)
            if pos != None:       
                pos[1] += float(row[2])
                pos[2] += 1
            else:
                linha.append(int(row[1]))           # coloca o id do filme na lista
                linha.append(float(row[2]))         # coloca a avaliação de x usuário na lista
                linha.append(1)
                info.addinfo(int(row[1]), linha)
            linha = []
            line = []
            filme = []
         
        for j in range(0, len(info.dados)):             #Faz a media das notas
            if info.dados[j] != None:
                info.dados[j][1] = info.dados[j][1]/info.dados[j][2]

        return info, user

def read_trie(info):
    arvore = trie('*')
    arvore2 = trie_genres('*')
    with open('movie_clean.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            csv_reader = csv.reader(csv_file, delimiter=',')
            pos = info.busca(int(row[0]))
            if pos != None:                             #Adiciona os generos dos filmes na tabela hash
                pos.append(row[1])
                pos.append(row[2])
            string = row[2].split("|")
            for i in string:
                arvore2.addword(arvore2,i,int(row[0]))
            arvore.addword(arvore, row[1], int(row[0]))
    return arvore, arvore2

def read_trietags():
    arvore = trie_tags('*')
    with open('tag_clean.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            arvore.addword(arvore, row[2], int(row[1]))
    return arvore

def ordenaN(ids, N):    #Ordena os primeiros N filmes por rating
    string = []
    for i in range(0,len(ids)):
        data = tabelahash.busca(ids[i])                 #id, media
        aux = []
        if data != None and data[2] > 999:
            aux.append(data[0])
            aux.append(data[1])
            string.append(aux)
    for i in range(0,N):
        max = -1
        pos = 0
        for j in range(i,len(string)):
            if string[j][1] > max:
                max = string[j][1]
                pos = j
        string[i], string[pos] = string[pos], string[i]
    return string[0:N] 

if __name__ == "__main__":      # Início da main
    listaprint = []
    listaindices = []
    t_inicio = timer()                              #Começa o timer para ver o tempo de procesamento dos dados

    contador = 0

    tabelahash, tabelausers = read_hash()           #Chama as funçoes que processam os dados
    trietitles, triegenres = read_trie(tabelahash)
    trietags = read_trietags()

    tempotot = timer() - t_inicio
    print(tempotot)                                 #Imprime o tempo total de execução

    root = Tk()
    Application(root)
    root.mainloop()



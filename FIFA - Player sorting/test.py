from unidecode import unidecode

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
        if(ch == " "):
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

def main():
    t = Trie()

    # Construct trie
    t.insert("nemanja matic", 30)
    t.insert("jose de jesus corona rodriguez", 15)

    t.insert("these", 45)
    t.insert("thea", 60)


    # Search for different keys
    print("{} ---- {}".format("the", t.prefixSearch("the")))

    print(t._charToIndex(" "))

if __name__ == '__main__':
    main()

# This code is contributed by Atul Kumar (www.facebook.com/atul.kr.007)

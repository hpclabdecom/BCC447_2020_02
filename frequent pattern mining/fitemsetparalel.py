import concurrent.futures

class Arvore:
    def __init__(self, label, cont=0):
        self.nodes = []
        self.cont = cont
        self.label = label

    def add_node(self, node):
        self.nodes.append(node)

    def cria_arvore(data):

        words = sorted(set(data))

        print(words)

        root = Arvore('root')
        for word in words:
            root.add_node(Arvore(word))

        return root



    def imprime2(self):
        for node in self.nodes:
            print(node.label, node.cont)
            node.imprime2()


    def imprime(self):
        if self.nodes == []:
            return

        for node in self.nodes:
            print(node.label, node.cont, "-", end="")

        print()

        arvore_aux = Arvore("aux")
        for node in self.nodes:
            for node2 in node.nodes:
                arvore_aux.nodes.append(node2)

        arvore_aux.imprime()

    def insere_aux(self,data):
        arvore, nodes = data[0], data[1]

        for node in nodes:
            my_node = [n for n in arvore.nodes if n.label == node]
            if my_node == []:
                my_node = Arvore(node, 1)
                arvore.nodes.append(my_node)
                arvore = my_node

            else:
                my_node = my_node[0]

                my_node.cont += 1
                arvore = my_node

    def insere_na_arvore(self,arvore, conj_itens):
        for conj in conj_itens:
            i = 0

            tamanho_conjunto = len(conj)
            lista_de_execucao = []
            while i < tamanho_conjunto:
                # daqui pra baixo paralelizavel
                # aumentar contador na cabeca
                lista_de_execucao.append((arvore, conj[i:]))

                i += 1

            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(self.insere_aux, lista_de_execucao)
                for result in results:
                    if result is None:
                        pass


def base_transacional():
    with open("base2.txt", "r") as file:
        data = file.readlines()

    data = [sorted(base[:len(base)-1].split(" ")) for base in data]

    return data


if __name__ == '__main__':
    data = base_transacional()
    print(data)
    arvore = Arvore.cria_arvore(['A', 'C', 'E', 'G', 'T'])
    arvore.insere_na_arvore(arvore, data)
    arvore.imprime()


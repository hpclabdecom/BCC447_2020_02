import operator

from paralelSum import (OperationParalel, OperationParalelIter)
import time
from matriz import MatrizParalel
from matriz2 import MatrizParalel2
from matriz3 import MatrizParalel3
from matriz4 import MatrizParalel4

def multiplicaMatriz(m1, m2):
    matriz_resultante = []
    for i in range(len(m1)):
        matriz_resultante.append([])
        for j in range(len(m2[0])):
            soma = 0
            for k in range(len(m1)):
                soma += m1[i][k]*m2[k][j]
            matriz_resultante[i].append(soma)

    return  matriz_resultante

def operationProd(values):
    if not values:
        prod = 0
    else:
        prod = 1
        for i in values:
            prod *= i

    return prod

def operationConcat(values):
    list_aux = []
    for value in values:
        list_aux += value

    return list_aux


def test_sum():
    """-------------------------------Soma---------------------------------------------------"""
    print("\n------------Testando Soma----------------\n")

    tempo_inicial = time.time()
    soma = sum(range(1, 10 ** 8))
    print(f'Soma Integrada Python {soma}\nTempo: {time.time() - tempo_inicial}\n')

    tempo_inicial = time.time()
    soma = OperationParalel(sum).run(range(1, 10 ** 8))
    print(f'Soma Paralela recursiva {soma}\nTempo: {time.time() - tempo_inicial}')

    print("\n------------Fim do Teste Soma----------------\n")
    "----------------------------------------------------------------------------------------"


def test_prod():
    """------------------------------Produto-----------------------------------------------------------------"""
    print("\n------------Testando Produto----------------\n")

    tempo_inicial = time.time()
    produto = operationProd((range(1, 10**5)))
    print(f'Produto Integrado Python\nTempo: {time.time() - tempo_inicial}\n')

    tempo_inicial = time.time()
    produto = OperationParalel(operationProd).run(range(1, 10**5))
    print(f'Produto Paralela recursivo\nTempo: {time.time() - tempo_inicial}')

    print("\n------------Fim do Teste Produto----------------\n")
    "----------------------------------------------------------------------------------------"

def test_concat():
    """-----------------Concatenacao-----------------------------------------------------------------"""

    print("\n------------Testando Concatenacao----------------\n")

    tempo_inicial = time.time()
    operationConcat([list(range(2)) for i in range(10**7)])
    print(f'Concatenacao Python\nTempo: {time.time() - tempo_inicial}')

    tempo_inicial = time.time()
    OperationParalel(operationConcat).run([list(range(2)) for i in range(10**7)])
    print(f'Concatenacao Paralela recursiva\nTempo: {time.time() - tempo_inicial}')

    print("\n------------Fim do Teste Concatenacao----------------\n")
    "----------------------------------------------------------------------------------------"

def geraMatriz(n):
    matriz = [[1]*n for i in range(n)]

    return matriz, matriz

def test_matiz():
    """-----------------Matriz-----------------------------------------------------------------"""

    print("\n------------Testando Matriz----------------\n")
    m1, m2 = geraMatriz(150)

    tempo_inicial = time.time()
    multiplicaMatriz(m1, m2)
    print(f'Matriz Python Integrado\nTempo: {time.time() - tempo_inicial}')

    tempo_inicial = time.time()
    MatrizParalel().run(m1,m2)
    print(f'Matriz Python Paralel\nTempo: {time.time() - tempo_inicial}')

    print("\n------------Fim do Teste Matriz----------------\n")
    "----------------------------------------------------------------------------------------"


if __name__ == "__main__":

    #test_sum()
    #test_prod()
    #test_concat()

    test_matiz()












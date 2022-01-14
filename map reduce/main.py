from paralelSum import (OperationParalel, OperationParalelIter)
import time

def operation(values):
    return sum(values)

def operation2(values):
    prod = 1
    for i in values:
        prod *= i

    return prod


if __name__ == "__main__":

    tempo_inicial = time.time()
    soma  = sum(range(1, 10 ** 4))
    print(f'Soma Integrada Python {soma}\nTempo: {time.time()-tempo_inicial}')

    """tempo_inicial = time.time()
    soma = OperationParalel(operation).run(range(0, 10 ** 3))
    print(f'Soma Paralela {soma}\nTempo: {time.time() - tempo_inicial}')"""

    
    tempo_inicial = time.time()
    soma = OperationParalelIter(operation).run(range(1, 10 ** 4))
    print(f'Soma Paralela iterativa {soma}\nTempo: {time.time() - tempo_inicial}')

    tempo_inicial = time.time()
    soma = OperationParalel(operation,8).run(range(1, 10 ** 4))
    print(f'Soma Paralela recursiva {soma}\nTempo: {time.time() - tempo_inicial}')
import os
import concurrent.futures
from paralelSum import OperationParalel
from reduceTwo import ReduceTwo
import time

def operationTest(value1, value2):
    values = []

    for i in range(len(value1)):
        values.append(value1[i]*value2[i])

    return values


class MatrizParalel3:
    def __init__(self, threadCounter = os.cpu_count()):
        self.cpu_count = threadCounter

    def run(self, m1, m2):

        matriz_resultante = []
        for i in range(len(m1)):
            matriz_resultante.append([])
            for j in range(len(m2[0])):
                line = []
                for k in range(len(m1)):
                    line.append(m1[i][k] * m2[k][j])
                matriz_resultante[i].append(OperationParalel(sum).run(line))

        return matriz_resultante







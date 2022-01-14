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


class MatrizParalel2:
    def __init__(self, threadCounter = os.cpu_count()):
        self.cpu_count = threadCounter

    def solver(self, row_id, columm_id, matriz1, matriz2):
        #dividir linhas e colunas
        row = matriz1[row_id]

        columm = []
        for i in range(len(matriz2)):
            columm.append(matriz2[i][columm_id])

        mutiply = ReduceTwo(operationTest).run(row, columm)

        sum_mat = OperationParalel(sum).run(mutiply)

        return sum_mat


    def run(self, matriz1, matriz2):
        matrizResult = []

        for i in range(len(matriz1)):
            matrizResult.append([])
            for j in range(len(matriz2[0])):
               matrizResult[i].append(self.solver(i, j, matriz1, matriz2))

        return matrizResult






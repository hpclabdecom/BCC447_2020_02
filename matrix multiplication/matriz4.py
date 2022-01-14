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


class MatrizParalel4:
    def __init__(self, threadCounter = os.cpu_count()):
        self.cpu_count = threadCounter

    def solver(self, row_id, columm_id, matriz1, matriz2):
        #dividir linhas e colunas
        row = matriz1[row_id]

        columm = []
        for i in range(len(matriz2)):
            columm.append(matriz2[i][columm_id])

        mutiply = [row[i]*columm[i] for i in range(len(row))]

        sum_mat = OperationParalel(sum).run(mutiply)

        return sum_mat


    def run(self, matriz1, matriz2):
        with concurrent.futures.ThreadPoolExecutor(self.cpu_count) as executor:
            # dividir vetor de acordo com os.cpu_count

            futures = []
            for i in range(len(matriz1)):
                futures.append([])
                for j in range(len(matriz2[0])):
                    futures[i].append(executor.submit(self.solver, i, j, matriz1, matriz2))

            matrizResult = []
            for i, future_line in enumerate(futures):
                matrizResult.append([])
                for future in future_line:
                    #inicial = time.time()
                    matrizResult[i].append(future.result())
                    #print("passou")
                    #print(time.time()-inicial)

        return matrizResult






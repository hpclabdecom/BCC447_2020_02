import os
import concurrent.futures


class ReduceTwo:
    def __init__(self, operation, threadCounter = os.cpu_count()):
        self.cpu_count = threadCounter
        self.operation = operation #pega dois elementos e retorna terceiro

    def splited(self, value1, value2):
        limite = self.cpu_count
        if self.cpu_count >= len(value1) // 2:
            limite = len(value1) // 2

        new_values = []
        j = 0
        for i in range(limite):
            if i == limite - 1:
                new_values.append((value1[j:],value2[j:]))
            else:
                new_values.append((value1[j:j + limite], value2[j:j + limite]))
            j += limite

        return new_values

    def run(self, value1, value2):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # dividir vetor de acordo com os.cpu_count

            new_values = self.splited(value1, value2)

            futures = []
            for value1, value2 in new_values:
                futures.append(executor.submit(self.operation, value1, value2))

            values = []
            for future in futures:
                values += future.result()

        return values


#print(ReduceTwo(operationTest).run([1,2,3], [4,5,6]))
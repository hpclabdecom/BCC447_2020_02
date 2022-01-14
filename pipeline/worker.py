import os
import concurrent.futures
from classConsumer import Cons
from classProducer import Prod
from paralelReduce import OperationParalel
from sys import argv

def operation2(value1, value2):
    return value1+value2

def splited(values, limite):
    print("Entrou no splited")
    if limite >= len(values) // 2:
        limite = len(values) // 2
    divisor = len(values) // limite
    new_values = []
    j = 0
    for i in range(limite):
        if i == limite - 1:
            new_values.append(values[j:])
        else:
            new_values.append(values[j:j + divisor])
        j += divisor
    print("vai sair do splited")
    return new_values

class Worker:
    def __init__(self):
        self.cpu_count = os.cpu_count()
        self.id = 0
        self.topic = "machine" + str(self.id)

    def work(self, data, nMachine, word):
        print("Entrou no worker 1, ")
        new_data = [int(num) for num in data.split(' ') if num != '']
        print("Entrou no worker 1, ", new_data)
        try:
            new_data = splited(new_data, int(nMachine))[self.id]
            print("Dado splitado: ", new_data)
        except IndexError:
            print("nao é o seu id")
            return


        data = str(OperationParalel(sum, operation2, os.cpu_count()//2).run(new_data))
        print("Publicando: ", data)
        prod = Prod("./python.config", "cont")
        prod.publish("data", {'data': data, 'word': word})
        try:
            prod.flush()
        except:
            pass


    def run(self):
        worker = Cons(".\python.config")
        worker.subscribe([self.topic])
        while True:
            # receber dados
            data, err = worker.run()
            print("Recebi: ", data)
            if data == None:
                continue
            elif err != None:
                continue
            else:
                nMachine = data['machine']
                word = data['word']
                data = data['data']
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.work, data, nMachine, word)
        worker.close()

if __name__ == "__main__":
    Worker().run()

import os
import concurrent.futures
from classConsumer import Cons
from classProducer import Prod
from paralelReduce import OperationParalel
from sys import argv

def operation2(value1, value2):
    return value1+value2

class Reduce:
    def __init__(self):
        self.cpu_count = os.cpu_count()

    def reduce(self, data, file, word):
        new_data = data.split(' ')
        file_name = file
        search_word = word

        def operation1(words):
            nonlocal search_word
            search = search_word
            cont = 0
            for word in words:
                if word == search:
                    cont += 1
            return cont

        data = str(OperationParalel(operation1, operation2, os.cpu_count()//2).run(new_data))
        
        prod = Prod("./python.config", "cont")
        prod.publish("data", {'data': data, 'word': word})
        try:
            prod.flush()
        except:
            pass


    def run(self):
        reduce = Cons(".\python.config")
        reduce.subscribe(["reduce"])
        while True:
            # receber dados
            data, err = reduce.run()
            print(data)
            if data == None:
                continue
            elif err != None:
                continue
            else:
                file = data['file']
                word = data['word']
                data = data['data']
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.reduce, data, file, word)
        reduce.close()

if __name__ == "__main__":
    Reduce().run()

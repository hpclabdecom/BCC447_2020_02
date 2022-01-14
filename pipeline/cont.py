import os
import concurrent.futures
from classConsumer import Cons
from classProducer import Prod
from paralelReduce import OperationParalel
from sys import argv, exec_prefix
from timeout_decorator import timeout


def timeout(subscriber):
    i = 0

    while i < 15:
        i += 1
        data, err = subscriber.run()

        if data is None:
            continue
        else:
            return data, err

    raise(TypeError)


class Cont:
    def __init__(self, nMachines):
        self.cpu_count = os.cpu_count()
        self.dictWord = {}
        self.nMachines = nMachines
        self.topics = ["machine" + str(num) for num in range(int(nMachines))]


    def run(self):
        cont = Cons(".\python.config")
        cont.subscribe(["cont"])
        dataFinal = {}
        while True:
            try:
                data, err = timeout(cont)
                print(f'Recebi data: {data}')
                if data == None:
                    continue
                elif err != None:
                    continue
                else:
                    word = data['word']
                    data = data['data']

                    if dataFinal.get(word) is None:
                        dataFinal[word] = data + ' '
                    else: 
                        dataFinal[word] += data + ' '

                    if self.dictWord.get(word) is None:
                        self.dictWord[word] = 0

                    print(f'Datafinal: {dataFinal}')
                    print(f'Contagem atual: {self.dictWord}')
            except Exception:
                # caso dê exesão, conferir se tem uam unica palavra a ser somada 
                print("timeout")
                for key, value in dataFinal.items():
                    splitado = [int(num) for num in dataFinal[key].split(' ') if num != '']
                    if 0 < len(splitado) < 3:
                        print(f'tamanho < 3, valor atul: {self.dictWord[key]}')
                        print(f'Valor a somar: {sum(splitado)}')
                        self.dictWord[key] += sum(splitado)
                        dataFinal[key] = ''
                        prod = Prod("./python.config", key)
                        prod.publish("data", {'data': str(self.dictWord[key]), 'word': word})
                        print(f'Publicando em {key} - {str(self.dictWord[key])}')
                        try:
                            prod.flush()
                        except:
                            pass
                    elif len(splitado) > 2:
                        for topic in self.topics:
                            prod = Prod("./python.config", topic)
                            prod.publish("data", {'data': value, 'word': word, 'machine': self.nMachines})
                            print(f'Publicando em machines - {value}')
                            try:
                                prod.flush()
                            except:
                                pass
                        dataFinal[key] = ''

        cont.close()

if __name__ == "__main__":
    Cont(argv[1]).run()

import os
import concurrent.futures
from classProducer import Prod
from classConsumer import Cons


class Decoder:
    def __init__(self):
        self.cpu_count = os.cpu_count()
        self.myAdrres = ("localhost", 8081)
        self.addrresTermClean = ("localhost", 8082)

    def decodify(self, data):
        return data

    def publishTosendClean(self, data, file, word):
        data = self.decodify(data)

        prod = Prod("./python.config", "termclean")
        prod.publish("data", {'data': data, 'file': file, 'word': word})
        try:
            prod.flush()
        except:
            pass


    def run(self):
        decoder = Cons(".\python.config")
        decoder.subscribe(["decode"])
        while True:
            # receber dados
            data, err = decoder.run()
            print(data)
            if data == None:
                continue
            elif err != None:
                continue
            else:
                print("Data: ---------------------\n",data,"\n----------------------")
                file = data['file']
                word = data['word']
                data = data['data']
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    executor.submit(self.publishTosendClean, data, file, word)
        decoder.close()

if __name__ == "__main__":
    Decoder().run()

import os
import concurrent.futures
from classProducer import Prod
from classConsumer import Cons



class TermClean:
    def __init__(self):
        self.cpu_count = os.cpu_count()
        self.myAdrres = ("localhost", 8082)
        self.addrresReduce = ("localhost", 8083)

    def clear(self, data):
        remove = ["a", "b", "c", "d", "e", "f", "g", "h"
                  "i", "j", "k", "l", "m", "n", "o", "p"
                  "q", "r", "s", "t", "u", "v", "w","x", "y", "z"]
        remove += [carac.upper() for carac in remove]
        remove += ["!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "+", "=", "´", ",", ".", ":", "?"]

        new_data = ""
        for word in data.split(" "):
            if word not in remove:
                new_data += word + " "
        return new_data

    def publishToReduce(self, data, file, word):
        data = self.clear(data)
        prod = Prod("./python.config", "reduce")
        prod.publish("data", {'data': data, 'file': file, 'word': word})
        try:
            prod.flush()
        except:
            pass

    def run(self):
        termClean = Cons(".\python.config")
        termClean.subscribe(["termclean"])
        while True:
            # receber dados
            data, err = termClean.run()
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
                    executor.submit(self.publishToReduce, data, file, word)
        termClean.close()
if __name__ == "__main__":
    TermClean().run()

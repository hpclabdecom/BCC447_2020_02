import os
import concurrent.futures
from classProducer import Prod
from threading import Lock

bloqueio = Lock()

class Loader:
    def __init__(self, path, word):
        self.path = path
        os.chdir(os.path.join(os.getcwd(), self.path))
        self.files = os.listdir()
        os.chdir('..')
        self.word = word
        

    def readFile(self, file):
        # ler arquivo
        bloqueio.acquire()
        os.chdir(os.path.join(os.getcwd(), self.path))
        with open(file) as f:
            data = f.read()
        os.chdir('..')
        bloqueio.release()
        return data


    def sendToDecoder(self, file):
        #ler arquivo
        data = self.readFile(file)
        
        prod = Prod("./python.config", "decode")

        print('data', {'data': data})
        prod.publish("data", {'data': data, 'file': file, 'word': self.word})
        try:
            prod.flush()
        except:
            pass
        
    def run(self):
        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            # dividir para as threads
            results = executor.map(self.sendToDecoder, self.files)
            for result in results:
                print(result)

if __name__ == "__main__":
    path = "Arquivos"
    word = "Manel"
    Loader(path, word).run()

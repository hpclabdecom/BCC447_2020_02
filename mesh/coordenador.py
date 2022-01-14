from classConsumer import Cons
from classProducer import Prod
from threading import Thread
import sys

class Coordinator:
    def __init__ (self, topic, coordinatorsTopic, topicClients):
        self.topic = topic
        self.topicClients = topicClients
        self.coordinatorsTopic = coordinatorsTopic

    def timeout(self, subscriber, seconds = 10):
        i = 0

        while i < seconds:
            i += 1
            data, err = subscriber.run()

            if data is None:
                continue
            else:
                return data, err

        raise(TypeError)

    def run(self):
        print("Entrou no coordenador ", self.topic)
        cont = Cons(".\python.config")
        cont.subscribe([self.topic])
        bodies = []
        while True:
            try:
                data, err = self.timeout(cont, 15)
                print(f'Recebi data: {data}')
                if data == None:
                    continue
                elif err != None:
                    continue
                else:
                    bodies.append(data)
            except TypeError:
                # caso dê exesão, conferir se tem uam unica palavra a ser somada 
                print("timeout")
                for topic in self.coordinatorsTopic:
                    print(f'publicando em coordenador')
                    for body in bodies:
                        prod = Prod("./python.config", topic)
                        prod.publish("data", body)
                        print(f'Publicando em {topic} - {str(body)}')
                        try:
                            prod.flush()
                        except:
                            pass
                if bodies == []:
                    continue
                self.run2(cont, bodies.copy())
                bodies = []

        cont.close()
    
    def run2(self, cont, bodies):
        while True:
            try:
                data, err = self.timeout(cont, 15)
                print(f'Recebi data: {data}')
                if data == None:
                    continue
                elif err != None:
                    continue
                else:
                    bodies.append(data)
            except TypeError:
                print("timeout run2 ", self.topic)
                for topic in self.topicClients:
                    for body in bodies:
                        prod = Prod("./python.config", topic)
                        prod.publish("data", body)
                        print(f'Publicando runc2 em {topic} - {str(body)}')
                        try:
                            prod.flush()
                        except:
                            pass
                bodies = []
                break

if __name__ == "__main__":
    # self, topic, coordinatorsTopic, topicClients
    if sys.argv[1] == "1":
        c0 = Coordinator("coordenador0", ["coordenador1"], ["c0"])
        c0.run()
    if sys.argv[1] == "2":
        c1 = Coordinator("coordenador1", ["coordenador0"], ["c1"])
        c1.run()

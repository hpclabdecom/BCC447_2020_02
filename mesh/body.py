import concurrent.futures
from classConsumer import Cons
from classProducer import Prod
import copy
import sys
import time
import random

class Body:
    def __init__ (self, x, y, size, xDisplacement = 1, yDisplacement = 1):
        self.x = x
        self.y = y
        self.xDisplacement = xDisplacement
        self.yDisplacement = yDisplacement
        self.size = size

    def __eq__ (self, other):
        x = self.x == other.x
        y = self.y == other.y
        xDisplacement = self.xDisplacement == other.xDisplacement
        yDisplacement = self.yDisplacement == other.yDisplacement
        size = self.size == other.size

        return x and y and xDisplacement and yDisplacement and size


    def colision (self, body):
        if self.xDisplacement == 0:
            self.xDisplacement = -body.xDisplacement
        else:
            self.xDisplacement = -self.xDisplacement
        if self.yDisplacement == 0:
            self.yDisplacement = -body.yDisplacement
        else:
            self.yDisplacement = -self.yDisplacement

        self.moveX(abs(body.size + self.size - self.size))
        self.moveY(abs(body.size + self.size - self.size)) 

    def changeAll (self, nBodys):
        for body in nBodys:
            self.change(body)
    
    def change (self, body):
        if self.x == body.x and self.y == body.y:
            self.colision(body)
        else:
            if body.size > self.size:
                displacementX = min(body.size - self.size, abs(body.x - self.x))
                displacementY = min(body.size - self.size, abs(body.y - self.y))

                if body.x - self.x < 0:
                    self.xDisplacement = -1
                elif body.x - self.x == 0:
                    self.xDisplacement = 0
                else:
                    self.xDisplacement = 1

                if body.y - self.y < 0:
                    self.yDisplacement = -1
                elif body.y - self.y == 0:
                    self.yDisplacement = 0
                else:
                    self.yDisplacement = 1
                print(f'x: {displacementX}  -  y: {displacementY}')
                self.moveX(displacementX)
                self.moveY(displacementY)

    def moveX (self, displacement):
        self.x = self.x + displacement * self.xDisplacement

    def moveY (self, displacement):
        self.y = self.y + displacement * self.yDisplacement
        

class Client:
    def __init__ (self, topic, coordenationTopic, bodies):
        self.topic = topic
        self.coordenationTopic = coordenationTopic
        self.bodies = bodies

    def run(self):
        print("Entrou no run")
        cont = Cons(".\python.config")
        cont.subscribe([self.topic])
        while True:
            reicivedBodies = []
            for body in self.bodies:
                    prod = Prod("./python.config", self.coordenationTopic)
                    prod.publish("data", body.__dict__)
                    print(f'Publicando em {self.coordenationTopic} - {body.__dict__}')
                    try:
                        prod.flush()
                    except:
                        pass
            while True:
                try:
                    data, err = self.timeout(cont, 50)
                    print(f'Recebi data: {data}')
                    if data == None:
                        continue
                    elif err != None:
                        continue
                    else:
                        reicivedBodies.append(Body(int(data['x']), int(data['y']), int(data['size']), int(data['xDisplacement']), int(data['yDisplacement'])))
                        print("Received bodies: ")
                except TypeError:
                    print("Entrou no exception")
                    if reicivedBodies == []:
                        print("reicivedBodies == []")
                        continue
                    with concurrent.futures.ThreadPoolExecutor(4) as executor:
                        # dividir para as threads
                        results = executor.map(self.changeAll, [(i, reicivedBodies.copy()) for i in self.bodies])
                        resultados = []
                        print("Trabalhando sobre: ", reicivedBodies)
                        print("Resultados")
                        for result in results:
                            resultados.append(result)
                            print("  ->", result.__dict__)
                        print("Atulização")
                        for i, result in enumerate(resultados):
                            self.bodies[i] = result
                    break
            # break
                
        cont.close()

    def changeAll (self, bodies):
        body = copy.deepcopy(bodies[0])
        recivedBodies = bodies[1]

        recivedBodies = [i for i in recivedBodies if i != body]

        body.changeAll(recivedBodies)
        for b in bodies[1]:
            print("imprimiendo changeAll: ", b.__dict__)
        return body

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
        
if __name__ == "__main__":
    bodies = []
    for _ in range (50):
        bodies.append(Body(random.randint(-100, 100), random.randint(-100, 100), random.randint(0, 100)))
    
    if sys.argv[1] == "1":
        Client("c1", f"coordenador{sys.argv[1]}", bodies).run()
    else:
        Client("c2", f"coordenador{sys.argv[1]}", bodies).run()

    
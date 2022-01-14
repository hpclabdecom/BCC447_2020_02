import classProducer as producer
from classConsumer import Cons

prod = producer.Prod(".\python.config", "teste")

for n in range(10):
    print('piblising', "hello", {'count': n})
    prod.publish("hello", {'count': n})
    try:
        prod.flush()
    except:
        pass

cons = Cons(".\python.config")

cons.subscribe(["decode"])

cons.run()

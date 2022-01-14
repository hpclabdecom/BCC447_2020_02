from confluent_kafka import Producer, KafkaError
import json
import ccloud_lib

class Prod:
    def __init__ (self, configFile, topic):
        self.conf = ccloud_lib.read_ccloud_config(configFile)
        self.producer_conf = ccloud_lib.pop_schema_registry_params_from_config(self.conf)
        self.producer = Producer(self.producer_conf)
        self.topic = topic
        ccloud_lib.create_topic(self.conf, topic)

    def acked(err, msg):
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    def flush (self):
        self.producer.flush()

    def publish (self, key, value):
        record_value = json.dumps(value)
        self.producer.produce(self.topic, key=key, value=record_value, on_delivery=self.acked)
        self.producer.poll(0)



if __name__ == '__main__':
    prod = Prod(".\python.config", "teste")

    for n in range(10):
        print('piblising', "hello", {'count': n})
        prod.publish("hello", {'count': n})
        try:
            prod.flush()
        except:
            pass
        
  


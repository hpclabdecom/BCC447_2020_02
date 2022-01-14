from confluent_kafka import Consumer
import json
import ccloud_lib

class Cons:
    def __init__ (self, configFile):
        self.conf = ccloud_lib.read_ccloud_config(configFile)
        self.consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(self.conf)
        self.consumer_conf['group.id'] = 'python_example_group_1'
        self.consumer_conf['auto.offset.reset'] = 'earliest'
        self.consumer = Consumer(self.consumer_conf)

    def subscribe(self, topics):
        self.consumer.subscribe(topics)

    def close(self):
        self.consumer.close()

    def run(self):
        while True:
            try:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    # No message available within timeout.
                    # Initial message consumption may take up to
                    # `session.timeout.ms` for the consumer group to
                    # rebalance and start consuming
                    return None, None
                elif msg.error():
                    return msg.error(), 'err'
                else:
                    record_value = msg.value()
                    return json.loads(record_value), None
            except KeyboardInterrupt:
                pass


if __name__ == '__main__':
    cons = Cons(".\python.config")

    cons.subscribe(["teste"])
    while True:
        cons.run()



import pika

class MQTT:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials("guest", "guest")
            )
        )
        self.traffic_alerts_channel = self.connection.channel()
        self.garbage_alerts_channel = self.connection.channel()
        self.crowd_alerts_channel = self.connection.channel()

        self.traffic_alerts_channel.queue_declare('traffic_alerts')
        self.garbage_alerts_channel.queue_declare('garbage_alerts')
        self.crowd_alerts_channel.queue_declare('crowd_alerts')
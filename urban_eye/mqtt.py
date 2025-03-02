
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
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='traffic_alerts', exchange_type='fanout')
        self.channel.exchange_declare(exchange='garbage_alerts', exchange_type='fanout')
        self.channel.exchange_declare(exchange='crowd_alerts', exchange_type='fanout')
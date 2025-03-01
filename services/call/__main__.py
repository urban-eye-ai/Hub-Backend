
import os
import pika
from twilio.rest import Client
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv(".services.call.env")

account = os.environ["TWILIO_ACCOUNT"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
ngrok_url = os.environ["NGROK_URL"]

client = Client(account, auth_token)

def traffic_alerts_callback(ch, method, properties, body):
    location = body
    encoded_location = quote(location)
    call = client.calls.create(
        url=f"{ngrok_url}/alerts/traffic?location={encoded_location}",
        to="+919545572005",
        from_=twilio_number,
    )
    print(call.sid)

def garbage_alerts_callback(ch, method, properties, body):
    pass

def crowd_alerts_callback(ch, method, properties, body):
    pass

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=pika.PlainCredentials("guest", "guest")
    )
)

channel = connection.channel()
channel.queue_declare('traffic_alerts')
channel.queue_declare('garbage_alerts')
channel.queue_declare('crowd_alerts')

channel.basic_consume(queue='traffic_alerts', on_message_callback=traffic_alerts_callback, auto_ack=True)
channel.basic_consume(queue='garbage_alerts', on_message_callback=garbage_alerts_callback, auto_ack=True)
channel.basic_consume(queue='crowd_alerts', on_message_callback=crowd_alerts_callback, auto_ack=True)

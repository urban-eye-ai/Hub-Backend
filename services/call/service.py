
import time
import os
import pika
from twilio.rest import Client
from urllib.parse import quote
from dotenv import load_dotenv
# from googlemaps import Client
# from googlemaps.places import places_nearby, place

load_dotenv("services.call.env")

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
ngrok_url = os.environ["NGROK_URL"]

client = Client(account_sid, auth_token)
# maps_client = Client("<API-KEY>")

def traffic_alerts_callback(ch, method, properties, body):
    # result = places_nearby(client, location=body, radius=5000, type='police')
    # if result.get('results'):
    #     nearest_police = result['results'][0]
    #     place_id = nearest_police['place_id']
        
    #     place_details = place(place_id=place_id, fields=['formatted_phone_number', 'name'])
    #     result = place_details.get('result', {})
        
    #     print("Nearest police station:")
    #     print("Name:", result.get('name'))
    #     print("Phone number:", result.get('formatted_phone_number'))
    # else:
    #     print("No nearby police stations found.")

    location = body
    encoded_location = quote(location)
    call = client.calls.create(
        url=f"{ngrok_url}/alerts/traffic?location={encoded_location}",
        to="+919545572005",
        from_=twilio_number,
    )
    print(call.sid)

def garbage_alerts_callback(ch, method, properties, body):
    location = body
    encoded_location = quote(location)
    call = client.calls.create(
        url=f"{ngrok_url}/alerts/garbage?location={encoded_location}",
        to="+919545572005",
        from_=twilio_number,
    )
    print(call.sid)

def crowd_alerts_callback(ch, method, properties, body):
    location = body
    encoded_location = quote(location)
    call = client.calls.create(
        url=f"{ngrok_url}/alerts/crowd?location={encoded_location}",
        to="+919545572005",
        from_=twilio_number,
    )
    print(call.sid)

if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials("guest", "guest")
        )
    )

    channel = connection.channel()

    channel.exchange_declare(exchange='traffic_alerts', exchange_type='fanout')
    channel.exchange_declare(exchange='garbage_alerts', exchange_type='fanout')
    channel.exchange_declare(exchange='crowd_alerts', exchange_type='fanout')

    traffic_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    garbage_queue = channel.queue_declare(queue='', exclusive=True).method.queue
    crowd_queue = channel.queue_declare(queue='', exclusive=True).method.queue

    channel.queue_bind(traffic_queue, 'traffic_alerts')
    channel.queue_bind(garbage_queue, 'garbage_alerts')
    channel.queue_bind(crowd_queue, 'crowd_alerts')

    channel.basic_consume(queue=traffic_queue, on_message_callback=traffic_alerts_callback, auto_ack=True)
    channel.basic_consume(queue=garbage_queue, on_message_callback=garbage_alerts_callback, auto_ack=True)
    channel.basic_consume(queue=crowd_queue, on_message_callback=crowd_alerts_callback, auto_ack=True)

    print("Starting...")
    channel.start_consuming()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
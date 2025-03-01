# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from urllib.parse import quote
from dotenv import load_dotenv
load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
ngrok_url = os.environ["NGROK_URL"]

client = Client(account_sid, auth_token)

location = "Hadapsar Road, Pune"
encoded_location = quote(location)

call = client.calls.create(
    url=f"{ngrok_url}/twiml?location={encoded_location}",
    to="+919545572005",
    from_=twilio_number,
)

print(call.sid)
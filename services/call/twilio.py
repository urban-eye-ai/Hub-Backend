
from flask import Flask, request, Response

app = Flask(__name__)

@app.post("/alerts/traffic")
def traffic_alert():
    location = request.args.get("location", "an unknown location")
    message = f"Alert! There is a heavy traffic jam on {location}. Please send traffic police to the site as soon as possible."

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">{message}</Say>
    </Response>"""

    return Response(xml_response, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
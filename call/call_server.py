from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/twiml", methods=['POST'])  # Use 'POST' if Twilio is making a POST request
def twiml():
    location = request.args.get("location", "an unknown location")
    
    # Corrected f-string formatting
    message = f"Alert! There is a heavy traffic jam on {location}. Please send traffic police to the site as soon as possible."

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">{message}</Say>
    </Response>"""

    return Response(xml_response, mimetype="text/xml")

if __name__ == "__main__":
    app.run(port=5000)

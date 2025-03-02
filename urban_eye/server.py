
import os
import cv2
from dotenv import load_dotenv

from urban_eye.detection import DetectionModel
from urban_eye.mqtt import MQTT

load_dotenv() # Load environment variables

rstp_uri = os.environ["RTSP_URI"]

shouldDetectTrafficAndCrowd = False
model = DetectionModel("cars.pt" if shouldDetectTrafficAndCrowd else "garbage.pt")
mqtt_broker = MQTT()

if __name__ == "__main__":
    for i in range(5):
        cap = cv2.VideoCapture(rstp_uri, cv2.CAP_FFMPEG)
        if cap.isOpened():
            print("RTSP Stream Opened Successfully!")
            break
        print(f"Retrying to open stream... ({i+1}/5)")
    else:
        print("Error: Could not open RTSP stream after multiple attempts.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        results = model.detect(frame)
        results.render()

        detections = results.pandas().xyxy[0]
        detection_list = []

        if shouldDetectTrafficAndCrowd:
            people = 0
            vehicles = 0

            for _, det in detections.iterrows():
                if det['name'] == 'person':
                    people += 1
                else:
                    vehicles += 1
                detection_list.append({
                    'class': det['name'],
                    'confidence': float(det['confidence']),
                    'bbox': [
                        float(det['xmin']), 
                        float(det['ymin']), 
                        float(det['xmax']),
                        float(det['ymax'])
                    ]
                })

            if vehicles >= 10:
                mqtt_broker.channel.basic_publish(exchange='traffic_alerts', routing_key='', body='Karve Nagar')

            if people >= 20:
                mqtt_broker.channel.basic_publish(exchange='crowd_alerts', routing_key='', body='Karve Nagar')
        
        else:
            items = 0
            for _, det in detections.iterrows():
                if det['name'] == 'garbage':
                    items += 1
            if items != 0:
                mqtt_broker.channel.basic_publish(exchange='garbage_alerts', routing_key='', body='Karve Nagar')

        cv2.imshow('VIDEO', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

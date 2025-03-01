
import os
import cv2
from dotenv import load_dotenv
from ultralytics import YOLO

from urban_eye.mqtt import MQTT

load_dotenv() # Load environment variables

rstp_uri = os.environ["RTSP_URI"]

yolo = YOLO("yolov8n.pt")
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

        results = yolo(frame)[0]

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = yolo.names[int(box.cls[0])]
            conf = box.conf[0].item()
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('VIDEO', frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

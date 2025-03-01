import cv2
import torch
from ultralytics import YOLO
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

local_ip = os.environ["LOCAL_IP"]
RTSP_URL = f"rtsp://{local_ip}:554/mjpeg/1"

# Open the RTSP stream
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

# Ensure the output directory exists
output_dir = "output/captured_videos"
os.makedirs(output_dir, exist_ok=True)

# Video Writer (initially None)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

recording = False
last_detected_time = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # Run YOLOv8 Object Detection
    results = model(frame)[0]  # Get first batch result
    
    # Check if a person is detected
    person_detected = any(model.names[int(box.cls[0])] == "person" for box in results.boxes)

    if person_detected:
        print("👀 Person detected! Starting real-time recording...")
        last_detected_time = time.time()

        # Start recording if not already started
        if not recording:
            filename = os.path.join(output_dir, f"recorded_{int(time.time())}.mp4")
            out = cv2.VideoWriter(filename, fourcc, 30, (frame.shape[1], frame.shape[0]))
            recording = True

    # Stop recording if no person seen for 15 seconds
    elif recording and (time.time() - last_detected_time > 15):
        print("🛑 No person detected for 15s. Stopping recording...")
        recording = False
        if out:
            out.release()
            out = None

    # Save frame if recording
    if recording and out:
        out.write(frame)

    # Display the Stream with Detections
    cv2.imshow("RTSP Object Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

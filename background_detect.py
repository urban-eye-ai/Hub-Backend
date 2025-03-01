import cv2
import time
import threading
import torch
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

RTSP_URL = "rtsp://192.168.244.47:554/mjpeg/1"

cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

latest_frame = None
recording = False
last_detected_time = 0
slow_mode = True
lock = threading.Lock()

# Video Writer (initially None)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = None

# Thread to continuously fetch the latest frame
def update_frame():
    global latest_frame
    while True:
        ret, frame = cap.read()
        if ret:
            with lock:
                latest_frame = frame  # Update with latest frame
        time.sleep(0.1)

# Start frame update thread
threading.Thread(target=update_frame, daemon=True).start()

while True:
    time.sleep(30 if slow_mode else 0.1)

    with lock:
        if latest_frame is None:
            continue  # Skip if no frame available yet
        frame = latest_frame.copy()

    # Run YOLOv8 detection
    results = model(frame)[0]

    # Check if a person is detected
    person_detected = any(model.names[int(box.cls[0])] == "person" for box in results.boxes)

    if person_detected:
        print("👀 Person detected! Starting real-time recording...")
        last_detected_time = time.time()
        slow_mode = False  # Switch to continuous mode

        # Start recording if not already started
        if not recording:
            filename = f"captured_videos/recorded_{int(time.time())}.mp4"
            out = cv2.VideoWriter(filename, fourcc, 30, (frame.shape[1], frame.shape[0]))
            recording = True

    elif recording:
        # Stop recording if no person seen for 30s
        if time.time() - last_detected_time > 30:
            print("🛑 No person detected for 30s. Stopping recording...")
            recording = False
            slow_mode = True  # Return to slow mode
            if out:
                out.release()
                out = None

    # Save frame if recording
    if recording and out:
        out.write(frame)

    # Show video with detection
    cv2.imshow("RTSP Object Detection", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

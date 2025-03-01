import cv2
import time
import os

RTSP_URL = "rtsp://192.168.244.47:554/mjpeg/1"
SAVE_DIR = "captured_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

# Try opening the stream multiple times
for i in range(5):
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
    time.sleep(2)  # Wait for 2 seconds
    if cap.isOpened():
        print("RTSP Stream Opened Successfully!")
        break
    print(f"Retrying to open stream... ({i+1}/5)")
else:
    print("Error: Could not open RTSP stream after multiple attempts.")
    exit()

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    cv2.imshow('VIDEO', frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

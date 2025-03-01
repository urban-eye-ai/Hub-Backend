import cv2
import time
import os

# Replace with your RTSP URL
RTSP_URL = "rtsp://192.168.244.47:554/mjpeg/1"
SAVE_DIR = "captured_frames"

# Create the directory if it doesn't exist
os.makedirs(SAVE_DIR, exist_ok=True)

# Open the RTSP stream
cap = cv2.VideoCapture(RTSP_URL)

print('capturing')

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # Save the frame every 10 seconds
    frame_filename = os.path.join(SAVE_DIR, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_filename, frame)
    print(f"Captured: {frame_filename}")

    frame_count += 1

    # Wait for 10 seconds before capturing the next frame
    time.sleep(10)

cap.release()
cv2.destroyAllWindows()

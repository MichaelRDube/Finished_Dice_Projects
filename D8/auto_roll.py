import serial
import time
import cv2
import os
import signal
import sys


# Create a directory to save the captured images
save_dir = "./captured_images"
processed_dir = './processed_images'
dieType = "D8"

# Replace 'COM3' with your Arduino's port (e.g., '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

time.sleep(2)  # Wait for Arduino to initialize

def send_command(command):
    arduino.write((command + '\n').encode())  # Send command with newline character
    response = ""
    while response == "":
        response = arduino.readline().decode().strip()  # Read response, if any
    return response

# Initialize the counter for saved images
counter = 0
for file in os.listdir(save_dir):
    try:
        candidate = file.split('_')[-1]
        candidate = int(candidate.split('.')[0])
        if candidate > counter:
            counter = candidate
    except:
        print("Badly named file in 'captured_images'. Skipping count.")

for file in os.listdir(processed_dir):
    try:
        candidate = file.split('_')[-1]
        candidate = int(candidate.split('.')[0])
        if candidate > counter:
            counter = candidate
    except:
        print("Badly named file in 'processed_images'. Skipping count.")

while True:
    send_command("R")
    print("Done rolling.  Allowing to settle.")
    # Set up webcam capture
    cap = cv2.VideoCapture(0)  # Use the first available camera
    #time.sleep(1)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit()
    ret, frame = cap.read()
    if ret:
        counter += 1
        filename = os.path.join(save_dir, dieType + "_" + str(counter) + ".png")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filename, frame)  # Save the captured frame as an image
        print(f'saved {filename}')
    cap.release()
    


cv2.destroyAllWindows()

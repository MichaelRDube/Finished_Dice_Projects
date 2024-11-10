import cv2
import os
import datetime

# Create a directory to save the captured images
save_dir = "./captured_images"
processed_dir = './processed_images'
dieType = "D20"


#initialize the counter
counter = 0
for file in os.listdir(save_dir):
    try:
        candidate = file.split('_')[-1]
        candidate = int(candidate.split('.')[0])
        if candidate > counter:
            counter = candidate
    except:
        print("Badly named file in \'processed_images\'.  Skipping count.")

for file in os.listdir(processed_dir):
    try:
        candidate = file.split('_')[-1]
        candidate = int(candidate.split('.')[0])
        if candidate > counter:
            counter = candidate
    except:
        print("Badly named file in \'processed_images\'.  Skipping count.")



# Set up webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

os.makedirs(save_dir, exist_ok=True)

# Set the desired window size
window_width = 2560  # Width in pixels
window_height = 1920  # Height in pixels
cv2.namedWindow('Webcam Stream', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Webcam Stream', window_width, window_height)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Resize the frame to match the window size
    resized_frame = cv2.resize(frame, (window_width, window_height))

    # Display the resized frame
    cv2.imshow('Webcam Stream', resized_frame)

    # Wait for the space bar (ASCII code 32) to be pressed
    key = cv2.waitKey(1)
    if key == 32:
        # Create a unique filename based on the current timestamp
        #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        #filename = os.path.join(save_dir, f"image_{timestamp}.png")
        counter += 1
        filename = os.path.join(save_dir, dieType + "_" + str(counter) + ".png")

        
        # Save the captured image (original size)
        #and make it greyscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
        print(f"{len(os.listdir(save_dir))} files in directory.")

    # Exit the loop when 'q' is pressed
    elif key == ord('q'):
        break
    """
    elif len(os.listdir(save_dir)) >= 35:
        print("All done!")
        break

    """
# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

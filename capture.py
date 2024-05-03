from serial import Serial
import cv2
import os
import datetime
import time

ser = Serial('COM7', 9600)  # Change 'COM7' to the correct serial port

# Specify the index of the external USB webcam
video_device_index = 1  # Adjust this index based on your system configuration
width = 1280
height = 720

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        if data == 'Entry detected':
            # Generate unique filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # filename = f"captured_photo_{timestamp}.jpg"
            filename = f"captured_photo.jpg"
            # Adjust camera settings
            capture = cv2.VideoCapture(video_device_index)  # Open external USB webcam
            # capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)  # Disable auto exposure
            # capture.set(cv2.CAP_PROP_EXPOSURE, 0.5)     # Set exposure value (0.0 - 1.0)
            # Allow a brief delay for the webcam to adjust
            time.sleep(4)  # Adjust the delay time as needed

            ret, frame = capture.read()  # Capture photo
            
            #exception handling
            if not capture.isOpened():
                print("Error: Unable to open webcam.")
                break


            # Save photo with unique filename
            cv2.imwrite(filename, frame)
            capture.release()  # Release webcam
            
            print(f'Photo captured: {filename}')

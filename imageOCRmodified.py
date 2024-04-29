import cv2
import easyocr
from PIL import Image
import re
import csv
import os
import time
from serial import Serial

# Mail imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ser = Serial('COM7', 9600)

# Function to send email
def send_email(to, subject, msg):
    # Email configuration
    sender_email = "foodiereserve@gmail.com"
    app_password = "jgvc flaz wgqa nvrl"  # Your app password

    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to
    message['Subject'] = subject

    # Attach HTML message
    message.attach(MIMEText(msg, 'html'))

    # Connect to Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # Login to Gmail account
        server.login(sender_email, app_password)
        # Send email
        server.send_message(message)
        print("Email sent successfully.")

# Function to add data to CSV file
def add_data_to_csv(filename, data, header):
    mode = 'w' if not os.path.isfile(filename) else 'a'
    with open(filename, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow(header)
        writer.writerows(data)

# Function to perform OCR on an image and return the recognized text
def ocr_license_plate(image_path):
    print("Performing OCR on the image...")
    image = Image.open(image_path)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    license_plate_text = result[0][1] if result else None
    print("OCR Result:", license_plate_text)
    if license_plate_text:
        license_plate_text = re.sub(r'\s+', '', license_plate_text)
    return license_plate_text

def create_slot_status_file(num_slots):
     print("Creating slot status CSV file...")
     csv_filename = 'slotStatus.csv'  # CSV file containing slot status
     header = ['Slot Number', 'Status']  # Header for CSV file
     data = []  # Initialize data
     # for i in range(1, num_slots + 1):  # Adjusted to use the provided number of slots
     #     data.append([f'slot{i}', 'empty'])  # Add slot data (slot1, slot2, ..., slotN)
     add_data_to_csv(csv_filename, data, header)  # Add data to CSV file


# Function to extract phone number and email from CSV based on license plate
def extract_phone_email_from_csv(filename, license_plate):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if row[4] == license_plate:
                return row[2], row[3]
    return None, None

# Function to detect license plates using Haar cascade
def detect_license_plate(image_path, cascade_path, output_path, csv_filename):
    print("Detecting license plates using Haar cascade...")
    image = cv2.imread(image_path)
    plate_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    print("Number of plates detected:", len(plates))
    for i, (x, y, w, h) in enumerate(plates):
        print(f"Processing plate {i+1}...")
        plate_roi = image[y:y+h, x:x+w]
        cv2.imwrite(output_path.format(i), plate_roi)
        detected_text = ocr_license_plate(output_path.format(i))
        print("Detected License Plate:", detected_text)
        if detected_text:
            if check_license_plate_in_csv(csv_filename, detected_text):
                print(f"License plate {detected_text} is in the CSV file.")
                phone_number, email = extract_phone_email_from_csv(csv_filename, detected_text)
                if phone_number and email:
                    print(f"Phone Number: {phone_number}")
                    print(f"Email: {email}")
                    # Example usage
                    to = email
                    subject = "still testing"
                    msg = f"""
                        <html>
                        <body>
                            <p style="font-size: 16px; font-weight: bold;">
                            {detected_text}
                        </p>
                        </body>
                        </html>
                        """
                    send_email(to, subject, msg)
                    
                else:
                    print("Phone number or email not found.")
            else:
                print(f"License plate {detected_text} is not in the CSV file.")
        else:
            print("License plate not recognized.")

# Function to check if license plate is in CSV file
def check_license_plate_in_csv(filename, license_plate):
    # Open the CSV file in read mode
    with open(filename, mode='r', newline='') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        # Iterate over each row in the CSV file
        for row in reader:
            # Check if the row has at least 5 elements
            if len(row) >= 5:
                # Check if the license plate matches the one provided
                if row[4] == license_plate:
                    # If a match is found, return True
                    return True
    # If no match is found or the row doesn't have enough elements, return False
    return False


def write_slot_status(slot, status):
    print(f"Writing slot status '{status}' to CSV file for slot '{slot}'...")
    csv_filename = 'slotStatus.csv'
    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([slot, status])

def read_serial_data(num_slots,image_path, cascade_path, output_path, csv_filename):
    print("Reading serial data...")
    data = ""
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            # print("Received:", data)
            if data == 'Entry detected':
                print("Entry detected")
                filename = f"car_image.jpg"
                # Adjust camera settings
                capture = cv2.VideoCapture(1)
                ret, frame = capture.read()  # Capture photo
                cv2.imwrite(filename, frame)
                capture.release()
                # Delete the existing slot status CSV file
                if os.path.exists('slotStatus.csv'):
                    os.remove('slotStatus.csv')
                    print("Deleted existing slot status CSV file.")
                # Recreate the slot status CSV file
                create_slot_status_file(num_slots)
                # Detect license plates
                detect_license_plate(image_path, cascade_path, output_path, csv_filename)
            elif data.startswith('Vehicle Parked at Slot'): #Slot Empty at
                slot_number = data.split()[-1]
                write_slot_status(f'slot{slot_number}', 'full')
            elif data.startswith('Slot Empty at Slot'): #Slot Empty at
                slot_number = data.split()[-1]
                write_slot_status(f'slot{slot_number}', 'Empty')
            elif data == 'No Entry detected':
                print("No Entry detected")
            

# Example usage
image_path = 'car_image.jpg'  # Replace with the path to your image
cascade_path = 'haarcascade_russian_plate_number.xml'  # Path to the Haar cascade XML file
output_path = 'detected_license_plate_{}.jpg'  # Output path pattern for the detected license plate images
csv_filename = 'userDATA.csv'  # CSV file containing user data
num_slots=3


# Start reading serial data
read_serial_data(num_slots,image_path, cascade_path, output_path, csv_filename)
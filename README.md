### Smart Car Parking using Arduino 
#### The aim of this project is to develop and implement a smart parking system utilizing Arduino, image processing for license plate recognition, and IR sensors. This system seeks to optimize parking space utilization, improve traffic flow, and enhance user experience by providing real-time parking availability updates, automated entry/exit control, and efficient management of parking spaces. By integrating these technologies, the project aims to address common parking-related challenges such as congestion, inefficient space usage, and difficulty in finding available parking spots, ultimately contributing to more sustainable and accessible urban environments.

### Reqirements:
- Arduino UNO r3 Processing Board
- Wires (Jumper Wires)
- Breadboard
- IR Sensors (Gate + Parking Lot)
- Servo Motor (Opening/Closing Gate)
- USB Web Cam (Lisence Plate Detection)
- Bluetooth module (HC-05) for Arduino board

----

### Block Diagram

<p align="center">
  <img  width="850" height="200" src="https://i.imgur.com/B7PiQVm.png">
</p>

----

### Circuit Diagram
<p align="center">
  <img  width="500" height="400" src="https://i.imgur.com/Zifsnqi.png">
</p>

----

### Screenshots

<p align="center">
  <img src="https://imgur.com/RB5wuEb.png">
</p>
<p align="center">
  <img src="https://imgur.com/I31SQjN.png">
</p>
<p align="center">
  <img src="https://imgur.com/PMKldB8.png">
</p>

### `capture.py` file runs in background to capture an image of the Lisence Plate when the it reads "Entry Detected" from serial port

#### More work incoming related to image capture and OCR for Lisence plate...



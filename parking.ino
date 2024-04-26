#include <SoftwareSerial.h>
#include <Servo.h>
Servo myServo;
bool gateOpen = false; // Flag to track if the gate is open

SoftwareSerial bluetooth(8, 9); // RX, TX

const int irSensorPin = 5; // IR Sensor pin

int irSensorPin1 = 2;
int irSensorPin2 = 3;
int irSensorPin3 = 4;
int irSensorPin4 = 5;

int irSensorValue1;
int irSensorValue2;
int irSensorValue3;
int irSensorValue4;

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600); // Default baud rate for most HC-05 modules
  pinMode(irSensorPin, INPUT);  // Initialize IR sensor pin
  //myServo.attach(10); // Attach the servo to pin 10
  //myServo.write(0);  // Close the gate initially
  //delay(100);
  //myServo.detach();
}

void loop() {
  irSensorValue1 = digitalRead(irSensorPin1);
  irSensorValue2 = digitalRead(irSensorPin2);
  irSensorValue3 = digitalRead(irSensorPin3);
  irSensorValue4 = digitalRead(irSensorPin4);

  // If obstacle is detected
  if (irSensorValue4 == HIGH) {
      // Print the state of the IR sensor
      Serial.println("No Entry detected\n");
      bluetooth.println("No Entry detected\n");
  }else{
     Serial.println("Entry detected");
      bluetooth.println("Entry detected\n");
    // Rotate the servo to avoid the obstacle
      myServo.attach(10);
//      delay(1);
//      myServo.write(0);      // Rotate servo to the left (adjust the angle as needed)
//      delay(3000);         // Keep the servo in this position for 3 seconds
//      myServo.write(80);     // Rotate servo back to the center position
//      delay(1000);         // Delay before resuming normal operation
     
      
      delay(2000);
      for (int angle = 80; angle >=0; angle--) {
        myServo.write(angle);
        delay(40); // Adjust delay as needed for smoother motion
      } 
      delay(2000);
        for (int angle = 0; angle <= 80; angle++) {
        myServo.write(angle);
        delay(40); // Adjust delay as needed for smoother motion
      }
       


      
      myServo.detach();      // Detach servo to save power

      if (irSensorValue1 == HIGH) {
        Serial.println("Slot 1 Empty");
        bluetooth.println("Slot 1 Empty"); // Sending '1' when Vehicle Parked at Slot  1
      } else {
        Serial.println("Vehicle Parked at Slot 1");
        bluetooth.println("Vehicle Parked at Slot 1"); // Sending '0' when Empty Slot  1
      }
    
      if (irSensorValue2 == HIGH) {
        Serial.println("Slot 2 Empty");
        bluetooth.println("Slot 2 Empty"); // Sending '1' when Vehicle Parked at Slot  2
      } else {
        Serial.println("Vehicle Parked at Slot 2");
        bluetooth.println("Vehicle Parked at Slot 2"); // Sending '0' when Empty Slot  2
      }
    
      if (irSensorValue3 == HIGH) {
        Serial.println("Slot 3 Empty");
        bluetooth.println("Slot 3 Empty"); // Sending '1' when Vehicle Parked at Slot  3
      } else {
        Serial.println("Vehicle Parked at Slot 3");
        bluetooth.println("Vehicle Parked at Slot 3"); // Sending '0' when Empty Slot  3
      }
  }
  delay(5000); //scanning delay
  Serial.println("____________________________");
  bluetooth.println("____________________________");
  String receivedMessage = "";
  while (bluetooth.available() > 0) {
    char receivedChar = bluetooth.read();
    if (receivedChar == '\n') {
      Serial.print("Received from slave: ");
      Serial.println(receivedMessage);
      receivedMessage = ""; // Clear the message buffer
    } else {
      receivedMessage += receivedChar;
      Serial.print("Received from slave (else): ");
      Serial.println(receivedMessage);
    }
  }
}

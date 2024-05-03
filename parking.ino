#include <SoftwareSerial.h>
#include <Servo.h>

// Define pin numbers for IR sensors
const int irSensorPin1 = 3;
const int irSensorPin2 = 2;
const int irSensorPin3 = 4;
const int irSensorPin4 = 5; //gate IR

// Define IR sensor values variable to store value of IR sensor state
int irSensorValue1; 
int irSensorValue2;
int irSensorValue3;
int irSensorValue4; //gate IR

// Create instances of Servo and SoftwareSerial
Servo myServo;
SoftwareSerial bluetooth(8, 9); //bluetooth RX, TX

// Function prototypes
void checkAndSendSlotStatus(int irSensorValue, const char* slotName);

void setup() {
  Serial.begin(9600); // setting serial communication baud rate
  bluetooth.begin(38400); // setting bluetooth baud rate
  pinMode(irSensorPin4, INPUT); // IR sensor 4 pin as input (gate)
}

void loop() {
  // Read values of all four IR sensors which are connected to digital pins
  irSensorValue1 = digitalRead(irSensorPin1);
  irSensorValue2 = digitalRead(irSensorPin2);
  irSensorValue3 = digitalRead(irSensorPin3);
  irSensorValue4 = digitalRead(irSensorPin4);

  // Check and send status of each parking slot in real time
  checkAndSendSlotStatus(irSensorValue1, "1");
  checkAndSendSlotStatus(irSensorValue2, "2");
  checkAndSendSlotStatus(irSensorValue3, "3");

  // Check if obstacle is detected by IR sensor 4 i.e. gate
  if (irSensorValue4 == HIGH) { 
    Serial.println("No Entry detected");
    bluetooth.println("No Entry detected");
  } 
  else {
    Serial.println("Entry detected");
    bluetooth.println("Entry detected");
    
    myServo.attach(10); // Attach servo to control gate
    delay(2000);  

    check(); //optional function call

    //open gate slowly
    for (int angle = 80; angle >= 0; angle--) {
      myServo.write(angle);
      delay(40);
    }

    //keep gate open until the vehicle is waiting at gate
    while (irSensorValue4 != HIGH) {
      irSensorValue4 = digitalRead(irSensorPin4); // Do nothing and keep checking irSensorValue4
      check();
      delay(100); // Adjust delay as needed
    }

    //close gate slowly
    delay(2000);
    for (int angle = 0; angle <= 80; angle++) {
      myServo.write(angle);
      delay(40);
    }
    myServo.detach(); // Detach servo to save power
  }

  check(); //optional function call
  delay(500); // refresh frequency (500 ms)
  
  // separator for every reading
  //Serial.println("________________________");
  bluetooth.println("________________________"); 

  // Receive messages from Bluetooth slave
  String receivedMessage = "";
  while (bluetooth.available() > 0) {
    char receivedChar = bluetooth.read();
    check(); //optional function call
    if (receivedChar == '\n') {
      Serial.print("Received from slave: ");
      Serial.println(receivedMessage);
      receivedMessage = "";
    } 
    else {
      receivedMessage += receivedChar;
      Serial.print("Received from slave (else): ");
      Serial.println(receivedMessage);
    }
  }
}


// Function to check and send status of the parking slots and
// prints slot information in serial monitor which is then 
// read by the python program running in the background 
// and display information in the flask web app

void checkAndSendSlotStatus(int irSensorValue, const char* slotName) {
  if (irSensorValue == HIGH) {
    Serial.print("Empty "); 
    Serial.println(slotName);

    bluetooth.print("Slot Empty at Slot ");
    bluetooth.println(slotName);
  } 
  else {
    Serial.print("Parked ");
    Serial.println(slotName);

    bluetooth.print("Vehicle Parked at Slot ");
    bluetooth.println(slotName);
  }
}

//check for parking lot slot status
void check(){
  irSensorValue1 = digitalRead(irSensorPin1);
  irSensorValue2 = digitalRead(irSensorPin2);
  irSensorValue3 = digitalRead(irSensorPin3);

  checkAndSendSlotStatus(irSensorValue1, "1");
  checkAndSendSlotStatus(irSensorValue2, "2");
  checkAndSendSlotStatus(irSensorValue3, "3");
}

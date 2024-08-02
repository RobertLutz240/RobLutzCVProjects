#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>
#include <Servo.h>
#include <Stepper.h> 
 
Servo pitchServo;
Servo rollServo;
Servo contServo;

const int buttonPin = 11;  // stepper code the number of the pushbutton pin
int buttonState = 0;  // stepper code variable for reading the pushbutton status
int cam = 0; // stepper code

const int stepsPerRevolution = 2038;  // stepper code. change this to fit the number of steps per revolution
 
float q0;
float q1;
float q2;
float q3;
 
float rollTarget=0;
float rollActual;
float rollError;
float rollServoVal=90;
 
float pitchTarget=0;
float pitchActual;
float pitchError;
float pitchServoVal=90;

float contServoGo = 0;
 
#define BNO055_SAMPLERATE_DELAY_MS (100)
 
Adafruit_BNO055 myIMU = Adafruit_BNO055();

Stepper myStepper(stepsPerRevolution, 7, 9, 8, 10); // stepper code

void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
myStepper.setSpeed(10); // stepper code
pinMode(buttonPin, INPUT); //stepper code for button
myIMU.begin();
delay(1000);
int8_t temp=myIMU.getTemp();
myIMU.setExtCrystalUse(true);
rollServo.attach(4);
pitchServo.attach(5);
contServo.attach(6);

 
rollServo.write(90);
delay(20);
pitchServo.write(90);
delay(20);

while (cam == 0){  // stepper zeroing initizalization loop
  buttonState = digitalRead(buttonPin);
  myStepper.step(1);
  delay(3);
  if (buttonState == HIGH) {
    cam = 1;
    Serial.print("button pressed, cam set to 1");
  }  // end stepper initialization loop
}
} 
void loop() {
  // put your main code here, to run repeatedly:
uint8_t system, gyro, accel, mg = 0;
myIMU.getCalibration(&system, &gyro, &accel, &mg);
 
imu::Quaternion quat=myIMU.getQuat();
 
q0=quat.w();
q1=quat.x();
q2=quat.y();
q3=quat.z();
 
rollActual=atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2));
pitchActual=asin(2*(q0*q2-q3*q1));
 
rollActual=rollActual/(2*3.141592654)*360;
pitchActual=pitchActual/(2*3.141592654)*360;
 
rollError=rollTarget-rollActual;
pitchError=pitchTarget-pitchActual;

for (int i = 0; i < 10; i++) {
contServo.write(1);
delay(20);
}

if (abs(pitchError)>1.5){
  pitchServoVal=pitchServoVal+pitchError/2;
  pitchServo.write(pitchServoVal);
  delay(20);
}
 
 
if (abs(rollError)>1.5){
  rollServoVal=rollServoVal+rollError/2;
  rollServo.write(rollServoVal);
  delay(20);
}
 
Serial.print(rollTarget);
Serial.print(",");
Serial.print(rollActual);
Serial.print(",");
Serial.print(pitchTarget);
Serial.print(",");
Serial.print(pitchActual);
Serial.print(",");
Serial.print(accel);
Serial.print(",");
Serial.print(gyro);
Serial.print(",");
Serial.print(mg);
Serial.print(",");
Serial.println(system);
 
delay(BNO055_SAMPLERATE_DELAY_MS);
}
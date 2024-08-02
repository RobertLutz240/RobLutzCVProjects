
#include <Joystick.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

#define BNO055_SAMPLERATE_DELAY_MS (100)
Joystick_ Joystick;

int JoystickX; // joystick
int JoystickY; //joystick
int JoystickZ; //joystick


float q0; //IMU
float q1; //IMU
float q2; ///IMU
float q3; //IMU

float pitch;
float yaw;
float roll;

Adafruit_BNO055 myIMU = Adafruit_BNO055();

void setup() {
  // put your setup code here, to run once:

//Initialize IMU
Serial.begin(115200);
myIMU.begin();
delay(1000);
int8_t temp=myIMU.getTemp();
myIMU.setExtCrystalUse(true);

// Initialize Joystick Library
  Joystick.begin();
  Joystick.setXAxisRange(0, 1024); 
  Joystick.setYAxisRange(0, 1024);
  Joystick.setZAxisRange(0, 1024);

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

//Calculate Quaternion Angles
yaw=-atan2(2*(q0*q3+q1*q2),1-2*(q2*q2+q3*q3))-3.14/2;
pitch=-asin(2*(q0*q2-q3*q1));
roll=-atan2(2*(q0*q1+q2*q3),1-2*(q1*q1+q2*q2));

// Read Joystick
  JoystickX = 512*roll+512; // Hall effect sensor connects to this analog pin
  JoystickY = 512*pitch+512; // Hall effect sensor connects to this analog pin

// Read Rudder Pedals
  JoystickZ = -1*((512*yaw+512)/2); // Hall effect sensor connects to this analog pin

// Output Controls
  Joystick.setXAxis(JoystickX);
  Joystick.setYAxis(JoystickY);
  Joystick.setZAxis(JoystickZ);
  Joystick.sendState();

Serial.print(pitch);
Serial.print(",");
Serial.print(roll);
Serial.print(",");
Serial.println(yaw);
//Serial.print(q0);
//Serial.print(",");
//Serial.print(q1);
//Serial.print(",");
//Serial.print(q2);
//Serial.print(",");
//Serial.print(q3);
//Serial.print(",");
//Serial.print(accel);
//Serial.print(",");
//Serial.print(gyro);
//Serial.print(",");
//Serial.print(mg);
//Serial.print(",");
//Serial.println(system);
 
delay(BNO055_SAMPLERATE_DELAY_MS);
}
// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

 
#include <AFMotor.h>

// Connect a stepper motor with 48 steps per revolution (7.5 degree)
// to motor port #2 (M3 and M4)
AF_Stepper motor_a(360, 1);
AF_Stepper motor_b(360, 2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");

  motor_a.setSpeed(30);  // 10 rpm   
  motor_b.setSpeed(30);
}

// the loop routine runs over and over again forever:
void loop(){
  if (Serial.available()){
char val = Serial.read();
Serial.println(val); 
if (val > 0){
}
if (val == 'i'){
for (int i=0; i<3; i += 1) {
  motor_a.step(2, BACKWARD, MICROSTEP); 
  motor_b.step(2, BACKWARD, MICROSTEP); 
  motor_a.step(2, BACKWARD, MICROSTEP); 
  motor_b.step(2, BACKWARD, MICROSTEP); 

 }
}
if (val == 'j'){
 for(int i=0; i<3; i += 1) {
  motor_a.step(2, FORWARD, MICROSTEP); 
  motor_b.step(2, FORWARD, MICROSTEP); 
  motor_a.step(2, FORWARD, MICROSTEP); 
  motor_b.step(2, FORWARD, MICROSTEP); 
 }

}


}
}


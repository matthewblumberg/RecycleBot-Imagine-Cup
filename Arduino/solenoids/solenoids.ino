/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;
int relay_one = 9;
// relay_one is the left relay
int relay_two = 8;
int relay_three = 11;
int relay_four = 12;
int buttonPin = 10;
int sensorPin = A0;


char noneFound = Serial.read();

// the setup routine runs once when you press reset:
void setup() {                
   //digitalWrite(relay_one, HIGH);
  // initialize the digital pin as an output.
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(relay_one, OUTPUT);
  pinMode(relay_two, OUTPUT);
  pinMode(relay_three, OUTPUT);
  pinMode(relay_four, OUTPUT);
  pinMode(sensorPin, INPUT);
  Serial.println("Ready"); 
    digitalWrite(relay_one, LOW);
    digitalWrite(relay_two, LOW);  
  
}

// the loop routine runs over and over again forever:
void loop(){
  int lightLevel = analogRead(sensorPin);
 
if (lightLevel >= 550){
   Serial.println(1);
}
else if (lightLevel >= 400){
   Serial.println(2);
}
else{
   Serial.println(0);
}
  if (Serial.available()){ 
char val = Serial.read();
//Serial.println(val); 


if (val > 0){
}
if (val == 'e'){
  //close the left solenoid
digitalWrite(relay_one, HIGH);
//delay(1000);
}
if (val == 'f'){
  //open the left solenoid
  digitalWrite(relay_one, LOW);
//  delay(50);
}

if (val == 'g'){
  //close the right solenoid
digitalWrite(relay_two, HIGH);
//delay(1000);
}
if (val == 'h'){
  //open the right solenoid
  digitalWrite(relay_two, LOW);
//  delay(50);
}
}
}


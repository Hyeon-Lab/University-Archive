#include <Servo.h>

Servo servo;

int motor = 2;

void setup() {
  Serial.begin(9600);
  servo.attach(motor);
  servo.write(0);
}

void loop() {
  if(Serial.available()>0){
    char u=Serial.read();
    if(u=='1') servo.write(30);
    if(u=='2') servo.write(90);
    if(u=='3') servo.write(150);
    delay(100);
  }
  
}

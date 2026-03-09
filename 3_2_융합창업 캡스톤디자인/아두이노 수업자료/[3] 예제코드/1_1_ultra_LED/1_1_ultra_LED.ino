#include <Servo.h>

Servo servo;

int motor = 2;
int trig=10;
int echo=11;

void setup()
{
  Serial.begin(9600);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);
  servo.attach(motor);
}

void loop() {
 
  digitalWrite(trig, HIGH);
  delay(50);
  digitalWrite(trig, LOW);
  
  int distance = pulseIn(echo, HIGH)*17/1000;
  
  Serial.print(distance);
  Serial.print("cm");
  Serial.println();

  if (distance>=0 & distance <=10){
  servo.write(90);
  delay(2000);
    }
    
  else if (distance>10 & distance <=20){
  servo.write(0);
  delay(2000);
  }
  
  else if (distance >20){
  servo.write(180);
  delay(2000);
  
    }
   }

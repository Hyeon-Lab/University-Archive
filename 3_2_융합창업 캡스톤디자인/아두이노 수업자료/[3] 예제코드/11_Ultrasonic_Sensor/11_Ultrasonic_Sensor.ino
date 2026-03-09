//#include <Servo.h>
//Servo servo;
//int motor = 2;
int echo = 7;
int trig = 8;
//int Red = 12;
//int Yellow = 11;
//int Blue = 10;

void setup() { 
 // servo.attach(motor);
  Serial.begin(9600);
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  //pinMode(Red, OUTPUT);
  //pinMode(Yellow, OUTPUT);
  //pinMode(Blue, OUTPUT);
  }

void loop() {
  long duration, distance;
  digitalWrite(trig, HIGH);
  delay(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = ((float)(340 * duration) / 1000) / 2;
  Serial.print("Distance : ");
  Serial.print(distance);
  Serial.println("mm");
  
 //   if (distance>=0 & distance <=50){
 // digitalWrite(Red, HIGH);
 //   servo.write(90);
 // delay(1000);
 // digitalWrite(Red, LOW);
 //   }
 // else if (distance>50 & distance <=100){
 // digitalWrite(Yellow, HIGH);
 //   servo.write(120);
 // delay(1000);
 //   digitalWrite(Yellow, LOW);
 // else if (distance >100){
 // digitalWrite(Blue, HIGH);
 //   servo.write(180);
    delay(1000);
//      digitalWrite(Blue, LOW);  
//  }
}

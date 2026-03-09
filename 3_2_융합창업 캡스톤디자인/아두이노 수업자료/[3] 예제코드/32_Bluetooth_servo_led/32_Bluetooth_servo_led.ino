#include <SoftwareSerial.h>
#include <Servo.h>
Servo servo;
int motor = 2;
#define BT_RXD 8
#define BT_TXD 7
SoftwareSerial bluetooth(BT_RXD, BT_TXD);
int blue = 10;
int yellow = 11;
int red = 12;

void setup() {
  bluetooth.begin(9600);
  servo.attach(motor);
  servo.write(0);
  pinMode(blue, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);
}

void loop(){
  if(bluetooth.available()){
  char bt = bluetooth.read();
  if (bt=='a'){ servo.write(60);
  digitalWrite(blue, HIGH);
  delay(1000);
  digitalWrite(blue, LOW);
  }
  if(bt=='b') {servo.write(120);
    digitalWrite(yellow, HIGH);
  delay(1000);
  digitalWrite(yellow, LOW);
  }  
  if(bt=='c') {servo.write(180);
     digitalWrite(red, HIGH);
  delay(1000);
  digitalWrite(red, LOW);
  }  
  }
  
}

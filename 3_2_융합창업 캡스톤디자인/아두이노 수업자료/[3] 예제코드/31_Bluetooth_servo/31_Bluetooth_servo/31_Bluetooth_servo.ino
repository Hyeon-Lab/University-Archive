#include <SoftwareSerial.h>
#include <Servo.h>
Servo servo;
int motor = 2;
#define BT_RXD 8
#define BT_TXD 7
SoftwareSerial bluetooth(BT_RXD, BT_TXD);


void setup() {
  bluetooth.begin(9600);
  servo.attach(motor);
  servo.write(0);
}

void loop(){
  if(bluetooth.available()){
  char bt = bluetooth.read();
  if(bt=='a') servo.write(60);
  if(bt=='b') servo.write(120);  
  if(bt=='c') servo.write(180);
 
  }
  
}

#include <SoftwareSerial.h>

#define BT_RXD 8
#define BT_TXD 7
SoftwareSerial bluetooth(BT_RXD, BT_TXD);
int blue = 10;
int yellow = 11;
int red = 12;

void setup() {
  bluetooth.begin(9600);
  pinMode(blue, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);
}

void loop(){
  if(bluetooth.available()){
  char bt;
  bt = bluetooth.read();
  if(bt=='a') digitalWrite(blue, HIGH);
  if(bt=='b') digitalWrite(blue, LOW);  
  if(bt=='c') digitalWrite(yellow, HIGH);
  if(bt=='d') digitalWrite(yellow, LOW);
  if(bt=='e') digitalWrite(red, HIGH);
  if(bt=='f') digitalWrite(red, LOW);  
  }
  
}

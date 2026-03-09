#include <IRremote.h>
#include <Servo.h>

int RECV_PIN = A0;
int motor = 2;
bool on_off = false;
bool flag = false;
int button = 13;

Servo servo;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn();
  pinMode(2, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  servo.attach(motor);
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    if(results.value != 0xFFFFFFFF){
     if(on_off == true) {
      on_off = false;
    }
    else {
      on_off = true;
    } 
    }
    irrecv.resume();
  }

  if(digitalRead(button) == LOW){
    if(flag == false) {
      flag = true;
    }
    else{
      if(on_off == true) {
        on_off = false;
      }
      else {
        on_off = true;
      } 
      flag = false;
    }
  }

  if(on_off == true) {
    //servo.write(90);
    Serial.println("on");
    //delay(2000);
  }
  else {
    //servo.write(0);
    Serial.println("off");
    //delay(2000);
  }
  
  delay(100);
}

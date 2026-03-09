#include <IRremote.h>

int RECV_PIN = A0;

IRrecv irrecv(RECV_PIN);
decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn();
  pinMode(2, OUTPUT);
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
   
   switch (results.value) {
        case 0xFF9867: digitalWrite(2, HIGH); break;
        case 0xFFA25D: digitalWrite(2, LOW); break;
      }
      
    irrecv.resume();
  }
  delay(100);
}

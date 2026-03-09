#include <Servo.h>

Servo servo;

int motor = 2;

void setup() {
  servo.attach(motor);
}

void loop() {
  servo.write(90);
  delay(2000);
  servo.write(180);
  delay(2000);
}

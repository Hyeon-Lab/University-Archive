#include<Stepper.h>

const int stepsPerRevolution = 64;

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

void setup() {
  myStepper.setSpeed(220);
}

void loop() {
  int sensorReading = analogRead(0);
  
  if (sensorReading < 300)
    myStepper.step(1);
  if (sensorReading > 800)
    myStepper.step(-1);
}

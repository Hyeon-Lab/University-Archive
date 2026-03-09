int GasPin = A0;
int Buzzer_Pin = 8;

void setup() {
  pinMode(GasPin, INPUT);
  pinMode(Buzzer_Pin, OUTPUT);
}

void loop() {
  int Gas = analogRead(GasPin);

  if(Gas < 600)
    tone(Buzzer_Pin, 523);
  if(Gas > 600)
    tone(Buzzer_Pin, 659);

  delay(1000);
}

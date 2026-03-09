int GasPin = A0;

void setup() {
  pinMode(GasPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int Gas = analogRead(GasPin);

  Serial.println(Gas);

  delay(1000);
}

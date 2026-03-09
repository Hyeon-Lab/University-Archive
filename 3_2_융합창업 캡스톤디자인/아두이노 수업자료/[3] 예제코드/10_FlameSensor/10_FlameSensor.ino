int flame = A0;
int buzzer = 8;

void setup() {
  Serial.begin(9600);
  pinMode(flame, INPUT);
  pinMode(buzzer, OUTPUT);
}

void loop() {
  int val = analogRead(flame);

  Serial.print("flame_sensor : ");
  Serial.println(val);

  if(val < 1023) {
    digitalWrite(buzzer, HIGH);
    Serial.println("FIRE!!!");
  }

  else {
    digitalWrite(buzzer, LOW);
    Serial.println("No Fire");
  }

  delay(200);
}

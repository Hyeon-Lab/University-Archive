int sensor = 8;

void setup() {
  Serial.begin(9600);
  pinMode(sensor, INPUT);
}

void loop() {
  int val = digitalRead(sensor);

  Serial.println(val);

  delay(1000);
}

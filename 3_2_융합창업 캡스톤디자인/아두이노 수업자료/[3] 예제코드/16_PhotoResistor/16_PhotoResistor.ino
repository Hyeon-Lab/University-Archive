int CDS = A0;
int LED = 7;

void setup() {
  Serial.begin(9600);
  pinMode(CDS, INPUT);
  pinMode(LED,OUTPUT);
}

void loop() {
  int val = analogRead(CDS);
  Serial.print("CDS_Sensor: ");
  Serial.println(val);

  if(val > 500) {
    digitalWrite(LED, HIGH);
    Serial.println("LED ON");
  }

  else {
    digitalWrite(LED, LOW);
    Serial.println("LED OFF");
  }

  delay(1000);
}

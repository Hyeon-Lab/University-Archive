float temperature;  

int reading;  
int lm35Pin = A0;

void setup()
{
  analogReference(INTERNAL);
  Serial.begin(9600);
  delay(5000);
}

void loop()
{
  reading = analogRead(lm35Pin);
  float voltage = reading*5.0;
  voltage /= 1024.0;
  temperature = reading / 9.31;
  Serial.print(temperature); Serial.println(" degrees C");
  delay(1000);
}

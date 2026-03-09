int Joy_x = A0;    
int Joy_y = A1;
int Joy_z = A2;

void setup()
{
  pinMode(Joy_z,INPUT_PULLUP);
  Serial.begin(9600);
}
 
void loop()
{
  int x = analogRead(Joy_x);
  int y = analogRead(Joy_y);
  int z = digitalRead(Joy_z); 
  Serial.print("X: ");
  Serial.print(x);
  Serial.print("  Y: ");
  Serial.print(y);

  if( z == 0 )
    Serial.println("    Pressed");
  else
    Serial.println("    Nothing");
  delay(500);
}

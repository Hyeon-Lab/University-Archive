int redPin = 10;
int greenPin = 11;
int bluePin = 12;
 
void setup()
{
 pinMode(redPin, OUTPUT);
 pinMode(greenPin, OUTPUT);
 pinMode(bluePin, OUTPUT); 
}
 
void loop()
{
  setColor(0, 255, 255); // red
  delay(1000); 
  setColor(255, 0, 255); // green
  delay(1000);  
  setColor(255, 255, 0); // blue
  delay(1000);
  setColor(0, 0, 255); // yellow
  delay(1000);
  setColor(0, 255, 0); // purple
  delay(1000);
  setColor(255, 0, 0); // aqua
  delay(1000);
  setColor(0, 0, 0); // white
  delay(1000);
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue); 
}

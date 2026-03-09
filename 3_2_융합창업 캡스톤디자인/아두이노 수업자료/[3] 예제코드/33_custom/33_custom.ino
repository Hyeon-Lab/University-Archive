#include <DHT.h>
#define DHTPIN A1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);     // 접근주소: 0x3F or 0x27

int redPin = 10;
int greenPin = 11;
int bluePin = 12;

void setup(){
  lcd.init();
  lcd.backlight();
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT); 
}

void loop(){
  int h = dht.readHumidity();
  int t = dht.readTemperature();

  lcd.setCursor(0,0);
  lcd.print("humidity: ");
  lcd.print(h);
  lcd.setCursor(0,1);
  lcd.print("temperature: ");
  lcd.print(t);
  
  if(t>=26) {
  setColor(0,255,255);
  delay(1000);
 }
 else if(t<20) {
  setColor(255,255,0);
  delay(1000);
 }
 else if(t<26,t>=20) {
  setColor(255,0,255);
  delay(1000);
 }
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue); 
}

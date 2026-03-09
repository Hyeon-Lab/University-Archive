#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); // 접근주소: 0x3F or 0x27
#include <DHT.h> //15번코드
#define DHTPIN A1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int redPin = 10; //2번코드
int greenPin = 11;
int bluePin = 9;
int Buzzer = 7; //7번코드

void setup()
{
  lcd.init();
  lcd.backlight();
   pinMode(redPin, OUTPUT);
 pinMode(greenPin, OUTPUT);
 pinMode(bluePin, OUTPUT); 
   pinMode(Buzzer, OUTPUT);

}

void loop()
{
  int h = dht.readHumidity();
  int t = dht.readTemperature();
  lcd.setCursor(0,0);
  lcd.print("humidity: ");lcd.print(h);lcd.print("%");
  lcd.setCursor(0,1);
  lcd.print("temperature: ");lcd.print(t);lcd.print("C");
  
  if(t>=26){
    setColor(0, 255, 255); // 2번코드
    tone(Buzzer, 523);
    delay(1000); 
  }
  if(t<20){
  setColor(255, 255, 0); // blue
    tone(Buzzer, 659);
  delay(1000);  
  }
  if(t<26, t>20) {
      setColor(255, 0, 255); // green
      noTone(Buzzer);
  delay(1000);  
    
  }
}

void setColor(int red, int green, int blue) //2번 코드
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue); 
}

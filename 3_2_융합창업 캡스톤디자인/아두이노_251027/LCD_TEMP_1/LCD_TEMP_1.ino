#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); // 접근주소: 0x3F or 0x27
#include <DHT.h>
#define DHTPIN A1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  lcd.init();
  lcd.backlight();

}

void loop()
{
  int h = dht.readHumidity();
  int t = dht.readTemperature();
  lcd.setCursor(0,0);
  lcd.print("humidity: ");lcd.print(h);lcd.print("%");
  lcd.setCursor(0,1);
  lcd.print("temperature: ");lcd.print(t);lcd.print("C");
  delay(1000);
}

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);
int ledPin = 8;
int inputPin = 7;
int val = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(inputPin, INPUT);
    lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Hello, world!");
  lcd.setCursor(0,1);
  lcd.print("Enjoy - Eduino");
  Serial.begin(9600);
}

void loop() {
  val = digitalRead(inputPin);

  if (val == HIGH) {
    digitalWrite(ledPin, HIGH);
    Serial.println("Welcome!");
    lcd.setCursor(0,0);
    lcd.print("Hello, world!");
  }
  else {
    digitalWrite(ledPin, LOW);
    Serial.println("Nothing");
      lcd.setCursor(0,0);
  lcd.print("Nothing");
  }

  delay(1000);
}

#include <RTClib.h>
RTC_DS3231 rtc;
char DOW[7][12]={"sun", "Mon", "Tue", "Wed", "thu", "fri", "sat"};
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

void setup()
{
  lcd.init();
  lcd.backlight();
  rtc.begin();
}

void loop(){
   DateTime now = rtc.now();
   lcd.clear();
   
   lcd.setCursor(0,0);
   lcd.print(now.year(), DEC);
   lcd.print("/");
   lcd.print(now.month(), DEC);
   lcd.print("/");
   lcd.print(now.day(), DEC);
   lcd.print("/");
   lcd.print(DOW[now.dayOfTheWeek()]);
   lcd.print("/");

   lcd.setCursor(0,1);
   lcd.print(now.hour(), DEC);
   lcd.print(":");
   lcd.print(now.minute(), DEC);
   lcd.print(":");
   lcd.print(now.second(), DEC);
   lcd.print("  ");
   lcd.print(int(rtc.getTemperature()));
   lcd.print(char(223));
   lcd.print("C");
   delay(1000);

   
   }

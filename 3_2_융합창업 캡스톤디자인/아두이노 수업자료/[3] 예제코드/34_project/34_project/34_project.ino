#include <IRremote.h>
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RtcDS3231.h>
RtcDS3231<TwoWire> Rtc(Wire);
LiquidCrystal_I2C lcd(0x27,16,2);     // 접근주소: 0x3F or 0x27

int RECV_PIN = A0;
int motor = 2;
bool on_off = false;
bool flag = false;
int button = 13;

Servo servo;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn();
  pinMode(2, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  servo.attach(motor);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("power on");
  Rtc.Begin();
  on_off = false;
  servo.write(0);

    RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
    printDateTime(compiled);
    Serial.println();

    if (!Rtc.IsDateTimeValid()) 
    {
        if (Rtc.LastError() != 0)
        {
            // we have a communications error
            // see https://www.arduino.cc/en/Reference/WireEndTransmission for 
            // what the number means
            Serial.print("RTC communications error = ");
            Serial.println(Rtc.LastError());
        }
        else
        {
            // Common Causes:
            //    1) first time you ran and the device wasn't running yet
            //    2) the battery on the device is low or even missing

            Serial.println("RTC lost confidence in the DateTime!");

            // following line sets the RTC to the date & time this sketch was compiled
            // it will also reset the valid flag internally unless the Rtc device is
            // having an issue

            Rtc.SetDateTime(compiled);
        }
    }

    if (!Rtc.GetIsRunning())
    {
        Serial.println("RTC was not actively running, starting now");
        Rtc.SetIsRunning(true);
    }

    RtcDateTime now = Rtc.GetDateTime();
    if (now < compiled) 
    {
        Serial.println("RTC is older than compile time!  (Updating DateTime)");
        Rtc.SetDateTime(compiled);
    }
    else if (now > compiled) 
    {
        Serial.println("RTC is newer than compile time. (this is expected)");
    }
    else if (now == compiled) 
    {
        Serial.println("RTC is the same as compile time! (not expected but all is fine)");
    }

    // never assume the Rtc was last configured by you, so
    // just clear them to your needed state
    Rtc.Enable32kHzPin(false);
    Rtc.SetSquareWavePin(DS3231SquareWavePin_ModeNone); 
}

void loop() {
  if (!Rtc.IsDateTimeValid()) 
    {
        if (Rtc.LastError() != 0)
        {
            // we have a communications error
            // see https://www.arduino.cc/en/Reference/WireEndTransmission for 
            // what the number means
            Serial.print("RTC communications error = ");
            Serial.println(Rtc.LastError());
        }
        else
        {
            // Common Causes:
            //    1) the battery on the device is low or even missing and the power line was disconnected
            Serial.println("RTC lost confidence in the DateTime!");
        }
    }
    
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    if(results.value == 0xFF38C7){
     if(on_off == true) {
      on_off = false;
      servo.write(0);
      //delay(2000);
      Serial.println("off");
      lcd.setCursor(0,0);
      //lcd.clear();
      lcd.print("off             ");
    }
    else {
      on_off = true;
      servo.write(90);
      //delay(2000);
      Serial.println("on");
      lcd.setCursor(0,0);
      //lcd.clear();
      lcd.print("on             ");
    } 
    }
    irrecv.resume();
  }

  if(digitalRead(button) == LOW){
    if(flag == false) {
      flag = true;
    }
    else{
      if(on_off == true) {
        on_off = false;
        servo.write(0);
        //delay(2000);
        Serial.println("off");
        lcd.setCursor(0,0);
        //lcd.clear();
        lcd.print("off             ");
        delay(500);
      }
      else {
        on_off = true;
        servo.write(90);
        //delay(2000);
        Serial.println("on");
        lcd.setCursor(0,0);
        //lcd.clear();
        lcd.print("on             ");
        delay(500);
      } 
      flag = false;
    }
  }

  RtcDateTime now = Rtc.GetDateTime();
  printDateTime(now);
  Serial.println();

  RtcTemperature temp = Rtc.GetTemperature();
  temp.Print(Serial);
  // you may also get the temperature as a float and print it
    // Serial.print(temp.AsFloatDegC());
    Serial.println("C");
}

#define countof(a) (sizeof(a) / sizeof(a[0]))

void printDateTime(const RtcDateTime& dt)
{
    char datestring[20];

    snprintf_P(datestring, 
            countof(datestring),
            PSTR("%02u/%02u/%04u %02u:%02u:%02u"),
            dt.Month(),
            dt.Day(),
            dt.Year(),
            dt.Hour(),
            dt.Minute(),
            dt.Second() );
    Serial.print(datestring);
    lcd.setCursor(0,1);
    lcd.print(datestring);
    
}

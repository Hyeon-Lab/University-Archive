#define TRIG 7 //TRIG 핀 설정 (초음파 보내는 핀)
#define ECHO 8 //ECHO 핀 설정 (초음파 받는 핀)


void setup() {
  Serial.begin(9600); 

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

}

void loop()

{
  long duration, distance;

  digitalWrite(TRIG, LOW);
  delay(1000);
  digitalWrite(TRIG, HIGH);
  delay(1000);
  digitalWrite(TRIG, LOW);

  duration = pulseIn (ECHO, HIGH);
  distance = duration * 17 / 1000;

  Serial.println(duration );
  Serial.print("\nDIstance : ");
  Serial.print(distance);
  Serial.println(" Cm");

  delay(1000);

}

int position_pin[] = {13,10,9,2};
int segment_pin[]  = {12,8,4,6,7,11,3,5};

const int delay_time = 5;
 
int potentiometer = A0;
 
byte data[] = {0xFC, 0x60, 0xDA, 0xF2, 0x66, 0xB6, 0xBE, 0xE4, 0xFE, 0xE6};

void setup() {  
  for (int i = 0; i < 4; i++)
    pinMode(position_pin[i], OUTPUT);

  for (int i = 0; i < 8; i++)
    pinMode(segment_pin[i], OUTPUT);

  Serial.begin(9600);
}

void loop() {
  int a = analogRead(potentiometer);

  int num1 = a / 1000;
  int num2 = (a % 1000) / 100;
  int num3 = (a % 100) / 10;
  int num4 = a % 10;

  show(1, num1);
  delay(delay_time);
  show(2, num2);
  delay(delay_time);
  show(3, num3);
  delay(delay_time);
  show(4, num4);
  delay(delay_time);
}

void show(int position, int number) {
  for (int i = 0; i < 4; i++) {
    if (i + 1 == position) {
      digitalWrite(position_pin[i], HIGH);
    } else {
      digitalWrite(position_pin[i], LOW);
    }
  }

  for (int i = 0; i < 8; i++) {
    byte segment = (data[number] & (0x01 << i)) >> i;
    if (segment == 1) {
      digitalWrite(segment_pin[7 - i], LOW);
    } else {
      digitalWrite(segment_pin[7 - i], HIGH);
    }
  }
}

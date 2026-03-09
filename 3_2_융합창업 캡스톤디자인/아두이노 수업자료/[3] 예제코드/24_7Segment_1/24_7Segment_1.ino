int leds[] = {2, 3, 4, 5, 6, 7, 8, 9};
int led_num = 8;
int button = 13;
int num= 0;

int set_number[10][8] = {
  {0, 0, 0, 0, 0, 0, 1, 1},
  {1, 0, 0, 1, 1, 1, 1, 1},
  {0, 0, 1, 0, 0, 1, 0, 1},
  {0, 0, 0, 0, 1, 1, 0, 1},
  {1, 0, 0, 1, 1, 0, 0, 1},
  {0, 1, 0, 0, 1, 0, 0, 1},
  {0, 1, 0, 0, 0, 0, 0, 1},
  {0, 0, 0, 1, 1, 1, 1, 1},
  {0, 0, 0, 0, 0, 0, 0, 1},
  {0, 0, 0, 0, 1, 0, 0, 1}
};

void setup() {
  for (int i = 0 ; i < led_num ; i++) {
    pinMode(leds[i], OUTPUT);
  }

  pinMode(button, INPUT_PULLUP);
}

void loop() {

  if(digitalRead(button) == LOW){
    if(num == 9) num = 0;
    else num ++;
  }

  for (int j = 0 ; j < led_num ; j++) {
      digitalWrite(leds[j], set_number[num][j]);
  }

  delay(150);
}

#include <FrequencyTimer2.h>

byte col = 0;
byte leds[8][8];

int cols[8] = {9, 3, 2, 12, 15, 11, 7, 6};

int rows[8] = {13, 8, 17, 10, 5, 16, 4, 14};
 
void setup() {
  for (int i = 2; i <= 17; i++) {
    pinMode(i, OUTPUT);
  }

  for (int i = 0; i < 8; i++) {
    digitalWrite(cols[i], HIGH );
  }
  
  for (int i = 0; i < 8; i++) {
    digitalWrite(rows[i], HIGH);
  }
  
  FrequencyTimer2::setOnOverflow(display);    
}

void loop() {
  for(int i = 0; i < 8; i++) {
    for(int j = 0; j < 8; j++) {
      leds[i][j] = 1;
      delay(100);
    }
  }
  for(int i = 0; i < 8; i++) {
    for(int j = 0; j < 8; j++) {
      leds[i][j] = 0;
      delay(100);
    }
  }
}

void display() {
  digitalWrite(cols[col], HIGH);
  col++;
  if (col == 8) {
    col = 0;
  }
  for (int row = 0; row <= 7; row++) {
    if (leds[col][7 - row] == 1) {
      digitalWrite(rows[row], HIGH);
    }
    else {
      digitalWrite(rows[row], LOW);
    }
  }
  digitalWrite(cols[col], LOW);
}

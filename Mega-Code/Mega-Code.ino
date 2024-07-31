/* 
Written By Samriddh Bhatla
for project Lakshya 
*/
#define STPH_IN1 4
#define STPH_IN2 5
#define STPH_IN3 6
#define STPH_IN4 7
#define STPV_IN1 8
#define STPV_IN2 9
#define STPV_IN3 10
#define STPV_IN4 11
#define BTN_UP 34
#define BTN_DOWN 30
#define BTN_RIGHT 36
#define BTN_LEFT 32
#define LASER 48
#define LED_Green 46
#define LED_Red 44

int dBTN_UP=0, dBTN_DOWN=0, dBTN_RIGHT=0, dBTN_LEFT=0;
int steps_h=0, steps_v=0;
int b = '0';

unsigned long last_serial = 0;
unsigned long prev_red_blink = 0;
unsigned long delay_red = 300;
unsigned long now = 0;
unsigned long prev_green_blink = 0;
unsigned long delay_green = 400;

void setup() {
  pinMode(STPH_IN1, OUTPUT);
  pinMode(STPH_IN2, OUTPUT);
  pinMode(STPH_IN3, OUTPUT);
  pinMode(STPH_IN4, OUTPUT);
  pinMode(STPV_IN1, OUTPUT);
  pinMode(STPV_IN2, OUTPUT);
  pinMode(STPV_IN3, OUTPUT);
  pinMode(STPV_IN4, OUTPUT);
  pinMode(BTN_UP, INPUT);
  pinMode(BTN_DOWN, INPUT);
  pinMode(BTN_RIGHT, INPUT);
  pinMode(BTN_LEFT, INPUT);
  pinMode(LASER, OUTPUT);
  pinMode(LED_Green, OUTPUT);
  pinMode(LED_Red, OUTPUT);

  pinMode(50, OUTPUT);
  digitalWrite(50, HIGH);

  

  dBTN_UP = digitalRead(BTN_UP);
  dBTN_DOWN = digitalRead(BTN_DOWN);
  dBTN_RIGHT = digitalRead(BTN_RIGHT);
  dBTN_LEFT = digitalRead(BTN_LEFT);

  digitalWrite(LED_Red, HIGH);
  Serial.begin(9600);
  while(now<10000){
    //rotate code

    while(digitalRead(BTN_UP)){
      //to move up
      if(digitalRead(BTN_RIGHT))
        OneStepH(false);
      else if(digitalRead(BTN_LEFT))
        OneStepH(true);
      OneStepV(true);
      delay(2);
    }

    while(digitalRead(BTN_DOWN)){
      //to move down
      if(digitalRead(BTN_RIGHT))
        OneStepH(false);
      else if(digitalRead(BTN_LEFT))
        OneStepH(true);
      OneStepV(false);
      delay(2);
    }

    while(digitalRead(BTN_RIGHT)){
      //to move right
      if(digitalRead(BTN_UP))
        OneStepV(true);
      else if(digitalRead(BTN_DOWN))
        OneStepV(false);
      OneStepH(false);
      delay(2);
    }

    while(digitalRead(BTN_LEFT)){
      //to move left
      if(digitalRead(BTN_UP))
        OneStepV(true);
      else if(digitalRead(BTN_DOWN))
        OneStepV(false);
      OneStepH(true);
      delay(2);
    }

    allStop();
    now = millis();
    if(now-prev_red_blink>delay_red){
      prev_red_blink=now;
      digitalWrite(LED_Red, !digitalRead(LED_Red));
    }

    dBTN_UP = digitalRead(BTN_UP);
    dBTN_DOWN = digitalRead(BTN_DOWN);
    dBTN_RIGHT = digitalRead(BTN_RIGHT);
    dBTN_LEFT = digitalRead(BTN_LEFT);
  }
  digitalWrite(LED_Red, LOW);
  digitalWrite(LED_Green, LOW);
  digitalWrite(LASER, LOW);
  
}

void loop() {

  dBTN_UP = digitalRead(BTN_UP);
  dBTN_DOWN = digitalRead(BTN_DOWN);
  dBTN_RIGHT = digitalRead(BTN_RIGHT);
  dBTN_LEFT = digitalRead(BTN_LEFT);

  if(dBTN_UP+dBTN_DOWN+dBTN_RIGHT+dBTN_LEFT>0){
    digitalWrite(LED_Red, HIGH);
    digitalWrite(LED_Green, LOW);
    //manual override code

    while(digitalRead(BTN_UP)){
      //to move up
      if(digitalRead(BTN_RIGHT))
        OneStepH(false);
      else if(digitalRead(BTN_LEFT))
        OneStepH(true);
      OneStepV(true);
      delay(2);
    }

    while(digitalRead(BTN_DOWN)){
      //to move down
      if(digitalRead(BTN_RIGHT))
        OneStepH(false);
      else if(digitalRead(BTN_LEFT))
        OneStepH(true);
      OneStepV(false);
      delay(2);
    }

    while(digitalRead(BTN_RIGHT)){
      //to move right
      if(digitalRead(BTN_UP))
        OneStepV(true);
      else if(digitalRead(BTN_DOWN))
        OneStepV(false);
      OneStepH(false);
      delay(2);
    }

    while(digitalRead(BTN_LEFT)){
      //to move left
      if(digitalRead(BTN_UP))
        OneStepV(true);
      else if(digitalRead(BTN_DOWN))
        OneStepV(false);
      OneStepH(true);
      delay(2);
    }

    allStop();
    b='0';
    digitalWrite(LED_Green, LOW);

  }
  else{
    digitalWrite(LED_Red, LOW);
    digitalWrite(LED_Green, HIGH);
    //driver code
    while(1){
    delay(2);
    int temp = b;
    b=Serial.read();
    if(b==-1 || b==10)
      b=temp;
    dBTN_UP = digitalRead(BTN_UP);
    dBTN_DOWN = digitalRead(BTN_DOWN);
    dBTN_RIGHT = digitalRead(BTN_RIGHT);
    dBTN_LEFT = digitalRead(BTN_LEFT);
    if(dBTN_UP+dBTN_DOWN+dBTN_RIGHT+dBTN_LEFT>0)
      break;
    switch(b){
        case '0':
          allStop();
          break;
        case '1':
          OneStepV(true);
          break;
        case '2':
          OneStepV(false);
          break;
        case '3':
          OneStepH(true);
          break;
        case '4':
          OneStepH(false);
          break;
        case '5':
          OneStepV(true);
          OneStepH(true);
          break;
        case '6':
          OneStepV(true);
          OneStepH(false);
          break;
        case '7':
          OneStepV(false);
          OneStepH(false);
          break;
        case '8':
          OneStepV(false);
          OneStepH(true);
          break;
        default:
          break;
      }
    }
  }
}

void OneStepH(bool dir){

  if(dir){
    switch(steps_h){

      case 0:
      digitalWrite(STPH_IN1, HIGH);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, LOW);
      break;

      case 1:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, HIGH);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, LOW);
      break;

      case 2:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, HIGH);
      digitalWrite(STPH_IN4, LOW);
      break;

      case 3:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, HIGH);
      break;

    }
  }

  else{
    switch(steps_h){
      case 0:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, HIGH);
      break;

      case 1:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, HIGH);
      digitalWrite(STPH_IN4, LOW);
      break;

      case 2:
      digitalWrite(STPH_IN1, LOW);
      digitalWrite(STPH_IN2, HIGH);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, LOW);
      break;

      case 3:
      digitalWrite(STPH_IN1, HIGH);
      digitalWrite(STPH_IN2, LOW);
      digitalWrite(STPH_IN3, LOW);
      digitalWrite(STPH_IN4, LOW);
      break;
    } 
  }

  steps_h++;
  if(steps_h > 3){
    steps_h = 0;
  }
}

void OneStepV(bool dir){

  if(dir){
    switch(steps_v){

      case 0:
      digitalWrite(STPV_IN1, HIGH);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, LOW);
      break;

      case 1:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, HIGH);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, LOW);
      break;

      case 2:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, HIGH);
      digitalWrite(STPV_IN4, LOW);
      break;

      case 3:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, HIGH);
      break;

    }
  }
  
  else{
    switch(steps_v){

      case 0:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, HIGH);
      break;

      case 1:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, HIGH);
      digitalWrite(STPV_IN4, LOW);
      break;

      case 2:
      digitalWrite(STPV_IN1, LOW);
      digitalWrite(STPV_IN2, HIGH);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, LOW);
      break;

      case 3:
      digitalWrite(STPV_IN1, HIGH);
      digitalWrite(STPV_IN2, LOW);
      digitalWrite(STPV_IN3, LOW);
      digitalWrite(STPV_IN4, LOW);
      break;

    }
  }

  steps_v++;
  if(steps_v > 3){
    steps_v = 0;
  }
}

void allStop(){
  digitalWrite(STPH_IN1, LOW);
  digitalWrite(STPH_IN2, LOW);
  digitalWrite(STPH_IN3, LOW);
  digitalWrite(STPH_IN4, LOW);
  digitalWrite(STPV_IN1, LOW);
  digitalWrite(STPV_IN2, LOW);
  digitalWrite(STPV_IN3, LOW);
  digitalWrite(STPV_IN4, LOW);
}

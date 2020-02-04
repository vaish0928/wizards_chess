
#include <Servo.h>

Servo number;
Servo letter;
Servo magnet;
String data;
int dataArr [20];
String  dataArrstring;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  //pinMode(12, OUTPUT);
  number.attach(12);

  //pinMode(11, OUTPUT);
  letter.attach(8);

  //pinMode(13, OUTPUT);
  magnet.attach(13);

  magnet.write(-10); // move magnet down
  letter.write(78); // stopping for letter
  number.write(89); // stopping for number

  pinMode(LED_BUILTIN, OUTPUT); //make the LED pin (13) as output
  digitalWrite (LED_BUILTIN, LOW);
  
  pinMode(7, OUTPUT); //make the LED pin (13) as output
  digitalWrite (7, LOW);
}


//letter.write(78); // stopping for letter
//number.write(89); // stopping for number
  
int place_row = 0;
int place_col = 0;



void loop() {
  // put your main code here, to run repeatedly:
  //digitalWrite(right_pin, HIGH);
  magnet.write(-10); // move magnet down
  letter.write(78); // stopping for letter
  number.write(89); // stopping for number

  
  while (Serial.available() > 0){
    int n = Serial.available();
    dataArrstring = Serial.readString();
    Serial.println(dataArrstring);
    char carray[20];

    for (int j = 0; j < 20; j++) {
      //Serial.println(dataArrstring[j]);
      dataArr[j] = dataArrstring[j] - '0';
      //Serial.println(dataArr[j]);
    }
    

   int LetterDelayOneSpaceNoMag = 1000;
   int LetterDelayOneSpaceWithMag = 2000;

   int NumberDelayOneSpaceNoMag = 1000;
   int NumberDelayOneSpaceWithMag = 1400;

//
////  //Move to spot
    magnet.write(-10); // move magnet down

      //rows (numbers)
    if (dataArr[0] > 0) {
      number.write(98); //up
      delay(NumberDelayOneSpaceNoMag*dataArr[0]);
      number.write(89); // stopping for letter
      delay(1000);
    }
    else if (dataArr[0] < 0) {
      number.write(83); // down
      delay(NumberDelayOneSpaceNoMag*(0 - dataArr[0]));
      number.write(89); // stopping for letter
      delay(1000);
    }
      else {
        number.write(89); // stopping for number
      }

      //columns (letters)
    if (dataArr[1] > 0) { //move right
      letter.write(90); //up
      delay(LetterDelayOneSpaceNoMag*dataArr[1]);
      letter.write(78); // stopping for letter
      delay(1000);
    }
    else if (dataArr[1] < 0) { //move left
      letter.write(66); // down
      delay(LetterDelayOneSpaceNoMag*(0 - dataArr[1]));
      letter.write(78); // stopping for letter
      delay(1000);
    }
      else {
        letter.write(78); // stopping for letter
      }


  //magnet up
  magnet.write(100);
  delay(1000);
  


  //move the piece
  //rows (numbers)
  if (dataArr[2] > 0) {
    number.write(98); //up
    delay(NumberDelayOneSpaceWithMag*dataArr[2]);
    number.write(89); // stopping for letter
    delay(1000);
  }
  else if (dataArr[2] < 0) {
    number.write(83); // down
    delay(NumberDelayOneSpaceWithMag*(0 - dataArr[2]));
    number.write(89); // stopping for letter
    delay(1000);
  }
    else {
      number.write(89); // stopping for number
    }

      //columns (letters)
  if (dataArr[3] > 0) { //move right
    letter.write(90); //up
    delay(LetterDelayOneSpaceWithMag*dataArr[3]);
    letter.write(78); // stopping for letter
    delay(1000);
  }
  else if (dataArr[3] < 0) { //move left
    letter.write(66); // down
    delay(LetterDelayOneSpaceWithMag*(0 - dataArr[3]));
    letter.write(78); // stopping for letter
    delay(1000);
  }
    else {
      letter.write(78); // stopping for letter
  }
    
  //magnet down
  magnet.write(-10);
  delay(1000);
    
  }
}

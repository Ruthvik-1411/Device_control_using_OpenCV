const int led1=8;
const int led2=9;
const int led3=10;
const int led4=11;
const int dled=12;

int databyte;
bool c1=0,c2=0,c3=0,c4=0;

const int d1=4;
const int d2=5;
const int d3=6;
const int d4=7;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  pinMode(led4,OUTPUT);
  pinMode(dled,OUTPUT);
  pinMode(d1,OUTPUT);
  pinMode(d2,OUTPUT);
  pinMode(d3,OUTPUT);
  pinMode(d4,OUTPUT);
  digitalWrite(dled,LOW);
  digitalWrite(d1,HIGH);
  digitalWrite(d2,HIGH);
  digitalWrite(d3,HIGH);
  digitalWrite(d4,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    databyte=Serial.read();
    //Selection
    if(databyte=='1'){
      digitalWrite(led1,HIGH);
      digitalWrite(led2,LOW);
      digitalWrite(led3,LOW);
      digitalWrite(led4,LOW);
    }
    else if(databyte=='2'){
      digitalWrite(led1,HIGH);
      digitalWrite(led2,HIGH);
      digitalWrite(led3,LOW);
      digitalWrite(led4,LOW);
    }
    else if(databyte=='3'){
      digitalWrite(led1,HIGH);
      digitalWrite(led2,HIGH);
      digitalWrite(led3,HIGH);
      digitalWrite(led4,LOW);
    }
    else if(databyte=='4'){
      digitalWrite(led1,HIGH);
      digitalWrite(led2,HIGH);
      digitalWrite(led3,HIGH);
      digitalWrite(led4,HIGH);
    }
    else if(databyte=='0'){
      digitalWrite(led1,HIGH);
      digitalWrite(led2,HIGH);
      digitalWrite(led3,HIGH);
      digitalWrite(led4,HIGH);
      delay(300);
      digitalWrite(led1,LOW);
      digitalWrite(led2,LOW);
      digitalWrite(led3,LOW);
      digitalWrite(led4,LOW);
    }
    if(databyte=='a'){
      confirmation();
      if(c1==0){
        digitalWrite(d1,LOW);
        c1=1;
      }
      else if(c1==1){
        digitalWrite(d1,HIGH);
        c1=0;
      }
    }
    else if(databyte=='b'){
      confirmation();
      if(c2==0){
        digitalWrite(d2,LOW);
        c2=1;
      }
      else if(c2==1){
        digitalWrite(d2,HIGH);
        c2=0;
      }
    }
    else if(databyte=='c'){
      confirmation();
      if(c3==0){
        digitalWrite(d3,LOW);
        c3=1;
      }
      else if(c3==1){
        digitalWrite(d3,HIGH);
        c3=0;
      }
    }
    else if(databyte=='d'){
      confirmation();
      if(c4==0){
        digitalWrite(d4,LOW);
        c4=1;
      }
      else if(c4==1){
        digitalWrite(d4,HIGH);
        c4=0;
      }
    }
    else if(databyte=='s'){
      confirmation();
      digitalWrite(d1,HIGH);
      digitalWrite(d2,HIGH);
      digitalWrite(d3,HIGH);
      digitalWrite(d4,HIGH);
    }
    else{}
    Serial.flush();
  }
}
void confirmation(){
  for(int i=0;i<4;i++){
     digitalWrite(dled,HIGH);
     delay(100);
     digitalWrite(dled,LOW);
     delay(100);
  }
}

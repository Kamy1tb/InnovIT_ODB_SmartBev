 #include <Servo.h> 
 #include <AFMotor.h>

const int stepsPerRevolution = 2048;
AF_Stepper motor(stepsPerRevolution, 1);
AF_DCMotor DCmotor(4);
Servo myservo;
Servo myservo2;
int actual_pos = 0 ;
String q;
void setup() {
  motor.setSpeed(10);
  Serial.begin(9600);
  myservo.attach(10); 
  myservo2.attach(9);
  myservo.write(0);
  myservo2.write(0);
  DCmotor.setSpeed(100);
	DCmotor.run(RELEASE);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {
    delay(50);
  }
  
  String request = Serial.readString();
  
  if (request[6]  == '1') {
     q = request.substring(8);
     Serial.print(q);
     int quant = atoi(q.c_str());
    motor_control(1,quant);
    Serial.println("Motor1Done");

  }
  else {
  if (request[6] == '2'){
    q = request.substring(8);
     int quant = atoi(q.c_str());
    motor_control(2,quant);
    Serial.println("Motor2Done");
  }
  else{
    if (request[6] ==  '3'){ 
      actual_pos = stepper_advance(actual_pos) ;
      Serial.println(actual_pos);
    }
  else{
    if(request[6] == '4'){
      mix() ;
    }
    else{
      Serial.println("MotorError");
    }
    
  }
    
  }
  }  

}


void motor_control(int motor_number,int quant) {
  
  Serial.print(quant);
  for (int q = 0 ; q < quant ; q++){
  int pos = 0;    // variable to store the servo position
  if (motor_number == 1){
  for (pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 90; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(2);                       // waits 15ms for the servo to reach the position
  } 
  }

  if (motor_number == 2){
  for (pos = 0; pos <= 90; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo2.write(pos);              // tell servo to go to position in variable 'pos'
    delay(1);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 90; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo2.write(pos);              // tell servo to go to position in variable 'pos'
    delay(1);                       // waits 15ms for the servo to reach the position
  } 
  }

  }
  
}

int stepper_advance(int actual_position){

  motor.step(2096, FORWARD, SINGLE);
  return (actual_position + 1) % 3;

}

void mix(){
  DCmotor.run(FORWARD);
  delay(4000);
  DCmotor.run(RELEASE);
}

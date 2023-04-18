#include "Ultrasonic.h"

Ultrasonic WaterLevel(7);
String q;
double pourcent = 0 ;
void setup() {
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {
    delay(50);
  }
  
   char request = Serial.read();
 // Serial.println(request);
  if (request == 'a') {
   // Serial.println(((19 - get_niveau(WaterLevel))/19) * 100);
   delay(500);
   Serial.println(String(((19 - get_niveau(WaterLevel))/19) * 100));
  }
  else{
  }
  
    

}



double get_niveau(Ultrasonic ultrasonic){
 double RangeInCentimeters;
 RangeInCentimeters = ultrasonic.read(); // two measurements should keep an interval
 return (RangeInCentimeters);
}

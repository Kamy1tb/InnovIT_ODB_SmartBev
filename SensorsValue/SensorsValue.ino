#include <OneWire.h>
#include <DallasTemperature.h>
#include "Ultrasonic.h"

Ultrasonic WaterLevel(7);
#define DEVICE_DISCONNECTED_C -127
#define resistancePin 4
#define ONE_WIRE_BUS 3
const int motionPin = A0; 
int thresholdValue = 600; 
int pirPin = 2; 
int resistanceActive=1;
double waterLvl = 0;
float tempC;

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

double get_niveau(Ultrasonic ultrasonic){
 double RangeInCentimeters;
 RangeInCentimeters = ultrasonic.read(); // two measurements should keep an interval
 return (RangeInCentimeters);
}

void setup() {
  Serial.begin(9600);
  sensors.begin();
  pinMode(pirPin, INPUT); 
  pinMode(resistancePin,OUTPUT);
  digitalWrite(resistancePin,HIGH);
}

void loop() {
  int motionValue = analogRead(motionPin);
  if (motionValue >= thresholdValue) { 
    //Serial.println(motionValue); 
  }

  int pirStatus = digitalRead(pirPin); 
  if (pirStatus == HIGH) { 
    //Serial.println("Motion detected");
  }

  sensors.requestTemperatures();
  tempC = sensors.getTempCByIndex(0);
  if(tempC != DEVICE_DISCONNECTED_C) 
  {
    //Serial.print("Temperature for the device 1 (index 0) is: ");
    //Serial.println(tempC);
    if(tempC >= 28){
      //Serial.print("Temperature is more than 70\n");
      digitalWrite(resistancePin,LOW);
      resistanceActive=0;
    }else if(tempC <= 24){
      //Serial.println("Temperature is less then 30\n");
      if(resistanceActive!=1){
        digitalWrite(resistancePin,HIGH);
        resistanceActive=1;
      }
    }
  } 

  waterLvl = get_niveau(WaterLevel);

  //Serial.print(waterLevel);
  //Serial.println("cm");


  if(Serial.available() > 0) { 
    int incomingInt = Serial.parseInt(); 
    if (incomingInt == 1) { 
      String jsonString = "{";
      jsonString += "\"temperature\":" + String(tempC) + ",";
      jsonString += "\"waterLevel\":" + String(((22-waterLvl)/22 )* 100);
      jsonString += "}";
      Serial.println(jsonString);
    }
  }

  delay(500);
}
#include <Stepper.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2


const int stepsPerRevolution = 1200; //divide by 2, so it will be a half rotation
//int no_Rotations=3;
//float no_Steps=no_Rotations*stepsPerRevolution;
const float max_steps =stepsPerRevolution;
const float min_steps=0;
float curSteps =0;
bool Shading = false ;
int Position = 0;
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11);

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
 float Celcius=0;
void setup(void)
{
  
  Serial.begin(9600);
  sensors.begin();
  myStepper.setSpeed(13);
  Serial.begin(9600);
  
}

void loop() {
  
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Serial.println(" C  ");
  Serial.print(Celcius);
  delay(1000);
  if (Shading==false and Celcius<27){ 
    while (curSteps<max_steps ){
      myStepper.step(-stepsPerRevolution);
      curSteps+=stepsPerRevolution;
      //Serial.print("steps per revolution: ");
      //Serial.print(-stepsPerRevolution);
      //Serial.print("curSteps: ");
      //Serial.print(curSteps);
      //Serial.print("maxSteps: ");
      //Serial.print(max_steps);
      Serial.print("\n");
      Serial.println("Putting the Shading on"); //println instead of print
      //Serial.print("\n");
      sensors.requestTemperatures(); 
      Celcius=sensors.getTempCByIndex(0);
      delay(100);
      Serial.print(Celcius);
      Serial.print("\n");
      Shading=true;
      
      
      }
  }
  
  if (Shading==true and Celcius>27){
    while (curSteps>min_steps){
      myStepper.step(stepsPerRevolution);
      curSteps-=stepsPerRevolution;
      Serial.print("\n");
      Serial.print("Taking the shading off");
      Serial.print("\n");
      sensors.requestTemperatures(); 
      Celcius=sensors.getTempCByIndex(0);
      delay(100);
      Serial.print(Celcius);
      //Serial.print("\n");
      Shading=false; 
      
         
  }
  }
}

#include <Stepper.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2


const float stepsPerRevolution = 1024; //Number of steps for a half rotation with the stepper motor. Maybe it should be 32*64 / 2 = 1024
float curSteps = 0; //Current Position value.
float steps2take = 0; //# of steps to go from current position to new desired position. 0 is midpoint, -stepsPerRevolution/2 = Leftmost position, +stepsPerRevolution/2 = Rightmost.
const float Low = 20.0; //Our "minimum" temperature, any lower temperatures will be evaluated as 20.
const float High = 30.0; //Our "maximum" temperature, any higher temperatures will be evaluated as 30.
const float Mid = (Low+High)/2; //The midpoint between high and low.
const float Range = High - Low; //how many degrees between high and low temperature.
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); //Order of pins is to avoid issues with stepper motor.

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
float Celcius=0;
void setup(void)
{
  Serial.begin(9600); //begins serial, so we can use the Serial monitor. 9600 is baudrate
  sensors.begin();
  myStepper.setSpeed(13); 
  Serial.begin(9600); 
}

void loop() {
  delay(1000);
  sensors.requestTemperatures(); 
  Celcius = sensors.getTempCByIndex(0); //Variable to hold temperature value.
  Celcius = Celcius * 1.1263 - 2.3072; //Measured data is manipulated to reflect reality better, per our calibration. R^2 value for linear fit is 0,9878 with 5 data points
  
  float steps2take = (stepsPerRevolution) * (Mid-Celcius)/Range -curSteps; 


  
  if (Celcius>High and curSteps > -(stepsPerRevolution/2)) {  //if temperature is higher than 'High' value and position is not leftmost yet, go to leftmost position.
      steps2take = -stepsPerRevolution/2 - curSteps; 
      myStepper.step(steps2take);
      curSteps+=steps2take;
  } else if (Celcius<20 and (curSteps < stepsPerRevolution/2)) {
      steps2take = stepsPerRevolution/2 - curSteps;
      myStepper.step(steps2take);
      curSteps+=steps2take;
  } else if (Celcius > Low and Celcius < High) {
      myStepper.step(steps2take);
      curSteps+=steps2take;
  } 
  //Print status for the computed loop.
  Serial.print("curSteps: ");
  Serial.println(curSteps);
  Serial.print("Steps2take: ");
  Serial.println(steps2take);
  Serial.print("C:");
  Serial.println(Celcius);
  
}

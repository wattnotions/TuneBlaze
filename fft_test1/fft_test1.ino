#include "arduinoFFT.h"

  
#define SAMPLES 1024               //Must be a power of 2
#define SAMPLING_FREQUENCY 50000  //Hz
#define REFRESH_RATE 10           //Hz
#define ARDUINO_IDE_PLOTTER_SIZE 500
  
arduinoFFT FFT = arduinoFFT();
  
unsigned long sampling_period_us;
unsigned long useconds_sampling;
 
unsigned long refresh_period_us;
unsigned long useconds_refresh;
  
double vReal[SAMPLES];
double vImag[SAMPLES];
 
uint8_t analogpin = A8;
  
void setup() {
  Serial.begin(115200);
 
  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY));
  refresh_period_us = round(1000000*(1.0/REFRESH_RATE));
 
  pinMode(analogpin, INPUT);
  pinMode(1, OUTPUT);
}
  
void loop() {
  digitalWrite(1, !digitalRead(1));
  
  useconds_refresh = micros();
   
  /*SAMPLING*/
  for(int i=0; i<SAMPLES; i++)
  {
    useconds_sampling = micros();
  
    vReal[i] = analogRead(analogpin);
    vImag[i] = 0;
  
    while(micros() < (useconds_sampling + sampling_period_us)){
      //wait...
    }
  }  
 
  /*FFT*/
 
  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
  
 
  /*PRINT RESULTS*/

  Serial.println("*");
  for(int i=2; i<(SAMPLES/2); i++){
    Serial.print(vReal[i], 1);
    Serial.print(',');
  }
  Serial.print('\n');

  /*
  for(int i=0; i<(ARDUINO_IDE_PLOTTER_SIZE - (SAMPLES/2)); i++){
    Serial.println(0);
  }
 
  while(micros() < (useconds_refresh + refresh_period_us)){
    //wait...
  }
  */
  
}

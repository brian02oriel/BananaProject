#include <ArduinoJson.h>

#include <DHT_U.h>
#include <DHT.h>

#include <Event.h>
#include <Timer.h>

#include <SoftwareSerial.h>

#define dataPin 4
#define DHTTYPE DHT22

DHT dht = DHT(dataPin, DHTTYPE);

Timer t1, t2;

const int capacity = JSON_OBJECT_SIZE(3);
StaticJsonDocument<capacity> data;
const int pinLedA = 2;
const int pinLedB = 3;

void setup() {
  // put your setup code here, to run once:
  
  pinMode(pinLedA, OUTPUT);
  pinMode(pinLedB, OUTPUT);
  Serial.begin(9600);
  dht.begin();
  int bright = t1.every(1000, Bright);
  int sensor = t2.every(1000, Sensor);
}

void loop() {
  // put your main code here, to run repeatedly:
  t1.update();
  t2.update();
}

void Bright(){
    digitalWrite(pinLedA, HIGH);
    digitalWrite(pinLedB, HIGH);
}

void Sensor(){
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if(isnan(h) || isnan(t)){
    Serial.println("Sensor inoperante");
    return;
  }

  data["temperature"] = t;
  data["humidity"]= h;
  serializeJson(data, Serial);
  
  Serial.println();
  
}

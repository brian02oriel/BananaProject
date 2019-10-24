#include <ArduinoJson.h>

#include <DHT_U.h>
#include <DHT.h>

#include <Event.h>
#include <Timer.h>

#include <SoftwareSerial.h>

#define dataPin 4
#define DHTTYPE DHT22

DHT dht = DHT(dataPin, DHTTYPE);

Timer t1;

const int capacity = JSON_OBJECT_SIZE(3);
StaticJsonDocument<capacity> data;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  int sensor = t1.every(1000, Sensor);
}

void loop() {
  // put your main code here, to run repeatedly:
  t1.update();
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

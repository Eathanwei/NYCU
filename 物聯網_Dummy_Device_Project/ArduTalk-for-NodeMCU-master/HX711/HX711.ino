//   ArduTalk
#define DefaultIoTtalkServerIP  "140.113.199.200"
#define DM_name  "NodeMCU" 
#define DF_list  {"D0~","D1~","D2~","D5","D6","D7","D8","A0"}
#define nODF     10  // The max number of ODFs which the DA can pull.

#include <ESP8266WiFi.h>
//#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266WiFiMulti.h>
#include <EEPROM.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 12;
const int LOADCELL_SCK_PIN = 13;
int adjust=179000;

HX711 scale;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {
  if (scale.is_ready()) {
    long reading = scale.read();
    long data = round((reading+adjust)/3600.0*7.5+0.3);
    Serial.print("HX711 reading: ");
    Serial.println(data);
  } else {
    Serial.println("HX711 not found.");
  }
  delay(1000);
}

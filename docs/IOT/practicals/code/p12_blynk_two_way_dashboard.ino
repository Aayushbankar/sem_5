// P12 — Two-way Blynk dashboard: monitor DHT + control LED from phone
// DHT DATA -> GPIO 4 · LED/relay -> GPIO 26 · Blynk library
// Fill in BLYNK_TEMPLATE_ID, BLYNK_TEMPLATE_NAME, BLYNK_AUTH_TOKEN below.

#define BLYNK_TEMPLATE_ID   "TMPLxxxxxxx"    // from blynk.cloud template
#define BLYNK_TEMPLATE_NAME "ESP32 Lab"
#define BLYNK_AUTH_TOKEN    "your-device-auth-token"

#include <WiFi.h>
#include <Blynk.h>
#include <DHT.h>

char ssid[] = "YOUR_WIFI_SSID";
char pass[] = "YOUR_WIFI_PASSWORD";

const int ledPin = 26;
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int vTemp = 0;      // datastream V0: temperature (up)
const int vLed  = 1;      // datastream V1: switch (down)

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  dht.begin();

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
}

// Fired when the phone switch on V1 sends a value (0 or 1)
BLYNK_WRITE(V1) {
  int state = param.asInt();          // 1 = ON, 0 = OFF
  digitalWrite(ledPin, state == 1 ? HIGH : LOW);
  Serial.print("V1 switch -> LED ");
  Serial.println(state == 1 ? "ON" : "OFF");
}

void loop() {
  Blynk.run();                        // keep cloud connection alive

  static unsigned long lastRead = 0;
  if (millis() - lastRead > 5000) {   // push temp to cloud every 5 s
    lastRead = millis();
    float t = dht.readTemperature();
    if (!isnan(t)) {
      Blynk.virtualWrite(vTemp, t);   // one-way UP: phone gauge shows it
      Serial.print("Pushed temp to V0: ");
      Serial.println(t);
    }
  }
}

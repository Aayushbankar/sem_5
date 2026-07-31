// P10 — HTTP GET to ThingSpeak: upload DHT11 temperature for graphing
// DHT DATA -> GPIO 4 · HTTPClient + WiFi (ESP32 core)
// Library: DHT sensor library (Adafruit) + Unified Sensor

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// >>> REPLACE WITH YOUR THINGSPEAK CHANNEL'S WRITE API KEY <<<
String apiKey = "XXXXXXXXXXXXXXXX";   // 16 hex chars, e.g. ABCDEF1234567890

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* server = "api.thingspeak.com";
const unsigned long INTERVAL = 20000;   // 20 s (> 15 s free-tier minimum)

unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  unsigned long now = millis();
  if (now - lastSend < INTERVAL) return;
  lastSend = now;

  float t = dht.readTemperature();
  if (isnan(t)) {
    Serial.println("DHT read failed, skipping upload");
    return;
  }

  HTTPClient http;
  String url = String("http://") + server + "/update?api_key=" + apiKey +
               "&field1=" + String(t, 1);

  http.begin(url);                 // HTTP GET (ThingSpeak update API)
  int code = http.GET();

  if (code == 200) {
    Serial.print("Uploaded temp=");
    Serial.print(t, 1);
    Serial.print(" *C  -> HTTP 200, entry ");
    Serial.println(http.getString());
  } else {
    Serial.print("Upload failed, HTTP code: ");
    Serial.println(code);
  }
  http.end();
}

// P13b — Soil moisture + DHT -> Wi-Fi -> ThingSpeak, with threshold alerts
// Soil A0 -> GPIO 34 · DHT DATA -> GPIO 4 · HTTPClient

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// >>> REPLACE WITH YOUR THINGSPEAK WRITE API KEY <<<
String apiKey = "XXXXXXXXXXXXXXXX";

// ---- Threshold values (process on the ESP32, before upload) ----
const int  SOIL_DRY = 2000;    // below this = soil needs irrigation
const float TEMP_HOT = 35.0;   // above this = heat alert
const float HUM_LOW  = 40.0;   // below this = dry-air alert

#define SOIL_PIN 34
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* server = "api.thingspeak.com";
const unsigned long INTERVAL = 20000;   // 20 s
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);

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

  int  soil = analogRead(SOIL_PIN);
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("DHT read failed, skipping cycle");
    return;
  }

  // ---- threshold / alert logic (edge processing on the ESP32) ----
  if (soil < SOIL_DRY) {
    Serial.println("ALERT: Soil DRY - irrigation needed!");
  }
  if (t > TEMP_HOT) {
    Serial.println("ALERT: High temperature!");
  }
  if (h < HUM_LOW) {
    Serial.println("ALERT: Low air humidity!");
  }

  // ---- upload all three values to ThingSpeak ----
  HTTPClient http;
  String url = String("http://") + server + "/update?api_key=" + apiKey +
               "&field1=" + String(t, 1) +
               "&field2=" + String(h, 1) +
               "&field3=" + String(soil);

  http.begin(url);
  int code = http.GET();

  Serial.print("Uploaded temp=");
  Serial.print(t, 1);
  Serial.print(" hum=");
  Serial.print(h, 1);
  Serial.print(" soil=");
  Serial.print(soil);
  Serial.print("  -> HTTP ");
  Serial.println(code == 200 ? "200" : String(code));
  http.end();
}

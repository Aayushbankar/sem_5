// P11 — Ultrasonic distance to ThingSpeak (tank fill-level application)
// TRIG -> GPIO 5, ECHO -> GPIO 18 (1k+2k divider) · NewPing + HTTPClient
// Library: NewPing

#include <WiFi.h>
#include <HTTPClient.h>
#include <NewPing.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// >>> REPLACE WITH YOUR THINGSPEAK WRITE API KEY <<<
String apiKey = "XXXXXXXXXXXXXXXX";

const float TANK_HEIGHT = 100.0;   // tank height in cm (example)

#define TRIG_PIN 5
#define ECHO_PIN 18
#define MAX_DIST 400

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DIST);

const char* server = "api.thingspeak.com";
const unsigned long INTERVAL = 20000;
unsigned long lastSend = 0;

void setup() {
  Serial.begin(115200);

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

  unsigned int dist = sonar.ping_cm();
  if (dist == 0 || dist > TANK_HEIGHT) {
    Serial.println("Distance out of range, skipping upload");
    return;
  }

  // convert distance from the top into a fill level / percentage
  float fillCm = TANK_HEIGHT - dist;
  float fillPct = (fillCm / TANK_HEIGHT) * 100.0;

  HTTPClient http;
  String url = String("http://") + server + "/update?api_key=" + apiKey +
               "&field1=" + String(dist) +
               "&field2=" + String(fillPct, 1);

  http.begin(url);
  int code = http.GET();

  if (code == 200) {
    Serial.print("Uploaded dist=");
    Serial.print(dist);
    Serial.print(" cm, fill=");
    Serial.print(fillPct, 1);
    Serial.print(" %  -> HTTP 200, entry ");
    Serial.println(http.getString());
  } else {
    Serial.print("Upload failed, HTTP code: ");
    Serial.println(code);
  }
  http.end();
}

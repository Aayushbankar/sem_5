// P14 — Smart Agriculture: soil moisture + DHT + PIR, auto & remote pump control
// Soil A0 -> GPIO 34 · DHT DATA -> GPIO 4 · PIR -> GPIO 25 · Relay -> GPIO 26
// Libraries: DHT sensor library (Adafruit), Unified Sensor, PubSubClient

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ---- MQTT (public broker) ----
const char* mqttServer = "broker.emqx.io";
const int   mqttPort = 1883;
const char* topicData = "agri/esp32/data";     // publish: sensor JSON
const char* topicPump = "agri/esp32/pump";     // subscribe: "1"/"0" from phone

// ---- Pins ----
#define SOIL_PIN 34
#define DHTPIN 4
#define DHTTYPE DHT11
#define PIR_PIN 25
#define RELAY_PIN 26
#define LED_PIN 2

DHT dht(DHTPIN, DHTTYPE);

// ---- Thresholds (edge processing) ----
const int SOIL_DRY = 2000;      // below -> auto-pump ON
const int SOIL_OK  = 2600;      // above -> auto-pump OFF (hysteresis)
const float TEMP_HOT = 35.0;

bool manualMode = false;        // true = phone controls pump, false = auto
bool pumpState  = false;

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastPub = 0;
const unsigned long PUB_MS = 10000;   // publish every 10 s

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);      // most relay boards: HIGH = OFF

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqttServer, mqttPort);
  client.setCallback(onMqtt);
}

// Phone publishes "1"/"0" to agri/esp32/pump -> manual pump control
void onMqtt(char* topic, byte* payload, unsigned int len) {
  String msg = "";
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];

  manualMode = true;                  // any manual command -> manual mode
  if (msg == "1")      setPump(true);
  else if (msg == "0") setPump(false);
  Serial.print("Manual pump command: ");
  Serial.println(msg);
}

void setPump(bool on) {
  pumpState = on;
  digitalWrite(RELAY_PIN, on ? LOW : HIGH);   // LOW-active relay
  digitalWrite(LED_PIN, on ? HIGH : LOW);
  Serial.print("Pump -> ");
  Serial.println(on ? "ON" : "OFF");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("MQTT...");
    if (client.connect("agri-node-01")) {
      Serial.println("connected");
      client.subscribe(topicPump);
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  int soil = analogRead(SOIL_PIN);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int pir = digitalRead(PIR_PIN);

  // ---- Automatic control with hysteresis (only when NOT manual) ----
  if (!manualMode) {
    if (soil < SOIL_DRY)     setPump(true);   // dry -> irrigate
    else if (soil > SOIL_OK) setPump(false);  // enough water -> stop
  }

  // ---- Publish every 10 s ----
  if (millis() - lastPub > PUB_MS) {
    lastPub = millis();
    if (!isnan(t) && !isnan(h)) {
      String payload = String("{\"temp\":") + String(t, 1) +
                       ",\"hum\":" + String(h, 1) +
                       ",\"soil\":" + String(soil) +
                       ",\"pir\":" + (pir == HIGH ? 1 : 0) +
                       ",\"pump\":" + (pumpState ? 1 : 0) + "}";
      client.publish(topicData, payload.c_str());
      Serial.print("Published: ");
      Serial.println(payload);
    }
  }

  delay(500);
}

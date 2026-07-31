// P08 — ESP32 as MQTT publisher: DHT11 temp & humidity to a public broker
// DHT DATA -> GPIO 4 · Wi-Fi + PubSubClient
// Libraries: PubSubClient, DHT sensor library (Adafruit) + Unified Sensor

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// ---- Wi-Fi credentials (EDIT THESE) ----
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ---- Public MQTT broker ----
const char* mqttServer = "broker.emqx.io";   // or test.mosquitto.org
const int   mqttPort = 1883;

// ---- Topics (reused by P09's subscriber) ----
const char* topicTemp = "esp32/dht/temperature";
const char* topicHum  = "esp32/dht/humidity";

// ---- DHT setup ----
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
const unsigned long INTERVAL = 5000;   // publish every 5 s

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
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqttServer, mqttPort);
}

void reconnect() {
  // Keep retrying until the broker accepts us
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("esp32-lab-01")) {   // unique client id
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5s");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > INTERVAL) {
    lastMsg = now;

    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (isnan(h) || isnan(t)) {
      Serial.println("DHT read failed, skipping publish");
      return;
    }

    // Convert floats to strings and publish
    char tempStr[8], humStr[8];
    dtostrf(t, 4, 1, tempStr);
    dtostrf(h, 4, 1, humStr);

    client.publish(topicTemp, tempStr);
    client.publish(topicHum, humStr);

    Serial.print("Published  temp=");
    Serial.print(tempStr);
    Serial.print(" *C  hum=");
    Serial.print(humStr);
    Serial.println(" %");
  }
}

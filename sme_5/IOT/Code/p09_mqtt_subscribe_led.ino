// P09 — ESP32 as MQTT subscriber: remote control of LED/relay
// Command topic: esp32/led/cmd   payload "ON" / "OFF"
// Libraries: PubSubClient

#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const char* mqttServer = "broker.emqx.io";
const int   mqttPort = 1883;

const char* topicCmd = "esp32/led/cmd";    // subscribed command topic

const int ledPin = 26;                     // LED (or relay IN) on GPIO 26

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP: ");
  Serial.println(WiFi.localIP());

  client.setServer(mqttServer, mqttPort);
  client.setCallback(onMessage);   // register the callback
}

// Called automatically by client.loop() when a message arrives
void onMessage(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on [");
  Serial.print(topic);
  Serial.print("]: ");

  // build a clean string from the payload bytes
  String msg = "";
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  Serial.println(msg);

  if (msg == "ON") {
    digitalWrite(ledPin, HIGH);
    Serial.println(">>> LED ON");
  } else if (msg == "OFF") {
    digitalWrite(ledPin, LOW);
    Serial.println(">>> LED OFF");
  } else {
    Serial.println("Unknown command (send ON or OFF)");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("esp32-led-sub-01")) {
      Serial.println("connected");
      client.subscribe(topicCmd);          // subscribe AFTER connecting
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
  client.loop();   // processes incoming messages -> fires onMessage()
}

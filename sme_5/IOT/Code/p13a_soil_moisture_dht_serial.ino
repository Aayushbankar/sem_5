// P13a — Soil moisture (analog) + DHT11 read, processed on the ESP32,
//         displayed on the Serial Monitor.
// Soil A0 -> GPIO 34 · DHT DATA -> GPIO 4

#include <DHT.h>

#define SOIL_PIN 34
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);
  Serial.println("P13a: Soil moisture + DHT on Serial Monitor");
}

void loop() {
  delay(2000);                       // DHT needs 2 s between reads

  int soil = analogRead(SOIL_PIN);   // 0..4095 (wet = high)
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  Serial.print("Soil raw: ");
  Serial.print(soil);
  Serial.print("  Humidity: ");
  if (isnan(h)) Serial.print("err"); else Serial.print(h);
  Serial.print(" %  Temperature: ");
  if (isnan(t)) Serial.print("err"); else Serial.print(t);
  Serial.println(" *C");
}

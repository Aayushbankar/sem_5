// P06 — DHT11/DHT22 temperature & humidity with Adafruit DHT library
// DATA -> GPIO 4, pull-up 4.7k-10k to 3V3
// Libraries: "DHT sensor library" by Adafruit + "Adafruit Unified Sensor"

#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 4               // data pin on GPIO 4
#define DHTTYPE DHT11          // change to DHT22 if using a DHT22

DHT dht(DHTPIN, DHTTYPE);      // create DHT object

void setup() {
  Serial.begin(115200);
  Serial.println("P06: DHT sensor interface started.");
  dht.begin();                 // initialise the sensor
}

void loop() {
  // Allow the sensor 2 seconds between reads (DHT requirement)
  delay(2000);

  float h = dht.readHumidity();     // humidity in %
  float t = dht.readTemperature();  // temperature in °C

  // Check for invalid reading (NaN) -> wire/library/checksum problem
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %");
  Serial.print("  |  Temperature: ");
  Serial.print(t);
  Serial.println(" *C");
}

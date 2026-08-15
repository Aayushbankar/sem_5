// P04 — Toggle an external LED (Digital Output)
// LED on GPIO 26, current-limited by a 220 ohm resistor.

const int ledPin = 26;          // GPIO 26 drives the external LED

void setup() {
  Serial.begin(115200);          // start serial monitor (115200 baud)
  pinMode(ledPin, OUTPUT);       // configure GPIO 26 as a digital output
  Serial.println("P04: External LED toggle started.");
}

void loop() {
  digitalWrite(ledPin, HIGH);    // LED ON (pin driven to 3.3 V)
  Serial.println("LED ON");
  delay(500);                    // stay ON for 500 ms

  digitalWrite(ledPin, LOW);     // LED OFF (pin driven to 0 V)
  Serial.println("LED OFF");
  delay(500);                    // stay OFF for 500 ms
}

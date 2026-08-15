// P05 — PIR motion (digital input) + LDR light level (analog input)
// PIR OUT  -> GPIO 25
// LDR divider mid-point -> GPIO 34 (ADC1, input-only)

const int pirPin = 25;          // digital input
const int ldrPin = 34;          // analog input (12-bit ADC)

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);       // PIR output is a digital signal
  pinMode(ldrPin, INPUT);       // ADC pin (no internal pull needed)
  Serial.println("P05: PIR + LDR interface started.");
}

void loop() {
  int motion = digitalRead(pirPin);     // HIGH = motion, LOW = idle
  int raw = analogRead(ldrPin);         // 0..4095

  // Invert to a friendly 0-100 "light %" (0 = dark, 100 = bright)
  int lightPct = map(raw, 0, 4095, 100, 0);
  lightPct = constrain(lightPct, 0, 100);

  Serial.print("Motion: ");
  Serial.print(motion == HIGH ? "DETECTED" : "none");
  Serial.print("  |  LDR raw: ");
  Serial.print(raw);
  Serial.print("  |  Light: ");
  Serial.print(lightPct);
  Serial.println(" %");

  delay(500);                   // sample twice per second
}

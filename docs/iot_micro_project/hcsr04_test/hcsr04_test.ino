const uint8_t TRIG_PIN = 5;  // D1 on NodeMCU V3
const uint8_t ECHO_PIN = 4;  // D2 on NodeMCU V3

const unsigned long PRINT_INTERVAL_MS = 500;
const unsigned long ECHO_TIMEOUT_US = 25000;  // ~400 cm max range

unsigned long lastPrintMs = 0;

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
}

void loop() {
  unsigned long now = millis();
  if (now - lastPrintMs < PRINT_INTERVAL_MS) {
    return;
  }
  lastPrintMs = now;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long durationUs = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);

  if (durationUs == 0) {
    Serial.println("Distance: out of range (no echo)");
    return;
  }

  float distanceCm = durationUs / 58.0;
  if (distanceCm < 2.0 || distanceCm > 400.0) {
    Serial.println("Distance: out of range");
    return;
  }

  Serial.print("Distance: ");
  Serial.print(distanceCm, 1);
  Serial.println(" cm");
}

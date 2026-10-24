const uint8_t TRIG_PIN = 5;   // D1
const uint8_t ECHO_PIN = 4;   // D2
const uint8_t IN1_PIN = 14;   // D5
const uint8_t IN2_PIN = 12;   // D6
const uint8_t IN3_PIN = 13;   // D7
const uint8_t IN4_PIN = 15;   // D8

const unsigned long PING_INTERVAL_MS = 100;
const unsigned long BLINK_INTERVAL_MS = 200;
const unsigned long ECHO_TIMEOUT_US = 23000;  // ~400 cm; keeps block < ping period
const float OBSTACLE_CM = 20.0;

unsigned long lastPingMs = 0;
unsigned long lastBlinkMs = 0;
bool collision = false;
bool ledLit = true;

void ledWrite(bool lit) {
  digitalWrite(LED_BUILTIN, lit ? LOW : HIGH);  // active LOW
}

void motorsForward() {
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
}

void motorsStop() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
}

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long us = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  return us == 0 ? -1.0 : us / 58.0;
}

void printStatus(float d) {
  Serial.print(collision ? "[COLLISION] " : "[RUN] ");
  if (d < 0.0) {
    Serial.print("no echo");
  } else {
    Serial.print("distance ");
    Serial.print(d, 1);
    Serial.print(" cm");
  }
  Serial.print(" | motors: ");
  Serial.print(collision ? "STOP" : "FWD");
  Serial.print(" | LED: ");
  Serial.println(collision ? (ledLit ? "BLINK-ON" : "BLINK-OFF") : "SOLID-ON");
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  digitalWrite(TRIG_PIN, LOW);
  pinMode(ECHO_PIN, INPUT);

  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  motorsForward();

  pinMode(LED_BUILTIN, OUTPUT);
  ledWrite(true);

  Serial.println();
  Serial.println("V3: ping 100ms | >=20cm FWD + LED solid | <20cm STOP + LED blink 200ms");
}

void loop() {
  unsigned long now = millis();

  if (collision && now - lastBlinkMs >= BLINK_INTERVAL_MS) {
    lastBlinkMs = now;
    ledLit = !ledLit;
    ledWrite(ledLit);
  }

  if (now - lastPingMs < PING_INTERVAL_MS) {
    return;
  }
  lastPingMs = now;

  float d = readDistanceCm();
  bool newCollision = (d > 0.0 && d < OBSTACLE_CM);

  if (newCollision) {
    if (!collision) {
      collision = true;
      lastBlinkMs = now;
      ledLit = true;
      ledWrite(true);
    }
    motorsStop();
  } else {
    if (collision) {
      collision = false;
      ledLit = true;
      ledWrite(true);
    }
    motorsForward();
  }

  printStatus(d);
}

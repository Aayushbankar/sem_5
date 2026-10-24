const uint8_t TRIG_PIN = 5;   // D1
const uint8_t ECHO_PIN = 4;   // D2
const uint8_t IN1_PIN = 14;   // D5  -> OUT1 (Left motor)
const uint8_t IN2_PIN = 12;   // D6  -> OUT2 (Left motor)
const uint8_t IN3_PIN = 13;   // D7  -> OUT3 (Right motor)
const uint8_t IN4_PIN = 15;   // D8  -> OUT4 (Right motor)

const unsigned long PING_INTERVAL_MS = 500;
const unsigned long ECHO_TIMEOUT_US = 25000;
const unsigned long PHASE_MS = 2500;   // each test step lasts 2.5 s
const float OBSTACLE_CM = 20.0;

unsigned long lastPingMs = 0;
unsigned long lastPhaseMs = 0;
uint8_t phase = 0;

void allLow() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
}

void setLeft(uint8_t dir) {           // 0=stop 1=fwd 2=rev
  digitalWrite(IN1_PIN, dir == 1 ? HIGH : LOW);
  digitalWrite(IN2_PIN, dir == 2 ? HIGH : LOW);
}

void setRight(uint8_t dir) {          // 0=stop 1=fwd 2=rev
  digitalWrite(IN3_PIN, dir == 1 ? HIGH : LOW);
  digitalWrite(IN4_PIN, dir == 2 ? HIGH : LOW);
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

const char *PHASE_NAMES[] = {
  "STOP          both idle",
  "LEFT  fwd     (IN1=H IN2=L)   <- left wheel must spin",
  "LEFT  rev     (IN1=L IN2=H)   <- left wheel must reverse",
  "RIGHT fwd     (IN3=H IN4=L)   <- right wheel must spin",
  "RIGHT rev     (IN3=L IN4=H)   <- right wheel must reverse",
  "BOTH  fwd     (LEFT+RIGHT)    <- both wheels forward",
  "BOTH  rev     (LEFT+RIGHT)    <- both wheels reverse",
  "STOP          both idle"
};

void applyPhase(uint8_t p) {
  allLow();
  switch (p) {
    case 0: case 7: break;
    case 1: setLeft(1); break;
    case 2: setLeft(2); break;
    case 3: setRight(1); break;
    case 4: setRight(2); break;
    case 5: setLeft(1); setRight(1); break;
    case 6: setLeft(2); setRight(2); break;
  }
  Serial.print("[MOTOR] ");
  Serial.println(PHASE_NAMES[p]);
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
  allLow();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);  // lit while running/idle

  Serial.println();
  Serial.println("=== HW DIAG: motor channels cycle every 2.5 s ===");
  Serial.println("=== ultrasonic reports every 500 ms            ===");
  applyPhase(0);
}

void loop() {
  unsigned long now = millis();

  if (now - lastPingMs >= PING_INTERVAL_MS) {
    lastPingMs = now;
    float d = readDistanceCm();
    if (d < 0.0) {
      Serial.println("[USON] no echo - check VCC(5V)/GND/TRIG/ECHO wiring");
    } else if (d < OBSTACLE_CM) {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.print("[USON] OBSTACLE ");
      Serial.print(d, 1);
      Serial.println(" cm  (LED pin HIGH)");
    } else {
      digitalWrite(LED_BUILTIN, LOW);
      Serial.print("[USON] clear    ");
      Serial.print(d, 1);
      Serial.println(" cm");
    }
  }

  if (now - lastPhaseMs >= PHASE_MS) {
    lastPhaseMs = now;
    phase = (phase + 1) % 8;
    applyPhase(phase);
  }
}

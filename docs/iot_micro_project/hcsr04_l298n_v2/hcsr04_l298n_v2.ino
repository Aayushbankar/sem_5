const uint8_t TRIG_PIN = 5;   // D1
const uint8_t ECHO_PIN = 4;   // D2
const uint8_t IN1_PIN = 14;   // D5
const uint8_t IN2_PIN = 12;   // D6
const uint8_t IN3_PIN = 13;   // D7
const uint8_t IN4_PIN = 15;   // D8

const unsigned long PING_INTERVAL_MS = 500;
const unsigned long ECHO_TIMEOUT_US = 25000;
const float OBSTACLE_CM = 20.0;

unsigned long lastPingMs = 0;

void motorsStop() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
}

void motorsForward() {
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, HIGH);
  digitalWrite(IN4_PIN, LOW);
}

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long durationUs = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  if (durationUs == 0) {
    return -1.0;  // no echo
  }
  return durationUs / 58.0;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);

  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  motorsForward();  // default: running
  digitalWrite(LED_BUILTIN, LOW);  // active-LOW: LOW = LED lit while running
}

void loop() {
  unsigned long now = millis();
  if (now - lastPingMs < PING_INTERVAL_MS) {
    return;
  }
  lastPingMs = now;

  float distanceCm = readDistanceCm();
  bool obstacle = (distanceCm >= 0.0 && distanceCm < OBSTACLE_CM);

  if (obstacle) {
    digitalWrite(LED_BUILTIN, HIGH);  // spec: HIGH when obstacle close
    motorsStop();
    Serial.print("STOP  obstacle @ ");
    Serial.print(distanceCm, 1);
    Serial.println(" cm");
  } else {
    digitalWrite(LED_BUILTIN, LOW);
    motorsForward();
    if (distanceCm < 0.0) {
      Serial.println("FWD   no echo (nothing detected)");
    } else {
      Serial.print("FWD   distance ");
      Serial.print(distanceCm, 1);
      Serial.println(" cm");
    }
  }
}

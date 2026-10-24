// Robot receiver (NodeMCU ESP8266) — ESP-NOW tank drive, phase 1
// HC-SR04 pins kept wired but NOT read (phase 2: telemetry + hard obstacle override)

#include <ESP8266WiFi.h>
#include <espnow.h>

const uint8_t IN1_PIN = 14;  // D5
const uint8_t IN2_PIN = 12;  // D6
const uint8_t IN3_PIN = 13;  // D7
const uint8_t IN4_PIN = 15;  // D8

const unsigned long FAILSAFE_MS = 200;
const uint8_t MAGIC = 0xA5;

enum Cmd : uint8_t { CMD_STOP = 0, CMD_FWD = 1, CMD_BACK = 2, CMD_LEFT = 3, CMD_RIGHT = 4 };

volatile uint8_t lastCmd = CMD_STOP;
volatile unsigned long lastCmdMs = 0;

void applyCmd(uint8_t cmd) {
  switch (cmd) {
    case CMD_FWD:
      digitalWrite(IN1_PIN, HIGH); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, HIGH); digitalWrite(IN4_PIN, LOW);
      break;
    case CMD_BACK:
      digitalWrite(IN1_PIN, LOW);  digitalWrite(IN2_PIN, HIGH);
      digitalWrite(IN3_PIN, LOW);  digitalWrite(IN4_PIN, HIGH);
      break;
    case CMD_LEFT:   // tank pivot: left rev, right fwd
      digitalWrite(IN1_PIN, LOW);  digitalWrite(IN2_PIN, HIGH);
      digitalWrite(IN3_PIN, HIGH); digitalWrite(IN4_PIN, LOW);
      break;
    case CMD_RIGHT:  // tank pivot: left fwd, right rev
      digitalWrite(IN1_PIN, HIGH); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, LOW);  digitalWrite(IN4_PIN, HIGH);
      break;
    default:
      digitalWrite(IN1_PIN, LOW); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, LOW); digitalWrite(IN4_PIN, LOW);
      break;
  }
}

const char *cmdName(uint8_t c) {
  switch (c) {
    case CMD_FWD:  return "FWD";
    case CMD_BACK: return "BACK";
    case CMD_LEFT: return "LEFT";
    case CMD_RIGHT:return "RIGHT";
    default:       return "STOP";
  }
}

void onReceive(uint8_t *mac, uint8_t *data, uint8_t len) {
  (void)mac;
  if (len < 2 || data[0] != MAGIC) return;
  uint8_t cmd = data[1];
  if (cmd > CMD_RIGHT) return;
  lastCmd = cmd;
  lastCmdMs = millis();
}

void setup() {
  Serial.begin(115200);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  applyCmd(CMD_STOP);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // off until link proven

  WiFi.mode(WIFI_STA);
  Serial.print("Robot MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != 0) {
    Serial.println("ESP-NOW init FAILED");
    return;
  }
  esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
  esp_now_register_recv_cb(onReceive);

  uint8_t broadcast[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  esp_now_add_peer(broadcast, ESP_NOW_ROLE_COMBO, 1, NULL, 0);

  Serial.println("rc_robot ready (phase 1: remote drive only)");
}

void loop() {
  static uint8_t shown = 255;
  bool linkAlive = (millis() - lastCmdMs) < FAILSAFE_MS;

  if (!linkAlive && lastCmd != CMD_STOP) {
    lastCmd = CMD_STOP;
    applyCmd(CMD_STOP);
  }

  digitalWrite(LED_BUILTIN, linkAlive ? LOW : HIGH);

  uint8_t c = lastCmd;
  if (c != shown) {
    shown = c;
    Serial.print(linkAlive ? "link  " : "FAILSAFE ");
    Serial.println(cmdName(c));
  }
  // phase 2 TODO: read HC-SR04 (D1/D2) every 100 ms,
  // hard-override to STOP if 0 < d < 20 cm, append distance to status
}

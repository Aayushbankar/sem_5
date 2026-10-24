#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* WIFI_SSID = "Airtel_akas_0733";
const char* WIFI_PASS = "Air@27921";

const uint8_t IN1_PIN = 14;  // D5 -> OUT1 left
const uint8_t IN2_PIN = 12;  // D6 -> OUT2 left
const uint8_t IN3_PIN = 13;  // D7 -> OUT3 right
const uint8_t IN4_PIN = 15;  // D8 -> OUT4 right

const unsigned long FAILSAFE_MS = 500;   // > worst Wi-Fi RTT (~134 ms)

ESP8266WebServer server(80);
unsigned long lastCmdMs = 0;
bool driving = false;

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Motor Test</title>
<style>
body{font-family:sans-serif;text-align:center;margin-top:10vh;background:#111;color:#eee}
button{font-size:3rem;padding:2rem 4rem;border:none;border-radius:1rem;background:#2a2;color:#fff;user-select:none;touch-action:none}
button:active{background:#4c4}
p{color:#888}
</style></head><body>
<h1>Motor test</h1>
<button id="go">HOLD - ALL MOTORS</button>
<p>Wheels off the ground. Release = stop.</p>
<script>
const b=document.getElementById('go');
let iv=null;
function send(c){fetch('/drive?c='+c).catch(()=>{});}
function down(e){
  e.preventDefault();
  if(iv)return;
  send('GO');
  iv=setInterval(()=>send('GO'),60);
}
function up(e){
  if(e)e.preventDefault();
  if(iv){clearInterval(iv);iv=null;}
  send('STOP');
}
b.addEventListener('pointerdown',down);
b.addEventListener('pointerup',up);
b.addEventListener('pointerleave',up);
b.addEventListener('pointercancel',up);
document.addEventListener('visibilitychange',()=>{if(document.hidden)up()});
window.addEventListener('pagehide',()=>{up();navigator.sendBeacon('/drive?c=STOP')});
</script>
</body></html>
)rawliteral";

void allLow() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
}

void applyCmd(int cmd) {
  if (cmd == 1) {
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
    digitalWrite(IN3_PIN, HIGH);
    digitalWrite(IN4_PIN, LOW);
    driving = true;
  } else {
    allLow();
    driving = false;
  }
  lastCmdMs = millis();
}

void handleDrive() {
  String c = server.arg("c");
  applyCmd(c == "GO" ? 1 : 0);
  server.send(200, "text/plain", "ok");
}

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void setup() {
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  allLow();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 15000) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(120);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(120);
  }
  digitalWrite(LED_BUILTIN, HIGH);

  if (WiFi.status() == WL_CONNECTED && MDNS.begin("nodemcu")) {
    MDNS.addService("http", "tcp", 80);
  }

  server.on("/", handleRoot);
  server.on("/drive", HTTP_GET, handleDrive);
  server.begin();

  Serial.begin(115200);
  Serial.print("MOTOR TEST ready  http://nodemcu.local  IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  server.handleClient();

  if (driving && millis() - lastCmdMs > FAILSAFE_MS) {
    applyCmd(0);
  }

  static unsigned long lastBlinkMs = 0;
  static bool ledOn = false;
  if (driving && millis() - lastBlinkMs >= 100) {
    lastBlinkMs = millis();
    ledOn = !ledOn;
    digitalWrite(LED_BUILTIN, ledOn ? LOW : HIGH);
  } else if (!driving && ledOn) {
    ledOn = false;
    digitalWrite(LED_BUILTIN, HIGH);
  }
}

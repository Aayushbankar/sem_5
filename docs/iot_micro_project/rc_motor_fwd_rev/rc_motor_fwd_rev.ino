#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* WIFI_SSID = "Airtel_akas_0733";
const char* WIFI_PASS = "Air@27921";

const uint8_t IN1_PIN = 14;  // D5 -> OUT1 left
const uint8_t IN2_PIN = 12;  // D6 -> OUT2 left
const uint8_t IN3_PIN = 13;  // D7 -> OUT3 right
const uint8_t IN4_PIN = 15;  // D8 -> OUT4 right

const unsigned long FAILSAFE_MS = 500;

ESP8266WebServer server(80);
unsigned long lastCmdMs = 0;
bool driving = false;

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Motor Fwd/Rev</title>
<style>
body{font-family:sans-serif;text-align:center;margin-top:8vh;background:#111;color:#eee}
.row{display:flex;gap:1rem;justify-content:center;margin-top:2rem}
button{font-size:2rem;padding:2.5rem 2rem;border:none;border-radius:1rem;color:#fff;user-select:none;touch-action:none;width:40vw}
#fwd{background:#2a2}#fwd:active{background:#4f4}
#rev{background:#a22}#rev:active{background:#f44}
p{color:#888}
</style></head><body>
<h1>Direction test</h1>
<div class="row">
  <button id="fwd">HOLD<br>FWD</button>
  <button id="rev">HOLD<br>REV</button>
</div>
<p>Wheels off the ground. Release = stop.</p>
<script>
const fwd=document.getElementById('fwd');
const rev=document.getElementById('rev');
let iv=null,dir=null;
function send(c){fetch('/drive?c='+c).catch(()=>{});}
function down(d){
  return function(e){
    e.preventDefault();
    if(iv){clearInterval(iv);iv=null;}
    dir=d;send(d);
    iv=setInterval(()=>send(d),60);
  };
}
function up(e){
  if(e)e.preventDefault();
  if(iv){clearInterval(iv);iv=null;}
  dir=null;send('STOP');
}
for(const [el,d] of [[fwd,'FWD'],[rev,'REV']]){
  el.addEventListener('pointerdown',down(d));
  el.addEventListener('pointerup',up);
  el.addEventListener('pointerleave',up);
  el.addEventListener('pointercancel',up);
}
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
  switch (cmd) {
    case 1:  // FWD: left fwd + right fwd
      digitalWrite(IN1_PIN, HIGH);
      digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, HIGH);
      digitalWrite(IN4_PIN, LOW);
      driving = true;
      break;
    case 2:  // REV: both pairs swapped
      digitalWrite(IN1_PIN, LOW);
      digitalWrite(IN2_PIN, HIGH);
      digitalWrite(IN3_PIN, LOW);
      digitalWrite(IN4_PIN, HIGH);
      driving = true;
      break;
    default:  // STOP
      allLow();
      driving = false;
      break;
  }
  lastCmdMs = millis();
}

void handleDrive() {
  String c = server.arg("c");
  if (c == "FWD") applyCmd(1);
  else if (c == "REV") applyCmd(2);
  else applyCmd(0);
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
  Serial.print("FWD/REV test ready  http://nodemcu.local  IP: ");
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

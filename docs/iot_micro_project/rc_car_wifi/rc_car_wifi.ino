// rc_car_wifi — NodeMCU joins phone hotspot, joystick page hosted on the car
// LED: blink = connecting to Wi-Fi, OFF = connected & idle, ON = motors driving
// Failsafe: no drive command for 200 ms -> STOP

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char *WIFI_SSID = "Airtel_akas_0733";
const char *WIFI_PASS = "Air@27921";
const char *MDNS_HOST = "nodemcu";  // http://nodemcu.local

const uint8_t IN1_PIN = 14;  // D5
const uint8_t IN2_PIN = 12;  // D6
const uint8_t IN3_PIN = 13;  // D7
const uint8_t IN4_PIN = 15;  // D8

const unsigned long FAILSAFE_MS = 200;
const unsigned long BLINK_MS = 300;

unsigned long lastCmdMs = 0;
unsigned long lastBlinkMs = 0;
bool ledPhase = false;
bool wifiWasDown = true;
bool mdnsUp = false;

uint8_t lastCmd = 0;  // 0=STOP 1=FWD 2=BACK 3=LEFT 4=RIGHT

ESP8266WebServer server(80);

void applyCmd(uint8_t cmd) {
  switch (cmd) {
    case 1:  // FWD
      digitalWrite(IN1_PIN, HIGH); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, HIGH); digitalWrite(IN4_PIN, LOW);
      break;
    case 2:  // BACK
      digitalWrite(IN1_PIN, LOW);  digitalWrite(IN2_PIN, HIGH);
      digitalWrite(IN3_PIN, LOW);  digitalWrite(IN4_PIN, HIGH);
      break;
    case 3:  // LEFT pivot: left rev, right fwd
      digitalWrite(IN1_PIN, LOW);  digitalWrite(IN2_PIN, HIGH);
      digitalWrite(IN3_PIN, HIGH); digitalWrite(IN4_PIN, LOW);
      break;
    case 4:  // RIGHT pivot: left fwd, right rev
      digitalWrite(IN1_PIN, HIGH); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, LOW);  digitalWrite(IN4_PIN, HIGH);
      break;
    default:  // STOP
      digitalWrite(IN1_PIN, LOW); digitalWrite(IN2_PIN, LOW);
      digitalWrite(IN3_PIN, LOW); digitalWrite(IN4_PIN, LOW);
      break;
  }
}

const char *cmdName(uint8_t c) {
  switch (c) {
    case 1: return "FWD";
    case 2: return "BACK";
    case 3: return "LEFT";
    case 4: return "RIGHT";
    default:return "STOP";
  }
}

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>RC Car</title>
<style>
html,body{margin:0;height:100%;background:#111;color:#eee;font-family:system-ui,sans-serif;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;user-select:none;-webkit-user-select:none;touch-action:none}
h1{font-size:20px;margin:0;letter-spacing:2px}
#st{font-size:14px;color:#f66}
.grid{display:grid;grid-template-columns:repeat(3,96px);grid-template-rows:repeat(3,96px);gap:10px}
button{font-size:22px;font-weight:700;border:0;border-radius:14px;background:#2a2a2e;color:#eee;touch-action:none}
button:active{background:#3d7cff}
.wide{grid-column:2}
</style></head><body>
<h1>RC CAR</h1><div id="st">STOP</div>
<div class="grid">
  <div></div><button data-c="FWD" class="wide">&#9650;</button><div></div>
  <button data-c="LEFT">&#9664;</button>
  <button data-c="STOP" id="stopBtn">&#9632;</button>
  <button data-c="RIGHT">&#9654;</button>
  <div></div><button data-c="BACK" class="wide">&#9660;</button><div></div>
</div>
<script>
let timer=null;
const st=document.getElementById('st');
async function send(c){
  st.textContent=c; st.style.color=(c==='STOP'?'#f66':'#8f8');
  try{await fetch('/drive?c='+c)}catch(e){}
}
function press(c){
  if(timer)clearInterval(timer);
  send(c);
  if(c!=='STOP')timer=setInterval(()=>send(c),60);
}
function release(){
  if(timer){clearInterval(timer);timer=null}
  send('STOP');
}
document.querySelectorAll('button[data-c]').forEach(b=>{
  b.addEventListener('pointerdown',e=>{e.preventDefault();press(b.dataset.c)});
  b.addEventListener('pointerup',release);
  b.addEventListener('pointerleave',()=>{if(timer)release()});
  b.addEventListener('pointercancel',release);
  b.addEventListener('contextmenu',e=>e.preventDefault());
});
document.addEventListener('visibilitychange',()=>{if(document.hidden)release()});
window.addEventListener('pagehide',release);
</script></body></html>
)rawliteral";

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleDrive() {
  if (!server.hasArg("c")) { server.send(400); return; }
  String c = server.arg("c");
  uint8_t cmd = 0;
  if      (c == "FWD")   cmd = 1;
  else if (c == "BACK")  cmd = 2;
  else if (c == "LEFT")  cmd = 3;
  else if (c == "RIGHT") cmd = 4;
  lastCmd = cmd;
  lastCmdMs = millis();
  server.send(200, "text/plain", "ok");
}

void setup() {
  Serial.begin(115200);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);
  applyCmd(0);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);  // off until connect (then blink while connecting)

  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  server.on("/", handleRoot);
  server.on("/drive", handleDrive);
  server.begin();
}

void loop() {
  unsigned long now = millis();

  if (lastCmd != 0 && now - lastCmdMs >= FAILSAFE_MS) {
    lastCmd = 0;
    applyCmd(0);
    Serial.println("FAILSAFE STOP (no command in 200 ms)");
  }

  bool connected = (WiFi.status() == WL_CONNECTED);

  if (!connected) {
    wifiWasDown = true;
    mdnsUp = false;
    if (now - lastBlinkMs >= BLINK_MS) {     // blink = trying to connect
      lastBlinkMs = now;
      ledPhase = !ledPhase;
      digitalWrite(LED_BUILTIN, ledPhase ? LOW : HIGH);
    }
    return;  // no server/mDNS work until connected; failsafe still runs above
  }

  if (wifiWasDown) {
    wifiWasDown = false;
    Serial.print("WiFi OK  IP: ");
    Serial.print(WiFi.localIP());
    if (MDNS.begin(MDNS_HOST)) {
      mdnsUp = true;
      Serial.print("  ->  http://");
      Serial.print(MDNS_HOST);
      Serial.println(".local");
    } else {
      Serial.println("  (mDNS failed)");
    }
  }

  if (mdnsUp) MDNS.update();
  server.handleClient();

  // LED after connect: OFF when idle/stop, ON while driving
  digitalWrite(LED_BUILTIN, (lastCmd != 0) ? LOW : HIGH);
}

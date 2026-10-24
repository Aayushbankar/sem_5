// Handheld remote (ESP32) — SoftAP web UI + ESP-NOW sender
// Phone joins AP "RCCar-ESP32" (pw: 12345678), open http://192.168.4.1

#include <WiFi.h>
#include <esp_now.h>
#include <WebServer.h>

const char *AP_SSID = "RCCar-ESP32";
const char *AP_PASS = "12345678";
const uint8_t MAGIC = 0xA5;
const uint8_t BROADCAST[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

enum Cmd : uint8_t { CMD_STOP = 0, CMD_FWD = 1, CMD_BACK = 2, CMD_LEFT = 3, CMD_RIGHT = 4 };

WebServer server(80);

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>RCCar</title>
<style>
html,body{margin:0;height:100%;background:#111;color:#eee;font-family:system-ui,sans-serif;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;user-select:none;-webkit-user-select:none;touch-action:none}
h1{font-size:20px;margin:0;letter-spacing:2px}
#st{font-size:14px;color:#8f8}
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
  if(c!=='STOP')timer=setInterval(()=>send(c),60);   // refresh: robot failsafe is 200 ms
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
</script></body></html>
)rawliteral";

void sendCmd(uint8_t cmd) {
  uint8_t pkt[2] = {MAGIC, cmd};
  esp_now_send(BROADCAST, pkt, sizeof(pkt));
}

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleDrive() {
  if (!server.hasArg("c")) { server.send(400); return; }
  String c = server.arg("c");
  uint8_t cmd = CMD_STOP;
  if      (c == "FWD")   cmd = CMD_FWD;
  else if (c == "BACK")  cmd = CMD_BACK;
  else if (c == "LEFT")  cmd = CMD_LEFT;
  else if (c == "RIGHT") cmd = CMD_RIGHT;
  sendCmd(cmd);
  server.send(200, "text/plain", "ok");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS);
  Serial.print("AP up: http://");
  Serial.println(WiFi.softAPIP());

  if (esp_now_init() != 0) { Serial.println("ESP-NOW init FAILED"); return; }
  esp_now_register_send_cb([](const esp_now_send_info_t *info, esp_now_send_status_t s) {
    (void)info; (void)s;
  });
  esp_now_peer_info_t peer = {};
  memcpy(peer.peer_addr, BROADCAST, ESP_NOW_ETH_ALEN);
  peer.channel = 0;              // current channel (SoftAP default = 1)
  peer.ifidx = WIFI_IF_AP;
  peer.encrypt = false;
  if (esp_now_add_peer(&peer) != 0) {
    Serial.println("add_peer FAILED");
  }

  server.on("/", handleRoot);
  server.on("/drive", handleDrive);
  server.begin();
  Serial.println("rc_remote ready");
}

void loop() {
  server.handleClient();
}

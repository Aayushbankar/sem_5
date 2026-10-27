// esp_softap — dedicated control LAN for the robot (spare ESP8266)
// Runs as a WPA2 access point; phone + car NodeMCU both join this network.
// Powered from laptop USB. No internet (expected — disable phone auto-switch).
//
//   SSID : CLEANBOT-NET
//   Pass : cleanbot28
//   AP IP: 192.168.4.1   (status page: http://192.168.4.1)
//
// Car must be reflashed with the CLEANBOT-NET variant to join this LAN.

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* AP_SSID = "CLEANBOT-NET";
const char* AP_PASS = "cleanbot28";  // WPA2, >= 8 chars
const uint8_t CHANNEL = 6;

ESP8266WebServer server(80);

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CLEANBOT AP</title>
<style>body{font-family:sans-serif;background:#111;color:#eee;text-align:center;margin-top:10vh}
h1{color:#6f6}span{font-size:2rem;color:#ff6}</style></head>
<body>
<h1>CLEANBOT-NET</h1>
<p>Control LAN status</p>
<p>Clients: <span id="c">?</span></p>
<p>Uptime: <span id="u">?</span> s</p>
<script>
async function tick(){
  const r=await fetch('/status').catch(()=>null);
  if(r){const j=await r.json();c.textContent=j.stations;u.textContent=j.uptime;}
}
setInterval(tick,1500);tick();
</script>
</body></html>
)rawliteral";

void handleRoot() {
  server.send_P(200, "text/html", INDEX_HTML);
}

void handleStatus() {
  String json = "{\"stations\":";
  json += WiFi.softAPgetStationNum();
  json += ",\"uptime\":";
  json += (millis() / 1000);
  json += "}";
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("=== CLEANBOT AP starting ===");

  WiFi.mode(WIFI_AP);
  bool ok = WiFi.softAP(AP_SSID, AP_PASS, CHANNEL, false, 4);

  server.on("/", handleRoot);
  server.on("/status", HTTP_GET, handleStatus);
  server.begin();

  Serial.println(ok ? "AP OK" : "AP FAILED");
  Serial.print("SSID: ");
  Serial.println(AP_SSID);
  Serial.print("IP:   ");
  Serial.println(WiFi.softAPIP());  // 192.168.4.1
}

void loop() {
  server.handleClient();
}

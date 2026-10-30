#include <Arduino.h>
#include <esp_camera.h>
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "Patel's F15";
const char* WIFI_PASS = "123456890";

#define PWDN_GPIO_NUM 32
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22
#define RED_LED 33    // active LOW
#define FLASH_LED 4   // active HIGH

bool camOk = false;
bool wifiOk = false;
WebServer server(80);

void handleRoot() {
  String p = "<h1>ESP32-CAM status</h1><p>CAMERA: ";
  p += camOk ? "<b style='color:green'>OK</b>" : "<b style='color:red'>FAIL</b>";
  p += "<br>WiFi: "; p += wifiOk ? "connected" : "NOT connected";
  p += "<br>IP: " + WiFi.localIP().toString();
  p += "<br>RSSI: " + String(WiFi.RSSI());
  p += "<br>uptime: " + String(millis() / 1000) + "s</p>";
  server.send(200, "text/html", p);
}

void setup() {
  pinMode(RED_LED, OUTPUT); digitalWrite(RED_LED, HIGH);
  pinMode(FLASH_LED, OUTPUT); digitalWrite(FLASH_LED, LOW);
  Serial.begin(115200);

  camera_config_t config = {};
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM; config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM; config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM; config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_DRAM;

  camOk = (esp_camera_init(&config) == ESP_OK);
  Serial.println(camOk ? "CAMERA OK" : "CAMERA FAIL");

  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("WIFI connecting");
  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 20000) {
    delay(500); Serial.print(".");
  }
  wifiOk = (WiFi.status() == WL_CONNECTED);
  Serial.println();
  Serial.println(wifiOk ? "WIFI OK " + WiFi.localIP().toString() : "WIFI FAIL");

  server.on("/", handleRoot);
  server.begin();
}

void loop() {
  if (wifiOk) server.handleClient();
  // red: solid = camera detected, BLINKS while not detected
  if (camOk) digitalWrite(RED_LED, LOW);
  else { digitalWrite(RED_LED, LOW); delay(400); digitalWrite(RED_LED, HIGH); delay(400); }
  // white flash LED: solid = wifi connected, slow blink = trying/failed
  if (wifiOk) { digitalWrite(FLASH_LED, HIGH); }
  else { digitalWrite(FLASH_LED, HIGH); delay(1200); digitalWrite(FLASH_LED, LOW); delay(1200); }
}

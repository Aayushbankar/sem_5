# IOT — Hands on Practice using IoT (DI05016071)

> **w.e.f. 2026-27** · GTU Diploma Engineering · Information Technology

Complete study kit: solved practicals, theory notes, and curated resources.

## 📊 Progress
- Practicals: **[tracker](./PRACTICALS.md)**

## 🧪 Practicals (14)
| # | Practical | Solution | Code |
|---|-----------|----------|------|
| P01 | Study the 4-layer IoT architecture (Smart Home & Industrial IoT) | [P01](./practicals/writeups/P01_iot_architecture_layers.md) | — |
| P02 | Compare Arduino UNO, ESP32 & Raspberry Pi + ESP32 pinout/dual-core | [P02](./practicals/writeups/P02_compare_hardware_platforms_esp32_pinout.md) | — |
| P03 | Study: Arduino IDE configuration for ESP32 + driver install | [P03](./practicals/writeups/P03_arduino_ide_setup_esp32.md) | — |
| P04 | Toggle an external LED (Digital Output), setup()/loop() | [P04](./practicals/writeups/P04_external_led_blink_toggle.md) | [p04_external_led_blink.ino](./practicals/code/p04_external_led_blink.ino) |
| P05 | PIR (Digital Input) + LDR (Analog Input) interface | [P05](./practicals/writeups/P05_pir_ldr_sensor_interface.md) | [p05_pir_ldr_sensor.ino](./practicals/code/p05_pir_ldr_sensor.ino) |
| P06 | DHT11/DHT22 temperature & humidity with DHT library | [P06](./practicals/writeups/P06_dht_temperature_humidity_sensor.md) | [p06_dht_sensor.ino](./practicals/code/p06_dht_sensor.ino) |
| P07 | Ultrasonic (HC-SR04) distance sensor | [P07](./practicals/writeups/P07_ultrasonic_distance_sensor.md) | [p07_ultrasonic_distance.ino](./practicals/code/p07_ultrasonic_distance.ino) |
| P08 | ESP32 as MQTT client publishing DHT data to a public broker | [P08](./practicals/writeups/P08_esp32_mqtt_publisher.md) | [p08_mqtt_publish_dht.ino](./practicals/code/p08_mqtt_publish_dht.ino) |
| P09 | ESP32 MQTT subscriber: remote LED/relay control | [P09](./practicals/writeups/P09_esp32_mqtt_subscriber_remote_control.md) | [p09_mqtt_subscribe_led.ino](./practicals/code/p09_mqtt_subscribe_led.ino) |
| P10 | HTTP GET/POST to ThingSpeak (temperature graphing) | [P10](./practicals/writeups/P10_thingspeak_http_temperature.md) | [p10_thingspeak_http_temperature.ino](./practicals/code/p10_thingspeak_http_temperature.ino) |
| P11 | Ultrasonic distance to ThingSpeak (fill-level dashboard) | [P11](./practicals/writeups/P11_ultrasonic_thingspeak_cloud.md) | [p11_thingspeak_http_ultrasonic.ino](./practicals/code/p11_thingspeak_http_ultrasonic.ino) |
| P12 | Two-way mobile dashboard (Blynk) with virtual-button control | [P12](./practicals/writeups/P12_blynk_two_way_dashboard.md) | [p12_blynk_two_way_dashboard.ino](./practicals/code/p12_blynk_two_way_dashboard.ino) |
| P13 | (a) Soil moisture + DHT on Serial · (b) Cloud upload with thresholds | [P13](./practicals/writeups/P13_soil_moisture_dht_cloud_thresholds.md) | [p13a](./practicals/code/p13a_soil_moisture_dht_serial.ino) + [p13b](./practicals/code/p13b_soil_dht_cloud_threshold.ino) |
| P14 | Mini-project: Smart Agriculture (BOM, wiring, full sketch, dashboards) | [P14](./practicals/writeups/P14_mini_project_smart_agriculture_guide.md) | [p14_smart_agriculture_project.ino](./practicals/code/p14_smart_agriculture_project.ino) |

## 📚 Theory Notes (per unit)
| Unit | Title | Weightage | Notes |
|------|-------|-----------|-------|
| 1 | Introduction to IoT | 10% (4h) | [UNIT_1](./notes/UNIT_1_Introduction_to_IoT.md) |
| 2 | IoT Sensors, Actuators and Hardware Platforms | 25% (6h) | [UNIT_2](./notes/UNIT_2_IoT_Sensors_Actuators_Hardware_Platforms.md) |
| 3 | Introduction to ESP32 & Development with Arduino IDE | 35% (9h) | [UNIT_3](./notes/UNIT_3_ESP32_and_Arduino_IDE_Development.md) |
| 4 | IoT Communication Protocols and Networking | 10% (4h) | [UNIT_4](./notes/UNIT_4_IoT_Communication_Protocols_and_Networking.md) |
| 5 | IoT Cloud Platforms and Applications of IoT | 20% (7h) | [UNIT_5](./notes/UNIT_5_IoT_Cloud_Platforms_and_Applications.md) |

## 🔗 Resources
- [Curated links (docs, drivers, libraries, courses, tools, books, videos)](./notes/RESOURCES.md)

## 🛠 Requirements
- **Hardware:** ESP32 DevKit V1, Micro-USB **data** cable, breadboard + jumpers, LEDs + 220 Ω resistors, DHT11/DHT22, HC-SR04 ultrasonic, PIR (HC-SR501), LDR, soil moisture sensor, relay module, push buttons, potentiometer.
- **Software:** Arduino IDE 2.x (arduino.cc) + Espressif ESP32 board package (see P03).
- **Libraries (Library Manager):** DHT sensor library by Adafruit + Adafruit Unified Sensor, NewPing, PubSubClient, Blynk.
- **Cloud accounts:** ThingSpeak (P10–P13, P14), Blynk (P12), plus free **MQTTX** / Mosquitto clients (P08–P09, P14).
- **Docs-only practicals (P01–P03):** no hardware — diagrams and setup walkthrough.

## ⚠️ Exam tips
- Unit 3 (35%) is the heaviest — master ESP32 features, GPIO/ADC/PWM, and the Wi-Fi connect block.
- Practical viva favourites: setup()/loop(), why GPIO 34–39 are input-only, ultrasonic formula, MQTT QoS/topics, ThingSpeak 15 s limit, relay LOW-active logic.
- This subject is 100% practical assessment (PA-I 50 + ESE-Viva 50) — run every sketch on real hardware; the "Verify on hardware" checklist in each writeup is your revision guide.
- Short-note favourites per unit: 4-layer architecture, sensor classification, actuator types, ESP32 features, MQTT vs CoAP vs XMPP, M2M vs IoT, cloud types, Smart Agriculture.

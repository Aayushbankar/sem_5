---
subject: IOT
full_name: Hands on Practice using IoT
code: DI05016071
units: 5
practicals: 14
status: not-started
tags: [subject/iot, dashboard]
---
# 🌐 Hands on Practice using IoT

> **DI05016071** · w.e.f. 2026-27 · GTU Diploma IT · Sem 5

---

## 📚 Theory Units

| Unit | Note | Status |
|---|---|---|
| Unit 1 | [[Unit 1 — Introduction to IoT]] | ⬜ |
| Unit 2 | [[Unit 2 — IoT Sensors Actuators Hardware Platforms]] | ⬜ |
| Unit 3 | [[Unit 3 — ESP32 and Arduino IDE Development]] | ⬜ |
| Unit 4 | [[Unit 4 — IoT Communication Protocols and Networking]] | ⬜ |
| Unit 5 | [[Unit 5 — IoT Cloud Platforms and Applications]] | ⬜ |

---

## 🧪 Practicals (14)

| # | Practical | Status |
|---|---|---|
| P01 | [[P01 — Iot Architecture Layers]] | ⬜ |
| P02 | [[P02 — Compare Hardware Platforms Esp32 Pinout]] | ⬜ |
| P03 | [[P03 — Arduino Ide Setup Esp32]] | ⬜ |
| P04 | [[P04 — External Led Blink Toggle]] | ⬜ |
| P05 | [[P05 — Pir Ldr Sensor Interface]] | ⬜ |
| P06 | [[P06 — Dht Temperature Humidity Sensor]] | ⬜ |
| P07 | [[P07 — Ultrasonic Distance Sensor]] | ⬜ |
| P08 | [[P08 — Esp32 Mqtt Publisher]] | ⬜ |
| P09 | [[P09 — Esp32 Mqtt Subscriber Remote Control]] | ⬜ |
| P10 | [[P10 — Thingspeak Http Temperature]] | ⬜ |
| P11 | [[P11 — Ultrasonic Thingspeak Cloud]] | ⬜ |
| P12 | [[P12 — Blynk Two Way Dashboard]] | ⬜ |
| P13 | [[P13 — Soil Moisture Dht Cloud Thresholds]] | ⬜ |
| P14 | [[P14 — Mini Project Smart Agriculture Guide]] | ⬜ |

---

## 💻 Code Files

- [[p04_external_led_blink.ino]]
- [[p05_pir_ldr_sensor.ino]]
- [[p06_dht_sensor.ino]]
- [[p07_ultrasonic_distance.ino]]
- [[p08_mqtt_publish_dht.ino]]
- [[p09_mqtt_subscribe_led.ino]]
- [[p10_thingspeak_http_temperature.ino]]
- [[p11_thingspeak_http_ultrasonic.ino]]
- [[p12_blynk_two_way_dashboard.ino]]
- [[p13a_soil_moisture_dht_serial.ino]]
- [[p13b_soil_dht_cloud_threshold.ino]]
- [[p14_smart_agriculture_project.ino]]

---

## 🔗 Quick Links

- [[IOT Resources|🔗 Resources]]
- [[IOT Practical Tracker|📋 Practical Tracker]]
- [[246230316006_tutorial1.pdf|📄 Syllabus (PDF)]]
- [[DI05016071-IOT.pdf|📄 Syllabus (PDF)]]

---

## ⚠️ Exam Tips

- Unit 3 (35%) is the heaviest — master ESP32 features, GPIO/ADC/PWM, and the Wi-Fi connect block.
- Practical viva favourites: setup()/loop(), why GPIO 34–39 are input-only, ultrasonic formula, MQTT QoS/topics, ThingSpeak 15 s limit, relay LOW-active logic.
- This subject is 100% practical assessment (PA-I 50 + ESE-Viva 50) — run every sketch on real hardware; the "Verify on hardware" checklist in each writeup is your revision guide.
- Short-note favourites per unit: 4-layer architecture, sensor classification, actuator types, ESP32 features, MQTT vs CoAP vs XMPP, M2M vs IoT, cloud types, Smart Agriculture.

---

## 🛠️ Requirements

- **Hardware:** ESP32 DevKit V1, Micro-USB **data** cable, breadboard + jumpers, LEDs + 220 Ω resistors, DHT11/DHT22, HC-SR04 ultrasonic, PIR (HC-SR501), LDR, soil moisture sensor, relay module, push buttons, potentiometer.
- **Software:** Arduino IDE 2.x (arduino.cc) + Espressif ESP32 board package (see P03).
- **Libraries (Library Manager):** DHT sensor library by Adafruit + Adafruit Unified Sensor, NewPing, PubSubClient, Blynk.
- **Cloud accounts:** ThingSpeak (P10–P13, P14), Blynk (P12), plus free **MQTTX** / Mosquitto clients (P08–P09, P14).
- **Docs-only practicals (P01–P03):** no hardware — diagrams and setup walkthrough.

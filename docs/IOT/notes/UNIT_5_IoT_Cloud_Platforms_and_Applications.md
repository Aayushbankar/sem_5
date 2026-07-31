# UNIT 5 — IoT Cloud Platforms & Applications of IoT ☁️

> **Hands on Practice using IoT (DI05016071)** · **7 hrs · 20% weightage**
> **Covers syllabus sections:** 5.1 Cloud Computing (concept, public/private/hybrid) · 5.2 Role of Cloud in IoT · 5.3 Cloud Platforms (ThingSpeak, Blynk IoT, Arduino IoT Cloud) · 5.4 Categories of Applications (Consumer, Commercial, Industrial, Infrastructure, Medical) · 5.5 Smart Home · 5.6 Smart Agriculture · 5.7 Smart Health Monitoring · 5.8 Smart Parking · 5.9 Smart City (street lighting, waste, environmental monitoring)
> **Related practicals:** [P10](../practicals/writeups/P10_thingspeak_http_temperature.md), [P11](../practicals/writeups/P11_ultrasonic_thingspeak_cloud.md), [P12](../practicals/writeups/P12_blynk_two_way_dashboard.md), [P13](../practicals/writeups/P13_soil_moisture_dht_cloud_thresholds.md), [P14](../practicals/writeups/P14_mini_project_smart_agriculture_guide.md)

---

## 🧭 Chapter Roadmap

20% weightage and **five practicals (P10–P14)** — the cloud unit is where the course turns from "sensors on a desk" into real IoT products. The exam loves the platform names, the application categories, and one specific smart application described end-to-end.

```
UNIT 5: Cloud Platforms & IoT Applications
├── 5.1 Introduction to Cloud Computing            ⭐⭐ (public/private/hybrid)
├── 5.2 Role of Cloud in IoT                       ⭐⭐ (the 4 reasons)
├── 5.3 IoT Cloud Platforms                        ⭐⭐⭐ (ThingSpeak · Blynk · Arduino IoT Cloud)
│     └── 5.3.1 Features + basic implementation (channel/datastream/widget)
├── 5.4 Categories of IoT Applications             ⭐⭐⭐ (5 categories table)
├── 5.5 Smart Home Automation                      ⭐⭐⭐
├── 5.6 Smart Agriculture System                   ⭐⭐⭐ (the P14 project!)
├── 5.7 Smart Health Monitoring                    ⭐⭐
├── 5.8 Smart Parking System                       ⭐⭐
└── 5.9 Smart City Applications                    ⭐⭐ (street lighting · waste · environment)
      └── 5.9.1-5.9.3 the three smart-city systems
```

### Learning outcomes — after this unit you can:
1. Define **cloud computing**, name the **three deployment types**, and state the **role of cloud in IoT**.
2. Compare **ThingSpeak, Blynk IoT and Arduino IoT Cloud** and describe the basic implementation flow of each.
3. Classify IoT applications into the **five categories** (Consumer/Commercial/Industrial/Infrastructure/Medical).
4. Describe **Smart Home, Smart Agriculture, Smart Health, Smart Parking** end-to-end (sensors → cloud → app).
5. Describe the three **Smart City** systems: street lighting, waste management, environmental monitoring.

---

## 5.1 Introduction to Cloud Computing ⭐⭐

> **Definition (memorize):** Cloud computing delivers **computing resources — servers, storage, databases, analytics, software — over the internet on demand**, paying only for what you use ("utility" computing).

**Three deployment types (the exam table):**

| Type | Who owns/manages it | Access | Example |
|---|---|---|---|
| **Public cloud** | A cloud provider (AWS, Azure, Google) | Open to anyone on the internet | ThingSpeak public channel |
| **Private cloud** | A single organisation, dedicated | Only that organisation | A hospital's private patient-data cloud |
| **Hybrid cloud** | Mix of public + private | Sensitive data on-premise, bursts to public | Bank: private ledger + public analytics |

> 💡 **Link to Unit 1 (CAP/architecture):** the public cloud is a *centralised* system — the "Data Processing" layer of the 4-layer architecture (P01) lives here.

## 5.2 Role of Cloud in IoT ⭐⭐

Why the ESP32 cannot be the whole system:

| Role | What the cloud adds | Practical evidence |
|---|---|---|
| **Storage** | Stores years of sensor history | ThingSpeak fields (P10–P13) |
| **Processing/analytics** | Rules, ML, dashboards run there | Threshold React apps (P13) |
| **Visualization** | Graphs & dashboards accessible anywhere | ThingSpeak/Blynk widgets (P10–P12) |
| **Control/actuation** | Commands routed back to devices | Blynk virtual button (P12), MQTT control (P09) |
| **Scalability** | Millions of devices with one dashboard | — |

```mermaid
flowchart TD
    ESP[ESP32 nodes] -- MQTT / HTTP --> CLOUD[Cloud platform]
    CLOUD --> STORE[(Sensor database)]
    CLOUD --> GRAPH[Charts & dashboards]
    CLOUD --> RULE[Threshold rules]
    RULE --> ALERT[Alerts]
    PHONE[Mobile app] <-- data + commands --> CLOUD
    PHONE -- command --> ESP
```

## 5.3 IoT Cloud Platforms ⭐⭐⭐ (the three syllabus platforms)

### 5.3.1 ThingSpeak
- **MathWorks** analytics platform; channel-based (up to **8 fields**), free tier.
- Data in via **HTTP GET/POST** (`/update?api_key=KEY&field1=value`) or **MQTT** (`mqtt.thingspeak.com`).
- **Rate limit:** one update per **15 s** (free).
- **Extra tools:** React (threshold-triggered alerts), MATLAB Analysis, public/private channels.
- **Implementation flow (P10/P11):** create channel → copy Write API Key → ESP32 sends `field1=temp` every 20 s → dashboard graphs appear.

### 5.3.2 Blynk IoT (Blynk 2.0)
- Mobile-first IoT platform with a **web console + mobile app**.
- **Template → Datastreams (virtual pins V0, V1…) → Devices → Widgets** (Gauge, Switch, Slider).
- Two-way by design: `Blynk.virtualWrite(V0, value)` up; `BLYNK_WRITE(V1)` down (P12).
- Firmware uses the **Blynk library** with `BLYNK_TEMPLATE_ID` / `BLYNK_AUTH_TOKEN`.

### 5.3.3 Arduino IoT Cloud
- Official Arduino platform; auto-generates **code from a dashboard**, based on **Thing Properties** (like Blynk datastreams).
- Device registered via the **Arduino IoT Cloud** web console; sketch built on the ESP32 core with `ArduinoIoTCloud` + `Arduino_ConnectionHandler` libraries.
- Great for people already at home in the Arduino IDE — you define properties, the IDE generates the connection skeleton.

| Criterion | ThingSpeak | Blynk IoT | Arduino IoT Cloud |
|---|---|---|---|
| Focus | Analytics & graphing | Two-way mobile control | Arduino-centric device cloud |
| Data input | HTTP / MQTT | MQTT (library) | MQTT (auto-generated) |
| Key concept | Channel/field | Template/datastream/widget | Thing/property |
| Best for | Graphs & analysis (P10–P13) | Phone control (P12, P14) | Beginners in Arduino ecosystem |
| Free tier | 15 s updates, 8 fields | Limited devices/datastreams | Limited properties |

## 5.4 Categories of IoT Applications ⭐⭐⭐

| Category | What it covers | Examples |
|---|---|---|
| **Consumer IoT** | Personal/domestic devices | Smart watches, smart speakers, smart-home lights |
| **Commercial IoT** | Business/retail/office | Smart vending machines, retail analytics, office HVAC |
| **Industrial IoT (IIoT)** | Factories/plants | Predictive maintenance, SCADA, robotic assembly |
| **Infrastructure IoT** | Cities & public utilities | Smart street lighting, water/waste grids |
| **Medical IoT** | Healthcare & wearables | Heart-rate monitors, connected infusion pumps, hospital asset tracking |

> 💡 **Viva link:** the P14 mini-project categories — Smart Home (consumer), Smart Agriculture (commercial/industrial), Smart Health (medical), Smart Parking + Smart City (infrastructure). Point at which category your project belongs to.

## 5.5 Smart Home Automation ⭐⭐⭐

**Goal:** comfort, security and energy savings in a home via automated sensing + remote control.

```
PIR (motion) ─┐
LDR (light) ──┼─► ESP32 ──► Blynk/cloud ──► phone app
DHT (climate) ┘                    │
                                   ▼
              "motion + dark" rule ──► relay ──► lights ON
              phone button ──────────► relay ──► fan/AC ON
```

| Component | Device | Practical basis |
|---|---|---|
| Occupancy | PIR sensor | P05 |
| Ambient light | LDR | P05 |
| Climate | DHT11/22 | P06 |
| Actuation | Relay-module lights/fan | P09, P12 |
| Control/dash | Blynk app | P12 |

## 5.6 Smart Agriculture System ⭐⭐⭐ (this is P14)

**Goal:** efficient irrigation — water only when the soil is actually dry.

```
Soil moisture ─┐
DHT temp/hum ──┼─► ESP32 ──► ThingSpeak/Blynk ──► farm dashboard
Ultrasonic (tank) ┘        │
              soil < 2000 ─┴──► relay ──► water pump ON (auto + manual override)
```

| Feature | Implementation |
|---|---|
| Sensing | Soil moisture (GPIO 34), DHT (GPIO 4), optional ultrasonic tank level |
| Decision | Threshold + hysteresis in the ESP32 (edge processing) |
| Actuation | Relay → water pump; manual override from phone (MQTT/Blynk) |
| Cloud | ThingSpeak graphs + alerts; Blynk for control |
| Benefits | ~30% water saved, remote farm monitoring |

> **Exam one-liner:** "Smart Agriculture closes the loop — sensor detects dry soil, the controller starts the pump, and the farmer watches it all from a phone." (Full walkthrough in [P14](../practicals/writeups/P14_mini_project_smart_agriculture_guide.md).)

## 5.7 Smart Health Monitoring ⭐⭐

**Goal:** continuous vital-sign tracking with alerts instead of periodic manual checks.

- **Sensors:** heart-rate/SpO2 (MAX30100/MAX30102), body temp (DHT22/MLX90614), motion (PIR/accelerometer).
- **Device:** wearable ESP32/BLE node → cloud.
- **Cloud:** stores vitals, triggers alerts when HR > threshold; doctor sees trends.
- **Examples:** smart watches, elderly fall detection, connected insulin pumps, hospital patient monitoring.

## 5.8 Smart Parking System ⭐⭐

**Goal:** show real-time free/occupied slots and guide drivers, reducing traffic circling.

- **Sensing:** HC-SR04 or inductive loop per slot — `distance < threshold → occupied` (P07/P11 logic).
- **Device:** ESP32 per slot (or multi-slot node) → cloud.
- **Cloud/app:** map of the lot with green/red slots; automated barrier and payment.
- **Exam point:** "occupancy = distance below threshold" is a direct reuse of P11.

## 5.9 Smart City Applications ⭐⭐

### 5.9.1 Smart street lighting 💡
- **LDR** detects dusk → lights ON; **PIR** dims lights when nobody is nearby (P05 sensors!).
- LED lights + central dashboard per-strip; **saves up to 50% energy**.

### 5.9.2 Waste management 🗑️
- **Ultrasonic** inside each bin measures fill level (P11).
- When fill > 80% → alert topic → municipal dashboard lists bins needing pickup → optimised routes.

### 5.9.3 Environmental monitoring 🌦️
- **Weather nodes:** DHT22, rain sensor, air-quality sensor (MQ-135), LDR.
- Continuous upload to ThingSpeak → **predictive alerts** (high AQI, flooding risk, heat wave).

```mermaid
flowchart LR
    ST[Street light<br/>LDR + PIR] --> C[City cloud]
    WM[Waste bin<br/>ultrasonic level] --> C
    ENV[Env node<br/>DHT + AQI] --> C
    C --> DASH[City dashboard]
    C --> ALERT[Alerts to officials]
```

---

## 🧠 Deep-Dive Topics

### Deep Dive A: The ThingSpeak "field1" pipeline (P10–P13, memorise)
`ESP32 → HTTP GET http://api.thingspeak.com/update?api_key=KEY&field1=27.4 → ThingSpeak stores + graphs → dashboard widget`. The 15-second rate limit forces `INTERVAL = 20000` in the sketches; HTTP code 200 + entry-id confirms a successful write; `-1` means bad key/network. This pipeline appears in P10, P11 and P13 — describe it once, reuse it three times.

### Deep Dive B: Blynk's two-way virtual pins (P12)
Datastream V0 = sensor values **up** (`Blynk.virtualWrite(V0, t)`), datastream V1 = phone switch **down** (`BLYNK_WRITE(V1)` → `param.asInt()` → `digitalWrite`). This up/down split is *the* exam answer for "what makes a dashboard two-way?" — and the same pattern reappears in P14's pump control.

### Deep Dive C: Edge vs Cloud decisions (P13/P14)
Thresholds live in **two places**: on the ESP32 (instant, works offline — P13's `ALERT: Soil DRY`) and in the cloud (ThingSpeak React apps, works for all devices at once). Smart design puts *fast safety-critical* decisions at the edge and *analytics* in the cloud — a great "role of cloud" extension answer.

---

## 🚀 Beyond the Textbook

1. **All three platforms speak MQTT underneath.** ThingSpeak, Blynk and Arduino IoT Cloud are *clients* of MQTT brokers (or their own); the ESP32's `PubSubClient` (P08/P09) is the common substrate.
2. **Public brokers vs managed clouds:** `broker.emqx.io` is open (anyone can read your topics); ThingSpeak/Blynk add authentication and storage on top. That's the security difference between P09 and P10.
3. **The free tiers are the limit, not the hardware.** ThingSpeak's 15 s cap and Blynk's datastream limits are *platform* constraints — the ESP32 can publish far faster. Know which layer imposes the limit.
4. **Green IoT is a real angle:** LDR street lights, threshold-based irrigation and low-power deep-sleep nodes all cut energy — a strong line for any "challenges/sustainability" question.
5. **Digital twins** (a live virtual copy of the device state) are the industry extension of a dashboard — ThingSpeak/Blynk are tiny prototypes of that idea.

---

## 🎯 High-Yield Exam Topics (likely GTU-style questions)

1. Define **cloud computing** and explain **public, private, hybrid** clouds. (4–7 m) ⭐⭐⭐
2. Explain the **role of cloud in IoT**. (4 m) ⭐⭐⭐
3. Short note: **ThingSpeak** — channel, fields, API key, implementation. (7 m) ⭐⭐⭐ (≈ P10/P11)
4. Short note: **Blynk IoT** — template, datastreams, virtual pins, two-way control. (7 m) ⭐⭐⭐ (≈ P12)
5. Compare **ThingSpeak, Blynk and Arduino IoT Cloud**. (4 m) ⭐⭐
6. Short note: **categories of IoT applications** (five categories). (4 m) ⭐⭐⭐
7. Describe a **Smart Home Automation** system end-to-end. (7 m) ⭐⭐⭐
8. Describe a **Smart Agriculture** system end-to-end. (7 m) ⭐⭐⭐ (≈ P14)
9. Short note: **Smart Health Monitoring**. (4–7 m) ⭐⭐
10. Short note: **Smart Parking System**. (4 m) ⭐⭐
11. Short note: **Smart City applications** (street lighting, waste management, environmental monitoring). (7 m) ⭐⭐⭐
12. Why is the cloud needed when the ESP32 can already process data? (3–4 m) ⭐⭐

### ✅ Solved model answers (highest-yield)

**Q1. (4–7 m) — Cloud computing: concept + types.**
> Cloud computing delivers computing resources — servers, storage, databases, analytics, software — **over the internet on demand**, billed like a utility. **Public cloud** is owned and operated by a provider (AWS, Azure, Google) and shared by many tenants; **private cloud** is dedicated to a single organisation, giving more control and compliance; **hybrid cloud** combines both — sensitive workloads stay private while elastic workloads run in the public cloud. In IoT, the cloud forms the **data-processing and application layers** of the architecture: it stores sensor history, runs analytics and serves dashboards that the low-power ESP32 node cannot host itself.

**Q3. (7 m) — Short note: ThingSpeak with implementation.**
> ThingSpeak is a free **IoT analytics platform** from MathWorks built around **channels**, each holding up to **8 fields**. Implementation flow (used in P10/P11/P13): (1) create a channel and enable the required fields (e.g., Field 1 = Temperature); (2) copy the **Write API Key** from the API Keys tab; (3) the ESP32 uploads data via HTTP GET — `http://api.thingspeak.com/update?api_key=KEY&field1=27.4` — every 20 s (free tier allows one update per 15 s); (4) ThingSpeak stores each value and plots it on the field's chart; (5) extra features: **React apps** fire alerts when a value crosses a threshold, **MATLAB Analysis** runs custom computations, and channels can be made public or private. A successful write returns HTTP 200 with an entry id; a `-1` response indicates a bad key or throttling.

**Q7. (8 m) — Smart Home Automation end-to-end.**
> A smart home senses its environment, automates responses and allows remote control. **Sensing:** a PIR detects presence, an LDR measures ambient light, and a DHT11 tracks temperature/humidity — all read by an ESP32 (P05/P06). **Processing/decision:** the ESP32 applies rules such as "if motion AND light level low → turn on the light" (threshold logic). **Actuation:** a relay module switches the light/fan (P09/P12). **Cloud & app:** the ESP32 uploads readings to Blynk/ThingSpeak; the user sees a live dashboard and presses a virtual switch to control the appliance from anywhere (P12). **Benefits:** energy saving (lights off when nobody is home), comfort (climate control), and security (motion alerts). This is the **Consumer IoT** category of applications.

---

## ✍️ Practice Problems (self-test — answers hidden)

1. Public, private, hybrid cloud — one line each with an IoT example.
2. List four roles the cloud plays in an IoT system.
3. What is the ThingSpeak free-tier rate limit and how does it shape the sketch's `INTERVAL`?
4. Name the key concept of each platform: ThingSpeak ___, Blynk ___, Arduino IoT Cloud ___.
5. Which category of IoT does each P14 alternative fall into: smart parking, smart health, smart street lighting?
6. Describe Smart Agriculture in four steps (sense → decide → act → show).
7. How does a Blynk virtual button control a GPIO? Name the two Blynk API calls.
8. Give one sensor + one action for each smart-city system (lighting, waste, environment).

<details>
<summary>📌 Model solutions</summary>

1. Public — provider-owned, open (ThingSpeak public channel); Private — single organisation (hospital records); Hybrid — mix (bank private ledger + public analytics).
2. Storage, processing/analytics, visualization/dashboards, remote control/actuation, scalability.
3. One update per 15 s (free) → practical sketches use `INTERVAL = 20000` (20 s) to stay legal.
4. ThingSpeak → **channel/field**; Blynk → **template/datastream/widget**; Arduino IoT Cloud → **thing/property**.
5. Smart parking — infrastructure; smart health — medical; smart street lighting — infrastructure.
6. Sense (soil moisture + DHT) → decide (threshold + hysteresis on ESP32) → act (relay → pump) → show (ThingSpeak/Blynk dashboard + remote override).
7. `Blynk.virtualWrite(V0, value)` pushes sensor data up; `BLYNK_WRITE(V1)` + `param.asInt()` receives the button state down and calls `digitalWrite()`.
8. Lighting — LDR detects dusk → lights ON; Waste — ultrasonic fill level > 80% → pickup alert; Environment — DHT/AQI node → predictive alert.
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **Cloud computing** | On-demand delivery of computing resources over the internet |
| **Public cloud** | Provider-owned, multi-tenant services (AWS, Azure) |
| **Private cloud** | Dedicated cloud for one organisation |
| **Hybrid cloud** | Combination of public + private |
| **ThingSpeak** | MathWorks IoT analytics platform (channels, 8 fields) |
| **Write API Key** | Secret that authenticates uploads to a channel |
| **Channel** | ThingSpeak container for up to 8 data fields |
| **React app** | ThingSpeak rule that triggers alerts on thresholds |
| **Blynk IoT** | Mobile-first two-way IoT platform (templates, datastreams) |
| **Datastream** | Blynk virtual pin (V0, V1…) with type/unit |
| **`BLYNK_WRITE(Vn)`** | Callback for commands arriving from the cloud |
| **`virtualWrite()`** | ESP32 → cloud value push |
| **Auth token** | Per-device secret for Blynk/Arduino IoT Cloud |
| **Arduino IoT Cloud** | Official Arduino platform (things, properties) |
| **Consumer IoT** | Personal/domestic devices |
| **Commercial IoT** | Retail/office/business systems |
| **Industrial IoT** | Factory/plant automation |
| **Infrastructure IoT** | City utilities and public systems |
| **Medical IoT** | Healthcare devices and wearables |
| **Smart Agriculture** | Sensor-driven irrigation/farming (P14) |
| **Smart Parking** | Occupancy detection for parking lots |
| **Smart street lighting** | LDR/PIR-based energy-saving lights |

---

## 🔗 Curated Resources (per concept)

**Cloud computing**
- Cloud computing basics (AWS): https://aws.amazon.com/what-is-cloud-computing/
- Public/private/hybrid (Google Cloud): https://cloud.google.com/learn/what-is-cloud-computing

**ThingSpeak (official)**
- ThingSpeak: https://thingspeak.com/
- ThingSpeak docs: https://docs.thingspeak.com/en/
- HTTP API reference: https://docs.thingspeak.com/en/reference/http/

**Blynk (official)**
- Blynk IoT: https://blynk.io/
- Blynk docs (quickstart): https://docs.blynk.io/en/
- Blynk library: https://github.com/blynkkk/blynk-library

**Arduino IoT Cloud (official)**
- Arduino IoT Cloud: https://cloud.arduino.cc/
- Arduino IoT Cloud docs: https://docs.arduino.cc/arduino-cloud/

**Applications (Smart Home / City / Health)**
- Smart agriculture systems (FAO/WMO): https://www.fao.org/3/ca6407en/ca6407en.pdf
- Smart city use cases: https://www.ibm.com/topics/smart-cities
- Digital health/IoMT: https://www.who.int/health-topics/health-and-digital-technologies

**Tutorials**
- ESP32 + ThingSpeak: https://randomnerdtutorials.com/esp32-thingspeak/
- ESP32 + Blynk: https://randomnerdtutorials.com/esp32-blynk-iot/
- ESP32 + Arduino IoT Cloud: https://randomnerdtutorials.com/esp32-arduino-iot-cloud/

**Books (from GTU syllabus)**
- David Hanes, *IoT Fundamentals: Networking Technologies, Protocols and Use Cases*, Cisco Press, 2017 — Part on IoT use cases & cloud.
- Arshdeep Bahga & Vijay Madisetti, *Internet of Things: A Hands-on Approach*, 2015 — cloud chapters.
- Adrian McEwen & Hakim Cassimally, *Designing the Internet of Things*, Wiley, 2014.

**Videos (high yield)**
- Random Nerd Tutorials ThingSpeak/Blynk playlists · edureka! IoT cloud tutorials · Simply Explained cloud computing.

---

## 🎥 Video Study Guide (YouTube)

> Don't like reading? Me neither. This is your **structured video path** for the whole unit — better than the syllabus because it tells you *exactly what to search* and *what to watch first*, in a sensible order. Everything below is search keywords (they never rot like links do) + channels you can trust.

### 🧑🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | Watch 1 explainer per topic from the table below (3–8 min each) |
| 🛠️ **Builder** | wiring things yourself | Watch the ThingSpeak/Blynk build-alongs → run [P10](../practicals/writeups/P10_thingspeak_http_temperature.md)–[P12](../practicals/writeups/P12_blynk_two_way_dashboard.md) |
| 🔧 **Tinkerer** | experimenting & demos | Watch demo videos → create your own channel/widgets and push values |
| 🧠 **Deep Diver** | full theory, "why" | Watch the whole-unit playlists at the bottom (university-level depth) |
| 🧭 **Explorer** | breadth & curiosity | Watch the "smart city / smart home" case-study videos first, then follow your curiosity |
| 🎓 **Academic** | exam marks | Watch the revision/GTU-style videos, then grind the High-Yield questions above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| Cloud computing basics | `cloud computing explained simply` · `public private hybrid cloud` · `what is the cloud` | Simply Explained, IBM Technology, PowerCert | 🎧 + 🧭 |
| Cloud + IoT | `role of cloud in iot` · `iot cloud architecture` · `why does iot need cloud` | edureka!, IBM Technology | 🎧 + 🎓 |
| ThingSpeak hands-on | `thingspeak tutorial esp32` · `thingspeak channel setup api key` · `send sensor data to thingspeak` | Random Nerd Tutorials, DroneBot Workshop, Core Electronics | 🛠️ Builder |
| ThingSpeak React & MATLAB | `thingspeak react app tutorial` · `thingspeak matlab analysis` | MathWorks, Paul McWhorter | 🔧 + 🧠 |
| Blynk IoT hands-on | `blynk iot setup tutorial` · `esp32 blynk two way control` · `blynk virtual pin v1 switch` | Random Nerd Tutorials, Core Electronics, Blynk | 🛠️ Builder |
| Arduino IoT Cloud | `arduino iot cloud tutorial esp32` · `arduino cloud things properties` | Random Nerd Tutorials, Arduino | 🛠️ Builder |
| IoT application categories | `iot application domains` · `consumer industrial iot examples` · `types of iot applications` | edureka!, IBM Technology | 🎧 + 🎓 |
| Smart home & agriculture | `smart home automation explained` · `smart agriculture iot system` · `iot irrigation system project` | edureka!, TechTerms, Random Nerd Tutorials | 🧭 Explorer |
| Smart city systems | `smart city explained` · `smart street lighting system` · `smart waste management iot` · `smart parking system iot` | edureka!, TechTerms, Intellipaat | 🧭 + 🎓 |
| Whole-unit revision (exam mode) | `iot cloud platforms unit notes` · `thingspeak blynk comparison` · `iot applications full lecture` | Neso Academy, Gate Smashers, edureka! | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"edureka! — IoT Full Course / IoT in 10 hours"** — covers cloud, platforms and every application category at university depth.
2. **"Random Nerd Tutorials — ESP32 with ThingSpeak & Blynk playlists"** — the exact hands-on flow of P10–P14, step by step.
3. **"MathWorks — ThingSpeak tutorials"** — official channel, MATLAB Analysis and React apps for the extra-marks tools.

### 🎬 Step 3 — Proof you got it (5 min)

- Describe Smart Agriculture in exactly four steps (sense → decide → act → show) without notes.
- Log into ThingSpeak, create a channel, and push one value with a browser URL — if the graph plots, the platform is yours.
- Name the five IoT application categories and put the P14 alternatives into them.

---

*Back to: [UNIT 1 — Introduction to IoT](./UNIT_1_Introduction_to_IoT.md)*

---
subject: IOT
status: not-started
tags: [subject/iot, unit/3]
unit: 3
title: "Introduction to ESP32 & Development with Arduino IDE"
hours: 9
weightage: "35%"
related_practicals: [P03, P04]
---
# UNIT 3 — Introduction to ESP32 & Development with Arduino IDE ⚡

> **Hands on Practice using IoT (DI05016071)** · **9 hrs · 35% weightage**
> **Covers syllabus sections:** 3.1 Introduction to ESP32 (overview, features, dual-core, memory, peripherals) · 3.2 Development Environment (Arduino IDE, board package, drivers, ports) · 3.3 GPIO Programming (pins, digital I/O, ADC, PWM) · 3.4 Core Libraries & Wi-Fi Programming · 3.5 Basic Interfacing (LED, push button, DHT sensor, actuators)
> **Related practicals:** [[P03 — Arduino Ide Setup Esp32|P03]], [[P04 — External Led Blink Toggle|P04]], [[P05 — Pir Ldr Sensor Interface|P05]], [[P06 — Dht Temperature Humidity Sensor|P06]], [[P07 — Ultrasonic Distance Sensor|P07]]

---

## 🧭 Chapter Roadmap

**35% — the heaviest unit in the subject.** Almost every practical (P03–P07) is pure ESP32 + Arduino IDE. If you can draw the ESP32 feature list, explain `setup()`/`loop()`, read a pin, and connect Wi-Fi, you have already scored the practical ESE. Nail this unit.

```
UNIT 3: ESP32 & Arduino IDE
├── 3.1 Introduction to ESP32                  ⭐⭐⭐ (feature list = guaranteed)
│     ├── 3.1.1 Overview & features
│     ├── 3.1.2 Dual-core processor
│     ├── 3.1.3 Memory organisation
│     └── 3.1.4 Built-in peripherals (Wi-Fi, BT, ADC, DAC, PWM)
├── 3.2 Development Environment                ⭐⭐⭐ (P03: step-by-step setup)
│     ├── 3.2.1 Installing Arduino IDE
│     ├── 3.2.2 Board package & drivers
│     └── 3.2.3 IDE interface & tools
├── 3.3 GPIO Programming                       ⭐⭐⭐ (setup()/loop() + pins)
│     ├── 3.3.1 GPIO pins, numbering
│     ├── 3.3.2 Digital input & output
│     ├── 3.3.3 Analog input (ADC)
│     └── 3.3.4 Analog output / PWM
├── 3.4 Core Libraries & Wi-Fi                 ⭐⭐⭐ (WiFi.h: connect + IP)
│     ├── 3.4.1 ESP32 core libraries & Library Manager
│     └── 3.4.2 Wi-Fi library, status, IP
└── 3.5 Basic Interfacing Concepts             ⭐⭐⭐ (LED · button · DHT · relay)
      └── 3.5.1-3.5.4 The four basic circuits
```

### Learning outcomes — after this unit you can:
1. List and explain **ESP32 features**: dual-core CPU, memory, and the built-in Wi-Fi/BT/ADC/DAC/PWM peripherals.
2. Recreate the **Arduino IDE setup** for ESP32 from memory (P03): board URL → Boards Manager → driver → port.
3. Explain `setup()` vs `loop()`, `pinMode()`/`digitalWrite()`/`digitalRead()`/`analogRead()`, and **PWM**.
4. Write a Wi-Fi connection block and explain `WL_CONNECTED`, `localIP()` and reconnection.
5. Draw the four **basic interfacing circuits**: LED, push button, DHT, relay.

---

## 3.1 Introduction to ESP32 ⭐⭐⭐

### 3.1.1 Overview & features
The **ESP32** is Espressif Systems' flagship **system-on-chip (SoC)** for IoT: a low-cost, low-power microcontroller with **Wi-Fi and Bluetooth on the same die**.

| Feature | Spec (ESP32 / DevKit V1) |
|---|---|
| CPU | 2 × Xtensa LX6 32-bit cores @ up to 240 MHz |
| SRAM | 520 KB |
| Flash | 4 MB (on DevKit) |
| Wi-Fi | 802.11 b/g/n (2.4 GHz) |
| Bluetooth | BT 4.2 Classic + BLE |
| ADC | 2 × 12-bit SAR (0–4095) |
| DAC | 2 × 8-bit (GPIO 25, 26) |
| PWM | LEDC: 16 channels, on most pins |
| Interfaces | UART×3, I²C×2, SPI×3, I²S, CAN, touch |
| Operating voltage | 3.3 V |
| Deep sleep | ~10 µA |
| Price | ≈ ₹400–800 (DevKit) |

### 3.1.2 Dual-core processor architecture ⭐⭐⭐ (viva favourite)
Two Xtensa LX6 cores, both 32-bit, clocked up to 240 MHz, sharing memory and peripherals:

| Core | Nickname | Job |
|---|---|---|
| **Core 0** | PRO_CPU (protocol) | Wi-Fi / Bluetooth protocol stacks |
| **Core 1** | APP_CPU (application) | Runs your Arduino `loop()` |

**Why it matters:** the Wi-Fi stack never ```mermaid
graph TD
    subgraph MEM["ESP32 Physical Memory Architecture (4.5 MB Total Address Space)"]
        subgraph SRAM["Internal SRAM (520 KB Total)"]
            DRAM["320 KB DRAM<br/>(Dynamic Heap Allocation & Task Stacks)"]
            IRAM["128 KB IRAM<br/>(Zero-Latency Code & ISR Handlers)"]
            RTC_FAST["8 KB RTC Fast Memory<br/>(CPUs Deep Sleep Boot Code)"]
            RTC_SLOW["8 KB RTC Slow Memory<br/>(ULP Co-processor Data & State)"]
        end

        subgraph FLASH["External SPI Flash (4 MB DevKit V1)"]
            BOOT["Bootloader Partition (0x1000, 36 KB)"]
            PART_TABLE["Partition Table (0x8000, 3 KB)"]
            NVS["NVS Storage Partition (0x9000, 20 KB)"]
            OTA_DATA["OTA Data Control Partition (0xE000, 8 KB)"]
            APP0["Factory / App 0 Slot (0x10000, 1.25 MB)"]
            APP1["OTA App 1 Slot (0x150000, 1.25 MB)"]
            FILESYS["LittleFS / SPIFFS Storage (0x290000, 1.43 MB)"]
        end
    end

    MMU["Flash Memory Management Unit (MMU Cache)"]

    IRAM & DRAM --> MMU
    MMU --> FLASH

    style SRAM fill:#1f2937,stroke:#60a5fa,stroke-width:2px,color:#fff
    style FLASH fill:#111827,stroke:#a78bfa,stroke-width:2px,color:#fff
    style MMU fill:#34d399,stroke:#059669,color:#fff
```

### 3.1.4 Built-in peripherals: Wi-Fi, Bluetooth, ADC, DAC, PWM ⭐⭐⭐

```mermaid
graph TD
    subgraph SOC["ESP32 System-on-Chip (SoC) Peripherals"]
        WIFI["Wi-Fi Subsystem<br/>(802.11 b/g/n 2.4 GHz)"]
        BT["Bluetooth Subsystem<br/>(BT 4.2 Classic + BLE)"]
        ADC1_BLOCK["ADC1 Peripheral<br/>(12-bit SAR: GPIO 34-39)"]
        DAC_BLOCK["DAC Peripheral<br/>(2 x 8-bit: GPIO 25, 26)"]
        LEDC_BLOCK["LEDC PWM Module<br/>(16 Channels, 4 Timers)"]
        COMM_BLOCK["Serial Comm Interfaces<br/>(UART x3, I2C x2, SPI x3)"]
    end

    subgraph API["Arduino-ESP32 Hardware Abstraction API"]
        WIFI_API["WiFi.begin() / WiFi.localIP()"]
        BLE_API["BLEDevice / BLEServer"]
        ADC_API["analogRead(pin) -> 0-4095"]
        DAC_API["dacWrite(pin, val) -> 0-255"]
        PWM_API["ledcSetup() / ledcWrite()"]
        SERIAL_API["Serial.begin(115200) / Wire / SPI"]
    end

    WIFI --> WIFI_API
    BT --> BLE_API
    ADC1_BLOCK --> ADC_API
    DAC_BLOCK --> DAC_API
    LEDC_BLOCK --> PWM_API
    COMM_BLOCK --> SERIAL_API

    style SOC fill:#1f2937,stroke:#3b82f6,color:#fff
    style API fill:#111827,stroke:#10b981,color:#fff
```

| Peripheral | Purpose | Code call |
|---|---|---|
| **Wi-Fi** | Connect to networks / internet | `WiFi.begin(ssid, pass)` |
| **Bluetooth** | BLE beacons/health wearables | `BLEDevice` lib |
| **ADC** | Read analog sensors (LDR, soil) | `analogRead(pin)` → 0–4095 |
| **DAC** | True analog voltage out (audio) | `dacWrite(pin, val)` |
| **PWM** | Fake analog: LED dim, servo, motor speed | `ledcSetup()` / `ledcWrite()` |

## 3.2 ESP32 Development Environment ⭐⭐⭐ (the P03 walkthrough)

### 3.2.1 Installing Arduino IDE
Download Arduino IDE 2.x from **arduino.cc/software** (Windows/macOS/Linux). Free, cross-platform, bundles a code editor, compiler, uploader and Serial Monitor.

### 3.2.2 Configuring for ESP32 — the two magic steps (memorize!)

| Step | What you do | Where |
|---|---|---|
| 1 | Add the Espressif board URL | **File → Preferences → Additional boards manager URLs** → `https://espressif.github.io/arduino-esp32/package_esp32_index.json` |
| 2 | Install the board package | **Tools → Board → Boards Manager → search `esp32` → Install "esp32 by Espressif"** |
| 3 | Install the USB driver | CP2102 (Silicon Labs) or CH340 (WCH), depending on the board's USB-UART chip |
| 4 | Select board + port | **Tools → Board → ESP32 Dev Module** · **Tools → Port → COMxx** |
| 5 | Verify | Upload **Blink** (onboard LED = GPIO 2) |

> [!warning] Boot-mode gotcha
> if upload fails with "Failed to connect to ESP32", hold the **BOOT** (GPIO 0) button while uploading, or lower Upload Speed to 115200.

### 3.2.3 Arduino IDE interface and tools
- **Sketch editor** — tabbed `.ino` files.
- **Verify (✓)** — compiles locally.
- **Upload (→)** — compiles and flashes over USB.
- **Serial Monitor / Serial Plotter** — live text / graph from `Serial.print()` (the "expected output" of P04–P07).
- **Library Manager** — installs "DHT sensor library by Adafruit", "NewPing", "PubSubClient", "Blynk" (used in every practical).

## 3.3 GPIO Programming using ESP32 ⭐⭐⭐

### 3.3.1 GPIO pins & numbering
- GPIOs are numbered **GPIO0–GPIO39** (the silkscreen number = the GPIO number; there is no separate Arduino-style mapping).
- **3.3 V logic**, most are digital I/O with optional internal pull-ups/pull-downs.
- **Special pins to respect:**

| Pin(s) | Constraint |
|---|---|
| 34, 35, 36, 39 | **Input-only** (no output, no pull-up) |
| 0, 12, 15 | **Strapping pins** — affect boot behaviour |
| 1, 3 | UART0 (Serial) — used for programming |
| 2 | Onboard LED (DevKit V1) |

### 3.3.2 Digital input & digital output ⭐⭐⭐
The four functions that power every practical:

```cpp
pinMode(pin, OUTPUT);              // configure as output (P04 LED)
digitalWrite(pin, HIGH);           // drive 3.3 V
digitalWrite(pin, LOW);            // drive 0 V

pinMode(pin, INPUT);               // configure as input (P05 PIR)
int val = digitalRead(pin);        // HIGH or LOW
```

### 3.3.3 Analog input using ADC ⭐⭐⭐
- `analogRead(pin)` → **0–4095** (12-bit) for 0–3.3 V.
- Use **ADC1 pins (GPIO 32–39)** for sensors to avoid Wi-Fi interference (ADC2 is shared with the radio).
- Example: LDR divider on GPIO 34 → `analogRead(34)` (P05).

### 3.3.4 Analog output / PWM concepts ⭐⭐⭐
- The ESP32 has **no analog voltage output on most pins** — it fakes it with **PWM (LEDC)**:
  - `ledcSetup(channel, freq, resolution)` → `ledcAttachPin(pin, channel)` → `ledcWrite(channel, duty)`.
  - Duty 0–255 (8-bit) → average voltage 0–3.3 V → LED brightness / motor speed.
- True analog out exists on only **GPIO 25 & 26 (DAC)**.

```mermaid
graph TD
    A["digitalWrite(pin, HIGH/LOW)"] --> D["Square Wave Output (0V or 3.3V Constant)<br/>Relay Switching / Fixed LED"]
    B["analogRead(pin)"] --> ADC["12-Bit Successive Approximation Register<br/>Reads 0V - 3.3V Potential -> 0 to 4095"]
    C["ledcWrite(channel, duty)"] --> P["LEDC Hardware PWM Counter<br/>Fakes Analog Voltage via High-Freq Duty Cycle"]

    style A fill:#1f2937,stroke:#60a5fa,color:#fff
    style B fill:#111827,stroke:#a78bfa,color:#fff
    style C fill:#1f2937,stroke:#34d399,color:#fff
```

## 3.4 ESP32 Core Libraries and Wi-Fi Programming ⭐⭐⭐

### 3.4.1 ESP32 core libraries & Library Manager
Installing "esp32 by Espressif" adds the **core libraries** you `#include`:
- `WiFi.h` — connect to networks.
- `HTTPClient.h` — HTTP GET/POST (P10, P11, P13).
- `Wire.h` — I²C (I2C sensors).
- `SPI.h` — SPI.
- `BluetoothSerial.h` — classic BT serial.

**Library Manager** (`Tools → Manage Libraries`) installs third-party libs — exact names used in this course:
| Library | Used for |
|---|---|
| DHT sensor library by Adafruit (+ Unified Sensor) | P06, P08, P10, P12–P14 |
| NewPing by Tim Eckel | P07, P11 |
| PubSubClient by Nick O'Leary | P08, P09, P14 |
| Blynk by Volodymyr Shymanskyy | P12 |

### 3.4.2 Wi-Fi library: connecting + checking status ⭐⭐⭐ (the block to memorise)

```cpp
#include <WiFi.h>
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WiFi.begin(ssid, password);                 // start connecting
while (WiFi.status() != WL_CONNECTED) {     // wait for connection
  delay(500);
  Serial.print(".");
}
Serial.println(WiFi.localIP());             // print assigned IP
```

| Function | Meaning |
|---|---|
| `WiFi.begin(ssid, pass)` | Start connecting (non-blocking) |
| `WiFi.status()` | Returns `WL_CONNECTED` when online |
| `WiFi.localIP()` | The IP address assigned to the ESP32 |
| `WiFi.disconnect()` / `WiFi.reconnect()` | Manual control / retry |
| `WiFi.mode(WIFI_STA)` | Station mode (connect to a router) |

> 💡 **Auto-reconnect pattern** (used by P08/P09/P14): wrap MQTT in a `reconnect()` loop that retries while `WiFi.status() != WL_CONNECTED`.

## 3.5 Basic Interfacing Concepts ⭐⭐⭐ (the four starter circuits)

### 3.5.1 LED interfacing (P04)
`GPIO 26 → 220 Ω → LED anode → LED cathode → GND`. Current limited by the resistor; `digitalWrite(26, HIGH/LOW)`.

### 3.5.2 Push button interfacing
```
3V3 ── button ── GPIO 4 ── 10 kΩ ── GND
(press → GPIO reads HIGH; pull-down keeps it LOW when idle)
```
Or use the internal pull-up: `pinMode(4, INPUT_PULLUP)` and read LOW when pressed. Debounce with `delay(50)`.

### 3.5.3 Sensor interfacing — temperature & humidity (P06)
`DHT DATA → GPIO 4` with a **4.7 kΩ–10 kΩ pull-up** to 3V3; read via the Adafruit DHT library; **≥ 2 s between reads**.

### 3.5.4 Actuator interfacing basics (P09/P14)
`GPIO 26 → Relay IN`; relay contacts switch the load (pump/fan). Most boards are **LOW-active** — `digitalWrite(pin, LOW)` = load ON. For motors: **H-bridge** (direction) + PWM (speed).

---

## 🧠 Deep-Dive Topics

### Deep Dive A: The two cores and FreeRTOS — what the Arduino core hides
When you write `setup()`/`loop()`, the Arduino-ESP32 core runs your code on **Core 1** while **Core 0** quietly runs the Wi-Fi/BT protocol tasks. The core even allows real parallelism via `xTaskCreatePinnedToCore()`. For viva: "the Wi-Fi stack runs on Core 0, my loop on Core 1 — that's why networking doesn't block sensing."

### Deep Dive B: Pull-ups and the input-only pins — wiring mistakes that break sketches
- GPIO 34–39 have **no internal pull-ups**, so a floating LDR/button reads random values — always add an external resistor or use a voltage divider.
- DHT's DATA line needs an **external pull-up** (open-drain protocol).
- Push buttons work best with `INPUT_PULLUP` (active-LOW) to avoid external resistors.

### Deep Dive C: Why PWM, not true analog?
LEDs/motors want a variable *power*, not a variable *voltage*. PWM chops the 3.3 V rail at high frequency and the *average* determines brightness/speed. The ESP32's 16 LEDC channels let you dim LEDs and drive servos/motors from any digital pin — with **true** DAC only on GPIO 25/26.

### Deep Dive D: The boot sequence — why "hold BOOT" works (P03)
At reset, the strapping pins (notably **GPIO 0**) are sampled: if GPIO 0 is held LOW, the chip enters **download mode** and the flasher can write new firmware; otherwise it boots the app from flash. That is the entire reason the "hold BOOT while uploading" trick works.

---

## 🚀 Beyond the Textbook

1. **The ESP32 is an SoC, not "just a chip"** — Wi-Fi/BT radio, dual CPUs, crypto accelerator, touch and CAN share one die. Espressif's ESP-IDF (C framework) is the professional alternative to Arduino.
2. **Why no `analogWrite()` on ESP32:** the Arduino UNO function does not exist in the ESP32 core — you must use `ledcWrite()`. A common compile error students hit (and a great viva anecdote).
3. **OTA updates** (over-the-air) are built into the ESP32 partition scheme — real products push firmware updates over Wi-Fi, not USB. Mentioning OTA in a "deployment challenge" answer (Unit 1) scores extra.
4. **`WiFi.status()` vs MQTT `connected()`:** Wi-Fi being up does NOT mean the broker is reachable — P08's `reconnect()` loop checks MQTT separately. Two different layers of connectivity!
5. **The 15-second ThingSpeak limit is a cloud constraint, not hardware** — the ESP32 can publish every second; the platform throttles. Know which layer imposes which limit (viva favourite).

---

## 🎯 High-Yield Exam Topics (likely GTU-style questions)

1. Short note: **features of ESP32**. (7 m) ⭐⭐⭐
2. Explain the **dual-core architecture** of ESP32. (4 m) ⭐⭐⭐
3. Explain the **memory organization** of ESP32. (4–7 m) ⭐⭐⭐
4. Short note: **built-in peripherals** of ESP32 (Wi-Fi, BT, ADC, DAC, PWM). (7 m) ⭐⭐⭐
5. Write the steps to **configure Arduino IDE for ESP32** and install drivers. (4–7 m) ⭐⭐⭐ (≈ P03)
6. Explain **`setup()` and `loop()`** with a blink example. (3–4 m) ⭐⭐⭐ (≈ P04)
7. Explain **digital input and output** programming with examples. (4 m) ⭐⭐⭐ (≈ P04/P05)
8. Explain **analog input using ADC** in ESP32. (4 m) ⭐⭐⭐ (≈ P05)
9. Explain **PWM / analog output** concepts in ESP32. (4 m) ⭐⭐⭐
10. Write the **Wi-Fi connection code** for ESP32 and explain the status functions. (4–7 m) ⭐⭐⭐ (≈ P08)
11. How is **library management** done in Arduino IDE? Name the libraries used in this course. (3–4 m) ⭐⭐
12. Explain the **input-only pins and strapping pins** of ESP32. (3 m) ⭐⭐

### ✅ Solved model answers (highest-yield)

**Q1. (7 m) — Short note: features of ESP32.**
> The ESP32 is Espressif's IoT SoC. Key features: **(1) Dual-core CPU** — two Xtensa LX6 cores up to 240 MHz (Core 0 runs Wi-Fi/BT, Core 1 runs the user program). **(2) Memory** — 520 KB SRAM and, on DevKits, 4 MB external flash with a partitionable layout (app + OTA). **(3) Wireless** — 802.11 b/g/n Wi-Fi and Bluetooth 4.2 Classic + BLE on-chip. **(4) Analogue peripherals** — two 12-bit SAR ADCs (0–3.3 V → 0–4095), two 8-bit DACs (GPIO 25/26). **(5) PWM (LEDC)** — 16 channels on most GPIOs for LED dimming, servos and motor speed. **(6) Interfaces** — UART×3, I²C×2, SPI×3, I²S, CAN, and capacitive touch. **(7) Low power** — deep sleep ~10 µA for battery nodes. **(8) Cost** — under ₹600, making it the standard IoT node in this course.

**Q5. (4–7 m) — Configure Arduino IDE for ESP32 + install drivers.**
> (1) Install Arduino IDE 2.x from arduino.cc. (2) In **File → Preferences**, paste the Espressif board-manager URL `https://espressif.github.io/arduino-esp32/package_esp32_index.json` into "Additional boards manager URLs". (3) In **Tools → Board → Boards Manager**, search `esp32` and install **"esp32 by Espressif Systems"**. (4) Install the correct **USB-to-serial driver**: CP210x (Silicon Labs) or CH340 (WCH), depending on the chip near the board's USB port. (5) Connect the board, select **Tools → Board → ESP32 Dev Module** and the matching **Port**. (6) Upload the Blink example (onboard LED on GPIO 2) to verify. If upload fails, hold the **BOOT** button or reduce the upload speed.

**Q10. (4–7 m) — Wi-Fi connection code for ESP32 with status functions.**
> ```cpp
> #include <WiFi.h>
> const char* ssid = "NETWORK";
> const char* password = "PASSWORD";
> void setup() {
>   Serial.begin(115200);
>   WiFi.begin(ssid, password);              // start connecting
>   while (WiFi.status() != WL_CONNECTED) {  // wait until online
>     delay(500);
>     Serial.print(".");
>   }
>   Serial.print("IP: ");
>   Serial.println(WiFi.localIP());          // show assigned IP
> }
> ```
> Explanation: `WiFi.begin()` starts a non-blocking connection; `WiFi.status()` returns `WL_CONNECTED` once joined; `WiFi.localIP()` gives the DHCP-assigned address printed on the Serial Monitor. Real sketches (P08/P09) wrap this in a `reconnect()` loop so the device reconnects automatically if the network drops.

---

## ✍️ Practice Problems (self-test — answers hidden)

1. List 6 ESP32 features and state which two make it "IoT-ready" over the Arduino UNO.
2. What is stored in SRAM vs Flash? Why does `millis()` reset on reboot but your sketch does not?
3. Which pins are input-only, and why does P05/P13 deliberately use GPIO 34?
4. Write the code to read a push button with an internal pull-up and print PRESSED/RELEASED.
5. Why doesn't `analogWrite()` compile on ESP32? What do you use instead?
6. Draw the ESP32 memory map (SRAM / RTC / external flash) and label partitions.
7. A sketch connects to Wi-Fi but MQTT still fails — what is the difference between `WiFi.status()` and `client.connected()`?
8. What is a strapping pin and why does holding GPIO 0 LOW at boot enter download mode?

<details>
<summary>📌 Model solutions</summary>

1. Dual-core 240 MHz, 520 KB SRAM, Wi-Fi b/g/n, BT+BLE, 12-bit ADC ×2, 8-bit DAC ×2, LEDC PWM, UART/I²C/SPI, deep sleep, low cost. IoT-ready = on-chip **Wi-Fi + Bluetooth**.
2. SRAM = volatile variables (lost on reset); Flash = the program + partitions (persistent). `millis()` is a counter in RAM → resets; the sketch lives in flash → survives.
3. GPIO 34, 35, 36, 39. GPIO 34 is an ADC1 input-only pin — avoids Wi-Fi/ADC2 conflicts and cannot be damaged by a sensor output.
4. `pinMode(4, INPUT_PULLUP); int v = digitalRead(4); if (v == LOW) Serial.println("PRESSED");` (active-LOW).
5. The ESP32 core has no `analogWrite()` — use `ledcSetup(ch, freq, res); ledcAttachPin(pin, ch); ledcWrite(ch, duty)`.
6. 520 KB SRAM (data/stack), 8 KB RTC RAM, 4 MB external flash partitioned into bootloader / app / OTA / filesystem.
7. `WiFi.status()` = link to the router; `client.connected()` = MQTT link to the broker. Wi-Fi up ≠ broker reachable (that's P08's `reconnect()`).
8. A pin sampled at reset to select boot mode; GPIO 0 LOW = download (flash) mode, HIGH = normal boot.
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **ESP32** | Espressif IoT SoC: dual-core LX6 + Wi-Fi/BT on-chip |
| **DevKit V1** | Common 30-pin ESP32 development board |
| **Core 0 / Core 1** | Protocol core (Wi-Fi/BT) / application core (user code) |
| **SRAM** | Volatile memory holding runtime variables (520 KB) |
| **Flash** | Persistent storage (4 MB), holds sketch + partitions |
| **Partition scheme** | Flash layout: bootloader, app, OTA, filesystem |
| **ADC** | Analog-to-digital converter (12-bit, 0–4095) |
| **DAC** | Digital-to-analog converter (8-bit, GPIO 25/26) |
| **PWM / LEDC** | Pulse-width modulation for dimming/speed/servos |
| **Strapping pin** | GPIO sampled at boot (0, 12, 15) that selects boot mode |
| **Input-only pin** | GPIO 34–39: read-only, no pull-up, no output |
| **Boards Manager URL** | Espressif JSON link enabling ESP32 support in Arduino IDE |
| **CP2102 / CH340** | USB-UART bridge chips whose drivers are needed |
| **Sketch** | An Arduino program (`.ino`) with `setup()` + `loop()` |
| **Serial Monitor** | IDE tool showing `Serial.print()` output at 115200 baud |
| **Library Manager** | IDE tool to install libraries (DHT, NewPing, PubSubClient, Blynk) |
| **`WL_CONNECTED`** | Status returned by `WiFi.status()` when joined to a network |
| **`localIP()`** | Returns the ESP32's assigned IP address |
| **`INPUT_PULLUP`** | Enables the internal pull-up resistor for a pin |
| **`ledcWrite()`** | Writes a PWM duty cycle to an LEDC channel |

---

## 🔗 Curated Resources (per concept)

**Official ESP32 docs (Espressif)**
- ESP32 overview & datasheet: https://www.espressif.com/en/products/socs/esp32
- ESP-IDF programming guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/
- Arduino-ESP32 core docs: https://docs.espressif.com/projects/arduino-esp32/en/latest/
- Espressif board-manager JSON (the URL from P03): https://espressif.github.io/arduino-esp32/package_esp32_index.json

**Arduino IDE**
- Arduino IDE download: https://www.arduino.cc/en/software
- Arduino language reference: https://www.arduino.cc/reference/en/

**Drivers**
- CP210x drivers (Silicon Labs): https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- CH340 driver (WCH): https://www.wch-ic.com/downloads/CH341SER_ZIP.html

**Tutorials**
- ESP32 getting started (Random Nerd Tutorials): https://randomnerdtutorials.com/getting-started-with-esp32/
- ESP32 pinout reference: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
- ESP32 ADC (Random Nerd Tutorials): https://randomnerdtutorials.com/esp32-adc-analog-read-arduino-ide/
- ESP32 PWM (Random Nerd Tutorials): https://randomnerdtutorials.com/esp32-pwm-arduino-ide/

**Books (from GTU syllabus)**
- Rajkamal, *Internet of Things: Architecture and Design Principles*, McGraw Hill, 2017.
- Rahul Dubey, *An Introduction to Internet of Things: Connecting Devices, Edge Gateway, and Cloud*, 2019.

**Videos (high yield)**
- Andreas Spiess ESP32 deep-dives · DroneBot Workshop ESP32 courses · Random Nerd Tutorials ESP32 playlists.

---

## 🎥 Video Study Guide (YouTube)

> Don't like reading? Me neither. This is your **structured video path** for the whole unit — better than the syllabus because it tells you *exactly what to search* and *what to watch first*, in a sensible order. Everything below is search keywords (they never rot like links do) + channels you can trust.

### 🧑🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | Watch 1 explainer per topic from the table below (3–8 min each) |
| 🛠️ **Builder** | wiring things yourself | Watch the setup video → then run [[P03 — Arduino Ide Setup Esp32|P03]]–[[P07 — Ultrasonic Distance Sensor|P07]] and break them |
| 🔧 **Tinkerer** | experimenting & demos | Watch demo videos → change pins/values and re-upload the practical sketches |
| 🧠 **Deep Diver** | full theory, "why" | Watch the whole-unit playlists at the bottom (university-level depth) |
| 🧭 **Explorer** | breadth & curiosity | Watch the "ESP32 vs other boards" explainers first, then follow your curiosity |
| 🎓 **Academic** | exam marks | Watch the revision/GTU-style videos, then grind the High-Yield questions above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| What is an ESP32 | `esp32 explained` · `esp32 features specifications` · `what can you do with esp32` | Andreas Spiess, DroneBot Workshop, Core Electronics | 🧭 + 🎧 |
| ESP32 vs other boards | `esp32 vs arduino vs raspberry pi` · `which board should i choose for iot` | Andreas Spiess, Core Electronics, EEVblog | 🧭 Explorer |
| Arduino IDE setup for ESP32 | `install esp32 in arduino ide` · `esp32 board manager install` · `cp2102 ch340 driver install` | Random Nerd Tutorials, DroneBot Workshop | 🛠️ Builder |
| setup() / loop() & blink | `arduino setup and loop explained` · `esp32 blink onboard led tutorial` · `arduino programming basics` | Paul McWhorter, Programming Electronics Academy | 🛠️ + 🎧 |
| Digital input/output | `arduino digital read button tutorial` · `esp32 digitalwrite digitalread` · `push button pull up pull down` | Paul McWhorter, DroneBot Workshop | 🔧 + 🛠️ |
| ADC & analog input | `esp32 analog read adc tutorial` · `adc explained arduino` · `esp32 adc input only pins` | Random Nerd Tutorials, Andreas Spiess | 🧠 + 🛠️ |
| PWM & analog output | `pwm explained arduino` · `esp32 pwm ledc tutorial` · `dim an led with pwm` | The Engineering Mindset, DroneBot Workshop | 🎧 + 🛠️ |
| Wi-Fi on ESP32 | `esp32 wifi connect tutorial` · `esp32 wifi library localip` · `esp32 reconnect wifi auto` | Random Nerd Tutorials, DroneBot Workshop | 🛠️ Builder |
| Dual core & FreeRTOS | `esp32 dual core freertos tutorial` · `esp32 multitasking` · `esp32 cores explained` | Andreas Spiess, G6EJD | 🧠 Deep Diver |
| Whole-unit revision (exam mode) | `esp32 features exam notes` · `esp32 unit 3 diploma` · `arduino ide setup esp32 full lecture` | Neso Academy, Gate Smashers, edureka! | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"Random Nerd Tutorials — ESP32 Tutorials"** — the closest thing to this unit's practicals: setup, GPIO, ADC, PWM, Wi-Fi, every sensor.
2. **"Andreas Spiess — ESP32 and ESP8266 deep dives"** — the *why* behind the hardware: dual cores, low power, Wi-Fi internals.
3. **"Paul McWhorter — Arduino/ESP32 full course"** — a structured beginner-to-intermediate path for builders.

### 🎬 Step 3 — Proof you got it (5 min)

- Recite the ESP32 feature list from memory in 30 seconds.
- Re-draw the Arduino IDE setup flow (URL → Boards Manager → driver → port) on paper.
- Explain to a friend why "hold BOOT" fixes an upload failure — if you can, the boot sequence is yours.

---

*Next: [[Unit 4 — IoT Communication Protocols and Networking|UNIT 4 — IoT Communication Protocols and Networking]]*

---



## 📖 Historical Context & Motivation

The development of embedded software for microcontrollers has historically suffered from a trade-off between **development velocity** and **hardware efficiency**. In the 1980s and 1990s, programming 8-bit microcontrollers (such as the Intel 8051 or Microchip PIC) required writing raw assembly language or device-specific C code using vendor-locked, expensive integrated development environments (IDEs) and hardware programmers (JTAG/BDM adapters).

In 2005, the **Arduino project** revolutionized embedded engineering by introducing an open-source hardware and software ecosystem based on the Atmel ATmega328P. Arduino abstracted hardware register manipulation behind a simplified C++ Hardware Abstraction Layer (HAL)—exposing standardized APIs such as `pinMode()`, `digitalWrite()`, and `analogRead()`—and utilized a USB serial bootloader that eliminated the need for specialized external programmers.

However, traditional 8-bit microcontrollers ran single-threaded execution loops (`setup()` followed by an infinite `loop()`) at modest clock speeds ($16\text{ MHz}$) with tiny RAM budgets ($2\text{ KB}$), rendering them incapable of running modern cryptographic ciphers (TLS 1.2/1.3) or network protocol stacks (TCP/IP, Wi-Fi, Bluetooth).

When Espressif Systems launched the **ESP32** in 2016, they bridged the gap between bare-metal microcontroller accessibility and advanced 32-bit System-on-Chip (SoC) performance. By porting **FreeRTOS** underneath the Arduino core interface, Espressif enabled developers to write familiar Arduino code while transparently leveraging a 32-bit dual-core processor running at $240\text{ MHz}$ with hardware cryptography engines and native RF stacks.

---

## 🔬 Deep Dive: System Architecture

### Xtensa Dual-Core Architecture, FreeRTOS Integration & Memory Management

The ESP32 is powered by two 32-bit Tensilica Xtensa LX6 microprocessors operating up to $240\text{ MHz}$, delivering up to 600 DMIPS of computational throughput.

```mermaid
graph TD
    subgraph SOC["ESP32 Dual-Core System-on-Chip Architecture"]
        subgraph CPU0["Core 0: PRO_CPU (Protocol Engine)"]
            WIFI_STACK["802.11 b/g/n Wi-Fi Driver"]
            BT_STACK["Bluetooth 4.2 / BLE Controller"]
            LWIP["LwIP TCP/IP Protocol Stack"]
            SYS_EVENT["System Event Loop Tasks"]
        end

        subgraph CPU1["Core 1: APP_CPU (Application Engine)"]
            MAIN_TASK["FreeRTOS mainTask<br/>Calls setup() then loop()"]
            USER_TASK["User Parallel FreeRTOS Tasks<br/>(xTaskCreatePinnedToCore)"]
            ADC_DRIVER["ADC1 Sensor Processing"]
        end

        SCHEDULER["FreeRTOS Preemptive Multiprocessing Scheduler & Interrupt Matrix"]
        
        subgraph MEM_BUS["Internal 520 KB SRAM Memory Bus"]
            DRAM_BLOCK["320 KB DRAM (Dynamic Heap / Stacks)"]
            IRAM_BLOCK["128 KB IRAM (ISR Handlers / Critical Functions)"]
        end

        MMU_CACHE["SPI Flash Cache Controller (MMU)"]
        
        subgraph SPI_FLASH["External SPI Flash Memory (4 MB)"]
            PART_TABLE_SYS["Bootloader | Partition Table | NVS"]
            APP0_SLOT["app0 Partition (Active Code Slot)"]
            APP1_SLOT["app1 Partition (OTA Update Target)"]
            FS_SLOT["LittleFS / SPIFFS File Storage"]
        end
    end

    CPU0 & CPU1 --> SCHEDULER
    SCHEDULER --> MEM_BUS
    MEM_BUS --> MMU_CACHE
    MMU_CACHE --> SPI_FLASH

    style CPU0 fill:#1e3a8a,stroke:#3b82f6,color:#fff
    style CPU1 fill:#14532d,stroke:#22c55e,color:#fff
    style SCHEDULER fill:#581c87,stroke:#a855f7,color:#fff
    style SPI_FLASH fill:#1f2937,stroke:#64748b,color:#fff
```

#### 1. Dual-Core Task Scheduling & FreeRTOS Architecture
The ESP32 runs a modified version of **FreeRTOS** capable of Symmetric Multiprocessing (SMP). The two cores are assigned distinct system roles by default:
- **Core 0 (PRO_CPU - Protocol CPU):** Dedicated to handling background network operations, including the 802.11 b/g/n Wi-Fi MAC/PHY driver, Bluetooth controller stack, TCP/IP stack (LwIP), and system event loops.
- **Core 1 (APP_CPU - Application CPU):** Assigned to execute the user's main application. When the ESP32 boots, the framework creates a FreeRTOS task named `mainTask` pinned to Core 1 at priority 1, which in turn calls `setup()` once and `loop()` continuously.

Developers can explicitly spawn parallel asynchronous tasks on specific cores using the FreeRTOS API `xTaskCreatePinnedToCore()`:

```cpp
TaskHandle_t SensorTaskHandle;

void SensorTaskCode( void * pvParameters ) {
  for(;;) {
    // Executes concurrently on Core 0 alongside network processing
    int rawADC = analogRead(34);
    vTaskDelay(pdMS_TO_TICKS(100)); // Non-blocking FreeRTOS yield
  }
}

void setup() {
  xTaskCreatePinnedToCore(
    SensorTaskCode,    // Task function
    "SensorTask",      // Task name
    4096,              // Stack size in words
    NULL,              // Task input parameter
    1,                 // Task priority
    &SensorTaskHandle, // Task handle
    0                  // Core ID (0 = PRO_CPU, 1 = APP_CPU)
  );
}
```

---

#### 2. Memory Organisation & Addressing Scheme
The ESP32 contains $520\text{ KB}$ of internal SRAM mapped into specific functional address spaces:
- **DRAM (Data RAM - $320\text{ KB}$):** Used for dynamic memory allocation (heap) and task execution stacks.
- **IRAM (Instruction RAM - $128\text{ KB}$):** Used to store critical code instructions (such as Interrupt Service Routines, ISRs) that must execute directly without waiting for Flash Memory Management Unit (MMU) cache fetch latency.
- **RTC Memory ($16\text{ KB}$):** Partitioned into $8\text{ KB}$ RTC Fast Memory (accessible by the main CPUs during boot from deep sleep) and $8\text{ KB}$ RTC Slow Memory (accessible by the low-power ULP co-processor while the main CPUs are powered down).

##### External Flash & Partition Tables
The ESP32 DevKit V1 incorporates a $4\text{ MB}$ external SPI Flash chip. The Memory Management Unit (MMU) maps sections of flash into the CPU code space. Flash memory is organized via a **Partition Table**:

```
+-------------------+--------------------+--------------------+--------------------+
| Partition Name    | Type / Subtype     | Offset             | Size               |
+-------------------+--------------------+--------------------+--------------------+
| nvs               | data / nvs         | 0x9000             | 20 KB (0x5000)     |
| otadata           | data / ota         | 0xE000             | 8 KB (0x2000)      |
| app0              | app / ota_0        | 0x10000            | 1.25 MB (0x140000) |
| app1              | app / ota_1        | 0x150000           | 1.25 MB (0x140000) |
| spiffs / littlefs | data / spiffs      | 0x290000           | 1.43 MB (0x170000) |
+-------------------+--------------------+--------------------+--------------------+
```

---

#### 3. GPIO Architecture, Hardware Matrix & Boot Strapping Pins
The ESP32 GPIO subsystem features a **Hardware GPIO Matrix** that routes internal peripheral signals (UART, SPI, I²C, LEDC PWM) to physical pins.

```mermaid
graph TD
    subgraph PERIPHERALS["Internal Hardware Signals"]
        SIG_UART["UART0 TX/RX Signals"]
        SIG_LEDC["LEDC PWM Channel 0 Out"]
        SIG_I2C["I2C SDA/SCL Clock & Data"]
    end

    MATRIX["ESP32 GPIO Matrix<br/>(Flexible Pin Routing Layer)"]

    subgraph PINS["Physical External Package Pins"]
        PIN_GPIO26["GPIO Pin 26 (Dimmable LED / Relay)"]
        PIN_GPIO21["GPIO Pin 21 (I2C SDA)"]
        PIN_GPIO22["GPIO Pin 22 (I2C SCL)"]
    end

    PERIPHERALS --> MATRIX
    MATRIX --> PINS

    style MATRIX fill:#f59e0b,stroke:#d97706,color:#fff
```

##### Strapping Pins & Boot Behavior
During hardware reset, the ESP32 samples the voltage levels of specific **Strapping Pins** (GPIO 0, 2, 12, 15) to configure its boot mode:

| Strapping Pin | State at Reset | Boot Mode Selected |
|---|---|---|
| **GPIO 0** | **LOW** | **Download / Flashing Mode** (Waits for serial image upload) |
| **GPIO 0** | **HIGH** | **SPI Flash Boot** (Boots application binary from Flash) |
| **GPIO 2** | Must be **LOW** | Required to enter Download Mode |
| **GPIO 12** | **LOW** ($3.3\text{ V}$) / **HIGH** ($1.8\text{ V}$) | Selects Flash LDO Voltage |
| **GPIO 15** | Must be **HIGH** | Enables debug log output on UART0 |

*Flashing Recovery Rule:* If an upload fails with `Failed to connect to ESP32: Timed out waiting for packet header`, holding the **BOOT button** pulls **GPIO 0 LOW**, forcing the internal ROM bootloader into Download Mode.

---

#### 4. LED Control (LEDC) Hardware PWM Architecture
The ESP32 replaces traditional single-timer `analogWrite()` with a dedicated **LEDC (LED Control)** hardware module. LEDC contains 16 independent PWM channels linked to 4 timers.

```mermaid
graph TD
    TIMER0["LEDC Hardware Timer 0<br/>(APB Clock 80 MHz, Freq=5000Hz, Res=10-bit)"] --> CHAN0["LEDC Channel 0 Controller<br/>(Duty Register = 512 / 1024)"]
    CHAN0 --> MATRIX["GPIO Matrix Router"]
    MATRIX --> PIN26["Physical GPIO Pin 26<br/>(Dimmable LED Output)"]

    style TIMER0 fill:#1f2937,stroke:#60a5fa,color:#fff
    style CHAN0 fill:#111827,stroke:#a78bfa,color:#fff
    style PIN26 fill:#34d399,stroke:#059669,color:#fff
```

The maximum usable PWM frequency $f_{\text{max}}$ is constrained by the chosen bit resolution $N_{\text{bits}}$ and APB bus clock ($f_{\text{APB\_CLK}} = 80\text{ MHz}$):

$$f_{\text{max}} = \frac{f_{\text{APB\_CLK}}}{2^{N_{\text{bits}}}} = \frac{80 \times 10^6\text{ Hz}}{2^{N_{\text{bits}}}}$$

For a 10-bit resolution ($2^{10} = 1024$ duty steps, $0 - 1023$):
$$f_{\text{max}} = \frac{80 \times 10^6}{1024} = 78.125\text{ kHz}$$

---

## 🏢 Real-World Case Study

### Over-The-Air (OTA) Firmware Deployment in Commercial Smart Meters

Commercial utility smart energy meters deployed across municipal power grids use ESP32 SoCs to record energy consumption and report telemetry to utility head-end systems over cellular/Wi-Fi links. Updating physical meter firmware via USB is cost-prohibitive. Thus, meters rely on **Over-The-Air (OTA)** updates.

```mermaid
stateDiagram-v2
    [*] --> RunningApp0: Booting from Flash app0 (v1.0)
    
    state RunningApp0 {
        [*] --> NormalOperation: Measuring Power & Uploading Telemetry
        NormalOperation --> DownloadOTA: Receive Remote OTA Push Notification
        DownloadOTA --> StreamToApp1: Connect via TLS & Download binary chunk-by-chunk
        StreamToApp1 --> VerifyCrypto: Write Bytes into Flash Slot app1 (0x150000)
    }

    VerifyCrypto --> ValidationFailed: Invalid SHA-256 / ECC Signature
    ValidationFailed --> NormalOperation: Abort OTA & Erase app1 Slot

    VerifyCrypto --> SetPendingReboot: SHA-256 Validated Successfully
    SetPendingReboot --> SystemRestart: Update otadata partition state -> Set boot to app1

    SystemRestart --> BootloaderCheck: Execute esp_restart()

    state BootloaderCheck {
        [*] --> BootingApp1: ROM Bootloader reads otadata -> Boot from app1 (v2.0)
        BootingApp1 --> StartWDT: Application Starts & Triggers Watchdog Timer (WDT)
    }

    StartWDT --> ConfirmValid: Wi-Fi Reconnected & Calls esp_ota_mark_app_valid_cancel_rollback()
    ConfirmValid --> RunningApp1: OTA Upgrade Complete (App1 Permanent Active)
    
    StartWDT --> WDT_Reset: Application Crashes or WDT Expires BEFORE Confirmation
    WDT_Reset --> AutomaticRollback: Reset System & Detect Failed Boot State
    AutomaticRollback --> RunningApp0: otadata ROLLS BACK automatically -> Boot safely from app0
```

#### Engineering Robustness & Rollback Mechanics
1. **Partition Isolation:** The physical flash memory is split into dual app slots (`app0` at `0x10000` and `app1` at `0x150000`). The active application runs out of `app0` while downloading the new firmware into `app1`.
2. **Cryptographic Validation:** Once downloaded, the application verifies the SHA-256 hash and Elliptic Curve Cryptography (ECC) signature appended to the binary to ensure the image was not tampered with.
3. **Fail-Safe Rollback:** If the new firmware image in `app1` contains a bug causing a crash or infinite loop before it establishes Wi-Fi, the ESP32's **Hardware Watchdog Timer (WDT)** triggers a system reset. The bootloader detects that `app1` failed to confirm runtime validity, invalidates `app1`, and automatically rolls back to boot from the known-good `app0` partition.

---

## 📝 End-of-Chapter Exercises

### Exercise 1: Dual-Core FreeRTOS Task Allocation & Queue Synchronization
Write a complete, compilable Arduino ESP32 code snippet demonstrating dual-core multitasking:

1. Create a FreeRTOS Queue named `sensorQueue` capable of holding up to 10 integer values.
2. Spawn `Task_ReadADC` on **Core 0** (priority 2). It must sample ADC pin GPIO 34 every $500\text{ ms}$ using `vTaskDelay()` and push raw ADC integer values into `sensorQueue`.
3. Spawn `Task_ProcessData` on **Core 1** (priority 1). It must read incoming integers from `sensorQueue`, calculate a running average of the last 5 readings, and print the result to `Serial`. Include thread-safe queue handling.

### Exercise 2: LEDC Hardware PWM & APB Frequency Calculation
An ESP32 system controls an industrial high-speed brushless DC motor driver requiring a precise $20\text{ kHz}$ PWM frequency.

1. Calculate the maximum theoretical integer duty cycle resolution $N_{\text{bits}}$ (in bits) that can be configured for an LEDC timer operating at $20\text{ kHz}$ using the $80\text{ MHz}$ APB clock.
2. Assuming you configure a resolution of $11\text{ bits}$ ($0 - 2047$ steps):
   - Verify if $11\text{ bits}$ is valid for $20\text{ kHz}$.
   - Calculate the precise integer value to pass into `ledcWrite(channel, duty)` to set a $72.5\%$ PWM duty cycle.

### Exercise 3: Strapping Pin Hardware Debugging & Boot Troubleshooting
A developer designs a custom PCB utilizing an ESP32-WROOM-32 module. The PCB routes an external push button to GPIO 0 with a pull-down resistor to GND, and connects a pull-down resistor to GPIO 12.

1. Predict the two distinct hardware failures that will occur when attempting to (a) upload new firmware over USB, and (b) boot the ESP32 into normal application mode.
2. Explain the hardware strapping pin logic responsible for both failures, and redraw the corrected pin schematic with appropriate pull-up/pull-down configurations.

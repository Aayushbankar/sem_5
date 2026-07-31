---
title: "P04 — External Led Blink Toggle"
sidebar:
  order: 4
---

# P04 — Toggle an External LED (Digital Output)

**Subject:** Hands on Practice using IoT | **Unit:** 2 | **Approx. Hrs:** 2
**PrO (verbatim):** *Write and execute a program to toggle an external LED (Digital Output) to understand the setup() and loop() structure.*

---

## 1. Objective
- Configure an ESP32 GPIO as a **digital output**.
- Understand the **`setup()`** (runs once) and **`loop()`** (runs forever) structure.
- Toggle an **external LED** on/off with `digitalWrite()` and a delay.

## 2. Theory (exam-ready)

### 2.1 `setup()` vs `loop()`
| Function | When it runs | Use it for |
|---|---|---|
| **`setup()`** | Once, when the board powers on/resets | `pinMode()`, Serial.begin, connect Wi-Fi, init libraries |
| **`loop()`** | Immediately after `setup()`, repeats forever | Read sensors, toggle outputs, publish data |

### 2.2 Digital output
- `pinMode(pin, OUTPUT)` marks the GPIO as an output driver.
- `digitalWrite(pin, HIGH)` drives the pin to **3.3 V**; `digitalWrite(pin, LOW)` drives it to **0 V**.
- ESP32 pins are **3.3 V logic** — connect the LED through a **current-limiting resistor (220 Ω)** so that current ≈ (3.3 − 1.8 V)/220 Ω ≈ 7 mA.

### 2.3 The "toggle" pattern
```
Blink: HIGH → delay(500) → LOW → delay(500) → repeat
Toggle: toggled = !toggled  (each loop flips the state)
```

## 3. Circuit / Wiring
| ESP32 pin | Component |
|---|---|
| **GPIO 26** | LED **anode (long leg)** via 220 Ω resistor |
| **GND** | LED **cathode (short leg)** |

Breadboard chain: `GPIO26 → 220 Ω → LED anode → LED cathode → GND`.

```mermaid
flowchart LR
    ESP32[ESP32] -- GPIO 26 --> R[220 Ω] --> A[LED anode]
    A --> K[LED cathode] --> G[ESP32 GND]
```

## 4. Code
```cpp
// P04 — Toggle an external LED (Digital Output)
// LED on GPIO 26, current-limited by a 220 ohm resistor.

const int ledPin = 26;          // GPIO 26 drives the external LED

void setup() {
  Serial.begin(115200);          // start serial monitor (115200 baud)
  pinMode(ledPin, OUTPUT);       // configure GPIO 26 as a digital output
  Serial.println("P04: External LED toggle started.");
}

void loop() {
  digitalWrite(ledPin, HIGH);    // LED ON (pin driven to 3.3 V)
  Serial.println("LED ON");
  delay(500);                    // stay ON for 500 ms

  digitalWrite(ledPin, LOW);     // LED OFF (pin driven to 0 V)
  Serial.println("LED OFF");
  delay(500);                    // stay OFF for 500 ms
}
```

> Full sketch: [`p04_external_led_blink.ino`](./p04_external_led_blink.ino.md)

## 5. Expected Serial Output
> ⚠️ **Not an actual run** — this practical was designed/verified on paper. On real hardware you should see:

```
P04: External LED toggle started.
LED ON
LED OFF
LED ON
LED OFF
... (repeats every 1 second forever)
```

**Interpretation:** one `LED ON` + `LED OFF` cycle = 1 s. The LED physically blinks in sync with these lines at **0.5 Hz**.

## 6. Verify on Hardware (checklist)
- [ ] Serial Monitor set to **115200 baud** → header line prints once.
- [ ] LED turns ON for exactly 500 ms, OFF for 500 ms — steady 1 s period.
- [ ] `LED ON`/`LED OFF` lines match the physical LED state.
- [ ] Changing `delay(500)` → `delay(1000)` doubles the blink period.
- [ ] Reverse LED legs → nothing lights (LED is polarity-sensitive; swap back).
- [ ] Remove the 220 Ω resistor → LED may overheat/damage (do not test this!).

## 7. Conclusion
`setup()` initialised the pin and serial once; `loop()` repeated the toggle forever. GPIO 26 behaved as a digital output that can source/sink current through a resistor, proving the fundamental ESP32 digital-output model used by every later practical (relays, LEDs, buzzers).

## 8. Viva Q&A
1. **How many times does `setup()` run?** — Exactly once per power-on/reset.
2. **Why the 220 Ω resistor?** — To limit LED current (≈7 mA) and protect both LED and GPIO.
3. **What voltage is `HIGH` on ESP32?** — 3.3 V (not 5 V like Arduino UNO).
4. **How would you change blink speed?** — Change the `delay()` values.
5. **Which pin did you use and why?** — GPIO 26 — a safe digital pin with no boot constraints (avoids input-only 34–39 and strapping pins).

## 9. Resources
- Arduino `digitalWrite` reference: https://www.arduino.cc/reference/en/language/functions/digital-io/digitalwrite/
- Arduino `pinMode` reference: https://www.arduino.cc/reference/en/language/functions/digital-io/pinmode/
- Tinkercad Circuits (online simulator): https://www.tinkercad.com/dashboard
- ESP32 LED blink guide: https://randomnerdtutorials.com/esp32-led-blink-arduino/

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **External Led Blink Toggle** in a real environment, it almost never works perfectly the first time. 
> 
> **Common Edge Cases to Test:**
> 1. **Network partitions:** What happens to this code if the Wi-Fi drops halfway through execution?
> 2. **Malformed Inputs:** How does the system behave if fed null values, extremely large datasets, or unexpected data types?
> 3. **Resource Exhaustion:** Does this script handle memory leaks or rate-limiting from APIs?

## 🔬 Extension Challenge

> [!example] Prove your expertise
> To truly master this practical, try modifying the code to achieve the following:
> - **Add robust error handling** (try/catch blocks) and structured logging instead of print statements.
> - **Parameterize the inputs** so the script can be run dynamically from the CLI without hardcoding values.
> - **Optimize it:** Can you reduce the execution time or memory footprint?

## 🎯 Key Takeaways

- **3.3 V logic** — connect the LED through a **current-limiting resistor (220 Ω)** so that current ≈ (3.3 − 1.8 V)/220 Ω ≈ 7 mA.
- **Not an actual run** — this practical was designed/verified on paper. On real hardware you should see:
- **How many times does `setup()` run?** — Exactly once per power-on/reset.
- **Why the 220 Ω resistor?** — To limit LED current (≈7 mA) and protect both LED and GPIO.
- **What voltage is `HIGH` on ESP32?** — 3.3 V (not 5 V like Arduino UNO).
- **How would you change blink speed?** — Change the `delay()` values.
- **Which pin did you use and why?** — GPIO 26 — a safe digital pin with no boot constraints (avoids input-only 34–39 and strapping pins).

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.

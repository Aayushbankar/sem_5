# IoT Robot Car — NodeMCU V3 (ESP8266)

**End goal: autonomous vacuum-cleaner robot** — drive + suction + sensors
packaged in a box, self-navigating, web-controlled/supervised. Built on
NodeMCU V3 (ESP8266) + L298N + HC-SR04 + differential (tank) drive, powered
by 18650 cells. The NodeMCU hosts its own control page — no app, no cloud.

## Status

| CP | Milestone | State |
|---|---|---|
| CP-01 | Simple forward move (hold-to-drive over Wi-Fi) | ✅ verified |
| CP-02 | FWD/REV direction control | ✅ verified |
| CP-03 | Multi-network bring-up + power diagnosis | ✅ verified |
| CP-04 | Straight-line fix (caster) | ✅ verified |

Full evidence, bug post-mortems and rules: **[CHECKPOINT.md](CHECKPOINT.md)**.
Session/operating context for continuing work: **[LEDGER.md](LEDGER.md)**.

## Hardware

- NodeMCU V3 (ESP8266MOD)
- L298N dual H-bridge (ENA/ENB shunts **ON**)
- HC-SR04 ultrasonic (obstacle sensing — phase 3)
- 2× BO motors (differential drive), 2× 18650 in holder (7.4 V) via switch
- USB cable (flashing only)

### Pinout

| NodeMCU | GPIO | Function |
|---|---|---|
| D1 | 5 | HC-SR04 TRIG |
| D2 | 4 | HC-SR04 ECHO |
| D5 | 14 | L298N IN1 (left) |
| D6 | 12 | L298N IN2 (left) |
| D7 | 13 | L298N IN3 (right) |
| D8 | 15 | L298N IN4 (right) |
| onboard | — | LED: blink = Wi-Fi joining / driving, off = idle |

### ⚠️ Power rules (read before powering)

1. **Battery OFF + USB in** → flash / serial monitor.
2. **Battery ON + USB OUT** → drive. Wheels off the ground for bench tests.
3. **Never both** — L298N `5V` → NodeMCU `VIN` can back-feed your laptop's
   USB through the L298N diodes.
4. Battery + → L298N `12V`, battery − → L298N `GND` (via switch), motors →
   `OUT1..OUT4`.

## Control

After power-on, join the same Wi-Fi router as the NodeMCU
(`Airtel_akas_0733`), wait ~3 s for the LED to stop its joining blink, then
open:

- `http://nodemcu.local` (mDNS), or
- `http://192.168.1.12` (DHCP fallback)

| Endpoint | Effect |
|---|---|
| `GET /drive?c=FWD` | both motors forward |
| `GET /drive?c=REV` | both motors reverse |
| `GET /drive?c=STOP` | coast stop |

Safety: page re-sends the command every **60 ms** while held; firmware
**failsafe stops all motors after 500 ms** without a command (Wi-Fi drop,
tab closed, etc.).

## Sketches

| Folder | Purpose |
|---|---|
| `rc_motor_fwd_rev/` | **current firmware** — FWD/REV hold buttons |
| `rc_motor_test/` | CP-01 forward-only hold test |
| `rc_car_wifi/` | full tank control: FWD/BACK/LEFT/RIGHT/STOP |
| `hcsr04_v3/` | ultrasonic stop-on-obstacle autonomy |
| `hw_diag_test/` | 8-phase hardware diagnostic (motors + sensor) |
| `rc_robot/`, `rc_remote/` | retired ESP-NOW variant (kept for reference) |

## Flash

```bash
arduino-cli compile --clean --fqbn esp8266:esp8266:nodemcuv2 rc_motor_fwd_rev
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp8266:esp8266:nodemcuv2 rc_motor_fwd_rev
```

(PlatformIO or the Arduino IDE work too — board: **NodeMCU 1.0 (ESP-12E)**.)

## Circuit diagrams

- Current: [`circitu_dig_oct10.png`](circitu_dig_oct10.png)
- Iteration 1: [`circuit_digram_iteration_1.png`](circuit_digram_iteration_1.png)

## Roadmap (deadline: 2026-10-28 — passed; faculty-guided continuation 30 Oct)

1. ✅ CP-01 forward · ✅ CP-02 FWD/REV · ✅ CP-03 network bring-up · ✅ CP-04 caster fix · 🟡 CP-05 ESP32-CAM bring-up (wrong-pin root cause fixed 30 Oct — retest pending)
2. Stable control LAN (mobile hotspot now; spare-AP blocked → faculty) + power-split redesign
3. AUTO mode: HC-SR04 obstacle-avoidance loop (web toggle)
4. Suction module + boxed enclosure (all components inside)
5. 🎯 CP-06 target: autonomous + vacuum demo
6. 🎥 **ESP32-CAM track:** video stream + object detection on laptop dashboard; programmer = **ESP32-CAM-MB Type-C board** (Uno retired — now only a 5V bench supply); camera pins fixed to `CAMERA_MODEL_AI_THINKER` in `board_config.h` (stock example ships ESP-EYE — the 0x106 root cause)

# IoT Robot Car — NodeMCU V3 (ESP8266)

Wi-Fi web-controlled robot car: NodeMCU V3 + L298N motor driver + HC-SR04
ultrasonic + differential (tank) drive on 2× BO motors, powered by 2×18650
(7.4 V). The NodeMCU hosts its own control page — no app, no cloud.

## Status

| CP | Milestone | State |
|---|---|---|
| CP-01 | Simple forward move (hold-to-drive over Wi-Fi) | ✅ verified |
| CP-02 | FWD/REV direction control | ✅ verified, **on board** |

Full evidence, bug post-mortems and rules: **[CHECKPOINT.md](CHECKPOINT.md)**
(updated at every milestone).

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

## Roadmap

1. ✅ CP-01 forward move · ✅ CP-02 FWD/REV
2. Full tank control (pivots) on the phone — re-flash `rc_car_wifi`
3. HC-SR04 hard-STOP override + distance telemetry in the HTTP response
4. Optional: 10 kΩ pull-down on D7 (kills power-on motor twitch)

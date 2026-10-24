# IoT Robot Car — Checkpoints

## CP-01 — Simple forward move (2026-10-24) ✅

**Milestone: web-commanded straight-line drive works end-to-end.**

### What is verified working
- `rc_motor_test` flashed on NodeMCU V3 (ESP8266): single HOLD button on
  `http://nodemcu.local` / `http://192.168.1.12` → **both motors forward**,
  release → stop.
- Wi-Fi joins in 2–3 s (STA: `Airtel_akas_0733`), mDNS `nodemcu.local`.
- NodeMCU LED: blinks while joining Wi-Fi, **blinks fast while driving**,
  OFF when idle.
- Signals reach L298N: motor power path + ENA/ENB + OUT3/OUT4 (right) and
  left channel all proven. Earlier "dead motors" was missing/unchecked
  D5–D8 → IN1–IN4 link, later the test page's single-shot GO.

### Bug that nearly broke the demo (kept as lesson)
- Page sent **one GO per press**; Wi-Fi RTT (measured up to 134 ms via
  DevTools) let the 200 ms failsafe fire mid-hold → motors died after ~2 s.
- Fix: re-send GO every **60 ms while held**, failsafe raised to **500 ms**,
  STOP on release / tab-hide / pagehide.

### Hardware state / rules
- Pins: TRIG D1, ECHO D2, IN1 D5, IN2 D6, IN3 D7, IN4 D8.
- **Battery OFF + USB ON** for flash/serial; **battery ON + USB out** for
  driving. Never both (L298N 5V→VIN backfeed risk).
- ENA/ENB shunts ON. 2×18650 (7.4 V) → L298N 12V/GND via switch.
- L298N power LED = rail only (not command-indicatable); NodeMCU LED is
  the command indicator.

### Sketch inventory
| Sketch | Status |
|---|---|
| `rc_motor_test` | **current on board** — hold-to-drive forward test |
| `rc_car_wifi` | full tank control (FWD/BACK/LEFT/RIGHT/STOP) — next to re-flash |
| `hcsr04_v3` | ultrasonic autonomy (validated earlier) |
| `hw_diag_test` | 8-phase hardware diag (validated earlier) |
| `rc_robot` / `rc_remote` | ESP-NOW variants, retired (no ESP32) |

### Next
1. Re-flash `rc_car_wifi` for full directional control on the phone.
2. Phase 2: HC-SR04 hard-STOP override + distance telemetry in HTTP reply.
3. Optional: 10 kΩ pull-down on D7 to kill power-on right-motor twitch.

# IoT Robot Car — Checkpoints

Protocol: each checkpoint = verified milestone, evidence, docs touched.
Keep this file updated on every new milestone (documentation is mandatory).

---

## CP-01 — Simple forward move (2026-10-24) ✅

**Milestone: web-commanded straight-line drive works end-to-end.**

### Docs / artifacts
- Sketch: [`rc_motor_test/rc_motor_test.ino`](rc_motor_test/rc_motor_test.ino)
- Circuit: [`circitu_dig_oct10.png`](circitu_dig_oct10.png) (current),
  [`circuit_digram_iteration_1.png`](circuit_digram_iteration_1.png) (v1)
- Root overview: [`README.md`](README.md)

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

---

## CP-02 — FWD / REV direction control (2026-10-24) ✅

**Milestone: reversible drive — both directions web-commanded and verified
on hardware.**

### Docs / artifacts
- Sketch: [`rc_motor_fwd_rev/rc_motor_fwd_rev.ino`](rc_motor_fwd_rev/rc_motor_fwd_rev.ino)
- Depends on CP-01 lessons (60 ms refresh + 500 ms failsafe), same wiring
  per [`circitu_dig_oct10.png`](circitu_dig_oct10.png).

### What is verified working
- Two hold buttons: **HOLD FWD** (green) and **HOLD REV** (red) on
  `http://nodemcu.local`.
- FWD pattern: D5=H/D6=L (left), D7=H/D8=L (right).
- REV pattern: D5=L/D6=H, D7=L/D8=H — each H-bridge pair swapped, both
  motors reverse.
- Release / tab-hide / pagehide → STOP; 500 ms failsafe; LED blinks while
  driving. Flash + bench-tested on NodeMCU (battery-only run).

### L298N drive logic reference
| IN1 | IN2 | Left motor |
|---|---|---|
| H | L | forward |
| L | H | reverse |
| H | H | brake |
| L | L | coast |

(IN3/IN4 identical for the right motor.)

---

## Current state & Next

- **On board now:** `rc_motor_fwd_rev` (CP-02).
- **Next up:**
  1. Re-flash `rc_car_wifi` for full tank control (pivots + back).
  2. Phase 3: HC-SR04 hard-STOP override + distance telemetry in HTTP reply.
  3. Optional: 10 kΩ pull-down on D7 to kill power-on right-motor twitch.

## Full sketch inventory
| Sketch | Status |
|---|---|
| `rc_motor_fwd_rev` | **current on board** — FWD/REV hold buttons (CP-02) |
| `rc_motor_test` | forward-only hold test (CP-01) |
| `rc_car_wifi` | full tank control — next to re-flash |
| `hcsr04_v3` | ultrasonic autonomy (validated earlier) |
| `hw_diag_test` | 8-phase hardware diag (validated earlier) |
| `hcsr04_l298n_test`, `hcsr04_l298n_v2`, `hcsr04_test` | earlier stages |
| `rc_robot` / `rc_remote` | ESP-NOW variants, retired (no ESP32) |

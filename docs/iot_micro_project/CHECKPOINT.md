# IoT Robot Car — Checkpoints

Protocol: each checkpoint = verified milestone, evidence, docs touched.
Keep this file updated on every new milestone (documentation is mandatory).
**Session continuity: read [`LEDGER.md`](LEDGER.md) first** — full operating
context (board state, network history, power analysis, tooling, repos).

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

## CP-03 — Multi-network bring-up + power diagnosis (2026-10-26) ✅

**Milestone: control page reachable from three different networks; floor-stall
root-caused (documented, fix pending).**

### Docs / artifacts
- Full context: [`LEDGER.md`](LEDGER.md) (§4 network journey, §6 power, §7 turns)
- Sketches: `rc_motor_fwd_rev_wifi/` (vivo — unusable, 5 GHz),
  `rc_motor_fwd_rev_gpmain/` (college — verified HTTP 200 cross-VLAN),
  `rc_motor_fwd_rev_patels/` (**current on board**)
- Network rules derived: ESP8266 = 2.4 GHz only, WPA2-PSK only;
  portals don't block LAN HTTP; use raw IP outside home LAN.

### What is verified working
- `GP-MAIN` join → IP 192.168.18.224, laptop→ESP ping + **HTTP 200 (0.1 s)**
  across VLANs; captive-portal probes clean (`generate_204` → 204).
- `Patel's F15` (2.4 GHz) join → IP **10.197.7.58** (current firmware).
- Serial workflow proven for IP recovery (DTR-pulse reset script, §8 LEDGER).

### Power diagnosis (findings, fix open)
- On-floor stall while in-air runs fine + ESP alive → ranked: L298N thermal
  shutdown > mechanical load > shared-rail sag. Options A (separate battery),
  B (buck → VIN, recommended), C (TB6612 swap, real fix) analyzed in
  [`LEDGER.md`](LEDGER.md) §6. Next: blocks-test, rigid mounting, buck, TB6612.

### Turn theory (ready for firmware)
- LEFT pivot = L rev + R fwd (`L H H L`); RIGHT = mirror (`H L L H`);
  PWM arc turns need ENA/ENB shunts removed. Details: LEDGER §7.

---

## CP-04 — Straight-line fix (2026-10-27) ✅

**Milestone: drive mechanics corrected — robot tracks straight.**

### Docs / artifacts
- Evidence: pen test `photos/Tubfront.jpeg` (user), analysis in
  [`LEDGER.md`](LEDGER.md) §10.0 + §12.

### What is verified working
- **Caster repositioned to the true centerline** (user, 27th) — straight-line
  defect closed; residual: powered-drift test + wheel-diameter check if any
  curve remains.

### Power-rail split — NOT done (attempted → rolled back)
- Tried once (27th), **user not satisfied → rolled back to the original
  wiring**. **Retry planned 28th with a better redesign** (§6 of LEDGER;
  rule unchanged: separate rails, D5–D8 + **common GND** only).

### Parked (not a failure — documented in LEDGER §12)
- Spare-ESP dedicated AP (`esp_softap/` written, compiled): **flash blocked
  by a marginal spare board** (random mid-session timeouts on ROM+stub,
  both cables tried, manual D3/RST download mode tried). Faculty help 28th;
  fallbacks: flash via car NodeMCU as USB-serial, or replace board.
- Control returns to the mobile hotspot (firmware `rc_motor_fwd_rev_patels`
  already on the car).

---

## CP-05 — ESP32-CAM bring-up + wrong-pin root cause (2026-10-30) ✅

**Milestone: CAM board proven (flash/serial/WiFi/page) + 0x106 root-caused to
a shipped example bug + **camera PASS on retest** — MJPEG stream live
(`10.164.40.97:81/stream`, ~4 FPS 240×240).**

### Docs / artifacts
- Full evidence: [`LEDGER.md`](LEDGER.md) §13 (CAM section, incl. full retest
  log) + §12 (30 Oct log) + §4 (vivo band change)
- Sketches: `esp32cam_flash/CameraWebServer/` (**current on cam — verified
  streaming**), `esp32cam_flash/cam_led_test/` (bench LED verdict firmware)
- Guide adopted: Instructables ESP32-CAM streaming (faculty-suggested)

### What is verified working
- ESP32-CAM-MB (CH340C) auto-reset upload: clean writes to
  `/dev/ttyUSB0`, `esp32:esp32:esp32cam` FQBN.
- Board healthy: serial output, WiFi joins (Patel's F15 earlier →
  **`vivo Y28 5G` now, IP `10.164.40.97`**), status page HTTP 200.
- Rails: 5V = 5.19 V, 3V3 = 3.19 V. MB-free power (Uno 5V/GND) works.
- **MB exonerated** as camera saboteur (identical failure Uno-powered).
- **Camera probe PASSES with correct AI-Thinker pins** (root cause fix
  validated) — GC2145 confirmed: rejects JPEG → RGB565 works.
- **Stream live:** root `:80` HTTP 200; `:81/stream` HTTP 200
  `multipart/x-mixed-replace`; 6-s capture = 23 complete 240×240 JPEG
  frames (~4 FPS), extracted frame decodes clean (`file`/ImageMagick).
  RGB565→JPEG conversion is software (`frame2jpg` in `stream_handler`).

### Root cause (found + validated 30 Oct)
- Stock example `board_config.h` **ships with `CAMERA_MODEL_ESP_EYE`
  active (line 15) / `CAMERA_MODEL_AI_THINKER` commented (line 23)** →
  every init used ESP-EYE pin table → `0x106 ESP_ERR_NOT_SUPPORTED`.
- Fix: line 15 off, line 23 on → **retest passed on first flash.**
- Second finding: GC2145 has **no JPEG encoder** → `PIXFORMAT_RGB565`
  in `CameraWebServer.ino` L45/46 (one-line revert to JPEG if an OV2640
  module ever lands).
- **Camera module healthy — never replace it.**

### Gotchas documented (do not regress)
- `arduino-cli upload` does **NOT** recompile — always `compile` first;
  `No changed sectors found` + stale cache `.ino.bin` = you just flashed
  an old build (bit us once with old Patel's creds).
- Wi-Fi passwords live only in sketch headers (private repo) — never docs.

### Next action (start of dashboard phase)
- Reflash robot NodeMCU with `rc_motor_fwd_rev_wifi` (`vivo Y28 5G` creds
  in header) → cam + robot + laptop on one LAN → build dashboard
  (`<img src="http://10.164.40.97:81/stream">` + `/drive` buttons).

---

## CP-06 — Autonomous cleaner + vision autonomy (target, 🟡 research done 2026-10-31)

**Goal:** self-driving cleaning demo — manual dashboard drive, AI
(dumb-follower) control, ultrasonic AUTO patrol, suction. Research complete,
implementation not started.

- **Full research doc (read before building):**
  [`CP06_RESEARCH.md`](CP06_RESEARCH.md) — parts inventory, LEFT/RIGHT
  steering plan (firmware-only, incl. the one-PWM-pin constraint), 2026
  vision-model benchmarks (YOLO26n vs MediaPipe BlazeFace vs Haar — all
  faster than our 4 FPS stream), streaming-protocol verdict (keep MJPEG),
  10 designs with pros/cons, build order.
- Prereq chain: NodeMCU → same hotspot → turn firmware → dashboard →
  YOLO26n follower → AUTO → power split → vacuum.

---

## Current state & Next

- **END GOAL:** autonomous vacuum cleaner (all parts boxed, self-driving,
  cleaning) — original deadline 2026-10-28 (passed; faculty-guided extra work).
- **Milestones:** CP-01 · CP-02 · CP-03 · CP-04 · CP-05 ✅ (CAM streaming live) · **CP-06 🟡 (research done — see [`CP06_RESEARCH.md`](CP06_RESEARCH.md))**.
- **Power split:** attempted 27th → **rolled back**; redesign pending.
- **On board (robot):** `rc_motor_fwd_rev_patels` — joins **Patel's F15**;
  get IP from serial after power-up. **Must move to `vivo Y28 5G`** (reflash
  `rc_motor_fwd_rev_wifi`) for same-LAN dashboard.
- **On board (cam):** `CameraWebServer` (RGB565) — joins **`vivo Y28 5G`**,
  IP **10.164.40.97** (DHCP — re-read from serial on reboot); live MJPEG at
  `http://10.164.40.97:81/stream`, control page `:80`.
- **Video track:** ESP32-CAM → MJPEG on laptop dashboard + drive buttons to
  NodeMCU `/drive` — **camera half DONE (CP-05)**; NodeMCU does not proxy
  video; robot needs the vivo-creds reflash for one LAN.
- **Authoritative plan:** [`LEDGER.md`](LEDGER.md) §10 (open items),
  §11 (vacuum build), §12 (session log), §13 (ESP32-CAM track).

## Full sketch inventory
| Sketch | Status |
|---|---|
| `rc_motor_fwd_rev` | **current on robot** — FWD/REV hold buttons (CP-02) |
| `rc_motor_test` | forward-only hold test (CP-01) |
| `rc_car_wifi` | full tank control — next to re-flash |
| `hcsr04_v3` | ultrasonic autonomy (validated earlier) |
| `hw_diag_test` | 8-phase hardware diag (validated earlier) |
| `hcsr04_l298n_test`, `hcsr04_l298n_v2`, `hcsr04_test` | earlier stages |
| `rc_robot` / `rc_remote` | ESP-NOW variants, retired (no ESP32) |
| `esp32cam_flash/CameraWebServer` | **current on cam — stream verified live (`10.164.40.97:81/stream`, CP-05)** |
| `esp32cam_flash/cam_led_test` | LED verdict firmware — archived bench tool |

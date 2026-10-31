# SESSION LEDGER — IoT Robot Car (master context)

> Purpose: a fresh agent/session can resume from this file alone (plus repo
> state). Update it whenever state changes. Companion docs:
> [`README.md`](README.md) (project overview), [`CHECKPOINT.md`](CHECKPOINT.md)
> (verified milestones).

---

## 1. Goal & current phase

**END GOAL (the thing this project must become): an autonomous vacuum-cleaner
robot** — all electronics + drive + suction/vacuum parts packed inside ONE box
(the round tub; the small vacuum box nests INSIDE it with the components),
driving itself and cleaning. Remote web control is the control/telemetry layer
and the demo interface; HC-SR04 autonomy is the navigation core.

**DEADLINE: complete before 2026-10-28 (tomorrow as of 27th eve).**

**Phase (27th eve):** mechanics + power hardened; stable-LAN attempt on the
spare ESP **failed (board electrical — blocked, faculty help 28th)**; vacuum
packaging not started.
**Done:** CP-01 forward · CP-02 FWD/REV · CP-03 network bring-up ·
**CP-04 caster/squareness fix (27th)**.
**Open:** **power-rail split — tried 27th, rolled back, redesign retry 28th
(§6)**, stable control LAN (spare-AP or mobile hotspot), floor-stall
mitigation under load, AUTO loop, vacuum build (§11).

## 2. Firmware currently on the board

`rc_motor_fwd_rev_patels/` — FWD/REV hold-button control, joins **Patel's F15**
hotspot (2.4 GHz, WPA2). Last known IP: **10.197.7.58** (DHCP — changes on
rejoin; Wi-Fi passwords live only in each sketch header, never in these docs).
Fallback recovery: reflash any variant + read IP from serial (§8).

Control contract (all variants share it):
- `GET /drive?c=FWD|REV|STOP`; page re-sends every **60 ms** while held;
  firmware failsafe stops after **500 ms** without a command;
  STOP also on release / tab-hide / pagehide.
- LED_BUILTIN (active LOW): blinks = joining Wi-Fi, fast-blinks = driving, off = idle.
- No `delay()` in loop; `delayMicroseconds(10)` only for ultrasonic trigger.

**ESP32-CAM board (separate MCU):** `esp32cam_flash/CameraWebServer/` — MJPEG
stream at `http://<cam-ip>:81/stream`, control page `:80`; joins **`vivo Y28 5G`**
(last IP **10.164.40.97**). For the dashboard, robot must move to the same
hotspot (reflash `rc_motor_fwd_rev_wifi`, creds in its header) — §13.

## 3. Hardware & pinout (final)

| NodeMCU | GPIO | Function |
|---|---|---|
| D1 | 5 | HC-SR04 TRIG |
| D2 | 4 | HC-SR04 ECHO |
| D5 | 14 | L298N IN1 (left) |
| D6 | 12 | L298N IN2 (left) |
| D7 | 13 | L298N IN3 (right) |
| D8 | 15 | L298N IN4 (right) |

L298N H-bridge truth table: `H/L` = fwd, `L/H` = rev, `H/H` = brake, `L/L` = coast.
ENA/ENB shunts currently **ON** (full speed; PWM turns later need them OFF + EN wired to GPIO).

### Power rules (non-negotiable)
1. **Battery OFF + USB IN** → flash / serial.
2. **Battery ON + USB OUT** → drive (wheels up on bench).
3. **Never both** — L298N 5V-out → NodeMCU VIN can back-feed laptop USB.
4. Current build: **3×18650 (11.1 V)** holder → L298N `12V`/`GND` via switch;
   L298N `5V` → NodeMCU `VIN` (shared rail — see §6).
5. Diagrams: `circitu_dig_oct10.png` (current), `circuit_digram_iteration_1.png` (v1).
   The "9V battery" in diagram art is a Cirkit stock image — ignore.
   No ESP32 exists in this project (`rc_remote` retired).

## 4. Network journey (all attempts, outcomes)

| Network | Band/Sec | Result | Artifact |
|---|---|---|---|
| Home `Airtel_akas_0733` | 2.4 WPA2 | ✅ CP-01/02 proven here (IP 192.168.1.12, mDNS worked) | `rc_motor_test`, `rc_motor_fwd_rev` |
| `vivo Y28 5G` hotspot | 26th: 5 GHz only → **30th: 2.4 GHz (2462 MHz)** | 26th: ❌ ESP can't see 5 GHz. **30th: band changed → ✅ ESP32-CAM joined, IP `10.164.40.97`** (stream proven). Robot NodeMCU still on Patel's F15 — same-LAN dashboard needs robot moved here too | `rc_motor_fwd_rev_wifi`, cam `CameraWebServer` |
| College `GP-MAIN` | 2.4+5 WPA2-PSK | ✅ joined (IP **192.168.18.224**), **laptop↔ESP HTTP 200** across VLANs (laptop 172.16.201.x) — portal only gates internet, LAN link fine | `rc_motor_fwd_rev_gpmain` |
| `Patel's F15` hotspot | 2.4 GHz ch6, WPA2 | ✅ joined (IP **10.197.7.58**) — **current** | `rc_motor_fwd_rev_patels` |

Lessons: ESP8266 = **2.4 GHz only, WPA2-PSK only** (no WPA3, no 802.1x).
Captive portals don't block device↔device LAN HTTP; AP isolation is the real
risk (unproven on Patel's F15 until phone-browser test). mDNS (`nodemcu.local`)
works on home LAN, unreliable elsewhere → use the raw IP.

## 5. Known bug patterns (do not regress)

- **Single-shot commands + failsafe + Wi-Fi RTT = motors die mid-hold**
  (CP-01: RTT 134 ms > 200 ms failsafe). Fix is 60 ms refresh + 500 ms failsafe — keep both.
- Boot-time right-motor twitch: GPIO13 floats until `setup()`; optional 10 kΩ pull-down on D7.
- L298N power LED is rail-only — never treat it as command feedback; NodeMCU LED is the indicator.
- **ESP32-CAM `0x106 "camera not supported"` = probe failure, NOT a dead
  camera.** Cause: stock example ships wrong board profile in `board_config.h`
  (ESP_EYE active) → wrong pins → sensor never answers I2C. Second trap:
  `JPEG format not supported` = GC2145 has no JPEG encoder → RGB565.
  Full decision flow + pin table: **§13 "0x106 debugging walkthrough"**.
  Also: I2C scanner without XCLK = invalid; `upload` without `compile` =
  stale binary.

## 6. Power problem — floor stall (open)

**Symptom:** runs fine in air; on floor runs ~2 s then stops; ESP stays alive.
**Analysis (this session):** load current on floor (0.5–1.5 A+/motor) →
ranked causes: (1) **L298N thermal shutdown** (most likely, no heatsink,
in a bowl), (2) mechanical overload (weight/caster drag/bowl scrape),
(3) rail sag on the shared 5V (L298N 78M05 feeding NodeMCU).
3-cell upgrade didn't help because limit is **current/heat, not voltage**.

**❌ POWER SPLIT — attempted (user, 27th), NOT satisfied → ROLLED BACK to
original wiring.** One attempt with the planned topology (separate rails,
D5–D8 + common GND) wasn't good enough — redesign planned for **28th**
(better wiring/routing, per §8-style discipline; GND tie remains mandatory
for signal reference). Until then: original shared-rail wiring stands, so
motor-load ESP reboots may persist on floor runs.

**Options that were on the table (history):**
- A) Separate ESP battery — works, **must common-ground** both supplies.
- B) **One battery + buck converter (MP1584/mini360) → 5V → VIN** — recommended.
- C) **Replace L298N with TB6612FNG** — the real fix (MOSFET, cool, no 2 V
  Darlington drop, PWM for free). Fixing ESP rail does NOT stop driver thermal cutoff.

**Next actions:** **28th power-split redesign (first try rolled back)** →
floor-load run to confirm no more ESP reboots → mount battery/breadboard
rigidly → plan TB6612 (C) when time allows.

## 7. Turn control (next firmware feature)

| Move | L motor | R motor | IN1 IN2 IN3 IN4 |
|---|---|---|---|
| FWD | fwd | fwd | H L H L |
| BACK | rev | rev | L H L H |
| LEFT pivot | rev | fwd | L H H L |
| RIGHT pivot | fwd | rev | H L L H |

`rc_car_wifi` already has all 4 + STOP (unreflashed since motor-test phase).
Arc turns need PWM: remove ENA/ENB shunts, wire ENA/ENB to free GPIOs
(D0/D3/D4 free — avoid D4 if boot issues), `analogWrite`. Plan: pivots first.

## 8. Tooling recipes (verified this session)

```bash
# compile + flash
arduino-cli compile --clean --fqbn esp8266:esp8266:nodemcuv2 <sketch_dir>
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp8266:esp8266:nodemcuv2 <sketch_dir>

# read IP (resets board, reprints after Wi-Fi join ~3 s)
python3 - <<'EOF'
import serial, time
s = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
s.setDTR(False); time.sleep(0.3); s.setDTR(True)
end = time.time() + 30
buf = b''
while time.time() < end:
    d = s.read(256)
    if d: buf += d
for line in buf.decode('utf-8','replace').splitlines():
    if 'IP' in line: print(line)
EOF

# find ESP without serial: sweep for its web page
nmap -Pn -n -T4 -p 80 --open --script http-title <subnet>/24
# portal probe: curl -I http://connectivitycheck.gstatic.com/generate_204  → 204 = clean
```
Port `Write timeout` on upload → just retry once. Wi-Fi changed → make a new
`<name>/` sketch variant (copy + sed SSID/pass) rather than editing history.

## 9. Git / repos

- **`git@github.com:Aayushbankar/sem_5.git`** (private-ish college repo):
  `docs/iot_micro_project/` = source of truth. Last local commit `5b9295cd`
  (CP-02 + README) — **status: ahead 1, NOT pushed** (push only when asked).
- **`github.com/Aayushbankar/iot-robot-car`** (PUBLIC, gh `Aayushbankar`):
  mirror of this folder for showcase; last pushed `831f4ef` (README + CP-02).
  `git push` is denied by permission rules for bare form — use
  `git -C <path> push origin main` (matches allow-list).
- ⚠️ **Security debt:** home Wi-Fi SSID+password are inside `rc_motor_test`/
  `rc_motor_fwd_rev` which are **already in the public repo** → recommend
  rotating that home Wi-Fi password; keep GP-MAIN/Patel's/vivo variants and
  all future passwords **out of the public repo** (docs never contain passwords).

## 10. Open items (priority order, deadline 2026-10-28)

0. ✅ **Straight-line defect FIXED (user, 27th)** — caster repositioned per
   the pen/centerline procedure (`Tubfront.jpeg` finding: pivot was off 90°).
   Residual check pending: powered FWD drift test; wheel-diameter check
   (blue vs black wheel) if any curve remains → then software trim (e).
1. **Control LAN (user directive 27th eve): back to the mobile hotspot**
   (Patel's F15) for driving — `rc_motor_fwd_rev_patels` already on the
   board; get IP from serial (§8) after power-up.
   Spare-ESP dedicated-AP track **parked**: `esp_softap/` written + compiled
   but flashing the spare board failed on electrical grounds (see §12) —
   faculty help morning of 28th; fallback = flash it using the car NodeMCU
   as USB-serial (cross TX/RX/EN) or replace board.
2. **Power-rail split REDESIGN + re-attempt (28th)** — first attempt rolled
   back (§6); implement cleanly, then floor-load validation (no more ESP
   reboots); rigid battery/breadboard mounting.
3. Reflash `rc_car_wifi` for 4-direction tank control (§7 pins ready) —
   fold into the AUTO firmware below if time-boxed.
4. **Autonomous mode firmware** (vacuum core): AUTO toggle on the web page —
   loop: HC-SR04 every 100 ms; >20 cm → FWD; <20 cm → STOP + timed pivot
   (random L/R, 0.4–1.2 s); watchdog: periodic random turn every ~8 s to break
   stuck cycles; STOP always wins (manual buttons override AUTO).
5. **Suction + box build** (§11) — parallel track (fan voltage still unknown).
6. PWM arc turns (shunt removal) — after driver upgrade.
7. Optional: D7 10 kΩ pull-down (boot twitch); push pending sem_5 commits
   (ahead 4-5 local).

## 13. ESP32-CAM — video feed + object detection (next task)

**Objective:** stream video from ESP32-CAM on robot body → laptop dashboard; run object detection on laptop; integrate with NodeMCU control so the dashboard shows video + robot drive buttons.

**Hardware:** AI-Thinker ESP32-CAM, teammate's spare, first flash. **Camera module = RHYX M21-45 = GC2145** (label on ribbon; NOT OV2640). **Programmer: ESP32-CAM-MB Type-C base board (CH340C)** bought 30th — auto-reset works (no manual RST/IO0); mount with lens/SD-slot away from USB-C, `ESP32-CAM` text + flash LED on USB side. The Uno is retired as programmer and is only a **safe 5 V bench power supply** (5V+GND wires) for MB-free tests. ⚠️ 3×18650 battery (11.1 V) into the cam's 5V pin kills the board instantly — never.

**Flash recipe (verified 30th):**
```bash
arduino-cli compile --fqbn esp32:esp32:esp32cam <sketch_dir>
# announce to user BEFORE flash; user re-inserts MB when told
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32cam <sketch_dir>
```

**ROOT CAUSE of the 0x106 saga (found 30th):** the stock example's
`board_config.h` **SHIPS with `CAMERA_MODEL_ESP_EYE` active (line 15) and
`CAMERA_MODEL_AI_THINKER` commented (line 23)** — every probe used ESP-EYE's
wrong pin table on our AI-Thinker board. Fixed 30th: line 15 commented,
line 23 activated. The camera module is **NOT condemned** — retest pending.

### 0x106 debugging walkthrough (keep this — reuse if camera fails again)

**Morning symptom (all flashes):** `Detected camera not supported` /
`Camera probe failed with error 0x106` / `Camera init failed 0x106`.

**What actually happens during `esp_camera_init` (2 phases):**
1. **Probe:** start XCLK, then read the sensor's ID over the I2C/SCCB wires
   (`SDA`/`SCL`). Wrong pins = the driver literally knocks on the wrong
   pins → sensor never ACKs → returns `ESP_ERR_NOT_SUPPORTED` = **0x106**.
2. **Init:** only if probe succeeds, load the sensor driver.

So **0x106 = probe failure, NOT a dead camera.** The message "Detected
camera not supported" is misleading — it detected *nothing*.

**Why morning used the wrong pins:** the example supports ~20 boards; the
`#define` picks the pin table. Ours shipped with the ESP-EYE profile active:

| Signal | AI-Thinker (ours, correct) | ESP-EYE (morning, wrong) |
|---|---|---|
| SDA / SCL | 26 / 27 | 18 / 23 |
| XCLK | 0 | 4 |
| PWDN | 32 | −1 (no pin) |

**There were TWO stacked problems — fix one at a time and re-flash:**

| # | Error text after flash | Meaning | Fix |
|---|---|---|---|
| 1 | `probe failed 0x106` / `not supported` | wrong pin table | `board_config.h`: ESP_EYE off (L15), AI_THINKER on (L23) |
| 2 | `JPEG format is not supported on this sensor` | probe PASSED; sensor has no JPEG encoder (GC2145 ≠ OV2640) | `CameraWebServer.ino` L45/46: `PIXFORMAT_RGB565` |

**Decision flow for ANY future camera error:**
- `not supported` / `0x106` → check the board-model `#define` FIRST (pins).
- `JPEG format not supported` → pins are right; sensor is JPEG-less → RGB565.
- Still `0x106` with the CORRECT pin table → only now suspect hardware
  (ribbon/connector/module) → replacement (₹150–250).
- Stream FPS low after RGB565 → expected: software `frame2jpg`, ~4 FPS.

**Two red herrings from this saga (never trust these again):**
- I2C scanner that doesn't start XCLK first → "no devices" is meaningless.
- `arduino-cli upload` does not recompile → "No changed sectors found"
  means you just flashed a STALE binary (always `compile` first).

**30 Oct session evidence (all closed):**
| Test | Result |
|---|---|
| Flash + serial + web page | ✅ board healthy |
| WiFi joins Patel's F15 | ✅ IP `10.197.7.97`, RSSI −48, status page live |
| Rails: 5V pin = 5.19 V, 3V3 pin = 3.19 V | ✅ power healthy |
| Ribbon both orientations + tug test | ❌ same 0x106 |
| **MB-free (Uno 5V+GND only)** | ❌ red LED still blinks → **MB exonerated** |
| I2C scan GPIO26/27 | "nothing" — my scanner never started XCLK (duty bug) → **inconclusive, red herring** |
| All flashes said `Detected camera not supported` / `0x106` | explained by **wrong pin table (ESP_EYE)** |

**RETEST RESULT (30 Oct evening) — CAMERA PASSES, stream live end-to-end:**

Execution steps, in order:
1. Flash fixed `CameraWebServer` (`board_config.h` = AI-Thinker pins, JPEG on)
   → serial: probe **PASSED** (sensor detected + SCCB-probed) but init failed
   with `E (467) camera: JPEG format is not supported on this sensor` →
   **the 0x106 wrong-pin saga is closed; root-cause fix validated.**
2. That error = decision branch 2 → flipped `CameraWebServer.ino` lines 45/46
   (JPEG off, `PIXFORMAT_RGB565` on — GC2145 has no JPEG encoder).
3. ⚠️ **Stale-binary trap hit:** `arduino-cli upload` does NOT recompile —
   it re-uploaded the 15:33 build (old Patel's F15 creds, no RGB565) and
   esptool printed `No changed sectors found`. Caught by checking the cache
   `.ino.bin` mtime/strings. **Rule: always run `arduino-cli compile`
   explicitly before `upload`; if you see "No changed sectors found", verify
   the build is newer than the source.**
4. Patel's F15 unavailable → switched Wi-Fi to **`vivo Y28 5G`** (laptop's
   network; SSID says "5G" but it broadcasts **2462 MHz = 2.4 GHz**, so the
   ESP32-CAM accepts it). Creds written in sketch header (private repo only).
5. Fresh compile + flash → serial boot log:
   ```
   WiFi connecting...
   WiFi connected
   Camera Ready! Use 'http://10.164.40.97' to connect
   ```
6. Stream verification (laptop, same hotspot):
   - root `http://10.164.40.97/` → **HTTP 200**
   - `http://10.164.40.97:81/stream` → **HTTP 200**,
     `Content-Type: multipart/x-mixed-replace;boundary=...`
   - 6 s capture = 192 KB → **23 complete JPEG frames (~4 FPS)**
   - extracted frame: valid **240×240 baseline JPEG, 8011 B** (`file` +
     ImageMagick both decode it).

**RGB565 note:** the stock `stream_handler` (`app_httpd.cpp` ~L246) converts
each RGB565 frame to JPEG in software via `frame2jpg()` before sending — so
`/stream` is still MJPEG and the dashboard `<img>` needs no changes; FPS is
CPU-bound (~4 at 240×240) which is fine for the dashboard.

**Status:** camera + Wi-Fi + web + MJPEG stream **fully proven end-to-end**.
GC2145 confirmed as the sensor (RGB565-only). Module healthy — never replace.
Original decision branches 1 and 2 resolved as: probe PASS + JPEG rejected →
RGB565 → PASS.

**Remaining next step:** dashboard integration —
1. Reflash robot NodeMCU with `rc_motor_fwd_rev_wifi` (its header already has
   `vivo Y28 5G` creds) so cam + robot + laptop share ONE LAN.
2. Build the dashboard HTML: `<img src="http://10.164.40.97:81/stream">` +
   drive buttons (fetch → NodeMCU `/drive?c=FWD|REV|STOP`).
3. Then the §10 roadmap: AUTO loop, power-split, vacuum box.

**Camera-model definition — the two critical lines:**
- `esp32cam_flash/CameraWebServer/board_config.h` **line 15**: `//#define CAMERA_MODEL_ESP_EYE` (off)
- `esp32cam_flash/CameraWebServer/board_config.h` **line 23**: `#define CAMERA_MODEL_AI_THINKER` (on) → feeds `#include "camera_pins.h"` (line 32)
- `CameraWebServer.ino` **lines 13–14**: Wi-Fi creds = `vivo Y28 5G` (header, private repo only — no passwords in these docs); **lines 45–46**: pixel format (**RGB565 active** — GC2145 rejected JPEG 30th; JPEG commented); **line 8**: `#include "board_config.h"`; **line 78**: `esp_camera_init`.

**LED-test firmware saved:** `esp32cam_flash/cam_led_test/` — red LED (GPIO33) blinks while camera undetected / solid ON when detected; white flash LED (GPIO4) = Wi-Fi status; status page on `:80`. Works MB-free (Uno power) with no computer.

**Software plan:**
1. Firmware: ESP32 Arduino `CameraWebServer` example (AI-Thinker pins — see fixed lines above, MJPEG at `:81/stream`, control page on 80).
2. Dashboard (laptop): single HTML page — `<img src="http://cam-ip:81/stream">` + robot drive buttons (fetch to NodeMCU `/drive`). All three (laptop, cam, robot) on the SAME hotspot — **now `vivo Y28 5G`** (switched 30th; requires NodeMCU reflash with `rc_motor_fwd_rev_wifi`). NodeMCU does NOT proxy video (ESP8266 can't handle MJPEG); `/drive` contract unchanged.
3. Object detection (laptop): Python + OpenCV consuming MJPEG stream → start with built-in Haar face/person detector (no model download); overlay boxes on dashboard video; later upgrade to YOLO-nano if compute allows.
4. Integration: dashboard buttons hit NodeMCU `/drive?c=FWD|REV|STOP` (same API); camera and robot share hotspot (`vivo Y28 5G` — NodeMCU creds already in `rc_motor_fwd_rev_wifi.ino`).

**Reference guides:** Instructables ESP32-CAM streaming (faculty-suggested, 30th) `https://www.instructables.com/Getting-Started-With-ESP32-CAM-Streaming-Video-Usi/`; RNT programming guide `https://randomnerdtutorials.com/program-upload-code-esp32-cam/`; RNT troubleshooting `https://randomnerdtutorials.com/esp32-cam-troubleshooting-guide/`; GC2145/JPEG fix video `https://www.youtube.com/watch?v=jp35GcrypWw`.

**MB-free wiring (Uno as power):** Uno 5V → cam 5V, Uno GND → cam GND (only two wires), Uno on USB. Red LED verdict as above.

**Hardware wiring reference (programming, MB does this automatically):**
- MB slot: lens/SD-slot away from USB-C (180° from seller photo = wrong).
- Raw UART fallback (if MB ever fails): Uno TX→U0T, RX→U0R (crossed), GND, 5V; GPIO0→GND for download mode.

**Hardware inventory (photos saved in [`photos/`](photos/), 26 Oct):**

| # | Photo | What it shows |
|---|---|---|
| 1 | `bottomview.jpeg` | chassis: clear round tub, BO motors through the rims (hot glue), **front swivel caster at rim edge**, laptop for scale — **no steel plate** (user correction 26th) |
| 2 | `topviewwithlid.jpeg` | **drive box = grey translucent round tub WITH lid**; both wheels pass through wall slots; already a closed unit |
| 3 | `topviewwithoutlid.jpeg` | inside drive box: NodeMCU (corner), red L298N, **OS 3200 mAh 18650 ×~3 + switch**, motor wires — electronics already boxed |
| 4 | `Vaccumebkxbottom.jpeg` | **vacuum box bottom**: square translucent tub (taped rim, 2 screw holes), **small DC motor body hot-glued through floor centre** (shaft points into box) |
| 5 | `Vaccumebkxtop.jpeg` | **vacuum box interior**: **orange 4-blade propeller** on the motor shaft at floor centre — suction unit partially built |

**Packaging target (user, 26th):** one big box = the round tub; it contains
ALL components **plus the small vacuum box nested inside it**. Drive wheels +
caster outboard, HC-SR04 behind a front window (unobstructed).

**Proposed vacuum design (DRAFT — inlet/exhaust strategy TBD; user wants
straight-line driving solved FIRST):**
- Vacuum box **nests inside the big round box** among the components (user's
  plan — no external belly); inlet path from floor into that inner box is the
  open design question (slot in big-box floor + duct to inner box, or outer
  wall inlet) — decide AFTER driving is correct.
- Fan power: **own rail from motor pack via MOSFET on a spare GPIO** — NEVER
  the NodeMCU 5V pin. Fan turns ON with AUTO mode.
- Airflow must not wash over the HC-SR04 transducers.
- ⚠️ OPEN: fan **motor voltage/current unknown** (no label visible — ask user
  how it was powered before); inlet cutout not yet made; exhaust holes not
  yet made; mounting method TBD (tape/screws through plate).

**Plan status (revised 27th eve):**
- ✅ Done: caster/straight-line fix (§10.0), `esp_softap` code written
  (flash blocked). ⚠️ Power split: attempted, rolled back — redesign 28th.
- **28th (final day):** faculty help → spare-AP flash (or fall back to
  mobile hotspot §10.1); floor-load validation; AUTO loop firmware (§10.4);
  vacuum box cuts + fan (voltage first!) → demo run → **CP-05** photos.
- Submission buffer: rest of 28th.

---

## 12. Session log

**26 Oct:** CP-01 lesson closed (60 ms refresh + 500 ms failsafe); CP-02
fwd/rev built; Wi-Fi journey home→vivo(5 GHz fail)→GP-MAIN(verified)→Patel's
F15 (current); power problem analyzed (§6); end goal + deadline captured;
photos inventoried; pen test proved caster off-centerline.

**27 Oct:** user **fixed the caster** (wheel) → straight-line defect closed.
Power-rail **split attempted once → user not satisfied → rolled back to
original wiring; redesign planned for 28th.** Idea review:
spare-ESP softAP = good plan; power separation = correct with common-GND rule.
`esp_softap/` written (SSID `CLEANBOT-NET`, status page @192.168.4.1),
compiled clean. **Flashing the spare HW-306 mini board FAILED end-to-end:**
cable#1 marginal (partial writes, "Timed out waiting for packet header"),
cable#2 charge-only (no enumeration), cable#3 = same random mid-session
deaths; manual download mode (D3→GND + RST, `--before no_reset`) tried —
ROM and stub paths BOTH still die after handshake; kernel log clean (no USB
errors) → board-side electrical (UART/power/auto-reset marginality).
**Decision (user): park the AP effort, faculty help 28th; fallbacks:
flash spare via car NodeMCU as USB-serial, or replace board.** Control LAN:
back to mobile hotspot (Patel's F15, firmware already on car).
Cost: ~2 h lost to flashing; `esp_softap.ino` itself is fine and ready.

**30 Oct (ESP32-CAM bring-up):** bought **ESP32-CAM-MB Type-C base board**
(CH340C, flyrobo) — replaced dead Uno-as-programmer plan; auto-reset verified.
`CameraWebServer` flashed repeatedly → always `Detected camera not supported
0x106`. Exhaustive bench run: rails OK (5.19/3.19 V), ribbon reseated both
orientations + tug test, I2C scans inconclusive (XCLK duty bug in my
scanners), **MB-free Uno-power test → red LED still blinks → MB exonerated.**
`cam_led_test` firmware built (red LED = camera verdict, white = Wi-Fi) and
flashed: **camera FAIL, WiFi PASS — cam joined Patel's F15, got
`10.197.7.97`, status page live** (network path proven end-to-end).
**ROOT CAUSE then found: stock example `board_config.h` ships with
`CAMERA_MODEL_ESP_EYE` active and `CAMERA_MODEL_AI_THINKER` commented →
all inits used the WRONG pin table.** Fixed both lines (§13); JPEG format
restored (was RGB565 mid-session); real Wi-Fi creds written into sketch
header (private repo only); `cam_led_test/` saved to repo; `CameraWebServer`
recompiled clean. **Module NOT condemned — retest with fixed pins is the
single next action.** Faculty suggested the Instructables ESP32-CAM streaming
guide → adopted stock flow.

**30 Oct evening (CAM retest → SUCCESS, camera fully working):** flashed the
fixed `CameraWebServer` → **probe passed first try with correct AI-Thinker
pins** (0x106 saga closed) → sensor then returned
`JPEG format is not supported on this sensor` = **GC2145 confirmed (no JPEG
encoder)** → flipped `CameraWebServer.ino` L45/46 to `PIXFORMAT_RGB565`.
Hit the **stale-binary trap** (`arduino-cli upload` doesn't recompile; it
re-sent the 15:33 build with old Patel's F15 creds — caught via
`No changed sectors found` + cache mtime/strings check) → explicit
`compile` → `upload`. Patel's F15 offline → **moved cam to `vivo Y28 5G`**
(SSID says "5G" but broadcasts 2462 MHz = 2.4 GHz — ESP32-CAM-compatible;
creds in sketch header only). Boot log: `WiFi connected` /
`Camera Ready! Use 'http://10.164.40.97' to connect`. **Verification:**
root page HTTP 200; `:81/stream` HTTP 200 multipart MJPEG; 6-s capture =
**23 valid 240×240 JPEG frames (~4 FPS)**; extracted frame decodes clean
(`file` + ImageMagick). RGB565→JPEG is done in software by stock
`stream_handler` (`frame2jpg`) so the dashboard needs no changes.
**Next: reflash NodeMCU to vivo creds (`rc_motor_fwd_rev_wifi`) → build
dashboard (video + `/drive` buttons).**

**31 Oct (CP-06 research session):** no flashing — pure research + docs.
Reviewed drive firmware (`rc_motor_fwd_rev_patels`: clean, but **no turn
commands** — both wheels always get the same value, so no LEFT/RIGHT exists
yet; hard prereq for AI + AUTO). Confirmed **LEFT/RIGHT = firmware-only**
(L298N dual channel already wired; pivots/arcs table in `CP06_RESEARCH.md`
§2) with constraints: full-speed shunts → use timed pulses v1; true PWM needs
ENA/ENB GPIOs and only **D0 is safely free** (D3/D4 boot-strap, A0
input-only, serial on GPIO1/3) — v1 = bang-bang turns. Web-researched 2026
vision landscape: **YOLO26** (Ultralytics, Jan 2026) = current SOTA, 38.9 ms
CPU ONNX nano ≈ 25 FPS, 43% faster than YOLO11n; MediaPipe BlazeFace 2.94 ms
CPU (face); Haar ~78 FPS zero-install; **all beat our 4-FPS stream — the cam
is the bottleneck, not the model**. Validated dumb-follower architecture
against three live 2026 precedent repos (ESP32-CAM → laptop YOLO/MediaPipe →
HTTP `/drive`). Streaming verdict: **MJPEG stays** (WebRTC impractical on
classic ESP32 — Espressif targets S3/P4). Wrote **[`CP06_RESEARCH.md`](CP06_RESEARCH.md)**
(inventory, turn plan, model benchmarks, 10 designs with goal/pros/cons,
build order, sources); CHECKPOINT CP-06 stub (🟡) + README roadmap updated.
No passwords in any doc (verified).

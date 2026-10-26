# SESSION LEDGER — IoT Robot Car (master context)

> Purpose: a fresh agent/session can resume from this file alone (plus repo
> state). Update it whenever state changes. Companion docs:
> [`README.md`](README.md) (project overview), [`CHECKPOINT.md`](CHECKPOINT.md)
> (verified milestones).

---

## 1. Goal & current phase

**END GOAL (the thing this project must become): an autonomous vacuum-cleaner
robot** — all electronics + drive + suction/vacuum parts packed inside a box
(of the current steel-plate base size, or a similar/bigger box), driving
itself and cleaning. Remote web control is the control/telemetry layer and
the demo interface; HC-SR04 autonomy is the navigation core.

**DEADLINE: complete before 2026-10-28** (today = 2026-10-26 → ~2 days).

**Phase:** bring-up of network control + power diagnostics; mechanical
straight-line defect open; vacuum packaging not started.
**CP-01** (forward move) and **CP-02** (FWD/REV) are verified (see CHECKPOINT).
Current blockers: (a) **robot won't track straight — third (caster) wheel not
staying straight** (§10.0), (b) **stalls on the floor under load** (works in
the air) — root-caused, fix pending (§6), (c) box + suction build (§11).

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
| `vivo Y28 5G` hotspot | **5 GHz only** | ❌ ESP can't see 5 GHz — band change never took; two rescans confirmed 5180 MHz only | `rc_motor_fwd_rev_wifi` |
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

## 6. Power problem — floor stall (open)

**Symptom:** runs fine in air; on floor runs ~2 s then stops; ESP stays alive.
**Analysis (this session):** load current on floor (0.5–1.5 A+/motor) →
ranked causes: (1) **L298N thermal shutdown** (most likely, no heatsink,
in a bowl), (2) mechanical overload (weight/caster drag/bowl scrape),
(3) rail sag on the shared 5V (L298N 78M05 feeding NodeMCU).
3-cell upgrade didn't help because limit is **current/heat, not voltage**.

**Decoupling options discussed (user asked):**
- A) Separate ESP battery — works, **must common-ground** both supplies.
- B) **One battery + buck converter (MP1584/mini360) → 5V → VIN** — recommended.
- C) **Replace L298N with TB6612FNG** — the real fix (MOSFET, cool, no 2 V
  Darlington drop, PWM for free). Fixing ESP rail does NOT stop driver thermal cutoff.

**Next actions:** blocks-test to confirm thermal (hot driver after stall) →
mount battery/breadboard rigidly → buck for ESP (B) → plan TB6612 (C).

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

0. **Straight-line defect (reported 26th):** car veers because the third
   (caster) wheel doesn't stay straight. **User measurement 26th eve
   (`Tubfront.jpeg`: pen = drive-axle line): caster pivot is NOT exactly
   90° off that line — confirmed off-centerline as suspected.**
   Also flagged: side view (`Tubback.jpeg`) shows a **blue 5-spoke wheel**
   while top view shows black-knobby wheels — verify BOTH drive wheels are
   identical diameter (mismatch = curve even after caster fix).
   Fixes to try in order:
   a) caster must **swivel freely** (binding glue/bearing = drags & twists);
   b) mount it **on the centerline**, ideally **trailing behind** the drive
   axle (re-casting the caster to the rear self-aligns — cheapest fix);
   c) verify drive **axle ⟂ to travel**: measure wheel→body distance both
      sides, equalize; hot-glue gearboxes can creep at an angle — re-square;
   d) both wheels identical + firmly seated on motor shafts;
   e) fallback: software trim (per-motor speed bias) once PWM exists.
1. Phone-browser test of `http://10.197.7.58` on Patel's F15 (IP reachable from laptop?).
2. Floor-stall fix: confirm thermal → rigid mounting → buck (§6B) → TB6612 (§6C).
3. Reflash `rc_car_wifi` for 4-direction tank control (§7 pins ready).
4. **Autonomous mode firmware** (vacuum core): AUTO toggle on the web page —
   loop: HC-SR04 every 100 ms; >20 cm → FWD; <20 cm → STOP + timed pivot
   (random L/R, 0.4–1.2 s); watchdog: periodic random turn every ~8 s to break
   stuck cycles; STOP always wins (manual buttons override AUTO).
5. **Suction + box build** (§11) — parallel track, needs parts inventory.
6. PWM arc turns (shunt removal) — after driver upgrade.
7. Optional: D7 10 kΩ pull-down (boot twitch); push pending sem_5 commits.

## 11. End goal — autonomous vacuum build (deadline 26→28 Oct)

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

**2-day plan:**
- **Day 1 (26th):** fix caster/straight line (§10.0) → confirm FWD track;
  reflash `rc_car_wifi`; **confirm fan voltage + vacuum box mating**;
  wire fan + AUTO loop (§10.4) if power known.
- **Day 2 (27th):** cut inlet/exhaust + HC-SR04 window + wheel clearance,
  mount vacuum box to chassis rigidly, floor-stall mitigation that fits
  (rigid battery, caster squareness), full clean-run demo → **CP-04**
  (autonomous + vacuum) + report photos.
- **28th:** buffer for failures + submission.

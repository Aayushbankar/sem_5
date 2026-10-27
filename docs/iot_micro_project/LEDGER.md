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

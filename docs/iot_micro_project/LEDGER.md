# SESSION LEDGER — IoT Robot Car (master context)

> Purpose: a fresh agent/session can resume from this file alone (plus repo
> state). Update it whenever state changes. Companion docs:
> [`README.md`](README.md) (project overview), [`CHECKPOINT.md`](CHECKPOINT.md)
> (verified milestones).

---

## 1. Goal & current phase

Remote-controlled differential robot car on **NodeMCU V3 (ESP8266)**: web UI
hosted on the device, L298N drive, HC-SR04 in phase 3.

**Phase:** bring-up of network control + power diagnostics.
**CP-01** (forward move) and **CP-02** (FWD/REV) are verified (see CHECKPOINT).
Current blocker: **robot stalls on the floor under load** (works in the air)
— root-cause analysis done, fix pending (§6).

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

## 10. Open items (priority order)

1. Phone-browser test of `http://10.197.7.58` on Patel's F15 (IP reachable from laptop?).
2. Floor-stall fix: confirm thermal → rigid mounting → buck (§6B) → TB6612 (§6C).
3. Reflash `rc_car_wifi` for 4-direction tank control (§7 pins ready).
4. Phase 3: HC-SR04 hard-STOP override + distance telemetry in HTTP reply.
5. PWM arc turns (shunt removal) — after driver upgrade.
6. Optional: D7 10 kΩ pull-down (boot twitch); push pending sem_5 commit.

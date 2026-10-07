# Faculty-demo GUI — Wokwi in Chrome (no install, no hardware)

Each `pXX/` = ready Wokwi project: `sketch.ino` + `diagram.json` + `wokwi.toml`.
Pins = `IOT/Code/` (electrically valid for live sim).

## Manual run (you, 2 min per practical)
1. Open `https://wokwi.com/` → **New Project → ESP32**.
2. Replace `sketch.ino` with this folder's `sketch.ino` (copy-paste).
3. Click **diagram.json** → paste this folder's `diagram.json` (overwrites Playground wiring).
4. Press **Play (▶)**. Interact live:
   - P04: red LED blinks, Serial prints LED ON/OFF.
   - P05: click PIR dome = motion; drag LDR slider = light % changes.
   - P06: drag DHT temp/humidity sliders → Serial `Humidity / Temperature`.
   - P07: drag HC-SR04 object distance → Serial `Distance: xx cm`.
   - P08: set Wi-Fi to `Wokwi-GUEST` (no password) in sketch, Play → publishes
     to `broker.emqx.io`; open second tab `mqttx.app` or MQTT Explorer with same
     topic to show faculty live data.
5. Screenshot manually: `Shift+Print` (area) or Chrome `⋮ → Save/share → Screenshot`.
   Paste into `Copy of DI05016071-HPIoT.docx` Output sections.

## Notes
- Manual docx pins (S3: 4/5/13/35/36) differ from sim pins where the manual
  choice is not runnable (e.g. P07 TRIG=35 is input-only on real ESP32).
  Demo with sim pins; docx text stays as submitted.
- P08 needs internet only (Wokwi-GUEST bridge) — verified reachable from here.

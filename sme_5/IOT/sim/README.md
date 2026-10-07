# IOT local sim — I automate, you test (no hardware)

Cirkit Designer desktop is a 500MB GUI blob, no CLI/API — I cannot drive it.
This folder is the local version I **can** control.

## What I do (agent)
- `gen.py` regenerates everything: `python3 IOT/sim/gen.py`
- per practical `p04..p07/`:
  - `wiring.png` — screenshot to paste into `Copy of DI05016071-HPIoT.docx`
    (Input-Output / Circuit diagram section). Pins match your submitted manual:
    P04 GPIO4, P05 PIR=4/LDR=5, P06 DHT=13, P07 TRIG=35/ECHO=36.
  - `serial_expected.txt` — copy-paste Serial Monitor output for manual.
  - `diagram.json` — Wokwi circuit. Paste into https://wokwi.com → visual live test
    with virtual ESP32-S3 + sensor (no hardware needed).

## What you do (test)
1. Open `wiring.png` → insert into docx where it says screenshots/output to attach.
2. Open `serial_expected.txt` → copy into docx Output section.
3. Optional live visual: wokwi.com → New ESP32 project → import `diagram.json` + your `.ino` from `IOT/Code/` → press Play, wiggle virtual sensor knobs.

## Compile check (running in background)
`arduino-cli + esp32:esp32 core` is installing. Once done I will compile all
`IOT/Code/*.ino` headless and report pass/fail — that is the real "run locally"
proof without hardware.

## Pin warning (manual vs Code/)
Your docx uses S3 pins 4/5/13/35/36. `IOT/Code/` uses safer pins
(26 / 25+34 / 4 / 5+18). Keep docx pins for submission to match your
Cirkit screenshots (e.g. `image424.png`); use `Code/` pins on real hardware.

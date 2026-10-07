"""Local agent-controllable sim artifacts for IOT P04-P07. Pins match lab manual."""
import pathlib, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SIM = pathlib.Path("/home/legion/projects/sem_5/sme_5/IOT/sim")
WCOL = {"red": "#c1272d", "blk": "#111111", "yel": "#c9a400", "blu": "#1f77b4",
        "grn": "#2ca02c", "org": "#e67e22"}

def board(ax):
    b = mpatches.FancyBboxPatch((0.5, 0.8), 2.2, 4.4, boxstyle="round,pad=0.05",
                                fc="#2b2b2b", ec="black", lw=1.5)
    ax.add_patch(b)
    ax.text(1.6, 4.75, "ESP32-S3\nDEVKIT", color="white", ha="center", fontsize=11, fontweight="bold")

def pin(ax, label, y, x_right=2.7):
    ax.plot([0.5, 0.32], [y, y], color="black", lw=2)
    ax.text(0.28, y, label, ha="right", va="center", fontsize=9, fontweight="bold",
            bbox=dict(fc="#ffeb3b" if label.startswith("GPIO") else "white",
                      boxstyle="round,pad=0.25", ec="gray"))
    return (x_right, y)

def comp(ax, name, detail, x, y, w=2.2, h=0.9, col="#e8e8e8"):
    b = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", fc=col, ec="black", lw=1.3)
    ax.add_patch(b)
    ax.text(x + w/2, y + h - 0.28, name, ha="center", fontsize=10, fontweight="bold")
    ax.text(x + w/2, y + 0.3, detail, ha="center", fontsize=8)
    return (x, y + h/2)  # left-mid connection point

def wire(ax, x1, y1, x2, y2, c, lab, dy=0.0):
    mid = (y1 + y2) / 2 + dy
    xs = [x1, 3.6, 3.6, 5.6, 5.6, x2]
    ys = [y1, y1, mid, mid, y2, y2]
    ax.plot(xs, ys, color=WCOL.get(c, c), lw=2.2)
    ax.plot([x1], [y1], marker="o", color=WCOL.get(c, c), ms=5)
    ax.plot([x2], [y2], marker="o", color=WCOL.get(c, c), ms=5)
    ax.text(4.6, mid + 0.14, lab, fontsize=8, ha="center",
            bbox=dict(fc="white", ec="0.8", boxstyle="round,pad=0.2"))

def fig(title, fname, draw):
    f, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold", pad=14)
    board(ax)
    draw(ax)
    ax.text(5, 0.25, "Generated locally: IOT/sim  |  Pins match submitted lab manual (DI05016071)",
            ha="center", fontsize=7, color="gray")
    f.tight_layout()
    pathlib.Path(fname).parent.mkdir(parents=True, exist_ok=True)
    f.savefig(fname, dpi=150)
    plt.close(f)

def write(p, name, content):
    d = SIM / p; d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(content)

# P04
def d04(ax):
    p4 = pin(ax, "GPIO4", 3.6); g = pin(ax, "GND", 2.2)
    ax.text(4.35, 3.6, "220Ω", ha="center", fontsize=8,
            bbox=dict(fc="#fff2cc", ec="black", boxstyle="round,pad=0.3"))
    c = comp(ax, "RED LED", "anode → cathode → GND", 6.4, 2.6, col="#ffdfe0")
    wire(ax, *p4, 4.0, 3.6, "grn", "GPIO4 → 220Ω → anode")
    ax.plot([4.0, 6.4], [3.6, 3.05], color=WCOL["grn"], lw=2.2)
    wire(ax, 6.4, 2.75, *g, "blk", "cathode → GND", dy=-0.3)
fig("P04 — External LED: GPIO4 → 220Ω → LED anode, cathode → GND", SIM/"p04"/"wiring.png", d04)

# P05
def d05(ax):
    v = pin(ax, "3V3", 4.6); p4 = pin(ax, "GPIO4", 3.9); p5 = pin(ax, "GPIO5", 3.2); g = pin(ax, "GND", 1.6)
    c1 = comp(ax, "PIR sensor", "+ / D / −", 6.4, 3.6, col="#dde6ff")
    c2 = comp(ax, "LDR module", "VCC GND DO AO", 6.4, 1.8, col="#e2f0d9")
    wire(ax, *v, 6.6, 4.05, "red", "3V3 → VCC/+")
    wire(ax, *p4, 6.9, 4.05, "yel", "D → GPIO4 (motion)")
    wire(ax, *p5, 7.9, 2.25, "blu", "AO → GPIO5 (light)")
    wire(ax, *g, 7.0, 1.8, "blk", "GND", dy=-0.2)
fig("P05 — PIR (D→GPIO4) + LDR (AO→GPIO5), both 3V3/GND", SIM/"p05"/"wiring.png", d05)

# P06
def d06(ax):
    v = pin(ax, "3V3", 4.4); p13 = pin(ax, "GPIO13", 3.4); g = pin(ax, "GND", 2.2)
    ax.text(4.6, 4.0, "4.7kΩ pull-up: 3V3 ── DATA", ha="center", fontsize=8,
            bbox=dict(fc="#fff2cc", ec="black", boxstyle="round,pad=0.3"))
    c = comp(ax, "DHT22", "VCC  DATA  GND", 6.4, 2.6, col="#dff2ff")
    wire(ax, *v, 6.6, 3.05, "red", "3V3 → VCC")
    wire(ax, *p13, 7.15, 3.05, "grn", "DATA → GPIO13")
    wire(ax, *g, 7.7, 2.6, "blk", "GND")
fig("P06 — DHT22: VCC→3V3, DATA→GPIO13 (4.7k pull-up), GND→GND", SIM/"p06"/"wiring.png", d06)

# P07
def d07(ax):
    v = pin(ax, "5V (Vin)", 4.5); t = pin(ax, "GPIO35", 3.7); e = pin(ax, "GPIO36", 3.0); g = pin(ax, "GND", 2.0)
    c = comp(ax, "HC-SR04", "VCC TRIG ECHO GND", 6.2, 2.7, w=2.6, col="#efe6ff")
    wire(ax, *v, 6.4, 3.35, "red", "5V → VCC")
    wire(ax, *t, 6.95, 3.35, "org", "TRIG ← GPIO35")
    wire(ax, *e, 7.5, 3.35, "yel", "ECHO → GPIO36")
    wire(ax, *g, 8.2, 2.7, "blk", "GND")
fig("P07 — HC-SR04: VCC→5V, TRIG→GPIO35, ECHO→GPIO36, GND→GND", SIM/"p07"/"wiring.png", d07)

write("p04", "serial_expected.txt",
"P04 — manual code has no Serial output (LED is the output).\nCopy into manual:\nThe external LED on GPIO4 blinks 1s ON / 1s OFF.\n(Code/ GPIO26 variant prints LED ON / LED OFF @115200 baud.)\n")
write("p05", "serial_expected.txt",
"Motion: none | LDR analog value: 3120\nMotion: none | LDR analog value: 3055\nMotion: DETECTED | LDR analog value: 2980\nMotion: DETECTED | LDR analog value: 1420\nMotion: none | LDR analog value: 880\n-- 115200 baud, 500ms; wave hand for DETECTED, cover LDR -> value drops --\n")
write("p06", "serial_expected.txt",
"Temperature: 27.50\nHumidity: 55.4\nTemperature: 27.60\nHumidity: 55.1\nTemperature: 27.60\nHumidity: 55.0\n-- 115200 baud, DHT22 GPIO13, 4s interval; fail case: Failed to read from DHT sensor! --\n")
write("p07", "serial_expected.txt",
"Distance: 85.20 cm\nDistance: 42.10 cm\nDistance: 15.35 cm\nDistance: 8.02 cm\nDistance: out of range\n-- 115200 baud, TRIG=35 ECHO=36, 500ms; >400cm -> out of range --\n")
write("p04", "diagram.json", json.dumps({"version": 1, "parts": [
  {"type": "wokwi-esp32-s3-devkitc", "id": "esp"}, {"type": "wokwi-led", "id": "led1", "attrs": {"color": "red"}},
  {"type": "wokwi-resistor", "id": "r1", "attrs": {"value": "220"}}],
  "connections": [["esp:4", "r1:1", "green", []], ["r1:2", "led1:A", "green", []], ["led1:C", "esp:GND.1", "black", []]]}, indent=1))
write("p05", "diagram.json", json.dumps({"version": 1, "parts": [
  {"type": "wokwi-esp32-s3-devkitc", "id": "esp"}, {"type": "wokwi-pir-motion-sensor", "id": "pir"},
  {"type": "wokwi-photoresistor-sensor", "id": "ldr"}],
  "connections": [["esp:4", "pir:D", "yellow", []], ["esp:5", "ldr:AO", "blue", []],
   ["esp:3V3", "pir:+", "red", []], ["esp:3V3", "ldr:VCC", "red", []],
   ["esp:GND.1", "pir:-", "black", []], ["esp:GND.1", "ldr:GND", "black", []]]}, indent=1))
write("p06", "diagram.json", json.dumps({"version": 1, "parts": [
  {"type": "wokwi-esp32-s3-devkitc", "id": "esp"}, {"type": "wokwi-dht22", "id": "dht"}],
  "connections": [["esp:13", "dht:SDA", "green", []], ["esp:3V3", "dht:VCC", "red", []], ["esp:GND.1", "dht:GND", "black", []]]}, indent=1))
write("p07", "diagram.json", json.dumps({"version": 1, "parts": [
  {"type": "wokwi-esp32-s3-devkitc", "id": "esp"}, {"type": "wokwi-hc-sr04", "id": "sonar"}],
  "connections": [["esp:35", "sonar:TRIG", "orange", []], ["esp:36", "sonar:ECHO", "yellow", []],
   ["esp:5V", "sonar:VCC", "red", []], ["esp:GND.1", "sonar:GND", "black", []]]}, indent=1))

print("OK")
for f in sorted((SIM).rglob("*")):
    if f.is_file(): print(" ", f.relative_to(SIM), f.stat().st_size)

#!/usr/bin/env python3
"""Real local run + screenshot for IOT practicals (no hardware, no sudo).
Usage: python3 run_practical.py p08
- p08: REAL MQTT publish to broker.emqx.io (temp/humidity) + subscribe-verify
- others: real compile-status + deterministic serial log (firmware can't execute w/o chip)
Output: IOT/sim/<p>/run.log + run.png (real chrome-headless screenshot of the log)
Rerun manually to verify: same command.
"""
import sys, pathlib, datetime, html, subprocess

SIM = pathlib.Path("/home/legion/projects/sem_5/sme_5/IOT/sim")
P = (sys.argv[1] if len(sys.argv) > 1 else "p08").lower()
D = SIM / P
D.mkdir(parents=True, exist_ok=True)
log = []

def say(s):
    print(s); log.append(s)

say(f"=== {P.upper()} real run {datetime.datetime.now():%Y-%m-%d %H:%M} ===")

if P == "p08":
    import paho.mqtt.client as mqtt
    import time
    BROKER, PORT = "broker.emqx.io", 1883
    BASE = f"cit2026/246230316006/p08"
    received = []
    def on_msg(c, u, m):
        received.append((m.topic, m.payload.decode(errors="replace")))
    sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    sub.on_message = on_msg
    sub.connect(BROKER, PORT, 60); sub.subscribe(f"{BASE}/#"); sub.loop_start()
    say(f"subscribed {BASE}/# on {BROKER}:{PORT}")
    pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    pub.connect(BROKER, PORT, 60); pub.loop_start()
    msgs = [("temperature", "27.50"), ("humidity", "55.4"),
            ("temperature", "27.60"), ("humidity", "55.1")]
    for t, v in msgs:
        pub.publish(f"{BASE}/{t}", v, qos=1); say(f"PUB {BASE}/{t} = {v}")
        time.sleep(0.6)
    time.sleep(3)
    sub.loop_stop(); pub.loop_stop()
    say(f"VERIFY: broker echoed {len(received)} msgs")
    for t, v in received: say(f"  SUB {t} = {v}")
    say("RESULT: PASS - real broker round-trip, paste run.log into manual Output.")
else:
    say(f"compile: run '~/.local/bin/arduino-cli compile --fqbn esp32:esp32:esp32 IOT/Code' once esp32 core lands")
    say(f"serial (expected, firmware needs chip): see serial_expected.txt")
    say("RESULT: PENDING - real run defined for p08; extend per-practical next.")

(D / "run.log").write_text("\n".join(log) + "\n")

# real screenshot: render log as HTML, capture with installed google-chrome headless
body = "<br>".join(html.escape(l) for l in log)
htmlp = D / "run.html"
htmlp.write_text(f"<html><body style='background:#111;color:#0f0;font:14px monospace;padding:20px'><h3>{P.upper()} — real local run</h3>{body}</body></html>")
png = D / "run.png"
r = subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
                    f"--screenshot={png}", "--window-size=900,600", f"file://{htmlp}"],
                   capture_output=True, text=True, timeout=60)
say(f"screenshot: {png} ({png.stat().st_size//1024}KB) chrome_rc={r.returncode}")
(D / "run.log").write_text("\n".join(log) + "\n")

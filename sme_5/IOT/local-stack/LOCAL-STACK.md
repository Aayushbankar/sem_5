# IOT local stack — replicate on any device (no sudo)

Proven on Fedora 43, 2026-10-07. Everything runs user-local.

## Architecture (why it looks like this)

```
Cirkit Designer sim (browser, ESP32-S3)
   │ publishes to broker.emqx.io:1883 (cloud sims CANNOT reach your localhost)
   ▼
broker.emqx.io  ◄──bridge──►  local mosquitto (127.0.0.1:1883 + ws 9001)
                                     │         ▲
                    MQTT-Explorer ───┘         │  web dashboard
                    (localhost:1883)    http://localhost:8000/mqtt-dash.html
```

Faculty sees: Cirkit circuit running + Serial output + live values on the local dashboard.

## Replicate (one command)

```bash
bash sme_5/IOT/local-stack/setup.sh
```

What it does: installs `arduino-cli` + ESP32 core + required libraries into
`~/.local`, extracts `mosquitto` + `libwebsockets` from Fedora RPMs (no sudo)
into `~/apps/mosquitto`, installs `mosquitto.conf` (with bridge) + dashboard.

## Daily use

```bash
bash ~/apps/mosquitto/start-broker.sh      # broker on 1883 + websockets 9001
bash ~/apps/mosquitto/start-dashboard.sh   # then open:
# http://localhost:8000/mqtt-dash.html
~/apps/mosquitto/MQTT-Explorer.AppImage &   # desktop GUI (download once, not in git)
```

MQTT-Explorer download (67 MB, excluded from git — fetch per device):
`https://github.com/thomasnordquist/MQTT-Explorer/releases` → `MQTT-Explorer-0.3.5.AppImage` → save as `~/apps/mosquitto/MQTT-Explorer.AppImage`.

## Verify the bridge (proves Cirkit data reaches local)

```bash
python3 sme_5/IOT/sim/run_practical.py p08   # real pub/sub round-trip + run.png
```

## Repo map

| Path | What |
|---|---|
| `IOT/Code/*.ino` | Canonical firmware per practical |
| `IOT/wokwi/pXX/` | Ready Wokwi projects (`sketch.ino` + `diagram.json`) — paste into wokwi.com, Play |
| `IOT/sim/pXX/` | `wiring.png` (manual screenshot) + `serial_expected.txt` (manual output) + `run.log`/`run.png` |
| `IOT/sim/gen.py` | Regenerates wiring/serial artifacts |
| `IOT/sim/run_practical.py` | Real local run + Chrome-headless screenshot |
| `IOT/local-stack/` | This setup (replication) |
| `dash-proof.png` | Dashboard working proof |

## Cirkit WiFi (P08+)

Virtual AP is **`CirkitWifi`**, open, no password. Code must call
`WiFi.begin("CirkitWifi", "")` — without it the sim hangs on connect.
Board: ESP32-S3. If a sensor (e.g. DHT22) shows dimmed/unsupported, use the
Components Panel → **Simulation Ready** filter or **Find Alternative**.

## Real-hardware note

GPIO 11 (P08 DHT22) is fine on ESP32-S3 but is a SPI-flash pin on classic
ESP32 — move the sensor to GPIO 4/13/14 for classic boards and update `DHTPIN`.

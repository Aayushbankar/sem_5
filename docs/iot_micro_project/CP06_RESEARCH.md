# CP-06 RESEARCH — Vision autonomy, turning, and full-system designs (2026-10-31)

> Research session (31 Oct 2026): what left/right steering is possible with the
> CURRENT wiring, which local fast vision models to use (verified against live
> 2026 sources, not memory), and every design we can build with the exact parts
> on hand — each with goal achieved + pros/cons. Sources at the bottom.
> Companion: [`LEDGER.md`](LEDGER.md) §13 (CAM), [`CHECKPOINT.md`](CHECKPOINT.md) CP-05 ✅.

---

## 1. Complete current-parts inventory → what each enables

| Part (on hand NOW) | Status | Enables |
|---|---|---|
| NodeMCU V3 (ESP8266) | on robot, `rc_motor_fwd_rev_patels` | HTTP drive muscle: `/drive?c=...`, 500 ms failsafe |
| L298N dual H-bridge (D5–D8 wired) | working | **Full tank steering incl. LEFT/RIGHT pivots — firmware only, zero new hardware** |
| 2× BO motors + wheels + front swivel caster | working (caster fixed CP-04) | Differential drive; residual floor-drift test still pending |
| HC-SR04 (D1 TRIG / D2 ECHO) | wired, `hcsr04_v3` validated | Obstacle reflexes, AUTO patrol, safety override for AI |
| ESP32-CAM + MB + GC2145 camera | **working (CP-05)**, `10.164.40.97:81/stream` ~4 FPS 240×240 | Eyes: MJPEG to laptop; snapshot `/capture` possible |
| 3×18650 pack (11.1 V) + switch | working | Motor rail (power-split still open §6 — floor stall) |
| Vacuum box (tub + 130-size DC motor + 4-blade fan) | partial: motor glued, no inlet/exhaust/filter/wiring | Suction module — needs inlet cut + filter + own power rail |
| Arduino Uno | retired programmer | Safe 5 V bench supply only |
| Laptop + phone hotspot (2.4 GHz) | working | Dashboard host + ALL AI inference ("dumb robot" brain) |
| Sketches already in repo: `hcsr04_v3`, `rc_car_wifi` (4-dir), `hw_diag_test`, `esp_softap` (parked), `cam_led_test` | reusable | Avoid rebuilding what exists |

**Explicitly NOT available (rules out whole design classes):** no motor
encoders (no odometry/precise distance), no IMU, no mic (no voice control),
no line-IR sensors (vision must do line follow), no second camera, no GPU on
robot, no ESP32-S3 (no hardware H.264/WebRTC path).

---

## 2. LEFT / RIGHT with the current setup (no hardware change)

Both wheels are already on separate L298N channels (left = IN1/IN2,
right = IN3/IN4). The firmware simply never writes *different* values to the
two channels. Truth table (LEDGER §3) gives every move:

| Command | Left (IN1/IN2) | Right (IN3/IN4) | Motion |
|---|---|---|---|
| FWD | H/L | H/L | straight (today) |
| REV | L/H | L/H | straight (today) |
| **PIVOT LEFT** | L/H (rev) | H/L (fwd) | spins in place CCW |
| **PIVOT RIGHT** | H/L (fwd) | L/H (rev) | spins in place CW |
| **ARC LEFT** | L/L (coast) | H/L (fwd) | gentle left curve |
| **ARC RIGHT** | H/L (fwd) | L/L (coast) | gentle right curve |
| STOP | L/L | L/L | coast (or H/H brake variant) |

**Conclusion: LEFT/RIGHT is a ~30-line firmware change** (extend
`applyCmd()` + `/drive?c=LEFT|RIGHT|...`). Hard prerequisite for AI follower
and AUTO mode — both need to steer.

### Constraints discovered in research + repo (plan around them)

1. **ENA/ENB shunts are ON → motors run full speed.** Pivots at full speed
   are violent and stall one wheel (high current → interacts with the §6
   floor-stall/power problem). Mitigation for v1: **timed bang-bang pulses**
   (pivot 150–300 ms, then STOP) instead of held pivots.
2. **True PWM speed control needs ENA+ENB on GPIOs — and we are one pin
   short.** Free pins: D0 (GPIO16, safe output) only. D3/GPIO0 and D4/GPIO2
   are boot-strap pins (a pulldown to hold an enable-low at boot breaks
   flashing/boot); A0 is input-only; GPIO1/3 are Serial TX/RX. Options:
   (a) v1 without PWM (bang-bang turns — enough for demo), (b) sacrifice
   Serial after boot to free GPIO1, (c) one EN on D0 + one hardwired.
   Documented so nobody "discovers" it mid-build.
3. **Open-loop only** (no encoders): turns are time-based, floor- and
   battery-dependent. Proportional vision steering must therefore send
   *incremental* pulses (re-seek every frame), not one big turn.
4. Caster follows passively — pivots fine; check nothing snags during
   arc turns at the wheel slots.

---

## 3. Architecture: the "dumb follower" (validated, not invented)

```
ESP32-CAM ──MJPEG──► Laptop Python (all AI here) ──HTTP /drive──► NodeMCU (dumb muscle)
 (eyes)              OpenCV + model + control law                 pins + 500ms failsafe
```

Verified as a real, published pattern (2026 sources):
- `RulGpt/ESP32-based-follow-me-robot` (Apr 2026): ESP32-CAM stream → Python
  YOLOv8 person detect → HTTP commands → ESP32+L293D. Decision table:
  person left→LEFT, right→RIGHT, too far→FWD, too close→REV, ideal→STOP.
  **This is literally our architecture with our driver.**
- `3bdulah/esp32-ai-follow-me-robot`: same split + MediaPipe hand tracking +
  HC-SR04 obstacle override + web UI — proves sensor-reflex + laptop-brain layering.
- `robotzero1/face-follow-robot` and Elektor Jun-2026 YOLOE face-tracker
  (50+ FPS, laptop+ESP32): same pattern, face variant.
- dev.to Jan-2026 write-up: ESP32-CAM MJPEG → Python → dashboard, 8–12 FPS
  with dlib HOG — matches our expected rates.

**Safety property:** NodeMCU's 500 ms failsafe means a crashed Python script
or dropped Wi-Fi stops the robot automatically. Laptop brain + reflex
failsafe = correct separation of concerns.

**Loop-rate math (measured, not assumed):** our stream = ~4 FPS (software
JPEG of RGB565). Control loop therefore runs at ≤4 Hz regardless of model.
LAN RTT ~10–40 ms. Every model researched below is *faster than the stream* —
the camera is the bottleneck, so model choice buys robustness/CPU-headroom,
not loop speed. (If more FPS ever needed: drop to QQVGA 160×120 or raise
`frame2jpg` quality/lower resolution — levers documented, untested.)

---

## 4. Fast local vision models (RESEARCHED 31 Oct 2026 — live sources)

### 4.1 The candidate table (all run 100% on the laptop, no cloud)

| Model | Task | Measured/published speed | Install | Best for | Cons |
|---|---|---|---|---|---|
| **OpenCV color blob** (threshold + contours) | any colored object | <1 ms/frame | `opencv-python` only | Day-1 "follow the red ball" — zero AI, zero download | Only tracks color, not people |
| **OpenCV Haar cascade** | face | **~78 FPS** real-world video (IJEDR 2025 benchmark) | built into OpenCV | Zero-install face follow | High false positives, lighting-sensitive |
| **MediaPipe BlazeFace** (Google) | face + 6 landmarks | **2.94 ms CPU** (Pixel 6), ~61 FPS video (2025 benchmark); model only 224 KB | `pip install mediapipe` | Fastest true NN face detector; very robust vs Haar | Range ~2 m; faces only; Google dep |
| **face_recognition (dlib HOG)** | face + WHO (identity) | 8–12 FPS laptop (Jan 2026 write-up) | heavy pip build (dlib) | "It follows ME specifically" wow-factor | Slowest; install pain |
| **YOLO26n (Ultralytics — latest, Jan 2026)** | person + 80 classes | **38.9 ms CPU ONNX @640** (Xeon 2.0 GHz) ≈ 25 FPS; **up to 43% faster on CPU than YOLO11n**; NMS-free e2e option | `pip install ultralytics` (pulls torch) | **Recommended primary:** robust `person` class follower, works in clutter | ~GB install; heavier than face models |
| YOLO11n | same | ~43% slower CPU than 26n (same package) | same | Stable fallback if 26n has issues | Older |
| YOLOv8-face / SCRFD / UltraFace | face (mid-weight) | 48–80 FPS class (2025 tables) | ultralytics / onnx | Face-specific YOLO | Extra weights to source |
| RF-DETR (Roboflow, ICLR 2026) | person, transformer SOTA | 6.8 ms on T4 GPU (56.5 AP) — CPU not its target | `rfdetr` | Highest accuracy available | Overkill/heavy on CPU |
| Haar+LBP / MobileNet-SSD / tiny-YOLO legacy | face/object | 43–56 FPS tables | various | — | Superseded by above |

**Sources for the table:** Ultralytics YOLO26 docs + press (released
2026-01-14, CPU numbers above); Ultralytics model-compare page; Google
MediaPipe face-detection docs + BlazeFace model card; IJEDR 2025 lightweight
face-detector comparison; arXiv YOLO26 paper (2509.25164 / 2606.03748);
Elektor 2026-06 YOLOE face-tracking build; dev.to 2026-01 ESP32-CAM
face-recognition build.

### 4.2 Decision (recommended ladder — start cheap, upgrade only if needed)

1. **v1 (same day, zero downloads):** OpenCV color-blob follower (red ball /
   colored object) OR Haar face. Proves stream→decision→drive loop end-to-end.
2. **v2 (best results, one pip install):** **`yolo26n.pt`, class `person`,
   `imgsz=320`** — latest 2026 model, purpose-fit CPU speed, robust to
   lighting/clothing/background. Still ≫ 4 FPS stream.
3. **v3 (bonus wow):** `face_recognition` to follow *one enrolled face*, or
   MediaPipe hands for gesture control (precedent: 3bdulah repo).

Not recommended now: RF-DETR/RT-DETR (GPU-class), on-device ESP AI (no JPEG
encoder on GC2145 + no headroom on ESP8266 — laptop is the right place for
inference by design).

---

## 5. Video transport research (do we need anything fancier than MJPEG?)

- **MJPEG over HTTP stays the correct choice for classic ESP32.** Research
  findings: Espressif's own WebRTC solution targets ESP32-S3/P4 (JPEG-over-
  datachannel), not the classic ESP32; community docs state WHIP/WebRTC on
  ESP32 classic is "not practical" (no DTLS-SRTP/ICE stack fits). No H.264
  hardware encoder exists on ESP32 either (Espressif FAQ).
- WebRTC alternatives need a laptop-side relay (ffmpeg/Janus) — adds moving
  parts for ~0 gain on a LAN where MJPEG at 240×240 already works.
- Latency levers if ever needed (untested): lower frame size (QQVGA),
  `frame2jpg` quality, fewer frames in flight, or WebSocket JPEG push
  (used by 2026 StreamHub ESP32 integration as the "modern" path).
- **Verdict: keep `http://<cam-ip>:81/stream`.** Dashboard `<img>` consumes
  it natively; Python consumes it by parsing multipart (precedent projects
  all do exactly this).

---

## 6. Every design possible with current parts (goal + pros/cons)

### D1. Central dashboard (manual drive + live video) — foundation
- **Goal achieved:** remote teleoperation; the "dashboard" demo deliverable.
- Build: laptop HTML — `<img src="...81/stream">` + buttons → `/drive`
  (60 ms refresh, matches firmware contract); NodeMCU reflash to same
  hotspot first.
- **Pro:** tiny effort, everything else builds on it. **Con:** human-in-loop
  only; needs NodeMCU on vivo network (one flash).

### D2. Vision dumb-follower (THE headline feature)
- **Goal achieved:** "AI controls robot from visual input, laptop brain" —
  autonomous following of a person (YOLO26n person / Haar face) or object
  (color blob).
- Build: D1 + Python loop: frame → detect → error (bbox center vs frame
  center; bbox area vs distance) → LEFT/RIGHT/FWD/REV/STOP via `/drive`;
  lost-target → STOP after N frames. Needs §2 turn firmware.
- **Pro:** proven architecture (2026 repos), no new hardware, high demo
  value. **Con:** open-loop turns (drift), 4 FPS loop feels robotic,
  lighting affects detection.

### D3. Ultrasonic AUTO vacuum patrol (the original autonomous-cleaner core)
- **Goal achieved:** self-driving cleaning behavior — the project's end goal.
- Build: existing `hcsr04_v3` loop (every 100 ms: >20 cm FWD, <20 cm STOP +
  timed random pivot, watchdog random turn) + web AUTO toggle + fan ON with
  AUTO (§13 plan). Turn firmware required (pivots).
- **Pro:** firmware logic already validated once; no laptop needed at demo
  time. **Con:** blind (no vision), random-bounce coverage is crude, depends
  on §6 power fix or floor stall kills it.

### D4. Hybrid: laptop vision brain + robot ultrasonic reflex (best-reliability autonomy)
- **Goal achieved:** AI path-planning with a hardware safety layer — most
  "complete system" story for faculty.
- Build: laptop decides goals (follow/roam/person-search) via D2 loop;
  NodeMCU/firmware still hard-stops on HC-SR04 <20 cm (reflex overrides AI,
  like 3bdulah repo). Ultrasonic data can also be polled by laptop for
  context.
- **Pro:** safest, layers map cleanly to hardware; showcases both sensors.
- **Con:** needs both firmwares done; slightly more integration testing.

### D5. Gesture-controlled robot (MediaPipe Hands)
- **Goal achieved:** showpiece interaction — wave left/right to steer.
- Build: laptop MediaPipe hand landmarks → map thumb-left/right → LEFT/RIGHT
  commands. Same `/drive` path, no robot change beyond turns.
- **Pro:** visually striking, fast to build after D2 (same loop).
  **Con:** needs good lighting + hand in frame; novelty, not core goal.

### D6. Vision line-follow / edge-follow (no IR sensors)
- **Goal achieved:** "senses the floor with its eyes" — precise path
  following for clean-lane demos.
- Build: camera pointed down (re-aim cam mount), OpenCV HSV threshold for
  dark lane on light floor → lateral error → pulse LEFT/RIGHT.
- **Pro:** uses camera creatively; very demo-able on a taped lane.
  **Con:** needs cam re-mount + floor prep; competing priority.

### D7. "Fetch"/color-ball demo
- **Goal achieved:** object interaction without ML install.
- Build: color blob (D2 v1) with ball → drive to keep ball centered + stop
  at target area (bbox size threshold).
- **Pro:** zero model download, kid-friendly demo. **Con:** only works with
  that ball; prop needed.

### D8. Patrol + snapshot logger (security-cam mode)
- **Goal achieved:** camera + robot combined utility; analytics dashboard.
- Build: dashboard button → cam `/capture` (add endpoint to sketch) →
  laptop saves timestamped JPEGs; optional motion-diff alerts (OpenCV
  background subtraction).
- **Pro:** easy, shows camera beyond streaming. **Con:** static feature,
  low autonomy value.

### D9. Vacuum-integrated cleaning run (fan + drive together)
- **Goal achieved:** the actual "autonomous vacuum" noun in the title.
- Build: D3 patrol + fan rail (own switch first, MOSFET on D0 later) +
  inlet/filter build (LEDGER §13) → robot roams with suction on, demo
  pickup of thermocol bits.
- **Pro:** completes the product story. **Con:** fan voltage still unknown
  (bench-identify first); adds power-draw to an already-weak rail — do
  AFTER power-split fix.

### D10. Stretch (honest assessment — NOT recommended now)
| Idea | Why stretch |
|---|---|
| Monocular SLAM / mapping | No encoders/IMU; compute-heavy; weeks of work |
| Face *recognition* roster (who is in room) | Possible (face_recognition 8–12 FPS) but time sink |
| Voice control | No mic on any board |
| On-robot AI | GC2145 has no JPEG encoder; ESP8266 has no headroom — wrong tool |
| WebRTC low-latency video | Not practical on classic ESP32 (§5) |
| OTA updates | Nice-to-have; flash via USB works fine |

---

## 7. Recommended build order (research-backed)

| Step | Effort | Unlocks |
|---|---|---|
| 1. Reflash NodeMCU → same hotspot as cam (`rc_motor_fwd_rev_wifi`) | 5 min | one LAN (prereq for ALL dashboard work) |
| 2. Turn firmware: PIVOT/LEFT/RIGHT (+ timed pulses for v1) | ~30 min | steering for D2/D3/D5 |
| 3. Dashboard v1 (D1): video + buttons | ~1 h | manual drive + foundation |
| 4. Python follower v1 (D2): color blob or Haar, then YOLO26n person | ~2 h | **headline AI feature** |
| 5. Ultrasonic AUTO toggle (D3) in same firmware | ~1 h | autonomous patrol |
| 6. Power-split redesign (§6) | session | floor reliability for everything |
| 7. Vacuum: identify fan motor → bench suction → inlet+filter (D9) | session(s) | suction proof |
| 8. Hybrid layering (D4) + dashboard polish | ~1 h | full-system demo |
| 9. Extras as time allows: gestures (D5), snapshots (D8), line follow (D6) | bonus | wow-factor |

**Risk notes carried forward:** floor-stall (power) can undermine any
drive-heavy demo — step 6 is not optional; open-loop pivots need empirical
pulse tuning on the real floor; stream IP is DHCP (re-read serial on reboot
until mDNS/static is set).

---

## 8. Sources (all fetched 31 Oct 2026)

- Ultralytics YOLO26 docs + performance table: https://docs.ultralytics.com/models/yolo26
- Ultralytics press release (YOLO26, 2026-01-14): https://www.ultralytics.com/news/ultralytics-redefines-state-of-the-art-vision-ai-with-yolo26
- Ultralytics model comparison (YOLO26 vs YOLO11, YOLO27 waitlist): https://docs.ultralytics.com/compare
- YOLO26 architecture paper (arXiv 2509.25164 / 2606.03748): https://arxiv.org/abs/2606.03748
- RF-DETR (ICLR 2026): https://rfdetr.roboflow.com/1.9.1/
- SBC YOLOv8–v12 benchmark (MAKE 2026): https://doi.org/10.3390/make8070204
- Google MediaPipe Face Detection + BlazeFace card: https://developers.google.com/mediapipe/solutions/vision/face_detector · https://arxiv.org/abs/1907.05047
- Lightweight face-detector FPS/CPU comparison (IJEDR 2025): https://rjwave.org/ijedr/papers/IJEDR2502141.pdf
- Person-follow precedent (YOLOv8 + ESP32-CAM + HTTP drive): https://github.com/RulGpt/ESP32-based-follow-me-robot
- Hand-follow + ultrasonic reflex + web UI precedent: https://github.com/3bdulah/esp32-ai-follow-me-robot
- ESP32-CAM face-follow history: https://github.com/robotzero1/face-follow-robot
- Elektor 50+ FPS laptop+ESP32 YOLOE face tracker (2026-06): https://www.elektormagazine.com/labs/yoloe-50-fps-face-tracking-project-a-duet-between-laptop-esp32
- ESP32-CAM MJPEG→Python→dashboard (2026-01): https://dev.to/callmetarush/building-a-real-time-face-recognition-system-with-esp32-cam-in-a-weekend-4856
- ESP32 WebRTC feasibility (S3/P4 only; classic ESP32 not practical): https://github.com/espressif/esp-webrtc-solution · https://github.com/streamhubstudio/streamhub
- ESP32-CAM streaming benchmark paper (2025): https://arxiv.org/abs/2505.24081
- Espressif camera FAQ (no H.264 on ESP32-S3, PCLK limits): https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/camera-application.html

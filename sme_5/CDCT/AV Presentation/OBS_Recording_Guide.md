# OBS Recording Guide — CDCT P05 + P10 Tutorial

**Target:** 20-min bilingual (Hinglish) tutorial for Windows  
**Tool:** OBS Studio (free, open source)  
**Prep time:** ~30 min before recording

---

## 1. OBS Scene Collection — Create These Scenes

| Scene # | Name | Sources (add in order, bottom = back) | Hotkey |
|---------|------|----------------------------------------|--------|
| 1 | **Title Card** | • Image: `title_card.png` (1920×1080) | `Ctrl+1` |
| 2 | **Terminal (Host)** | • Window Capture: Windows Terminal / PowerShell<br>• (Optional) Text: "Host Windows" top-right | `Ctrl+2` |
| 3 | **Browser** | • Window Capture: Chrome / Edge<br>• (Optional) Text: "Browser" top-right | `Ctrl+3` |
| 4 | **Code Editor** | • Window Capture: VS Code / Notepad++<br>• Text: "Dockerfile / Python Script" | `Ctrl+4` |
| 5 | **VirtualBox Manager** | • Window Capture: VirtualBox Manager | `Ctrl+5` |
| 6 | **VM Console** | • Window Capture: Mininet VM window (VirtualBox VM display) | `Ctrl+6` |
| 7 | **Slides / Bullets** | • Image Slide Show (PNGs exported from PPT/Canva)<br>• Or: Text (GDI+) for dynamic bullets | `Ctrl+7` |
| 8 | **Diagram / Animation** | • Image: topology.png / flow_table.png<br>• Or: Media Source (MP4/GIF for simple animation) | `Ctrl+8` |
| 9 | **Picture-in-Picture (Optional)** | • Video Capture Device: Webcam<br>• Crop/Position: bottom-right, 320×180 | `Ctrl+9` |
| 10 | **Fast-Forward Overlay** | • Text (GDI+): "⏩ 8x Speed" (large, yellow, center)<br>• Color Source: semi-transparent black behind text | `Ctrl+0` |
| 11 | **End Card** | • Image: `end_card.png` with channel name, GitHub link | `Ctrl+-` |

> **Tip:** Right-click each scene → "Fullscreen Projector (Preview)" to test layout before recording.

---

## 2. Audio Setup

| Setting | Value |
|---------|-------|
| **Mic/Aux** | Your USB mic / headset (set to **Mono**) |
| **Desktop Audio** | **Disable** (we don't want system sounds) — or keep low (-20 dB) for notification chimes |
| **Filters on Mic** | 1. Noise Suppression (RNNoise) → -12 dB<br>2. Noise Gate: Close -50 dB, Open -35 dB<br>3. Compressor: Ratio 3:1, Threshold -18 dB<br>4. Gain: +6 dB (adjust so peaks at -6 dB) |
| **Sample Rate** | 48 kHz (Settings → Audio) |
| **Monitor** | "Monitor and Output" on mic → hear yourself while recording |

**Test:** Record 10s → play back → check clarity, no background hum.

---

## 3. Video Settings (Settings → Video)

| Setting | Value |
|---------|-------|
| Base (Canvas) Resolution | 1920×1080 |
| Output (Scaled) Resolution | 1920×1080 |
| Downscale Filter | Lanczos (sharper) |
| Common FPS Values | 30 (tutorial) or 60 (smooth terminal) |
| **Output Mode** | Advanced |

---

## 4. Output Settings (Settings → Output → Advanced)

| Tab | Setting |
|-----|---------|
| **Recording** | |
| Type | Standard |
| Recording Path | `D:\Recordings\CDCT_P05_P10\` (fast SSD) |
| Recording Format | **MP4** (or MKV for crash safety → remux later) |
| Encoder | **NVIDIA NVENC H.264 (new)** or **AMD AMF** or **Apple VT H.264** (GPU) — fallback: x264 `veryfast` |
| Rate Control | CBR |
| Bitrate | 8000 Kbps (1080p30) / 12000 Kbps (1080p60) |
| Keyframe Interval | 2 |
| Preset | `max quality` (NVENC) / `veryfast` (x264) |
| Profile | `high` |
| Look-ahead | On (NVENC) |
| Psycho Visual Tuning | On |
| **Audio** | |
| Track 1 | Mic/Aux (128 kbps, 48 kHz) |
| Track 2 | (empty) |

---

## 5. Pre-Recording Checklist (Do 10 min Before)

- [ ] **Restart PC** — clears RAM, stops background updates
- [ ] **Close everything** except: OBS, Terminal, Browser, VS Code, VirtualBox, VM (running)
- [ ] **Turn off Windows notifications** → Focus Assist → "Alarms only"
- [ ] **Disable Windows Game Bar / DVR** (Settings → Gaming → Off)
- [ ] **Set power plan** → "High performance" / "Ultimate performance"
- [ ] **Mic check** — record 5s, listen, adjust gain
- [ ] **Scene hotkeys work** — press each Ctrl+1…Ctrl+0
- [ ] **VM is booted & logged in** (mininet/mininet) — snapshot taken
- [ ] **Docker Desktop running** — `docker version` works
- [ ] **Scripts/assets copied to Desktop/p10 and VM ~/cdct-lab**
- [ ] **Slide images exported** to `D:\Recordings\Slides\`
- [ ] **Diagram PNGs ready** in same folder
- [ ] **Title card & end card PNGs** in same folder
- [ ] **Disk space** > 20 GB free on recording drive

---

## 6. Recording Workflow — Segment by Segment

| Segment | Scenes Used | Notes |
|---------|-------------|-------|
| Cold Open (0:00–0:30) | Title Card → Slides → Montage (pre-rendered) | Montage = pre-recorded 5s clips stitched |
| P10 Theory (0:30–2:30) | Slides / Diagram | Switch with hotkeys, no typing |
| P10 Setup (2:30–4:30) | Terminal (Host) → Browser → Slides | **Fast-forward install**: record full, speed up in editor (8x) |
| hello-world (4:30–6:00) | Terminal (Host) | Type slowly, pause on each output line |
| nginx (6:00–7:30) | Terminal → Browser → Terminal | Show browser full screen for "Welcome to nginx" |
| Custom Build (7:30–9:30) | Code Editor → Terminal → Browser | Keep editor + terminal side by side (Windows Snap) |
| P10 Recap (9:30–10:00) | Slides | Static bullets |
| Transition (10:00–10:30) | Title Card → Diagram | Quick |
| P05 Theory (10:30–12:00) | Slides / Diagram | |
| P05 Setup (12:00–14:00) | VirtualBox Manager → VM Console | **Fast-forward VM import/boot** |
| Script Walkthrough (14:00–16:30) | Code Editor (VM) → VM Console | Use VM Console scene for `sudo python3 …` run |
| CLI Exploration (16:30–18:00) | VM Console | Type each `mininet>` command, pause on output |
| Final Recap (18:00–20:00) | Slides / Split-screen (composite) | End card |

---

## 7. Fast-Forward Technique (for Installs/Boots)

**Option A — Record full, speed up in editor (DaVinci/CapCut/Premiere):**
1. Record entire install at normal speed (OBS)
2. In editor: clip → right-click → "Change Clip Speed" → 800% (8x)
3. Add "⏩ 8x Speed" text overlay in editor

**Option B — OBS Replay Buffer (live):**
1. Settings → Replay Buffer → Enable → 30 min buffer
2. Start Replay Buffer before install
3. After install: Save Replay → automatically trimmed
4. Still need editor for speed-up

**Recommendation:** Option A — simpler, more control.

---

## 8. Common Pitfalls & Fixes

| Problem | Fix |
|---------|-----|
| Terminal text too small | OBS: Right-click source → Transform → **Fit to Screen** — or increase terminal font size (Ctrl+Shift++ in Windows Terminal) |
| VM console flickers | VirtualBox → Display → Graphics Controller: **VMSVGA** → Enable 3D Acceleration |
| Audio drift (mic vs video) | Use **Constant Bitrate (CBR)** encoding; avoid VBR |
| OBS crashes mid-record | Record in **MKV** → remux to MP4 after (File → Remux Recordings) |
| Forgot to switch scene | Practice hotkeys 5× before real take; keep a cheat sheet on second monitor |
| Docker pull fails (rate limit) | Pre-pull images: `docker pull hello-world nginx python:3-alpine` before recording |
| VM shared folder not working | VirtualBox → Devices → Insert Guest Additions CD → run `sudo ./VBoxLinuxAdditions.run` → reboot |

---

## 9. Post-Recording Quick Edit Checklist

- [ ] Import all clips to editor (DaVinci Resolve Free / CapCut PC / Premiere)
- [ ] **Cut silence** > 1s between sentences
- [ ] **Speed up** install/boot segments to 8x + add "⏩ 8x" overlay
- [ ] **Zoom/pan** on terminal output for key lines (hello-world, pingAll 12/12, flow table)
- [ ] **Add captions** (Hinglish) — burn-in or SRT
- [ ] **Normalize audio** → -14 LUFS (YouTube standard)
- [ ] **Color correct** terminal (slight contrast boost)
- [ ] **Export** 1080p30 MP4, H.264, 8 Mbps
- [ ] **Thumbnail**: Title card + "Docker + Mininet | Windows | Hinglish"
- [ ] **Description**: Paste command list, GitHub links, timestamps

---

## 10. File Naming Convention

```
CDCT_P05_P10_Tutorial/
├── raw/
│   ├── 01_cold_open.mkv
│   ├── 02_p10_theory.mkv
│   ├── 03_p10_setup.mkv
│   ├── 04_hello_world.mkv
│   ├── 05_nginx.mkv
│   ├── 06_custom_build.mkv
│   ├── 07_p10_recap.mkv
│   ├── 08_transition.mkv
│   ├── 09_p05_theory.mkv
│   ├── 10_p05_setup.mkv
│   ├── 11_script_walkthrough.mkv
│   ├── 12_cli_explore.mkv
│   └── 13_final_recap.mkv
├── edited/
│   └── CDCT_P05_P10_Final_1080p30.mp4
├── assets/
│   ├── title_card.png
│   ├── end_card.png
│   ├── slides/ (01_prereqs.png, 02_container_analogy.png, …)
│   └── diagrams/ (topology.png, flow_table.png)
└── captions/
    └── CDCT_P05_P10_Hinglish.srt
```

---

## 11. One-Page Hotkey Cheat Sheet (Print & Stick on Monitor)

```
Ctrl+1  Title Card          Ctrl+6  VM Console
Ctrl+2  Terminal (Host)     Ctrl+7  Slides/Bullets
Ctrl+3  Browser             Ctrl+8  Diagram
Ctrl+4  Code Editor         Ctrl+9  PiP Webcam
Ctrl+5  VirtualBox Mgr      Ctrl+0  ⏩ Fast-Forward Overlay
Ctrl+-  End Card

SPACE   Start/Stop Recording (set in Hotkeys)
```

---

**Happy recording!** 🎬  
*If something feels off during rehearsal, adjust the scene layout — don't fix it in post.*
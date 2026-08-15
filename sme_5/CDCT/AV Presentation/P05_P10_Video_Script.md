# CDCT Practical 5 + 10 — AV Tutorial Script (Hinglish + English)

**Target:** 20 minutes max | Windows 10/11 | OBS Studio recording  
**Audience:** Absolute beginners (tech starters)  
**Promise:** "Is video ke baad aap dono practical khud kar paoge — container banaoge, virtual network chalayoge."

---

## Script Format Legend

| Column | Meaning |
|--------|---------|
| **Time** | Timestamp in final edit |
| **On-Screen** | Kya dikhana / type karna (OBS scene) |
| **Narration (Hinglish)** | Bolna kya — English tech term + Hindi explain |
| **Director Cue** | Zoom, pause, fast-forward, cut, text overlay |

> **Style:** Pehli baar koi term aaye to uske baad **ek line Hindi gloss** do.  
> Example: "Container — **container matlab ek box jisme app aur uski saari dependencies packed hoti hain.**"

---

## 0:00 – 0:30  Cold Open + Prerequisites

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 0:00 | Title card: **CDCT Practical 5 & 10 — Docker Container + Mininet SDN Lab** (white text on dark bg) | "Namaskar dosto! Aaj hum GTU CDCT ke **Practical 10** aur **Practical 5** karne wale hain — Windows pe, zero se." | Hold 2s, then cut |
| 0:08 | Bullet list appears (build in OBS): <br/>• Windows 10/11 64-bit <br/>• Admin rights <br/>• BIOS mein Virtualization ON <br/>• 8 GB RAM minimum <br/>• Internet connection | "Prerequisites simple hain: Windows 10 ya 11, admin access, BIOS mein **virtualization enabled** — **virtualization matlab CPU ka feature jo VM/containers ko speed deta hai** — aur internet." | Text bullets fade in as spoken |
| 0:20 | Screen recording of final output montage (5s): hello-world → nginx browser → custom site → Mininet pingAll 12/12 | "Is 20 minute video ke end tak aap **hello-world container**, **nginx web server**, **apna custom Docker image**, aur ek **2-switch 4-host virtual SDN network** — sab khud run kar paoge." | Fast montage, upbeat bg music low |
| 0:30 | Cut to: "Chalte hain Practical 10 se — Docker." | "Chalte hain **Practical 10 — Docker First Container** se." | Hard cut |

---

## 0:30 – 2:30  P10 Theory — Container Kya Hai? (2 min)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 0:30 | Simple animation: shipping container → laptop → server (same box) | "Socho ek **shipping container** — andar sab kuch pack hai: saman, tools, manual. Jahan bhi le jao — ship, train, truck — **waise hi kaam karta hai**. **Container** = app + uski saari cheezein (code, runtime, libraries) ek box mein." | Simple 2D animation or slide |
| 0:55 | Split screen: **VM** (full OS, heavy) vs **Container** (shared kernel, light) | "VM = poora OS install karna padta hai, heavy. **Container = host OS ka kernel share karta hai** — **kernel matlab OS ka core jo hardware se baat karta hai** — isliye fast, chhota." | Side-by-side diagram |
| 1:20 | Text: **Image = read-only template (recipe)** <br/> **Container = running instance (cooked dish)** | "**Image** = read-only template, jaise **recipe**. **Container** = us recipe se bana **cooked dish** — chal raha process. Ek image se kai containers bana sakte hain." | Icons appear on each word |
| 1:45 | Dockerfile snippet on screen (highlight FROM, COPY, CMD) | "**Dockerfile** = image banane ki **recipe** — `FROM` base image, `COPY` files, `CMD` kaise chalega. Aaj hum khud likhenge." | Highlight lines as spoken |
| 2:10 | Quick preview of 3 demos: hello-world → nginx → custom build | "Teen steps: 1) hello-world — test karna. 2) nginx — ready web server. 3) apna Dockerfile + HTML — **custom image**." | Numbered list fade in |
| 2:30 | "Ab setup karte hain." | "Ab **setup** karte hain — WSL2 aur Docker Desktop." | Cut to terminal |

---

## 2:30 – 4:30  P10 Setup — WSL2 + Docker Desktop (2 min, fast-forwarded)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 2:30 | PowerShell (Admin): `wsl --install` → reboot prompt | "**WSL2** = Windows Subsystem for Linux — **Linux kernel Windows ke andar chalta hai**. Command: `wsl --install` — ye Ubuntu install karta hai. Reboot mangega." | Record live, then speed up 8x |
| 3:00 | Browser: docker.com/products/docker-desktop → download → installer → "Use WSL 2 instead of Hyper-V" checked | "Docker Desktop download karein. Installer mein **'Use WSL 2' select karein** — **ye Docker ko WSL2 backend pe chalata hai**, bina Hyper-V ke." | Fast-forward install (30s → 5s) |
| 3:30 | Docker Desktop starts → whale icon → sign-in (optional, skip) → tutorial skip | "Docker Desktop start hoga. Sign-in optional — **skip kar sakte hain**. Tutorial bhi skip." | Cut to verification |
| 3:50 | Terminal: `docker version` → shows Client + Server | "Verify karein: `docker version` — **Client aur Server dono dikhne chahiye** — matlab Docker daemon chal raha hai." | Pause 2s on output |
| 4:00 | Text overlay: ✅ Docker Ready | "**Setup done. Ab pehle container chalaate hain.**" | Hold 1s |

---

## 4:30 – 6:00  P10 Demo 1 — hello-world (1:30)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 4:30 | Terminal: `docker run --rm hello-world` | "Command: `docker run --rm hello-world` — **`run` naya container banata hai**, `--rm` matlab **kaam khatam hone pe container delete kar do**." | Type slowly, speak each flag |
| 4:45 | Output appears line by line (pause on each): <br/>1. "Unable to find image locally" <br/>2. "Pulling from library/hello-world" <br/>3. "Digest: sha256:..." <br/>4. "Hello from Docker!" message | "**Pehli baar** image local nahi hoti to **Docker Hub se pull hoti hai** — **Docker Hub = public image registry**. Phir container banta hai, message print karta hai, exit karta hai." | Pause 1s on each line, read aloud |
| 5:20 | Text overlay: **Image pulled → Container created → Ran → Exited** | "Flow: **Image pull → Container create → Run → Exit**. Yehi cycle har baar hota hai." | Hold 2s |
| 5:35 | `docker images` → shows hello-world | "`docker images` se local images dekho — hello-world aagaya." | Quick |
| 5:50 | "Chalte hain nginx." | "Ab **nginx web server** chalaate hain — real use case." | Cut |

---

## 6:00 – 7:30  P10 Demo 2 — nginx on :8080 (1:30)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|----------|
| 6:00 | Terminal: `docker run -d -p 8080:80 --name p10-nginx nginx` | "`docker run -d -p 8080:80 --name p10-nginx nginx` — **`-d` = detached (background)**, **`-p 8080:80` = port mapping: host 8080 → container 80**, **`--name` = naam de diya**." | Type & explain flags |
| 6:20 | Output: container ID → `docker ps` shows running | "Container ID aaya. `docker ps` se check karein — **STATUS: Up**, **PORTS: 0.0.0.0:8080→80/tcp**." | Highlight PORTS column |
| 6:35 | Browser: `http://localhost:8080` → "Welcome to nginx!" | "Browser pe `localhost:8080` — **nginx welcome page**. Matlab **container ke andar nginx chal raha hai**, humne port map kiya." | Zoom on browser |
| 6:50 | Terminal: `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080` → 200 | "Programmatic check: `curl` se **HTTP 200** — **200 matlab success**." | Show curl command |
| 7:05 | `docker stop p10-nginx && docker rm p10-nginx` | "Cleanup: `docker stop` + `docker rm` — container hata diya." | Quick |
| 7:20 | "Ab apna custom image banate hain." | "Ab **apna custom Docker image** banate hain — Dockerfile likhenge." | Cut to folder |

---

## 7:30 – 9:30  P10 Demo 3 — Custom Build + Run (2:00)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 7:30 | File Explorer: Desktop → `p10` folder → `Dockerfile` + `p10_site/index.html` | "Desktop pe `p10` folder banao. Andar **`Dockerfile`** aur **`p10_site/index.html`** rakho — **ye assets main description mein milega**." | Show folder tree |
| 7:45 | Open `Dockerfile` in Notepad/VS Code — read each line | "**Dockerfile line-by-line:**<br/>`FROM python:3-alpine` — **chhota base image** (~50 MB).<br/>`WORKDIR /usr/share/app` — **andar ka folder**.<br/>`COPY p10_site/ ./p10_site/` — **HTML copy kiya**.<br/>`EXPOSE 80` — **port document kiya**.<br/>`CMD python -m http.server 80` — **simple server chalega**." | Highlight each line as spoken |
| 8:20 | Open `index.html` — show "Hello, Docker! 🚀" | "`index.html` — simple page. **Aap apna likh sakte hain**." | Quick scroll |
| 8:30 | Terminal (in `p10` folder): `docker build -t p10-cdct-site .` | "`docker build -t p10-cdct-site .` — **`-t` = tag/naam**, **`.` = current folder (build context)**. Layers dikhenge — **layer = image ka ek step**." | Show build output, pause on "naming to docker.io/library/p10-cdct-site:latest done" |
| 9:00 | `docker run -d -p 8081:80 --name p10-cdct-site p10-cdct-site` | "`docker run -d -p 8081:80 --name p10-cdct-site p10-cdct-site` — **naya port 8081** taki nginx se conflict na ho." | Type |
| 9:10 | Browser: `http://localhost:8081` → custom page | "`localhost:8081` — **apna page!** Container ke andar humara server chal raha hai." | Celebrate moment |
| 9:20 | `docker ps`, `docker images` — show both | "`docker ps` — dono containers (agar nginx bhi chal raha ho). `docker images` — hello-world, nginx, p10-cdct-site." | Quick |
| 9:30 | "P10 done. Cleanup commands screen." | "**Practical 10 complete.** Cleanup: `docker stop p10-nginx p10-cdct-site && docker rm p10-nginx p10-cdct-site`." | Hold cleanup screen 3s |

---

## 9:30 – 10:00  P10 Recap + Deliverable Checklist

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 9:30 | Slide: **P10 — Key Commands Recap** (bulleted) | "P10 ke key commands yaad rakho: `docker version`, `docker run hello-world`, `docker run -d -p 8080:80 nginx`, `docker build -t name .`, `docker run -d -p 8081:80 name`, `docker ps`, `docker images`, `docker stop/rm`." | Text on screen |
| 9:45 | Slide: **Lab Report Checklist** <br/>• `docker version` screenshot <br/>• hello-world output <br/>• nginx `docker ps` + browser <br/>• Dockerfile content <br/>• Build log + `curl` 200 <br/>• Explanation: image vs container, layers, port mapping | "Report mein ye screenshots chahiye: docker version, hello-world output, nginx running proof, Dockerfile, build log, curl 200. Aur explain karna: **image vs container**, **layered build**, **port publishing**." | Hold 4s |
| 9:55 | "Ab Practical 5 — Mininet SDN Lab." | "Ab **Practical 5 — Virtual SDN Lab with Mininet**." | Hard cut, music sting |

---

## 10:00 – 10:30  Transition to P05

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 10:00 | Title: **P05 — Virtual SDN Lab (Mininet)** | "Dosto, ab hum ek **poora virtual network** banayenge — **2 switches, 4 hosts** — apne Windows PC pe." | |
| 10:10 | Animation: 4 PCs connected via 2 switches → Mininet logo | "**Mininet** = **network emulator** — **emulator matlab software jo real network jaisa behave karta hai** lekin single machine pe. Ye **Linux network namespaces** aur **virtual ethernet pairs (veth)** use karta hai." | Simple animation |
| 10:20 | "SDN = Control Plane (brain) + Data Plane (roads)" | "**SDN** = **Software-Defined Networking**. **Control plane = dimag (controller)** jo decide karta hai packet kahan jayega. **Data plane = sadak (switches)** jo bas forward karte hain. **OpenFlow** = controller-switch ke beech ki language." | Diagram on screen |
| 10:30 | "Setup: VirtualBox + Mininet VM." | "Windows pe Mininet chalane ka best tarika: **VirtualBox + Mininet VM appliance**." | Cut to VirtualBox |

---

## 10:30 – 12:00  P05 Theory — SDN + Mininet (1:30)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 10:30 | Diagram: Controller (c0) → s1, s2 → h1,h2,h3,h4 | "Hamara topology: **Controller c0**, **2 switches (s1, s2)**, **4 hosts (h1-h4)**. Hosts apne switch se jude hain, switches ek dusre se." | Mermaid or draw.io diagram |
| 10:50 | Bullet: <br/>• Host = Linux network namespace (isolated stack) <br/>• Switch = Open vSwitch (software) <br/>• Link = veth pair <br/>• Controller = NOX/POX/RYU (default) | "**Mininet internals:** Har **host = Linux network namespace** — **namespace matlab alag network stack, apna IP**. **Switch = Open vSwitch** (software switch). **Link = veth pair** — virtual cable. **Controller** default hota hai." | Bullets appear |
| 11:15 | "WSL2 pe Mininet unreliable — use VirtualBox VM." | "**WSL2 pe Mininet chalana unreliable hai** — **Open vSwitch kernel module load nahi hota**. Isliye **official Mininet VM (OVA) use karenge** — ye ready-to-use aata hai." | Warning icon |
| 11:30 | mininet.org download page scroll | "mininet.org → **Download** → **Mininet VM (OVA)** — ~1.3 GB. VirtualBox pe import karenge." | Show browser |
| 12:00 | "Chalte hain setup." | "Ab **VirtualBox install + VM import** karte hain." | Cut |

---

## 12:00 – 14:00  P05 Setup — VirtualBox + Mininet VM (2 min, fast-forwarded)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 12:00 | VirtualBox.org → download → install (default) | "VirtualBox install karein — default options theek hain." | Fast-forward 2 min → 15s |
| 12:20 | VirtualBox Manager: File → Import Appliance → select `.ova` → Next → Import | "VirtualBox open → **File → Import Appliance** → downloaded `.ova` select → **Import** — ye 1-2 minute lega." | Fast-forward |
| 12:40 | VM boots → login prompt: `mininet` / `mininet` | "VM start hoga. Login: **username `mininet`, password `mininet`**." | Pause on login screen |
| 12:55 | Terminal inside VM: `sudo mn --version` → shows 2.3.x | "`sudo mn --version` — **Mininet 2.3.x** confirm. `sudo` zaroori hai kyunki **network namespaces root mangte hain**." | Hold output 2s |
| 13:10 | `mkdir -p ~/cdct-lab && cd ~/cdct-lab` | "Lab folder banao: `mkdir -p ~/cdct-lab && cd ~/cdct-lab`." | Quick |
| 13:20 | Copy script: show `p05_mininet_2switch_4host.py` on host → shared folder / drag-drop / scp | "Host se script copy karein VM mein — **Shared Folder** ya **drag-drop** enable karein VirtualBox settings mein. Ya `scp` use karein." | Show one method |
| 13:40 | `ls -l p05_mininet_2switch_4host.py` | "File aagayi — `ls -l` se check." | Quick |
| 14:00 | "Ab script samjhte hain." | "Ab **script line-by-line samjhte hain**." | Cut to editor |

---

## 14:00 – 16:30  P05 Script Walkthrough + Run (2:30)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 14:00 | Open `p05_mininet_2switch_4host.py` in VS Code / nano — highlight sections | "**Script structure:**<br/>1. **Imports** — `Topo`, `Mininet`, `TCLink`, `CLI`.<br/>2. **Class `TwoSwitchFourHostTopo`** — `build()` mein: `addSwitch('s1')`, `addSwitch('s2')`, `addHost` with IPs, `addLink` host-switch, `addLink(s1,s2)`.<br/>3. **`run()`** — `setLogLevel`, `Mininet(topo, link=TCLink)`, `addController('c0')`, `net.start()`, `pingAll()`, `CLI(net)`, `net.stop()`." | Scroll slowly, highlight each block |
| 15:00 | Terminal: `sudo python3 p05_mininet_2switch_4host.py` | "**Run:** `sudo python3 p05_mininet_2switch_4host.py` — **`sudo` zaroori** kyunki namespaces create karne hain." | Type command |
| 15:10 | Output appears: <br/>*** Creating network <br/>*** Adding controller <br/>*** Adding hosts: h1 h2 h3 h4 <br/>*** Adding switches: s1 s2 <br/>*** Adding links... <br/>*** Configuring hosts <br/>*** Starting controller <br/>*** Starting 2 switches | "Output dekho: **topology build ho rahi hai** — hosts, switches, links, controller, switches start." | Pause on each section |
| 15:35 | `>>> Ping test (full mesh)` → `h1 -> h2 h3 h4` … `*** Results: 0% dropped (12/12 received)` | "**Sabse important moment:** `pingAll` — **har host har dusre host ko ping karta hai**. **12/12 received, 0% dropped** — **matlab poora network connected hai**!" | **Emphasize**, zoom, hold 3s |
| 15:55 | `>>> h1 -> h4 connectivity` → 3 pings to 10.0.0.4 | "`h1` se `h4` (10.0.0.4) — **ye packet `s1 → s2` gaya** — inter-switch link use hua." | Arrow animation on topology |
| 16:10 | `mininet>` prompt appears | "Ab **interactive CLI** — `mininet>` prompt. Yahan commands chala sakte hain." | Hold prompt |
| 16:20 | "Agale segment mein CLI explore karenge." | "Agale segment mein **CLI explore karenge** — flows, nodes, links." | Cut |

---

## 16:30 – 18:00  P05 CLI Exploration (1:30)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 16:30 | `mininet> nodes` → lists h1 h2 h3 h4 s1 s2 | "`nodes` — **saare nodes dikhta hai**." | Type, show output |
| 16:40 | `mininet> net` — topology with IPs | "`net` — **poora topology with IPs**." | Show |
| 16:45 | `mininet> h1 ping -c 3 h4` → 3 replies | "`h1 ping -c 3 h4` — **manual ping**." | |
| 16:50 | `mininet> s1 dpctl dump-flows` → shows flow entries | "**Sabse powerful:** `s1 dpctl dump-flows` — **switch s1 ke flow table entries**." | |
| 17:05 | Explain output: `cookie=0, duration=..., table=0, n_packets=..., n_bytes=..., idle_age=..., priority=..., icmp,in_port=1 actions=output:2` | "**Flow entry matlab:** jab pehli baar packet aaya, **controller ne rule bana di** — **'icmp packet in_port 1 → output port 2'**. Ab agla packet **bina controller pooche** forward hoga. Yehi **SDN ka 'learning'** hai." | Annotate flow line |
| 17:25 | `mininet> links` — shows veth pairs | "`links` — **virtual cables (veth pairs)**." | Quick |
| 17:35 | `mininet> exit` → cleanup → back to bash | "`exit` — **CLI band, cleanup, wapas bash**." | |
| 17:50 | "P05 bhi complete." | "**Practical 5 bhi complete.** Ab dono ka recap." | Cut |

---

## 18:00 – 20:00  Final Recap + Deliverables + Outro (2:00)

| Time | On-Screen | Narration (Hinglish) | Director Cue |
|------|-----------|----------------------|--------------|
| 18:00 | Split screen: P10 left, P05 right — key outputs | "Recap: **P10** — hello-world, nginx, custom image. **P05** — Mininet VM, 2-switch topology, `pingAll 12/12`, `dpctl dump-flows`." | Side by side |
| 18:20 | Slide: **P10 Report Checklist** (same as 9:45) | "P10 report: docker version, hello-world, nginx proof, Dockerfile, build log, curl 200, explanation." | Hold 3s |
| 18:35 | Slide: **P05 Report Checklist** <br/>• `mn --version` <br/>• Topology script (or GitHub link) <br/>• Screenshot: topology build + pingAll 12/12 <br/>• Screenshot: `s1 dpctl dump-flows` <br/>• Conclusion: control/data plane separation | "P05 report: mn version, script, topology build + pingAll screenshot, dpctl dump-flows screenshot, conclusion — **controller = brain, switches = dumb pipes**." | Hold 4s |
| 18:55 | Text: **Key Takeaways** <br/>• Container = app + deps in a box <br/>• Image vs container = recipe vs dish <br/>• SDN = brain (controller) + roads (switches) <br/>• Mininet = virtual network on one PC <br/>• Flow table = learned shortcuts | "Key takeaways yaad rakho: **Container = box**, **Image = recipe**, **SDN = brain + roads**, **Mininet = virtual net**, **Flow table = learned shortcuts**." | Bullet animation |
| 19:20 | "Agar video pasand aayi to like/subscribe. Code links description mein." | "Agar video helpful lagi to **like, subscribe, share** karein. **Saare code files, commands, checklists description mein milega**." | Friendly |
| 19:40 | "Next video: CDCT Practical 9 — MinIO Secure Object Storage." | "Next video: **Practical 9 — MinIO Secure Object Storage**." | Tease |
| 19:50 | End card: Channel name, GitHub repo link, "Thanks for watching!" | "Dhanyavaad! Milte hain agle video mein. **Happy learning!**" | Hold 5s, fade out |

---

## Appendix — Hinglish Glossary (for your reference while recording)

| English Term | Hinglish One-Liner |
|--------------|-------------------|
| Container | ek box jisme app + saari dependencies packed hain |
| Image | read-only template / recipe |
| Dockerfile | image banane ki recipe (FROM, COPY, CMD) |
| Layer | image ka ek step / change |
| Port mapping (`-p 8080:80`) | host ka 8080 port container ke 80 se joda |
| Detached (`-d`) | background mein chalao |
| Registry (Docker Hub) | public image ka godown |
| WSL2 | Windows ke andar Linux kernel |
| Virtualization | CPU ka feature jo VM/containers ko speed deta hai |
| Kernel | OS ka core jo hardware se baat karta hai |
| SDN | Software-Defined Networking — control plane alag, data plane alag |
| Control plane | network ka dimag (controller) |
| Data plane | network ki sadaken (switches) |
| OpenFlow | controller-switch ke beech ki language |
| Mininet | network emulator — ek PC pe virtual network |
| Network namespace | isolated network stack (apna IP, apna interface) |
| veth pair | virtual cable — do ends ek dusre se jude |
| Open vSwitch | software switch (Linux kernel module) |
| Flow table / flow entry | switch ka rule — 'packet type X → output port Y' |
| Learned flow | pehli baar controller ne rule banaya, phir switch khud forward karta hai |
| `pingAll` | har host har dusre host ko ping karta hai |
| `dpctl dump-flows` | switch ke flow table entries dikhao |

---

## Director's Quick Reference — OBS Scenes to Prepare

| Scene Name | Sources |
|------------|---------|
| **Title Card** | Image + text |
| **Terminal** | Window capture (Windows Terminal / PowerShell) |
| **Browser** | Window capture (Chrome/Edge) |
| **Code Editor** | Window capture (VS Code / Notepad++) |
| **VirtualBox** | Window capture (VM console) |
| **VM Terminal** | Window capture (inside Mininet VM) |
| **Slides/Bullets** | Media source (PNG/MP4) or OBS text |
| **Diagram** | Image source (Mermaid export / draw.io PNG) |
| **Picture-in-Picture** | Webcam (optional) over terminal |
| **Fast-Forward Overlay** | Text "⏩ 8x speed" + speed lines animation |

**Hotkeys:** Set hotkeys for each scene switch (Ctrl+1…Ctrl+9). Practice once before recording.

---

*End of Script. All assets (Dockerfile, index.html, .py, commands.txt, checklists) are in the `p10/` and `p05/` folders alongside this script.*
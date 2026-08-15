# Practical 10 — Docker First Container (Flask App via Docker Desktop) : Speaking Script
**Read from phone while recording. Cues in [BRACKETS]. Terminal commands in `CODE`. Target ~10 min.**

---

## [SLIDE 1] Title & Aim — 0:00–0:30
> "Hello. Practical 10: **Creating & Executing Your First Container with Docker** – this time a tiny **Flask web application** built, shipped, and run via **Docker Desktop**.  
> Aim: verify Docker Desktop (or Engine) on this machine, run `hello-world`, deploy an nginx container for reference, write a **Flask app + Dockerfile**, build the image, run the container with port publishing, capture live HTTP traffic in Wireshark, and demonstrate container inspection (`logs`, `exec`). At the end a one‑liner VM install for lab submission."

---

## [SLIDE 2] Quick Theory: Container vs VM — 0:30–1:30
> "A **container** packages app + runtime + deps into a portable unit that shares the **host kernel** (OS‑level virtualization).  
> A **VM** runs a full guest OS on a hypervisor (hardware‑level).  
> Containers start in seconds, images are MBs (layered), isolation via Linux **namespaces** (PID, NET, MNT…) + **cgroups** (resource limits).  
> Key terms: **Image** = read‑only layered template. **Container** = running instance with thin writable layer. **Dockerfile** = recipe (FROM, WORKDIR, COPY, EXPOSE, CMD). **`-p host:container`** publishes a container port on the host."

---

## [SLIDE 3] Docker Desktop Overview — 1:30–2:15
> "Docker Desktop bundles the Docker Engine, CLI, Compose, and a GUI dashboard. On Linux it runs a lightweight VM (via `docker-desktop` context) but exposes the same `docker` CLI.  
> We’ll use the CLI for the demo, but you can watch containers appear in the **Dashboard → Containers** view in real time.  
> If Docker Desktop isn’t started: open the app or run `systemctl --user start docker-desktop`."

---

## [SLIDE 4] Our Three Steps — 2:15–2:35
> "1️⃣ `hello-world` – proves client/daemon/registry/pull/run/exit.  
> 2️⃣ `nginx` – real web server, detached, port 8080→80 (quick reference).  
> 3️⃣ **Flask app** – Dockerfile + tiny Python web service, build, run on 8081, verify in browser, capture traffic."

---

## [SLIDE 5] Flask App + Dockerfile Walkthrough — 2:35–4:00
> **[OPEN `p10_flask_app/` IN EDITOR – SHOW THREE FILES]**  
> **`app.py`** – minimal Flask:  
> ```python
> from flask import Flask
> app = Flask(__name__)
> @app.route("/")
> def hello(): return "<h1>Hello from Flask in a container! 🚀</h1>"
> if __name__ == "__main__": app.run(host="0.0.0.0", port=80)
> ```  
> **`requirements.txt`** – `flask==3.0.3`  
> **`Dockerfile`** – line by line:  
> `FROM python:3-alpine` – ~50 MB base.  
> `WORKDIR /app`  
> `COPY requirements.txt .` → `RUN pip install --no-cache-dir -r requirements.txt` (installs Flask, creates layer).  
> `COPY app.py .` – copies source (new layer).  
> `EXPOSE 80` – documents port.  
> `CMD ["python","app.py"]` – runs the Flask dev server on 0.0.0.0:80."

---

## [SLIDE 6] Ensure Docker Desktop / Engine Running — 4:00–4:20
> "On Endeavour OS with Docker Desktop installed: open the app → whale icon → “Dashboard”.  
> CLI check: `docker version` must show **Client** and **Server** (Engine). If `docker ps` errors, start the service: `systemctl --user start docker-desktop` or `sudo systemctl start docker` for the standalone Engine."

---

## [TERMINAL] Step 1: hello‑world — 4:20–4:50
> **[RUN: `docker run --rm hello-world`]**  
> "Output shows: client contacted daemon, image pulled from Docker Hub, container created, executable ran, output streamed, container exited, `--rm` auto‑removed it. Full stack verified."

---

## [TERMINAL] Step 2: nginx (reference) — 4:50–5:40
> **[RUN: `docker run -d -p 8080:80 --name p10-nginx nginx`]**  
> "`-d` detached, `-p 8080:80` host→container, `--name` friendly.  
> **[RUN: `curl -s -o /dev/null -w \"%{http_code}\\n\" http://localhost:8080/`]** → **HTTP 200**.  
> **[RUN: `docker ps`]** – shows `p10-nginx` with `0.0.0.0:8080->80/tcp`.  
> In **Docker Desktop → Containers** you’ll see `p10-nginx` running, logs streaming, port mapping listed."

---

## [TERMINAL] Step 3: Build & Run Flask App — 5:40–7:30
> **[RUN: `docker build -t p10-flask-app -f p10_flask_app/Dockerfile p10_flask_app`]**  
> "Watch layered build: FROM → WORKDIR → COPY requirements → RUN pip install → COPY app.py → EXPOSE → CMD → tag `p10-flask-app:latest`.  
> **[RUN: `docker images`]** – lists new image.  
> **[RUN: `docker run -d -p 8081:80 --name p10-flask p10-flask-app`]**  
> **[RUN: `curl http://localhost:8081/`]** – shows `<h1>Hello from Flask in a container! 🚀</h1>`.  
> **[RUN: `docker ps`]** – both containers: nginx on 8080, Flask on 8081.  
> Open browser → http://localhost:8081 → **Flask page renders**.  
> In **Docker Desktop** you now see two containers side‑by‑side with live log tails."

---

## [WIRESHARK] Capture HTTP to Flask Container — 7:30–8:30
> **[OPEN WIRESHARK → CAPTURE ON `lo` (loopback) → SET FILTER `tcp.port==8081` OR `http` → START]**  
> **[RUN: `curl -v http://localhost:8081/`]** (verbose).  
> **Stop capture.** Filter `http`. You see:  
> `GET / HTTP/1.1` → `HTTP/1.1 200 OK` with HTML body.  
> Expand TCP stream – full request/response. Proves container serves on published host port via Docker’s DNAT (iptables) on the host."

---

## [TERMINAL] Container Inspection — 8:30–9:10
> "**[RUN: `docker logs p10-flask`]** – Flask startup lines + the GET request we just made.  
> **[RUN: `docker exec -it p10-flask sh`]** – shell *inside* running container. `ls`, `cat app.py`, `ps aux` (only python process). `exit`.  
> **[RUN: `docker stop p10-flask && docker rm p10-flask`]** – stop & remove.  
> **[RUN: `docker rmi p10-flask-app`]** – remove image."

---

## [SLIDE 7] VM Setup for Lab Submission — 9:10–9:45
> "If you need a clean VM for the report:  
> 1. Install Ubuntu 22.04/24.04 in VirtualBox.  
> 2. Inside VM: `curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER && newgrp docker`.  
> 3. Verify: `docker version` (both client & server).  
> 4. Copy the `p10_flask_app/` folder and run the three steps above.  
> All commands identical – the VM just provides a fresh Docker Engine."

---

## [SLIDE 8] Conclusion & Viva Prep — 9:45–10:30
> "Done: Docker Desktop/Engine verified, hello‑world OK, nginx on 8080, **Flask app built (layered) and running on 8081**, HTTP captured on published port, `logs` & `exec` demonstrated, Docker Desktop dashboard shown live.  
> **Key takeaways**: image vs container, layered builds (each Dockerfile instruction = layer), `-p` publishes ports, `EXPOSE` documents, Alpine for minimal images, namespaces+cgroups isolation, Docker Desktop GUI for visibility.  
> **Viva Qs**: 1) Image vs container 2) VM vs container 3) `-p 8080:80` meaning 4) Dockerfile purpose & 5 common instructions 5) Why `python:3-alpine` 6) `EXPOSE` vs `-p` 7) Docker isolation mechanisms 8) Build output layers 9) `--rm` effect 10) Docker daemon role 11) What does `docker exec` do? 12) How does Docker Desktop differ from plain Engine? Thank you."

---

## 🎙️ Recording Checklist
- [ ] `docker version` (client & server) shown
- [ ] Docker Desktop dashboard open (show whale icon, Containers list)
- [ ] Theory slides (container vs VM, architecture)
- [ ] Flask app files (`app.py`, `requirements.txt`, `Dockerfile`) displayed & narrated
- [ ] `hello-world` with `--rm` explanation
- [ ] nginx: `-d`, `-p`, `--name`, curl HTTP 200, `docker ps` + Desktop view
- [ ] Build output showing layers for Flask image
- [ ] Flask container run on 8081 + curl + browser check
- [ ] `docker ps` both containers + Desktop both listed
- [ ] Wireshark HTTP capture on port 8081
- [ ] `docker logs`, `docker exec -it` demo
- [ ] VM install one‑liner slide
- [ ] Conclusion slide with viva Qs
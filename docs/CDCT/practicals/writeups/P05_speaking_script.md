# Practical 5 — Mininet Virtual SDN Lab: Speaking Script (Live on Endeavour OS)
**Read from phone while recording. Cues in [BRACKETS]. Terminal commands in `CODE`. Target ~10 min.**

---

## [SLIDE 1] Title & Aim — 0:00–0:30
> "Hello. Practical 5: **Virtual SDN Lab with Mininet**.  
> Aim: run Mininet on this Linux machine, create a 2‑switch 4‑host topology via Python, verify full‑mesh connectivity, inspect OpenFlow flow tables, and capture cross‑switch ICMP with Wireshark. At the end I’ll show the one‑line VM install for lab submission."

---

## [SLIDE 2] Quick Theory: SDN & Mininet — 0:30–1:30
> "SDN separates **control plane** (controller decides routes) from **data plane** (switches forward). OpenFlow is the southbound protocol.  
> Mininet instantiates real Linux **network namespaces** for hosts, **Open vSwitch** processes for switches, and **veth pairs** for links — all on one kernel, no VMs."

---

## [SLIDE 3] Topology Diagram — 1:30–2:00
> "[SHOW MERMAID DIAGRAM] Two switches s1,s2; hosts h1,h2 on s1 (10.0.0.1/2, 10.0.0.2/24), h3,h4 on s2 (10.0.0.3/24, 10.0.0.4/24); inter‑switch link s1↔s2; controller c0 talks OpenFlow to both."

---

## [SLIDE 4] Python Script Walkthrough — 2:00–3:00
> **[OPEN `p05_mininet_2switch_4host.py` IN EDITOR – SCROLL SLOWLY]**  
> "Class `TwoSwitchFourHostTopo` inherits `Topo`. `build()` adds s1,s2; four hosts with static IPs; five links (h1‑s1, h2‑s1, h3‑s2, h4‑s2, s1‑s2). `run()` sets log level, creates `Mininet(topo=…, link=TCLink)`, adds default controller `c0`, `net.start()`, prints switches/hosts, runs `net.pingAll()`, a directed `h1→h4` ping, then `CLI(net)` for interactive exploration."

---

## [SLIDE 5] "Running the Topology Now" — 3:00–3:10
> "We need root for namespace creation, so `sudo python3 …`."

---

## [TERMINAL] Live Run — 3:10–5:00
> **[RUN: `sudo python3 p05_mininet_2switch_4host.py`]**  
> "Watch: controller c0 added, four hosts, two switches, five links, hosts configured, controller started, switches connected.  
> **pingAll** – 12 pings, **0% dropped (12/12 received)** – full mesh works, including cross‑switch paths. Directed h1→h4 ping succeeds. Now at `mininet>` prompt."

---

## [TERMINAL] Mininet CLI Exploration — 5:00–6:30
> "**[RUN: `nodes`]** – lists h1 h2 h3 h4 s1 s2.  
> **[RUN: `links`]** – shows five veth pairs with interface names.  
> **[RUN: `net`]** – full topology with IPs, MACs, port numbers.  
> **[RUN: `h1 ifconfig`]** – h1’s eth0 (10.0.0.1) inside its namespace.  
> **[RUN: `h1 ping -c 3 h4`]** – instant cross‑switch ping (flows already learned).  
> **[RUN: `h2 traceroute h3`]** – path h2 → s1 → s2 → h3 (3 hops).  
> **[RUN: `s1 dpctl dump-flows`]** – **key SDN proof**: flow entries with `priority=100` matching `in_port` + `nw_dst` → `output:<port>`; a `priority=0` miss entry sending to CONTROLLER. Controller programmed the data plane."

---

## [WIRESHARK] Capture ICMP Across Switches — 6:30–7:30
> **[OPEN WIRESHARK → CAPTURE ON `any` → SET FILTER `icmp` → START]**  
> **Back in CLI:** **[RUN: `h1 ping -c 5 h3`]** (h1 on s1 → h3 on s2).  
> **Stop capture.** Filter `icmp`. You see Echo Request 10.0.0.1 → 10.0.0.3 and Echo Reply back – traversing the inter‑switch link. Expand a frame: Ethernet src/dst MACs belong to the veth ends on s1 and s2.

---

## [SLIDE 6] VM Setup for Lab Submission — 7:30–8:15
> "If you need a clean VM for the lab report:  
> 1. Install Ubuntu 22.04/24.04 in VirtualBox.  
> 2. Inside VM: `sudo apt update && sudo apt install -y mininet openvswitch-switch`.  
> 3. Verify: `mn --version`.  
> 4. Copy the same Python script into the VM and run `sudo python3 …`.  
> All steps identical – the VM just provides the namespaces/OVS that Mininet requires."

---

## [SLIDE 7] Conclusion & Viva Prep — 8:15–9:00
> "Done: Mininet live on this host, 2‑switch 4‑host SDN fabric up, 0% loss, flow tables inspected, live ICMP captured across switches.  
> **Viva Qs**: 1) Mininet & namespaces 2) Control vs data plane 3) OpenFlow role 4) What `pingAll` proves 5) `dpctl dump-flows` output meaning 6) Why OVS over user switch 7) Mininet vs simulator. Thank you."

---

## 🎙️ Recording Checklist
- [ ] `mn --version` shown
- [ ] Theory slides (SDN, Mininet)
- [ ] Topology diagram visible
- [ ] Script file scrolled with narration
- [ ] Full run output + `pingAll` 0% dropped
- [ ] CLI: `nodes`, `links`, `net`, `ifconfig`, `traceroute`, `dpctl dump-flows`
- [ ] Wireshark ICMP capture (h1→h3)
- [ ] VM setup slide
- [ ] Conclusion slide with viva Qs
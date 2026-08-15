# P05 — Virtual SDN Lab with Mininet
## Cloud & Data Center Technology (CDCT) — Practical 5
**Presenter:** ___________________  
**Date:** ___________________  
**Environment:** Native Linux host (EndeavourOS) – Mininet 2.3.1b4, OVS 3.7, Wireshark 4.7  

---

## Agenda
1. **What is SDN?** – Control vs Data plane, OpenFlow
2. **Why Mininet?** – Namespaces, veth, OVS on one box
3. **Today’s Topology** – 2 switches, 4 hosts, IP plan
4. **Launch & Verify** – Run script, `net`, `nodes`, `links`
5. **Live Traffic & Wireshark** – `pingall`, cross‑switch ping, capture ARP/ICMP
6. **SDN in Action** – `dpctl dump-flows`, OpenFlow `flow_mod` in Wireshark
7. **Namespace Peek** – `ifconfig`, `ip route` inside a host namespace
8. **Wrap‑up & Viva Pointers**

---

## 1. What is SDN? (Software‑Defined Networking)

### Traditional Network
- Control plane **and** data plane live together in every switch/router
- Distributed protocols (OSPF, BGP, STP) run on each device
- Changing network-wide policy = touch every box

### SDN Architecture
```
+-------------------+      OpenFlow      +-------------------+
|   CONTROL PLANE   | <----------------> |   DATA PLANE      |
|  (SDN Controller) |   Flow Rules       |  (OVS Switches)   |
|                   |                    |                   |
| • Global topology |                    | • Flow tables     |
| • Path computation|                    | • Match + Action  |
| • Policy logic    |                    | • No decisions    |
+-------------------+                    +-------------------+
```
- **Control plane centralized** → single brain
- **Data plane dumb** → only match‑and‑forward
- **OpenFlow** = southbound protocol (controller ↔ switch)

**Key takeaway:** *The controller decides; the switch obeys.*

---

## 2. Why Mininet?

| Concept | Mininet Implementation |
|---------|------------------------|
| **Host** | Linux **network namespace** – isolated stack (own NICs, ARP, routes) |
| **Switch** | **Open vSwitch (OVS)** – kernel datapath + `ovs-vswitchd`, speaks OpenFlow |
| **Link** | **veth pair** – virtual Ethernet cable connecting two namespaces (or ns↔OVS) |
| **Controller** | Userspace process (`controller`, POX, RYU, ONOS…) – talks OpenFlow to OVS |

All of the above run **inside a single Linux kernel** – no VMs, no hardware.

---

## 3. Today’s Topology – 2 Switches, 4 Hosts

```
                         10.0.0.0/24
        ═══════════════════════════════════
        
    h1 (10.0.0.1) ──┐                       │
                    │                       │
    h2 (10.0.0.2) ──┤     s1 (OVS)          │  ← Access switch
                    │                       │
                    └───────────┬───────────┘
                                │ s1–s2 inter‑switch link
                    ┌───────────┴───────────┐
                    │                       │
                    │     s2 (OVS)          │  ← Aggregation switch
    h3 (10.0.0.3) ──┤                       │
                    │                       │
    h4 (10.0.0.4) ──┘                       │
        ═══════════════════════════════════
```

| Node | Interface | IP/Netmask | Location |
|------|-----------|------------|----------|
| h1 | h1‑eth0 | 10.0.0.1/24 | s1 |
| h2 | h2‑eth0 | 10.0.0.2/24 | s1 |
| h3 | h3‑eth0 | 10.0.0.3/24 | s2 |
| h4 | h4‑eth0 | 10.0.0.4/24 | s2 |
| s1 | – | – | OVS (access) |
| s2 | – | – | OVS (aggregation) |
| c0 | – | – | Default OpenFlow controller |

**Critical path:** *h1 → h4 must cross the **s1↔s2 inter‑switch link** – we will see that in Wireshark.*

---

## 4. The Python Script (What It Does)

```python
class TwoSwitchFourHostTopo(Topo):
    def build(self):
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        h1 = self.addHost("h1", ip="10.0.0.1/24")
        h2 = self.addHost("h2", ip="10.0.0.2/24")
        h3 = self.addHost("h3", ip="10.0.0.3/24")
        h4 = self.addHost("h4", ip="10.0.0.4/24")
        self.addLink(h1, s1); self.addLink(h2, s1)
        self.addLink(h3, s2); self.addLink(h4, s2)
        self.addLink(s1, s2)          # <-- inter‑switch link

def run():
    net = Mininet(topo=TwoSwitchFourHostTopo(), link=TCLink, controller=None)
    net.addController("c0")           # starts reference controller
    net.start()
    print(net.pingAll())              # full‑mesh test
    print(net["h1"].cmd("ping -c 3 10.0.0.4"))
    CLI(net)                          # interactive prompt
    net.stop()
```

*Run it:*  

```bash
cd /mnt/work/college/sem_5/docs/CDCT/practicals/code
sudo python3 p05_mininet_2switch_4host.py
```

---

## 5. Launch & Verify – Commands You’ll Show

| Command | What It Shows | Talking Point |
|---------|---------------|---------------|
| `mininet> net` | Full topology, IPs, connections | “Visual proof – h1/h2 on s1, h3/h4 on s2, s1↔s2 link” |
| `mininet> nodes` | List of 6 nodes | “4 hosts + 2 switches = 6 network namespaces” |
| `mininet> links` | All veth pairs | “Each link = a veth pair living in the kernel” |
| `mininet> h1 ifconfig` | h1’s virtual NIC (h1‑eth0) | “h1 sees **only** its own interface – isolation!” |
| `mininet> h1 ip route` | h1 routing table | “Default via 10.0.0.1 dev h1‑eth0” |
| `mininet> pingall` | 12 pings, 0% loss | “Full L2/L3 connectivity across the fabric” |
| `mininet> h1 ping -c 3 10.0.0.4` | Cross‑switch ping | “Traffic **must** traverse s1→s2” |

---

## 6. Live Wireshark Capture – What to Show

### Capture Setup (run **before** any ping)
```bash
# Simple – capture every veth on the host
sudo wireshark -k -i any
```

### Display Filters (prepare as a profile)
| Filter | Purpose |
|--------|---------|
| `arp` | ARP request/reply – first packet floods via s1→s2 |
| `icmp` | Ping request/reply – see same frame on both switch ports |
| `openflow` / `tcp.port==6653` | OFPT_PACKET_IN, OFPT_FLOW_MOD – controller installs flow |
| `ip.addr==10.0.0.1 && ip.addr==10.0.0.4` | End‑to‑end view of one conversation |

**Narration cues**  
- *ARP*: “h1 asks ‘who has 10.0.0.4?’ – broadcast goes s1→s2”  
- *ICMP*: “Request crosses inter‑switch link, reply returns”  
- *OpenFlow*: “Controller sees first packet (packet‑in), computes output port, pushes flow_mod – **reactive flow installation** = SDN”

---

## 7. SDN in Action – Flow Table Inspection

```bash
mininet> s1 dpctl dump-flows
```

Typical output (after first ping):
```
cookie=0x0, duration=..., table=0, n_packets=1, n_bytes=98, idle_age=..., priority=1,icmp,in_port=1 actions=output:3
cookie=0x0, duration=..., table=0, n_packets=1, n_bytes=98, idle_age=..., priority=1,arp,in_port=1 actions=output:3
```
- **in_port=1** = port toward h1  
- **output:3** = port toward s2 (inter‑switch link)  
- Installed **reactively** after the first ARP/ICMP – no static config.

In Wireshark (`openflow` filter) you will see:
1. **OFPT_PACKET_IN** (switch → controller)  
2. **OFPT_FLOW_MOD** (controller → switch) – adds the rule above  

*That two‑message exchange is the heart of SDN.*

---

## 8. Namespace Peek – Proof of Isolation

```bash
mininet> h1 ifconfig
# h1-eth0: 10.0.0.1/24  (no other interfaces visible)

mininet> h1 ip route
# default via 10.0.0.1 dev h1-eth0
```

- Each host lives in its **own network namespace** – completely isolated stack.
- `nsenter` / `ip netns exec` can be used from the host to inspect from outside.

---

## 9. Wrap‑Up & Viva Pointers

| Question | Expected Answer |
|----------|-----------------|
| **What is Mininet?** | Network emulator using Linux namespaces + veth + OVS |
| **SDN vs Traditional?** | Centralized control plane, OpenFlow southbound, dumb data plane |
| **Why namespaces?** | Isolate network stack per host on a single kernel |
| **What does `pingAll` prove?** | End‑to‑end L2/L3 connectivity across the emulated fabric |
| **Controller vs Switch?** | Controller computes routes; switches only match‑and‑forward per flow rules |
| **Flow installation trigger?** | First packet (ARP/ICMP) → packet‑in → controller → flow‑mod |
| **TTL behavior?** | Decrements at each L3 hop (router); unchanged across pure L2 switches |

---

## 10. Recording Checklist (for you)

- [ ] OBS / SimpleScreenRecorder configured – **two windows side‑by‑side** (Terminal left, Wireshark right)
- [ ] Wireshark capture started **before** script runs (`sudo wireshark -k -i any`)
- [ ] Display filters saved as a profile (`arp`, `icmp`, `openflow`, `ip.addr==10.0.0.1 && ip.addr==10.0.0.4`)
- [ ] Terminal font size ≥ 14pt for readability
- [ ] Run a quick `sudo mn --test pingpair` beforehand to sanity‑check
- [ ] Keep a copy of this markdown open (or printed) for narration cues

---

*End of presentation – good luck with the recording!* 🚀
---
subject: CDCT
status: not-started
tags: [subject/cdct, practical, unit/2]
practical: 3
unit: 2
hours: 2
---
# P03 — Install VirtualBox + Linux VM on Windows 8+

**Subject:** Cloud and Data Center Technology | **Unit:** 2 | **Approx. Hrs:** 2
**PrO (verbatim):** *Install Virtualbox/VMware/ Equivalent open source cloud Workstation with different platforms of Linux or Windows OS on top of windows 8 and above.*

---

## 1. Objective
- Install **Oracle VirtualBox** on Windows 8 / 10 / 11.
- Create a **Ubuntu (Linux) virtual machine** with exact settings: **2 vCPU, 4 GB RAM, 20 GB disk**.
- Verify the VM boots, connects to the network, and is usable.

## 2. Theory (exam-ready)
A **hypervisor** creates and runs **virtual machines (VMs)**. **VirtualBox** is a **Type-2 (hosted) hypervisor** — it runs as a normal application *on top of* an existing OS (Windows here), unlike a Type-1 hypervisor (e.g., VMware ESXi, KVM) which runs directly on hardware. Each VM gets virtualised vCPU, RAM, disk, and network from the host.

**Virtualisation concepts used:** VT-x/AMD-V (hardware acceleration), NAT vs Bridged networking, virtual disk images (`.vdi`), guest additions (shared folders, clipboard, display drivers).

## 3. Step-by-step

### 3.1 Download & install VirtualBox
1. Go to https://www.virtualbox.org → **Downloads** → `Windows hosts` (e.g., `VirtualBox-7.1.x-Win.exe`).
2. Run the installer. Accept defaults (`Oracle VM VirtualBox Extension Pack` is optional — needed for USB 3.0/VRDP).
3. **Check prerequisites:** Windows 8+ 64-bit, **VT-x/AMD-V enabled in BIOS/UEFI** (Settings → Virtualization Technology → Enabled), ≥ 8 GB RAM recommended.

### 3.2 Download the Ubuntu ISO
1. Go to https://ubuntu.com/download/desktop → download the **LTS ISO** (e.g., `ubuntu-24.04.x-desktop-amd64.iso`, ~6 GB).
2. Save it somewhere you can find (e.g., `C:\Users\<you>\Downloads`).
   - (For a lighter lab you may also use `ubuntu-24.04-live-server-amd64.iso`.)

### 3.3 Create the VM (exact settings)
In VirtualBox Manager → **New**:
| Setting | Value |
|---|---|
| Name | `Ubuntu-CDCT-Lab` |
| Type / Version | Linux / Ubuntu (64-bit) |
| Memory (RAM) | **4096 MB (4 GB)** |
| Hard disk | **Create a virtual hard disk now** → VDI → Dynamically allocated → **20 GB** |
| CPUs (after creation: Settings → System → Processor) | **2 cores**, enable *PAE/NX* |
| Network | **NAT** (default) or **Bridged Adapter** for a real LAN IP |
| Display (Settings → Display) | Video memory 128 MB, scale factor 150% |
| Storage (Settings → Storage → Empty → disk icon) | **Attach the Ubuntu ISO** |

### 3.4 Install Ubuntu
1. Start the VM → it boots from the ISO → choose **Try or Install Ubuntu**.
2. Select language/keyboard → **Install Ubuntu** → *Interactive installation* → default features.
3. Disk: **Erase disk and install Ubuntu** (this erases only the *virtual* disk) → Install.
4. Create a **user** (`student` / password) → click through → reboot when asked → **remove the ISO** (Settings → Storage → detach, or press Enter on *"Remove the installation media"*).

### 3.5 Install Guest Additions (recommended)
1. In the running VM: **Devices → Insert Guest Additions CD image**.
2. In Ubuntu: run the autorun (`software & updates` prompt) or:
   ```bash
   cd /media/student/VBox_GAs_*/
   sudo ./VBoxLinuxAdditions.run
   ```
3. Reboot the VM. Now you get full screen resolution, shared folders, and clipboard sharing.

## 4. Post-install checklist
- [ ] `free -h` shows ~4 GB RAM; `nproc` shows 2 CPUs.
- [ ] Internet works: `ping -c 3 8.8.8.8` and `sudo apt update`.
- [ ] Screen resolution adapts to the window (Guest Additions OK).
- [ ] Snapshot taken: Machine → **Take Snapshot** `base-clean` (so you can roll back after labs).
- [ ] `df -h /` shows the ~20 GB virtual disk.

## 5. VMware alternative (same settings)
- Download **VMware Workstation Player** (free for personal use) → New Virtual Machine → *Use ISO* → Ubuntu → Customize hardware → **2 CPUs, 4 GB RAM, 20 GB disk** → install **VMware Tools** (Player → Manage → Install VMware Tools).

## 6. Expected output (live check in the VM)
```
student@ubuntu:~$ nproc
2
student@ubuntu:~$ free -h
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       950Mi       2.4Gi        24Mi       511Mi       2.6Gi
student@ubuntu:~$ sudo apt update
Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
...
```
> ✅ This practical was followed in this environment with **QEMU/KVM** (the same virtualisation concepts) — VirtualBox-specific steps are documented from the official guide because this machine runs Linux, not Windows.

## 7. Viva Q&A
1. **Type-1 vs Type-2 hypervisor?** — Type-1 runs on bare metal (KVM, ESXi); Type-2 runs on an OS (VirtualBox, VMware Workstation).
2. **Why 2 vCPU / 4 GB / 20 GB?** — Minimum comfortable resource set for a desktop Ubuntu VM on a student laptop.
3. **NAT vs Bridged?** — NAT = VM shares host IP (outbound only); Bridged = VM gets its own LAN IP.
4. **What is a VDI?** — VirtualBox's virtual disk format; *dynamically allocated* grows on demand.
5. **What do Guest Additions do?** — Better display drivers, shared folders, clipboard, seamless mouse.

## 8. Resources
- VirtualBox manual: https://www.virtualbox.org/manual/
- VirtualBox downloads: https://www.virtualbox.org/wiki/Downloads
- Ubuntu downloads: https://ubuntu.com/download/desktop
- Ubuntu installation guide: https://ubuntu.com/tutorials/install-ubuntu-desktop
- VMware Workstation Player: https://www.vmware.com/products/workstation-player.html

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Install Virtualbox Linux Vm** in a real environment, it almost never works perfectly the first time. 
> 
> **Common Edge Cases to Test:**
> 1. **Network partitions:** What happens to this code if the Wi-Fi drops halfway through execution?
> 2. **Malformed Inputs:** How does the system behave if fed null values, extremely large datasets, or unexpected data types?
> 3. **Resource Exhaustion:** Does this script handle memory leaks or rate-limiting from APIs?

## 🔬 Extension Challenge

> [!example] Prove your expertise
> To truly master this practical, try modifying the code to achieve the following:
> - **Add robust error handling** (try/catch blocks) and structured logging instead of print statements.
> - **Parameterize the inputs** so the script can be run dynamically from the CLI without hardcoding values.
> - **Optimize it:** Can you reduce the execution time or memory footprint?

## 🎯 Key Takeaways

- **Type-2 (hosted) hypervisor** — it runs as a normal application *on top of* an existing OS (Windows here), unlike a Type-1 hypervisor (e.g., VMware ESXi, KVM) which runs directly on hardware. Each VM gets virtualised vCPU, RAM, disk, and network from the host.
- **Type-1 vs Type-2 hypervisor?** — Type-1 runs on bare metal (KVM, ESXi); Type-2 runs on an OS (VirtualBox, VMware Workstation).
- **Why 2 vCPU / 4 GB / 20 GB?** — Minimum comfortable resource set for a desktop Ubuntu VM on a student laptop.
- **NAT vs Bridged?** — NAT = VM shares host IP (outbound only); Bridged = VM gets its own LAN IP.
- **What is a VDI?** — VirtualBox's virtual disk format; *dynamically allocated* grows on demand.
- **What do Guest Additions do?** — Better display drivers, shared folders, clipboard, seamless mouse.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.

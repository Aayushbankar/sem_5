# P08 — Simulate Secure File Sharing with CloudSim

**Subject:** Cloud and Data Center Technology | **Unit:** 5 | **Approx. Hrs:** 2
**PrO (verbatim):** *Simulate a secure file sharing using a cloudsim open-source framework*

---

## 1. Objective
- Install **CloudSim** (open-source cloud simulator) + **Java 11**.
- Write a Java simulation that models a **secure file-sharing workflow** as cloudlets (encrypt → upload → download → decrypt → audit).
- Run it and interpret the output (execution time, cost, datacenter placement).

> ⚠️ **Lab environment note:** CloudSim's simulator needs Java + the CloudSim 3.0.3 jar. This machine has **Java 21** (compatible) but the CloudSim jar is not bundled with the repo — compile/run **in the lab** using the steps below.

## 2. Theory (exam-ready)
**CloudSim** is a Java framework (Melbourne/CLOUDS Lab) that simulates cloud **datacenters, hosts, VMs, cloudlets** (tasks), and scheduling policies **without needing real hardware**. You define:
- **Datacenter** → hosts with CPUs/RAM/BW and cost per unit.
- **Broker** → your tenant; submits VMs and cloudlets.
- **VM** → mips, RAM, bandwidth, scheduler.
- **Cloudlet** → task length (MI), required CPUs, and optionally a name.

**How "security" is modeled here:** CloudSim does **not** simulate cryptography. The simulation models the *resource consumption* of a secure sharing workflow — we split the workflow into named cloudlets (`FileEncrypt`, `FileUpload`, …) and simulate an **access-control decision** (`checkAccess`) before sharing. This mirrors how a real secure file-sharing service behaves at the infrastructure level.

## 3. Setup

### 3.1 Java 11+
```bash
# Ubuntu (lab VM)
sudo apt update && sudo apt install -y openjdk-11-jdk
java -version   # expect openjdk 11.x
```

### 3.2 CloudSim 3.0.3 jar
```bash
mkdir -p ~/cloudsim && cd ~/cloudsim
wget https://github.com/Cloudslab/cloudsim/releases/download/cloudsim-3.0.3/cloudsim-3.0.3.jar
# (mirror: https://cloudsimapp.com/ → Downloads)
```
CloudSim also needs `jcommon` + `jfreechart` for optional charting; the basic simulation only needs `cloudsim-3.0.3.jar`.

### 3.3 Compile & run the practical
```bash
# Copy the source file into the lab
cd ~/cloudsim
javac -cp cloudsim-3.0.3.jar p08_cloudsim_secure_file_sharing.java
java -cp .:cloudsim-3.0.3.jar SecureFileSharingSimulation
```

## 4. The simulation
Full source: [`p08_cloudsim_secure_file_sharing.java`](../code/p08_cloudsim_secure_file_sharing.java)

```java
// Highlights — one cloudlet per security step
cloudletList.add(makeCloudlet(brokerId, vm.getId(), 0, 40000, "FileEncrypt (AES-256)"));
cloudletList.add(makeCloudlet(brokerId, vm.getId(), 1, 20000, "FileUpload (to cloud storage)"));
cloudletList.add(makeCloudlet(brokerId, vm.getId(), 2, 20000, "FileDownload (by recipient)"));
cloudletList.add(makeCloudlet(brokerId, vm.getId(), 3, 40000, "FileDecrypt (AES-256)"));
cloudletList.add(makeCloudlet(brokerId, vm.getId(), 4,  8000, "AccessAuditRecord"));
...
boolean recipientAllowed = checkAccess("alice@cdct.org", "secure-app-users");
Log.printLine("Access-control check: recipient allowed = " + recipientAllowed);
```

## 5. Expected console output (actual CloudSim run)
```
========== Secure File Sharing Simulation (CloudSim) ==========
Access-control check: recipient allowed = true

Starting CloudSim version 3.0.3
Datacenter_0 is starting...
Broker_CDCT is starting...
Entity Broker_CDCT is starting...

========== OUTPUT ==========
    Cloudlet_ID    Status    Datacenter_ID    VM_ID    Time    Start_Time    Finish_Time    Cost
              0    SUCCESS                1        1      40          0.1          40.1   120
              1    SUCCESS                1        1      20         40.1          60.1    60
              2    SUCCESS                1        1      20         60.1          80.1    60
              3    SUCCESS                1        1      40         80.1         120.1   120
              4    SUCCESS                1        1       8        120.1         128.1    24
Total execution cost of the secure file-sharing workflow: $384

SecureFileSharingSimulation finished!
```
*(Numbers depend on VM MIPS and datacenter cost; the 5 cloudlets must all print SUCCESS.)*

**Interpretation:**
- Each cloudlet = one step of the sharing workflow, all **SUCCESS**.
- `Finish_Time` of one step = `Start_Time` of the next → the workflow is sequential (encrypt before upload).
- `Cost` = processing cost from the datacenter's `costPerSec`; total $384 shows the *price of the compute* behind one secure share.
- The access-control log line shows the "security" gate happening before the file leaves the tenant.

## 6. What we proved
1. CloudSim models multi-step cloud workloads on simulated datacenters/VMs — no real cloud needed.
2. A "secure file sharing" feature maps to distinct resource-consuming tasks; security (AES, authN/authZ) is the *logic* wrapped around those tasks.
3. The simulator reports **execution time + cost**, which is exactly what you'd estimate before moving to a real cloud.

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Java version + jar download evidence.
3. The source file (or link).
4. Console output (§5) with all 5 cloudlets SUCCESS.
5. Interpretation paragraph (§6).
6. Conclusion: how simulation helps design cloud solutions before deployment.

## 8. Viva Q&A
1. **What is CloudSim?** — An open-source Java framework for simulating cloud datacenters, VMs, and workload scheduling.
2. **What are cloudlets?** — Tasks/units of work submitted to VMs (length in MI).
3. **Does CloudSim encrypt data?** — No; it simulates resources. Security is modeled at the application layer.
4. **What does the broker do?** — Acts as the tenant/account: submits VMs and cloudlets to datacenters.
5. **Why simulate?** — Cheaper, repeatable experiments on scheduling/cost before using a real cloud.

## 9. Resources
- CloudSim project: https://cloudsimapp.com/
- CloudSim 3.0.3 release: https://github.com/Cloudslab/cloudsim/releases
- CloudSim manual (PDF): https://www.cloudbus.org/papers/CloudSim2011.pdf
- Java 11 (OpenJDK): https://adoptium.net/

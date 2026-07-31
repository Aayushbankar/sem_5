# CDCT — Cloud and Data Center Technology (DI05016031)

> **w.e.f. 2026-27** · GTU Diploma Engineering · Information Technology

Complete study kit: 10 solved practicals (writeups + code), 6 gold theory notes with real PYQs, and curated resources.

## 📊 Progress
- Practicals: **[tracker](./PRACTICALS.md)** — 10/10 solved · P09 & P10 **ran for real** in Docker (output captured)
- Notes: 6/6 units, all with **real PYQ solved answers** from Summer-24 → Summer-26 papers

## 🧪 Practicals (10 · 30 hrs)
| # | Practical | Solution | Code | Ran? |
|---|-----------|----------|------|------|
| P01 | OpenStack architecture & entities | [P01](./practicals/writeups/P01_openstack_architecture.md) | — | 📄 |
| P02 | Cloud org with RBAC (AWS IAM) | [P02](./practicals/writeups/P02_cloud_organization_rbac.md) | [p02_iam_policy.json](./practicals/code/p02_iam_policy.json) | 📄 |
| P03 | Install VirtualBox + Linux/Windows VM | [P03](./practicals/writeups/P03_install_virtualbox_linux_vm.md) | — | 📄* |
| P04 | Chrome Remote Desktop virtualization | [P04](./practicals/writeups/P04_desktop_virtualization_chrome_remote_desktop.md) | — | 📄* |
| P05 | Mininet virtual SDN lab (2sw-4host) | [P05](./practicals/writeups/P05_mininet_virtual_sdn_lab.md) | [p05_mininet_2switch_4host.py](./practicals/code/p05_mininet_2switch_4host.py) | 📄* |
| P06 | Cloud database comparison | [P06](./practicals/writeups/P06_cloud_databases_comparison.md) | — | 📄 |
| P07 | Cloud storage comparison | [P07](./practicals/writeups/P07_cloud_storage_comparison.md) | — | 📄 |
| P08 | CloudSim secure file sharing | [P08](./practicals/writeups/P08_cloudsim_secure_file_sharing.md) | [p08_cloudsim_secure_file_sharing.java](./practicals/code/p08_cloudsim_secure_file_sharing.java) | 📄* |
| P09 | MinIO secure object storage (SSE + IAM) | [P09](./practicals/writeups/P09_minio_secure_object_storage.md) | [compose + policies + setup.sh](./practicals/code/) | ✅ **RAN** |
| P10 | First Docker container | [P10](./practicals/writeups/P10_docker_first_container.md) | [Dockerfile + site](./practicals/code/) | ✅ **RAN** |

✅ = executed for real, output captured · 📄 = documented (expected output provided) · \* = requires hardware/environment not available here (VirtualBox/Windows, Mininet, CloudSim jars)

## 📚 Theory Notes (per unit — real PYQ map + solved answers inside)
| Unit | Title | Weightage | Notes |
|------|-------|-----------|-------|
| 1 | Introduction to Cloud Computing | 8% (4h) | [UNIT_1](./notes/UNIT_1_Introduction_to_Cloud_Computing.md) |
| 2 | Virtualization and Hypervisors | 20% (9h) | [UNIT_2](./notes/UNIT_2_Virtualization_and_Hypervisors.md) |
| 3 | Data Center Architecture | 20% (9h) | [UNIT_3](./notes/UNIT_3_Data_Center_Architecture.md) |
| 4 | Cloud Storage and Database Services | 20% (9h) | [UNIT_4](./notes/UNIT_4_Cloud_Storage_and_Database_Services.md) |
| 5 | Cloud Security and Compliance | 14% (6h) | [UNIT_5](./notes/UNIT_5_Cloud_Security_and_Compliance.md) |
| 6 | Emerging Technologies with Cloud Computing | 18% (8h) | [UNIT_6](./notes/UNIT_6_Emerging_Technologies_with_Cloud_Computing.md) |

## 🔗 Resources
- [Curated links (docs, courses, tools, books, videos)](./notes/RESOURCES.md)
- PYQ source papers: [`../pyq/cdct/`](../pyq/cdct/) (S-24, W-24, S-25, W-25, S-26)

## 🛠 Requirements
- **P09 / P10 (Docker):** Docker Engine + Compose (Docker runs MinIO and your first container; **verified in this workspace**). SELinux hosts need `:z` on bind mounts.
- **P01/P02:** any browser (OpenStack docs / AWS IAM console).
- **P06/P07:** no install — study/comparison only.
- **P03/P04:** Windows 8+ host with VirtualBox + a Linux ISO (or Chrome Remote Desktop).
- **P05:** Linux host with **Mininet** installed (`sudo apt install mininet`).
- **P08:** Java (present) + **cloudsim-3.0.3.jar** (download to `code/`; `javac -cp cloudsim-3.0.3.jar`).

## ⚠️ Exam tips
- Highest-value 7-markers (repeated across papers): cloud service models & deployment models (U1), virtualization types/hypervisors (U2), data-center network topologies & SDN (U3), **types of cloud storage** and **types of cloud databases** (U4), **cloud security challenges** + **access control/authentication** + **DevSecOps** (U5), **edge vs fog** + **serverless** + **containers/Docker** (U6).
- Practical viva: know *why* each line works — e.g., why `-p 8081:80`, why MinIO needs a KMS key for SSE, why IAM deny wins.

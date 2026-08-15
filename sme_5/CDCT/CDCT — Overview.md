---
subject: CDCT
full_name: Cloud and Data Center Technology
code: DI05016031
units: 6
practicals: 10
status: not-started
tags: [subject/cdct, dashboard]
---
# ☁️ Cloud and Data Center Technology

> **DI05016031** · w.e.f. 2026-27 · GTU Diploma IT · Sem 5

---

## 📚 Theory Units

| Unit | Note | Status |
|---|---|---|
| Unit 1 | [[Unit 1 — Introduction to Cloud Computing]] | ⬜ |
| Unit 2 | [[Unit 2 — Virtualization and Hypervisors]] | ⬜ |
| Unit 3 | [[Unit 3 — Data Center Architecture]] | ⬜ |
| Unit 4 | [[Unit 4 — Cloud Storage and Database Services]] | ⬜ |
| Unit 5 | [[Unit 5 — Cloud Security and Compliance]] | ⬜ |
| Unit 6 | [[Unit 6 — Emerging Technologies with Cloud Computing]] | ⬜ |

---

## 🧪 Practicals (10)

| # | Practical | Status |
|---|---|---|
| P01 | [[P01 — Openstack Architecture]] | ⬜ |
| P02 | [[P02 — Cloud Organization Rbac]] | ⬜ |
| P03 | [[P03 — Install Virtualbox Linux Vm]] | ⬜ |
| P04 | [[P04 — Desktop Virtualization Chrome Remote Desktop]] | ⬜ |
| P05 | [[P05 — Mininet Virtual Sdn Lab]] | ⬜ |
| P06 | [[P06 — Cloud Databases Comparison]] | ⬜ |
| P07 | [[P07 — Cloud Storage Comparison]] | ⬜ |
| P08 | [[P08 — Cloudsim Secure File Sharing]] | ⬜ |
| P09 | [[P09 — Minio Secure Object Storage]] | ⬜ |
| P10 | [[P10 — Docker First Container]] | ⬜ |

---

## 💻 Code Files

- [[p02_iam_policy.json]]
- [[p05_mininet_2switch_4host.py]]
- [[p08_cloudsim_secure_file_sharing.java]]
- [[p09_admin_policy.json]]
- [[p09_bucket_policy.json]]
- [[p09_docker-compose.yml]]
- [[p09_readonly_policy.json]]
- [[p09_setup.sh]]
- [[p10_Dockerfile]]

---

## 🔗 Quick Links

- [[CDCT Resources|🔗 Resources]]
- [[CDCT Practical Tracker|📋 Practical Tracker]]
- [[DI05016031-CDCT.pdf|📄 Syllabus (PDF)]]

---

## ⚠️ Exam Tips

- Highest-value 7-markers (repeated across papers): cloud service models & deployment models (U1), virtualization types/hypervisors (U2), data-center network topologies & SDN (U3), **types of cloud storage** and **types of cloud databases** (U4), **cloud security challenges** + **access control/authentication** + **DevSecOps** (U5), **edge vs fog** + **serverless** + **containers/Docker** (U6).
- Practical viva: know *why* each line works — e.g., why `-p 8081:80`, why MinIO needs a KMS key for SSE, why IAM deny wins.

---

## 🛠️ Requirements

- **P09 / P10 (Docker):** Docker Engine + Compose (Docker runs MinIO and your first container; **verified in this workspace**). SELinux hosts need `:z` on bind mounts.
- **P01/P02:** any browser (OpenStack docs / AWS IAM console).
- **P06/P07:** no install — study/comparison only.
- **P03/P04:** Windows 8+ host with VirtualBox + a Linux ISO (or Chrome Remote Desktop).
- **P05:** Linux host with **Mininet** installed (`sudo apt install mininet`).
- **P08:** Java (present) + **cloudsim-3.0.3.jar** (download to `code/`; `javac -cp cloudsim-3.0.3.jar`).

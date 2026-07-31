# Practical Tracker — Cloud and Data Center Technology

Suggested Course Practical List from GTU syllabus (DI05016031, w.e.f. 2026-27).

**Progress: 10 / 10 practicals solved · 2 ran for real (P09, P10) · 8 documented · 30 / 30 hrs**

| Sr. | Practical Outcome (PrO) | Unit | Hrs | Status | Solution | Code | Remarks |
|-----|-------------------------|------|-----|--------|----------|------|---------|
| 1 | Sketch and analyze the architecture of Openstack/ Eucalyptus/ OpenNebula/ KVM and identify entities | I | 2 | [x] | [P01](./practicals/writeups/P01_openstack_architecture.md) | — | Documented (mermaid diagrams + comparison tables) |
| 2 | Create a Cloud Organization with Role-based access control | I | 4 | [x] | [P02](./practicals/writeups/P02_cloud_organization_rbac.md) | [p02_iam_policy.json](./practicals/code/p02_iam_policy.json) | Documented (AWS IAM + permission matrix) |
| 3 | Install VirtualBox with Linux/Windows VM on Windows 8+ | II | 2 | [x] | [P03](./practicals/writeups/P03_install_virtualbox_linux_vm.md) | — | Documented — requires VirtualBox + Windows host |
| 4 | Create desktop Virtualization using Chrome Remote Desktop | II | 4 | [x] | [P04](./practicals/writeups/P04_desktop_virtualization_chrome_remote_desktop.md) | — | Documented — requires Google account + hosts |
| 5 | Set up a virtual SDN lab using Mininet | III | 4 | [x] | [P05](./practicals/writeups/P05_mininet_virtual_sdn_lab.md) | [p05_mininet_2switch_4host.py](./practicals/code/p05_mininet_2switch_4host.py) | Documented — requires Mininet (`sudo apt install mininet`) |
| 6 | Study & compare cloud databases (RDS, Cloud SQL, Azure SQL, Db2, Firebase, Atlas, Oracle ATP) | IV | 4 | [x] | [P06](./practicals/writeups/P06_cloud_databases_comparison.md) | — | Documented (7-DB comparison + decision guide) |
| 7 | Study & compare cloud storage (S3, GCS, Azure Blob, IBM COS) | IV | 2 | [x] | [P07](./practicals/writeups/P07_cloud_storage_comparison.md) | — | Documented (durability/tiers/scaling/pricing) |
| 8 | Simulate secure file sharing using CloudSim | V | 2 | [x] | [P08](./practicals/writeups/P08_cloudsim_secure_file_sharing.md) | [p08_cloudsim_secure_file_sharing.java](./practicals/code/p08_cloudsim_secure_file_sharing.java) | Documented — requires cloudsim-3.0.3.jar (`javac -cp cloudsim-3.0.3.jar`) |
| 9 | Implement secure object storage with access control and encryption | V | 2 | [x] | [P09](./practicals/writeups/P09_minio_secure_object_storage.md) | [compose + policies + setup.sh](./practicals/code/p09_docker-compose.yml) | ✅ **RAN for real** — MinIO + SSE-S3 + IAM users |
| 10 | Create and execute your first container using Docker | VI | 4 | [x] | [P10](./practicals/writeups/P10_docker_first_container.md) | [p10_Dockerfile](./practicals/code/p10_Dockerfile) + [site](./practicals/code/p10_site/index.html) | ✅ **RAN for real** — build → run → HTTP 200 |
| | **Total** | | **30** | **10/10** | | | |

> Note: More Practical Exercises can be designed and offered by the respective course teacher to develop the industry relevant skills/outcomes to match the COs. The above table is only a suggestive list.
>
> **RAN for real** = executed in this workspace with output captured (`/tmp/opencode/p09_output.txt`, `/tmp/opencode/p10_output.txt`). All others include the full documented procedure + expected output blocks; they need the environment noted in Remarks.

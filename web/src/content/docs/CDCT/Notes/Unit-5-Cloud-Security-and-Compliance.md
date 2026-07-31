---
title: "Unit 5 — Cloud Security and Compliance"
sidebar:
  order: 5
---

# UNIT 5 — Cloud Security and Compliance 🔐

> **Cloud and Data Center Technology (DI05016031)** · **6 hrs · 14% weightage**
> **Covers syllabus sections:** 5.1 Security in the Cloud (challenges, IAM, access control & authentication) · 5.2 Data Security in Cloud (technologies) · 5.3 Securing Private & Public Cloud Architecture (SLA metrics, DevSecOps)
> **Related practicals:** [P02](./P02%20—%20Cloud%20Organization%20Rbac.md) (IAM RBAC), [P09](./P09%20—%20Minio%20Secure%20Object%20Storage.md) (encryption + access control), [P08](./P08%20—%20Cloudsim%20Secure%20File%20Sharing.md) (secure file sharing)

---

## 🧭 Chapter Roadmap

Unit 5 (14%) is the **security** chapter. Every single paper asks a security question — the three repeated killers are **cloud security challenges (7m)**, **access control and authentication (7m)**, and **DevSecOps (7m)**. IAM, data-security technologies and SLA metrics round it out. P02 (IAM policy) and P09 (encryption + IAM users in MinIO) give you hands-on anchors.

| # | Concept | Exam importance | Related |
|---|---------|-----------------|---------|
| 5.1 | Cloud security challenges | ★★★★★ | — |
| 5.1 | Identity & Access Management (IAM) | ★★★★★ | P02, P09 |
| 5.1 | Access control vs authentication | ★★★★★ | P02 |
| 5.2 | Data security technologies | ★★★★★ | P08, P09 |
| 5.3 | SLA metrics | ★★★★ | — |
| 5.3 | DevSecOps | ★★★★★ | P10 |

### Learning outcomes — after this unit you can:
1. List and explain the **cloud security challenges**.
2. Explain **identity and access management** and distinguish **authentication** from **access control**.
3. Explain the **technologies for data security** (encryption, masking, DLP, key management…).
4. Explain how to **secure private and public cloud architectures**.
5. Define **SLAs and their metrics**.
6. Explain **DevSecOps** and how it differs from plain DevOps.

---

## 5.1 Security in the Cloud ⭐⭐

### 5.1.1 Cloud security challenges (s_24/w_25 Q.5c, w_24 Q.5a, s_25 Q.2a) ⭐⭐
**Cloud security** = the protection of data, applications and infrastructure in a cloud environment (confidentiality, integrity, availability — **CIA**) against threats, using provider + customer controls. Main challenges:

| # | Challenge | What it means |
|---|---|---|
| 1 | **Data breaches / leaks** | Unauthorized access to stored or transmitted data (misconfigured buckets, leaked keys) |
| 2 | **Misconfiguration** | Open buckets, over-permissive IAM roles, exposed ports |
| 3 | **Insecure APIs / interfaces** | The management consoles and REST APIs are attack surfaces |
| 4 | **Account hijacking** | Stolen credentials → attacker controls your cloud account |
| 5 | **Insider threats** | Employees/partners with legitimate access misuse it |
| 6 | **Shared responsibility confusion** | Customer assumes the provider secures *their* apps/data (it doesn't) |
| 7 | **DDoS / availability attacks** | Flooding services → downtime (violates Availability) |
| 8 | **Data loss** | Accidental deletion, weak backup/DR |
| 9 | **Limited visibility & compliance** | Hard to see/audit everything; regulatory rules must still be met |
| 10 | **Multi-tenancy risk** | Weak isolation lets one tenant affect another |

```mermaid
mindmap
  root((Cloud security<br/>challenges))
    Data risks
      Breaches
      Data loss
      Misconfiguration
    Access risks
      Account hijack
      Insider threats
      Over-permissive IAM
    Platform risks
      Insecure APIs
      DDoS
      Multi-tenancy
    Governance risks
      Compliance
      Shared-responsibility confusion
      Visibility
```

### 5.1.2 Identity and Access Management (IAM) (s_24 Q.5a-alt, s_25 Q.2c, w_24 Q.5b) ⭐⭐
**IAM** = the discipline of managing **who** (identity) is allowed to do **what** (authorization) **where**. Components: **users, groups, roles, permissions/policies, and MFA**. In AWS (P02): you create an **IAM user**, put it in a **group**, attach a **policy** (JSON allow/deny statements), and enforce **least privilege**. Role of IAM: central authentication, fine-grained access control, auditability, and meeting compliance. → hands-on in [P02](./P02%20—%20Cloud%20Organization%20Rbac.md).

### 5.1.3 Authentication vs Access Control (s_24 Q.5a, s_25 Q.2a-alt, w_25 Q.5c-alt, s_26 Q.5c) ⭐⭐
- **Authentication ("who are you?")** — verifying identity via **something you know** (password/PIN), **have** (OTP, smart card), **are** (biometrics), or **do** (behavior). Multi-factor = combine two+.
- **Access control ("what may you do?")** — deciding *after* identity is proven whether the user may perform an action. Models: **MAC, DAC, RBAC, ABAC**.

**Justification that they are different (s_24 Q.5a):** proving "I am Ramesh" (authentication) does not grant permission to touch everything — Ramesh may *see* a document but not *delete* it. Authentication answers identity; access control answers authorization. A system that authenticates but never authorizes is as insecure as one that authorizes without authenticating — you need both layers (defense in depth).

```mermaid
flowchart TD
    subgraph ClientReq["Incoming Request Tier"]
        User["User / App Client"]
        Creds["Credentials Payload<br/>(Username/Pass + TOTP MFA Token)"]
        User --> Creds
    end

    subgraph AuthPhase["Phase 1: Authentication Engine ('Who Are You?')"]
        IdP["Identity Provider / Auth Server (OAuth2 / OIDC / Keystone)"]
        MFA["Multi-Factor Authentication (MFA Validator)"]
        TokenGen["Cryptographic JWT Token Generator"]
        Creds --> IdP --> MFA --> TokenGen
    end

    subgraph AccessPhase["Phase 2: Access Control & Authorization ('What May You Do?')"]
        JWTToken["Signed Bearer JWT Token"]
        IAMEngine["IAM Policy Evaluation Engine"]
        
        subgraph PolicyModels["Authorization Policy Rules"]
            RBAC["Role-Based Access Control (RBAC)"]
            ABAC["Attribute-Based Access Control (ABAC)"]
            DenyCheck["Explicit Deny Priority Evaluation"]
        end
        
        TokenGen --> JWTToken --> IAMEngine
        IAMEngine --- RBAC & ABAC & DenyCheck
    end

    subgraph DecisionTier["Execution & Audit Phase"]
        Allowed["ALLOW: Grant API Access to Resource"]
        Denied["DENY: 403 Forbidden Response"]
        SIEM["CloudTrail / SIEM Audit Logging"]
        
        IAMEngine -- "Policy Evaluates ALLOW" --> Allowed
        IAMEngine -- "Explicit Deny / Default Deny" --> Denied
        Allowed & Denied --> SIEM
    end
```

## 5.2 Data Security in Cloud ⭐⭐
### 5.2.1 Technologies for data security (w_24 Q.5c, s_25 Q.5b-alt) ⭐⭐
1. **Encryption** — at rest (AES-256 SSE) and in transit (TLS/SSL): ciphertext is useless without the key. (P09: MinIO SSE-S3 with AES-256; P08: encrypt/decrypt in CloudSim.)
2. **Key management (KMS)** — central storage/rotation of encryption keys (AWS KMS, MinIO KMS).
3. **Identity & Access Management** — least-privilege policies (P02).
4. **Tokenization & data masking** — replace/obscure sensitive fields (credit-card numbers, PII).
5. **DLP (Data Loss Prevention)** — detect & block sensitive data leaving the environment.
6. **Firewalls, IDS/IPS, WAF** — network perimeter + app-layer filtering.
7. **Audit & monitoring** — CloudTrail/CloudWatch-style logging, alerts, SIEM.
8. **Backup & DR** — versioning, snapshots, cross-region copies.

## 5.3 Securing Private and Public Cloud Architecture ⭐
### 5.3.1 Metrics for SLAs (w_25 Q.5a, s_25 Q.5b) ⭐
**SLA (Service Level Agreement)** = the formal contract between provider and customer defining the guaranteed **service level** and the **penalty** when it isn't met. Metrics (measurable, SLO-based):
- **Availability/uptime %** — e.g., 99.9% ≈ 8.77 hrs downtime/yr
- **RTO / RPO** — Recovery Time/Point Objective (DR)
- **Latency & throughput** — response time, requests/sec
- **Error rate** — % of failed requests
- **Durability / data-loss rate**
- **Support response time** — ticket SLA
- **Monthly/annual reporting & credits** — how violations are compensated

### 5.3.2 DevSecOps (s_24/s_25/s_26 Q.5c-alt, 7m) ⭐⭐
**DevSecOps (Development, Security, Operations)** = baking **security into every stage** of the DevOps pipeline ("shift left") instead of bolting it on at the end.
- **In DevSecOps** security is everyone's job: code scanning (SAST) at commit, dependency/image scanning at build (Docker images!), secret scanning, IaC policy-as-code, and continuous compliance in CI/CD.
- **In traditional DevOps** security is a final gate → late, slow, and costly fixes.

```mermaid
flowchart TD
    subgraph DevPhase["(1) Plan & Code (Shift-Left)"]
        Dev["Software Developer"]
        IDE["IDE Plugin Security (SonarLint)"]
        PreCommit["Git Pre-Commit Hook (Secret Scanning / TruffleHog)"]
        Dev --> IDE --> PreCommit
    end

    subgraph BuildPhase["(2) Build & Image Hygiene"]
        CI["CI/CD Runner (GitHub Actions / GitLab CI)"]
        SAST["Static Application Security Testing (SAST / Semgrep)"]
        SCA["Software Composition Analysis (Dependency Check)"]
        ContainerScan["Container Image Vulnerability Scanner (Trivy / Clair - P10)"]
        PreCommit --> CI --> SAST & SCA & ContainerScan
    end

    subgraph DeployPhase["(3) Staging & Deployment"]
        IaC_Gate["IaC Policy-as-Code Gate (OPA / Checkov)"]
        DAST["Dynamic Application Security Testing (DAST / ZAP)"]
        Sign["Image Cryptographic Signing (Cosign / Notary)"]
        ContainerScan --> IaC_Gate --> DAST --> Sign
    end

    subgraph RuntimePhase["(4) Production Runtime & Monitoring"]
        K8s["Kubernetes Production Cluster"]
        eBPF["Runtime Threat Detection (Falco / eBPF)"]
        SIEM_Log["SIEM & CloudTrail Audit Logging"]
        Sign --> K8s --> eBPF --> SIEM_Log
    end

    SIEM_Log -. "Continuous Feedback & Vulnerability Remediation" .-> Dev
```

> [!warning] DevSecOps mantra
> "Every pipeline step is a security checkpoint — shift security **left**, not to the end." This pairs with P10 (Docker image hygiene: small images, no secrets in image, pinned base images).

---

## 🧠 Deep-Dive Topics

### Deep Dive A: "Justify: authentication and access control are two different aspects" (s_24 Q.5a)
Authentication verifies identity; access control limits action. Two attack stories prove the difference: (1) **weak authentication + perfect authorization** — someone steals Ramesh's password, so the system believes he *is* Ramesh, and the (correct) access rules then let the attacker do everything Ramesh can → MFA should stop this; (2) **strong authentication + weak authorization** — every user authenticates with a biometric, but a single over-broad IAM policy lets any employee read the salary file → least-privilege RBAC should stop this. Security needs both layers because each protects against a different failure.

### Deep Dive B: Hypervisor security (s_26 Q.2b — cross-link to Unit 2)
Because all VMs on a host share the hypervisor, a **hypervisor compromise = compromise of every guest**. Security aspects: keep hypervisor patched & minimal (attack surface reduction), restrict management interfaces, isolate guests (micro-segmentation), protect against **VM escape** (a guest breaking out to the host), secure live migration traffic, and monitor for "same-host co-location" risks in multi-tenant clouds.

### Deep Dive C: Shared Responsibility Model
| Layer | Provider (public cloud) | Customer |
|---|---|---|
| Physical security, hardware, hypervisor | ✅ | |
| OS, patches, network config inside VM | | ✅ |
| Data, access, IAM policies | | ✅ |
| Managed services (S3, RDS) | Security **of** service | Security **in** service (data, keys, policies) |

Misunderstanding this boundary is itself a listed cloud security challenge — and the single most common cause of breaches.

### Deep Dive D: SLA arithmetic examiners love
99.9% uptime = **8 h 45 min** downtime/year; 99.99% = **52.6 min**/year; 99.999% ("five nines") = **5.3 min**/year. A 3-mark question often asks to compute or compare these.

---

## 🚀 Beyond the Textbook

1. **MinIO's `mc admin policy attach` is IAM-in-miniature** — the same "user → policy → resource" model as AWS IAM; P09 proves it (read-only user denied PUT, admin user allowed).
2. **P08 (CloudSim) shows encryption as application code** — real clouds do it twice: provider SSE + customer KMS keys (envelope encryption).
3. **Zero Trust is the modern slogan** — "never trust, always verify": every request authenticated/authorized regardless of network (matches 5.1.3).
4. **DevSecOps tooling is what the exam won't tell you** — SAST (SonarQube), SCA (Dependabot), container scanning (Trivy), IaC scanners (Checkov), CI (GitHub Actions/Jenkins).
5. **Security is a cost center that can save money** — compliance failures (e.g., data protection law fines) dwarf the cost of prevention; this is the "benefits of cloud security" answer for s_26 Q.5a.

---

## 📝 PYQ Map — UNIT 5 (all available papers)

| Paper | Q. | Topic | Marks |
|---|---|---|---|
| **Summer 2024** | Q.5(a) | Justify: authentication and access control are different aspects of security | 3 |
| | Q.5(c) | Explain cloud security challenges | 7 |
| | Q.5(a)-alt | Role of identity access management | 3 |
| | Q.5(c)-alt | Explain DevSecOps (Development Security and Operations) | 7 |
| **Winter 2024** | Q.5(a) | Define cloud security; list challenges for cloud security | 3 |
| | Q.5(b) | Short note on Identity Management and Access Control | 4 |
| | Q.5(c) | Technologies used for data security in cloud | 7 |
| **Summer 2025** | Q.2(a) | Which are cloud security challenges? | 3 |
| | Q.2(c) | Explain Identity and Access Management in detail | 7 |
| | Q.2(a)-alt | Need for access control and authentication in cloud | 3 |
| | Q.2(c)-alt | Explain DevSecOps in detail | 7 |
| | Q.5(b)-alt | What is Data Security in Cloud? Explain in detail | 4 |
| **Winter 2025** | Q.5(a) | Metrics for Service Level Agreements (SLAs) | 3 |
| | Q.5(c) | Explain cloud security challenges | 7 |
| | Q.5(a)-alt | Explain securing private and public cloud architecture | 3 |
| | Q.5(c)-alt | Access control and authentication in cloud computing | 7 |
| **Summer 2026** | Q.2(b) | Security aspects involved with using a hypervisor | 4 |
| | Q.5(a) | List the benefits of cloud security | 3 |
| | Q.5(c) | Access control and authentication in cloud computing | 7 |
| | Q.5(a)-alt | List the cloud security challenges | 3 |
| | Q.5(c)-alt | Explain DevSecOps (Development Security and Operations) | 7 |

### ✅ Solved PYQ answers (UNIT 5)

**Q. (w_24 Q.5a, 3 marks) — Define cloud security. List challenges.**
> Cloud security is the set of policies, controls and technologies that protect **data, applications and infrastructure** in the cloud — preserving **confidentiality, integrity and availability (CIA)** across provider and customer layers. Challenges include: data breaches, misconfigured storage/security, insecure APIs, account hijacking, insider threats, **shared-responsibility confusion**, DDoS/availability attacks, data loss, weak multi-tenant isolation, and compliance/visibility limits.

**Q. (s_24 Q.5a, 3 marks) — Justify: authentication and access control are two different aspects of security.**
> Authentication answers *"who are you?"* (verify identity by password, OTP, biometrics), while access control answers *"what may you do?"* (grant/deny actions on resources, via RBAC/ABAC policies). Proof they differ: a user can authenticate successfully yet still be denied every action — proving identity does not imply permission. Likewise, a system that grants permissions without verifying identity lets anyone impersonate. Both are independent layers: authentication fails are stopped by strong MFA; authorization failures are stopped by least-privilege IAM. Defense-in-depth requires both.

**Q. (s_25 Q.2c, 7 marks) — Explain Identity and Access Management in detail.**
> IAM is the framework that manages **identities** (who you are) and their **permissions** (what they may do) across cloud resources. **Components:** users (a person/app), groups (collections of users sharing permissions), roles (permission sets assumed by users/services, e.g., EC2→S3), and **policies** (JSON documents with Allow/Deny actions on resources, following **least privilege**). **Working:** a request is authenticated, then the IAM engine evaluates all policies against the action → Allow or Deny (explicit Deny always wins). **Services:** AWS IAM, Azure AD/Entra ID, OpenStack Keystone. **Role of IAM (s_24 Q.5a-alt):** centralized authentication, fine-grained access control, MFA, audit trail and compliance. **Hands-on:** [P02](./P02%20—%20Cloud%20Organization%20Rbac.md) builds an IAM policy allowing EC2 control + S3 read but denying IAM changes; [P09](./P09%20—%20Minio%20Secure%20Object%20Storage.md) does the same with `mc admin policy` on MinIO.

**Q. (w_24 Q.5c, 7 marks) — Explain the technologies used for data security in cloud.**
> (1) **Encryption:** data at rest (AES-256, e.g., S3 SSE-S3 — done in P09) and data in transit (TLS/SSL). (2) **Key management (KMS):** centralized creation, rotation and protection of keys. (3) **IAM / access control:** least-privilege policies deciding who reads/writes (P02). (4) **Tokenization and masking:** replace sensitive values (PII, card numbers) with tokens. (5) **DLP:** detect/prevent sensitive data from leaving the cloud. (6) **Network security:** firewalls, IDS/IPS, WAFs, VPC isolation. (7) **Audit & monitoring:** logs (CloudTrail), metrics, SIEM alerts. (8) **Backup & DR:** snapshots, versioning, cross-region replication. Layered together these give **defense in depth**: even if one control fails, the others still protect the data.

**Q. (s_25 Q.5b, 4 marks / w_25 Q.5a, 3 marks) — SLA: full form, explanation and metrics.**
> **SLA = Service Level Agreement** — the contract between provider and customer stating guaranteed service levels and the penalties if they're missed. It is backed by measurable **SLOs**. **Key metrics:** availability/uptime % (99.9% ≈ 8 h 45 m down/year), **latency and throughput**, **error rate**, **durability** (11 nines), **RTO/RPO** for disaster recovery, support response time, and reporting/credit mechanism for breaches. SLAs let customers *prove* and *price* quality, e.g., "99.99% availability or you get service credits."

**Q. (w_25 Q.5a-alt, 3 marks) — Explain securing private and public cloud architecture.**
> **Public cloud** is secured via the **shared responsibility model**: provider protects the physical platform (hardware, hypervisor, managed services), while the customer secures their part — IAM/MFA, VPC isolation/firewalls, encryption, data policies, monitoring and compliance audits. **Private cloud** (on-premise) has a *single* owner responsible for *everything* — physical security, hypervisors, network, OS, apps — but benefits from full control. **Best practice for both:** defense in depth — network security (firewalls, VPN, micro-segmentation), access control (IAM + RBAC + MFA), data protection (encryption at rest/in transit, DLP), continuous monitoring/auditing, and IaC-managed security rules.

**Q. (s_24 Q.5c-alt, 7 marks) — Explain DevSecOps.**
> DevSecOps = **Development + Security + Operations**: integrating security into every stage of the software delivery pipeline — *"shifting security left"* — rather than a final check. **How it works:** at *commit*, static code analysis (SAST) and secret scanning; at *build*, dependency and **container-image scanning** (Docker, P10); at *test*, dynamic scanning; at *deploy*, **policy-as-code** gates and IaC security scans (Terraform/CloudFormation); in *production*, runtime monitoring, audit and automated response — with feedback looping back to developers. **Benefits:** early detection (cheap to fix), continuous compliance, fewer breaches, faster releases without sacrificing security. **DevOps vs DevSecOps:** DevOps automates build→deploy; DevSecOps makes security a *continuous, automated* part of that flow instead of a manual end gate.

---

## ✍️ Practice Problems (self-test — answers hidden)

1. List any five cloud security challenges and give one real fix for each.
2. "Authentication and access control are different" — give two attack stories that prove it.
3. What is the shared responsibility model? Who is responsible for an S3 bucket's data policy?
4. Compute downtime per year for 99.9% vs 99.99% availability.
5. Name five data-security technologies and match each to a practical (P02/P08/P09 where possible).
6. What makes DevSecOps different from DevOps? Name one scan at each pipeline stage.
7. List four SLA metrics and explain what "99.99% availability" promises.

<details>
<summary>📌 Model solutions</summary>

1. Breach → encryption+least privilege; misconfig → policy-as-code scans; insecure APIs → MFA+API gateways; hijacking → MFA; insider → audit+DLP; DDoS → WAF/rate limiting; data loss → backups; multi-tenancy → strong isolation.
2. Stolen password = weak authentication beats perfect authorization; over-broad policy = strong authentication can't stop an authorized insider.
3. Provider: physical/hypervisor/platform. Customer: their data, access, IAM, in-VM config. For an S3 bucket: customer owns data + bucket policy.
4. 99.9% → 525.6 min ≈ 8.76 h; 99.99% → 52.56 min ≈ 0.88 h.
5. Encryption → P09 (SSE-S3) & P08 (encrypt cloudlet); IAM → P02 & P09 users/policies; KMS → P09 `MINIO_KMS_SECRET_KEY`; DLP/audit → P09 IAM deny logs; backup/DR → versioning in P09/P07.
6. DevSecOps shifts security left into every CI/CD stage; SAST at commit, image scan at build, policy-as-code at deploy, runtime monitoring in prod.
7. Availability %, latency, error rate, durability, RTO/RPO, support response. 99.99% = ~52.6 min max downtime per year, else penalty/credits.
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **Cloud security** | Protection of data/apps/infra in the cloud (CIA) |
| **CIA triad** | Confidentiality, Integrity, Availability |
| **Authentication** | Verifying identity ("who are you?") |
| **Access control** | Granting/denying actions ("what may you do?") |
| **IAM** | Identity & Access Management: users, groups, roles, policies |
| **Least privilege** | Grant only the minimum permissions needed |
| **RBAC / ABAC** | Role-based / attribute-based access control |
| **MFA** | Multi-factor authentication |
| **SSE / TLS** | Server-side encryption / transport encryption |
| **KMS** | Key Management Service |
| **DLP** | Data Loss Prevention |
| **Shared responsibility** | Provider vs customer security split |
| **SLA / SLO** | Service Level Agreement / Objective |
| **Availability %** | Uptime guarantee (99.9% ≈ 8.8 h/yr down) |
| **RTO / RPO** | Recovery Time / Recovery Point Objective |
| **DevSecOps** | Security integrated into DevOps ("shift left") |
| **SAST / SCA** | Static analysis / software composition (dependency) analysis |
| **Hypervisor escape** | Guest breaking out to host (Unit 2 link) |
| **Zero Trust** | Never trust, always verify |

---

## 🔗 Curated Resources (per concept)

**Cloud security challenges & model**
- AWS shared responsibility model: https://aws.amazon.com/compliance/shared-responsibility-model/
- OWASP Cloud Security / CSA top threats: https://cloudsecurityalliance.org/ (Top Threats series)

**IAM & access control**
- AWS IAM docs: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html
- OpenStack Keystone: https://docs.openstack.org/keystone/latest/

**Data security technologies**
- S3 SSE: https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html
- MinIO encryption & KMS: https://min.io/docs/minio/linux/operations/server-side-encryption.html

**SLA & DevSecOps**
- SLA metrics guide (Wikipedia): https://en.wikipedia.org/wiki/Service-level_agreement
- DevSecOps (Red Hat): https://www.redhat.com/en/topics/devops/what-is-devsecops

**Books (GTU syllabus)**
- Sosinsky, *Cloud Computing Bible* (Wiley) — security & compliance chapters
- Buyya et al., *Mastering Cloud Computing* — security chapter

**Videos (high yield)**
- *Cloud Security Challenges* — IBM Technology
- *IAM explained* — AWS / Stephane Maarek
- *DevSecOps explained* — IBM Technology

---

## 🎥 Video Study Guide (YouTube)

> Search keywords + trusted channels, in watching order.

### 🧑‍🎓 Step 0 — Pick your learning style
| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short explainers | 1 video per topic (5–10 min each) |
| 🛠️ **Builder** | doing it | Redo [P02](./P02%20—%20Cloud%20Organization%20Rbac.md) + [P09](./P09%20—%20Minio%20Secure%20Object%20Storage.md) |
| 🧠 **Deep Diver** | the "why" | Shared-responsibility + zero-trust deep dives |
| 🎓 **Academic** | exam marks | Master the three 7-mark monsters from the PYQ map |

### 🎬 Step 1 — Watch by topic
| Topic | YouTube search keywords | Best channels |
|---|---|---|
| Security challenges | `cloud security challenges` · `cloud security risks` | IBM Technology, Simplilearn |
| IAM | `aws iam explained` · `what is iam` | AWS, Stephane Maarek, TechWorld with Nana |
| Auth vs access | `authentication vs authorization` | IBM Technology, freeCodeCamp |
| Data security tech | `data security in cloud` · `encryption at rest in transit` | IBM Technology, AWS |
| SLA | `what is an sla` · `sla metrics 99.9` | IBM Technology |
| DevSecOps | `devsecops explained` · `shift left security` | IBM Technology, Nana |
| Hypervisor security | `hypervisor security vm escape` | SANS, IBM Technology |
| Revision | `cloud security unit 5 diploma` | Gate Smashers, Neso Academy |

### 🎬 Step 2 — Full playlists (Deep Divers & Academics)
1. *Cloud Security Fundamentals* — IBM Technology playlist.
2. *IAM & Security on AWS* — freeCodeCamp / ExamPro.
3. NPTEL *Cloud Computing* (security unit): https://archive.nptel.ac.in/courses/106/105/106105167/

### 🎬 Step 3 — Proof you got it (5 min)
- Recite 5 security challenges + one fix each in one minute.
- Explain the auth-vs-access-control difference using one attack story.
- Draw the DevSecOps pipeline and name a scan per stage.

---

*Next: [UNIT 6 — Emerging Technologies with Cloud Computing](./Unit%206%20—%20Emerging%20Technologies%20with%20Cloud%20Computing.md)*

---



---

## 📖 Historical Context & Motivation

Traditionally, enterprise IT security operated under a physical perimeter paradigm known as the **"Castle-and-Moat" model**. Organizations secured their data by building hard perimeter defenses—firewalls, intrusion detection systems (IDS), and VPN access points—around physical data center boundaries. Anyone inside the physical corporate network was implicitly trusted, while anyone outside was distrusted. However, the multi-tenant cloud revolution shattered this physical perimeter. In a public cloud IaaS/PaaS environment, physical hardware is shared with multi-tenant competitors, data flows over shared optical fibers, and employees access APIs from un-managed mobile devices worldwide.

The failure of the traditional perimeter model was highlighted by high-profile breaches. In 2014, Google pioneered the **BeyondCorp Architecture**, replacing perimeter security with the **Zero Trust Security Model** ("never trust, always verify"). Under Zero Trust, network location provides zero implicit privilege; every single API invocation must be authenticated, authorized, encrypted, and logged regardless of whether it originates inside or outside the network. Concurrently, cloud adoption established the **Shared Responsibility Model**, formally dividing security duties between the cloud provider ("Security *of* the Cloud"—hardware, hypervisor, physical facility) and the customer ("Security *in* the Cloud"—IAM roles, data encryption, network firewalls, app code). Major incidents—such as the 2019 Capital One S3 bucket exfiltration via Server-Side Request Forgery (SSRF)—demonstrated that misconfigurations in customer-managed IAM policies and Instance Metadata Services (IMDS) pose the single greatest threat to cloud security.

---

## 🔬 Deep Dive: System Architecture

### Cryptographic Envelope Encryption, KMS Architecture, and Deterministic IAM Policy Evaluation Engines

Cloud security relies on two primary cryptographic and authorization foundations: Key Management Services (KMS) for data protection and Policy Evaluation Engines for access control.

```mermaid
flowchart TB
    subgraph KMS HSM Boundary["AWS KMS / Cloud KMS (FIPS 140-2 Level 3 HSM)"]
        KMSKey["Customer Master Key (CMK / KMS Key)<br/>[Never leaves HSM memory]"]
    end
    subgraph ClientMem["Client Application Memory"]
        DEKPlain["Plaintext Data Encryption Key (DEK)"]
        DataPlain["Raw Object Payload"]
        AESEngine["AES-256-GCM Encryption Engine"]
        CipherPayload["Encrypted Object Payload"]
        AESEngine -- "Outputs" --> CipherPayload
    end
    subgraph S3Storage["Cloud Object Storage (MinIO / S3)"]
        DEKEncrypted["Encrypted Data Encryption Key (E-DEK)"]
        StoredObject["S3 Object File = (CipherPayload + E-DEK)"]
    end
    KMSKey -- "GenerateDataKey API" --> DEKPlain & DEKEncrypted
    DataPlain & DEKPlain --> AESEngine
    CipherPayload & DEKEncrypted --> StoredObject
```

```mermaid
sequenceDiagram
    autonumber
    participant App as Client Application Memory
    participant KMS as AWS KMS / HSM (FIPS 140-2 L3)
    participant S3 as AWS S3 Object Storage

    App->>KMS: 1. POST `GenerateDataKey` (KeyId: master-cmk-id, KeySpec: AES_256)
    KMS->>KMS: 2. HSM generates 256-bit Data Encryption Key (DEK)
    KMS->>KMS: 3. HSM encrypts DEK using Master CMK -> Encrypted-DEK (E-DEK)
    KMS-->>App: 4. Return Plaintext-DEK (256-bit) & Encrypted-DEK (E-DEK)
    
    App->>App: 5. Encrypt Raw Data Payload locally via AES-256-GCM using Plaintext-DEK
    App->>App: 6. Zero-out Plaintext-DEK from Application Memory
    
    App->>S3: 7. PUT Object (Payload: Ciphertext + Metadata: E-DEK + IV + Tag)
    S3-->>App: 8. HTTP 200 OK (Object Saved with Envelope Encryption)

    Note over App, S3: Decryption Phase (Reading Data back)
    App->>S3: 9. GET Object (Retrieve Ciphertext + E-DEK)
    App->>KMS: 10. POST `Decrypt` (CiphertextBlob: E-DEK)
    KMS->>KMS: 11. HSM decrypts E-DEK using Master CMK -> Plaintext-DEK
    KMS-->>App: 12. Return Plaintext-DEK
    App->>App: 13. Decrypt Payload in local RAM via AES-256-GCM
```

#### 1. Cryptographic Envelope Encryption & Key Management (KMS)
To encrypt Petabytes of cloud data without risking master key exposure or bottlenecking a central Key Management Service (KMS), cloud systems implement **Envelope Encryption**:
1. **Key Hierarchy**: The KMS contains a **KMS Customer Master Key (CMK)** stored inside a FIPS 140-2 Level 3 Hardware Security Module (HSM). The CMK never leaves the HSM unencrypted.
2. **Data Key Generation**: When an object is written, the client invokes `KMS:GenerateDataKey`. The KMS generates a symmetric **Data Encryption Key (DEK)** (AES-256), returns a *Plaintext DEK* and an *Encrypted DEK* (encrypted using the CMK), and purges the Plaintext DEK from KMS memory.
3. **Local Encryption**: The client uses the *Plaintext DEK* to encrypt raw data locally via Galois/Counter Mode (AES-256-GCM), providing both confidentiality and Authenticated Encryption with Associated Data (AEAD) integrity.
4. **Envelope Storage**: The *Plaintext DEK* is zeroed out in client RAM. The *Encrypted DEK* is stored alongside the encrypted object payload inside cloud storage.

When reading data, `KMS:Decrypt` decrypts the *Encrypted DEK* inside the HSM, returning the *Plaintext DEK* to RAM to decrypt the payload.

#### 2. Deterministic IAM Policy Evaluation Engine Algorithm
Access Control in cloud platforms (AWS IAM, OpenStack Keystone, MinIO RBAC) is governed by formal deterministic policy engines evaluating JSON access policies.

```
Evaluator Input Request Payload:
  Context = { Principal, Action, Resource, EnvironmentAttributes (IP, Time, Tags) }
```

The IAM Evaluation Algorithm operates according to a strict deterministic priority order:

```mermaid
flowchart TD
    Start([Incoming API Request]) --> Step1{Explicit Deny in any matching policy?}
    Step1 -- Yes --> Deny([DENY REQUEST])
    Step1 -- No --> Step2{Explicit Allow in any matching policy?}
    Step2 -- Yes --> Allow([ALLOW REQUEST])
    Step2 -- No --> DefaultDeny([DEFAULT DENY])
```

Formally, let $P = \{p_1, p_2, \dots, p_n\}$ be the set of attached policy statements. Each statement $p_i$ evaluates to $Result(p_i) \in \{\text{ExplicitDeny}, \text{ExplicitAllow}, \text{NoMatch}\}$. The final evaluation decision $D$ is defined as:

$$D = \begin{cases} 
\text{DENY} & \text{if } \exists p_i \in P \text{ s.t. } Result(p_i) = \text{ExplicitDeny} \\
\text{ALLOW} & \text{if } \Big(\forall p_i \in P, Result(p_i) \neq \text{ExplicitDeny}\Big) \land \Big(\exists p_j \in P \text{ s.t. } Result(p_j) = \text{ExplicitAllow}\Big) \\
\text{DENY} & \text{otherwise (Default Deny)}
\end{cases}$$

---

## 🏢 Real-World Case Study

### The 2019 Capital One Data Breach & Cloudflare Zero Trust Architecture

In July 2019, a former cloud engineer breached Capital One’s AWS environment, exfiltrating 100 million customer credit card applications and Social Security numbers stored in AWS S3 buckets.

```mermaid
flowchart TD
    subgraph VulnerableExploit["Vulnerable IMDSv1 SSRF Attack Path (2019)"]
        Attacker["Attacker"] -- "(1) Craft Malicious HTTP Request" --> WAF["Vulnerable EC2 WAF (ModSecurity)"]
        WAF -- "(2) SSRF Proxy Request to Internal IP" --> IMDSv1["IMDSv1 Endpoint<br/>(http://169.254.169.254/latest/meta-data/)"]
        IMDSv1 -- "(3) Returns Temporary IAM Credentials (No Auth)" --> WAF
        WAF -- "(4) Use Stolen IAM Creds to Exfiltrate S3 Buckets" --> S3["AWS S3 Data Lake (100M Records)"]
    end

    subgraph DefenseMitigation["Architectural Remediation (IMDSv2 + Zero Trust)"]
        subgraph IMDSv2_Flow["IMDSv2 Token Negotiation"]
            ClientApp["Client App"] -- "PUT /latest/api/token (TTL: 60s)" --> TokenEngine["IMDSv2 Service"]
            TokenEngine -- "Returns Secret Session Token" --> ClientApp
            ClientApp -- "GET /meta-data + Token Header" --> TokenEngine
        end
        subgraph NetworkControls["Network Edge Control"]
            HopLimit["IP Packet TTL Hop Limit = 1<br/>(Blocks Multi-Hop SSRF Proxying)"]
            mTLS["Cloudflare Zero Trust mTLS Mesh"]
        end
    end

    VulnerableExploit == "Remediated By" ==> DefenseMitigation
```

#### Attack Anatomy & Cloud Architectural Countermeasures:
1. **SSRF Exploitation**: The attacker identified a Server-Side Request Forgery (SSRF) vulnerability in a misconfigured open-source Web Application Firewall (WAF) running on an EC2 instance.
2. **IMDSv1 Credential Exfiltration**: The WAF misconfiguration allowed the attacker to send an HTTP request to the internal **AWS Instance Metadata Service v1 (IMDSv1)** at non-routable IP `169.254.169.254`. IMDSv1 returned temporary IAM role credentials assigned to the EC2 instance without requiring session authentication.
3. **Over-Privileged IAM Role**: The EC2 instance's IAM role possessed wildcard `s3:Sync` and `s3:GetObject` permissions across all corporate S3 buckets, allowing the attacker to dump 100 million customer records.
4. **Modern Remediation**: AWS introduced **IMDSv2**, requiring session-oriented token negotiation (`PUT` request with `X-aws-ec2-metadata-token`) and enforcing a network TTL hop-limit of 1 to prevent SSRF proxying. Simultaneously, enterprises adopted **Cloudflare Zero Trust** with mutual TLS (mTLS) authentication across microservices.

---

## 📝 End-of-Chapter Exercises

### Exercise 1: Formal IAM Policy Evaluation Matrix Resolution
Given the following three attached JSON policy statements evaluating a request from user `developer-alice` performing `s3:GetObject` on `arn:aws:s3:::corp-data-lake/finance/q4.csv` from IP address `203.0.113.45`:

- **Policy 1**: `Allow` action `s3:*` on resource `arn:aws:s3:::corp-data-lake/*`.
- **Policy 2**: `Deny` action `s3:GetObject` on resource `arn:aws:s3:::corp-data-lake/finance/*` if `aws:PrincipalTag/Department` != `Finance`.
- **Policy 3**: `Deny` action `s3:*` on all resources if `aws:SourceIp` is NOT `198.51.100.0/24`.

- (a) Trace the deterministic decision matrix step-by-step assuming `developer-alice` belongs to the `Finance` department (`PrincipalTag/Department = Finance`).
- (b) Determine the final access decision (ALLOW vs. DENY) and cite the exact evaluation rule triggered.
- (c) Re-evaluate the decision if `developer-alice` connects via a VPN IP of `198.51.100.12`.

### Exercise 2: SLA Uptime Arithmetic & Financial Penalty Modeling
A enterprise Cloud Service Agreement (SLA) guarantees $99.99\%$ annual service availability for a mission-critical Cloud Database.
- (a) Calculate the maximum allowable cumulative downtime in minutes and seconds per year (365 days) before an SLA breach occurs.
- (b) If an infrastructure outage causes 2 hours and 15 minutes of continuous downtime during a quarterly region failure:
  - Calculate the percentage breach below the guaranteed SLA.
  - Calculate the financial service credit owed to the customer if the contract mandates a 20% billing credit for every 0.01% drop below the guaranteed threshold on a \$100,000 monthly cloud invoice.
- (c) Calculate the net compound availability SLA of a system connecting an API Gateway ($99.99\%$), a Web Application Tier ($99.9\%$), and a Managed Database Tier ($99.95\%$) in serial series.

### Exercise 3: Cryptographic Envelope Encryption Protocol Implementation
Write C/Python-style pseudo-code for an enterprise object storage client implementing AES-256-GCM Envelope Encryption integrated with AWS KMS / MinIO KMS.
- (a) Write function `encrypt_payload(byte[] plaintext, string kms_key_id)` that invokes `KMS:GenerateDataKey`, performs AES-256-GCM payload encryption, prepends the 12-byte initialization vector (IV) and 16-byte authentication tag, and returns `(encrypted_payload, encrypted_dek)`.
- (b) Write function `decrypt_payload(byte[] encrypted_payload, byte[] encrypted_dek, string kms_key_id)` that invokes `KMS:Decrypt` to recover the plaintext DEK, decrypts the payload, and validates authentication tag integrity.
- (c) Analyze why reusing an AES-GCM 12-byte Initialization Vector (IV) across multiple payload encryptions under the same DEK catastrophically compromises cryptographic security (nonce reuse attack).

### Exercise 4: IMDSv1 vs IMDSv2 SSRF Vulnerability & Hop-Limit Analysis
An attacker attempts an SSRF exploit against an EC2 instance running a vulnerable web server proxy.
- (a) Diagram the network packet flow of an IMDSv1 request to `http://169.254.169.254/latest/meta-data/iam/security-credentials/`.
- (b) Diagram how IMDSv2 blocks the SSRF attack by introducing a `PUT` token request and setting the IP packet Time-To-Live (TTL) hop-limit to `1` on the hypervisor virtual network interface.
- (c) Formulate an AWS CLI / IaC Terraform security rule to enforce `HttpTokens = required` and `HttpPutResponseHopLimit = 1` across an autoscaling group of 500 EC2 instances.


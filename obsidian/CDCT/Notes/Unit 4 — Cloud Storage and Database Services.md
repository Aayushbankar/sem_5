---
subject: CDCT
status: not-started
tags: [subject/cdct, unit/4]
unit: 4
title: Cloud Storage and Database Services
hours: 9
weightage: "20%"
related_practicals: [P06, P07, P09]
---
# UNIT 4 — Cloud Storage and Database Services 💾

> **Cloud and Data Center Technology (DI05016031)** · **9 hrs · 20% weightage**
> **Covers syllabus sections:** 4.1 Cloud Storage Solutions (object/block/file, consistency & durability) · 4.2 Cloud Databases (SQL/NoSQL, scaling & replication)
> **Related practicals:** [[P06 — Cloud Databases Comparison|P06]], [[P07 — Cloud Storage Comparison|P07]], [[P09 — Minio Secure Object Storage|P09]]

---

## 🧭 Chapter Roadmap

This unit (20%) is the **storage & database** chapter — hugely PYQ-heavy. Two 7-mark monsters repeat in nearly every paper: **"types of cloud storage"** and **"types of cloud databases"** (SQL vs NoSQL), plus the consistency/durability distinction. P06, P07 and P09 are your practical anchors.

| # | Concept | Exam importance | Related |
|---|---------|-----------------|---------|
| 4.1 | Object vs block vs file storage | ★★★★★ | P07, P09 |
| 4.1 | Data consistency vs durability | ★★★★★ | P07 |
| 4.1 | Storage solutions (S3, GCS, Azure Blob, etc.) | ★★★★ | P07 |
| 4.2 | Cloud databases: SQL vs NoSQL | ★★★★★ | P06 |
| 4.2 | Data scaling & replication | ★★★★ | P06 |

### Learning outcomes — after this unit you can:
1. Define cloud storage and explain **object / block / file** storage with examples.
2. Distinguish **consistency** and **durability** (and justify why each is essential).
3. Compare major storage services (S3, GCS, Azure Blob, IBM COS, MinIO).
4. Explain cloud **database services** and the **SQL vs NoSQL** divide.
5. Explain **data scaling** (vertical/horizontal) and **replication** (HA, read replicas, sharding).

---

## 4.1 Cloud Storage Solutions ⭐⭐

### 4.1.1 The three storage models
| Model | What it stores | How you access it | Ideal for | Examples |
|---|---|---|---|---|
| **Object storage** | Data as **objects** (file + metadata + ID) in **buckets** | HTTP(S) REST / S3 API | Media, backups, data lakes, static sites (huge, unstructured) | **S3, GCS, Azure Blob, IBM COS, MinIO (P09)** |
| **Block storage** | Raw **fixed-size blocks** (volumes) | Attached to a VM like a hard disk (iSCSI/SCSI/NVMe) | OS disks, databases needing low-latency random I/O | AWS EBS, Azure Disk, Cinder (P01) |
| **File storage** | Files in a **hierarchical directory tree** | **NFS / SMB** shares (network mount) | Shared documents, legacy apps, home directories | AWS EFS, Azure Files, NetApp |

```mermaid
flowchart TD
    subgraph StorageModels["Cloud Storage Abstraction Models"]
        subgraph ObjStorage["Object Storage"]
            OBJ_API["HTTP / REST API (PUT, GET, DELETE)"]
            OBJ_Data["Flat Key-Value Storage<br/>(Bucket / Key + Data Shards + Metadata)"]
            OBJ_Ex["Amazon S3 · GCS · Azure Blob · MinIO"]
            OBJ_API --> OBJ_Data --> OBJ_Ex
        end

        subgraph BlockStorage["Block Storage"]
            BLK_API["iSCSI / NVMe-oF Protocol"]
            BLK_Data["Raw Block Device Array<br/>(Fixed 4KB Blocks attached to VM)"]
            BLK_Ex["AWS EBS · OpenStack Cinder · Azure Disk"]
            BLK_API --> BLK_Data --> BLK_Ex
        end

        subgraph FileStorage["File Storage"]
            FIL_API["POSIX File Interface (NFS / SMB)"]
            FIL_Data["Hierarchical Directory Tree<br/>(Folders / Files / Links)"]
            FIL_Ex["AWS EFS · Azure Files · NetApp ONTAP"]
            FIL_API --> FIL_Data --> FIL_Ex
        end
    end
```

### 4.1.2 Consistency and durability ⭐⭐
**Consistency** — *do all readers see the same (latest) data?* **Strong consistency** = every read reflects the latest write; **eventual consistency** = reads may briefly return stale data and converge later. (Funded by the **CAP theorem** — a system can pick at most two of Consistency/Availability/Partition tolerance.)

**Durability** — *is the data safe from loss?* = the probability that data survives failures (disk crash, node loss, region failure) intact. Achieved via **replication** (copies in multiple AZs) and **erasure coding**.

| Criterion | Consistency | Durability |
|---|---|---|
| Question | Is every read the *latest* write? | Is the data *never lost*? |
| Handled by | Replication/sync protocols, quorums | Redundant copies, erasure coding |
| Failure mode | Stale reads, split-brain | Data loss (irrecoverable) |
| Cloud promise | S3/GCS are strongly consistent | 99.999999999% (11 nines) |
| Money-transfer example (s_26 Q.4-b-alt) | Both accounts must reflect the transfer *immediately* | The transfer record must survive forever |

> [!warning] Exam trap
> students blur the two. *Durability = survival; consistency = agreement.* A system can be 11-nines durable yet only eventually consistent (e.g., old S3, some NoSQL replicas) — and vice versa.

### 4.1.3 Managed vs unmanaged storage (w_25 Q.4-b)
- **Managed (cloud storage as a service):** provider handles capacity, replication, encryption, lifecycle — you just PUT/GET (S3, GCS, MinIO). Pay per GB/request.
- **Unmanaged:** you provision your own storage (block volumes, self-hosted NAS) and manage RAID, backups, sizing yourself. More control, more work.

### 4.1.4 Major solutions (s_24/s_26 Q.4-a) ⭐
- **Amazon S3** (object), **EBS** (block), **EFS** (file)
- **Google Cloud Storage** (object), **Persistent Disk** (block), **Filestore** (file)
- **Microsoft Azure Blob** (object), **Azure Disk** (block), **Azure Files** (file)
- **IBM Cloud Object Storage**, **MinIO** (self-hosted S3-compatible, P09)
→ Full comparison in [[P07 — Cloud Storage Comparison|P07]].

## 4.2 Cloud Databases ⭐⭐

### 4.2.1 Database services & their features (s_24/s_26 Q.4-a-alt) ⭐
A **cloud database service** is a database hosted and **managed** by the provider. **Features:** managed provisioning (no install), automated **backups & restore**, **high availability** (multi-AZ failover), **scaling** (vertical/horizontal), **monitoring & patching**, access control/encryption (Unit 5), and pay-per-use pricing. → Full service comparison in [[P06 — Cloud Databases Comparison|P06]].

### 4.2.2 SQL vs NoSQL ⭐⭐
| Criterion | SQL (relational) | NoSQL |
|---|---|---|
| **Data model** | Tables, rows, fixed schema | Documents/JSON, key-value, wide-column, graph |
| **Schema** | Rigid (migrations needed) | **Flexible** (evolve freely) |
| **Transactions** | **ACID** (strong consistency) | Often **BASE** (eventually consistent) |
| **Scaling** | Vertical + read replicas (hard to shard) | **Horizontal by design** (sharding) |
| **Query** | SQL (joins) | API/map-reduce style |
| **Use cases** | Banking, ERP, e-commerce orders | Real-time apps, IoT, catalogs, caching, analytics |
| **Cloud examples** | **RDS, Cloud SQL, Azure SQL DB, Db2, Oracle ATP** | **MongoDB Atlas, Firebase RTDB** (P06) |

> Remember the practical list P06: RDS / Cloud SQL / Azure SQL / Db2 (SQL) + Firebase RTDB / MongoDB Atlas (NoSQL) + Oracle Autonomous DB (SQL, self-driving).

### 4.2.3 Data scaling and replication (s_24/w_24/s_26 Q.4-c-alt) ⭐⭐
**Scaling**
- **Vertical (scale-up):** bigger VM/CPU/RAM for the single database — easy, limited by max size, downtime to resize.
- **Horizontal (scale-out):** more database nodes — **sharding** splits data by key across nodes (write scaling); **read replicas** serve reads off copies (read scaling).

**Replication**
- **Master–slave / primary–standby:** writes go to primary; copies serve reads / act as failover → **HA + read scaling**.
- **Multi-region replication:** synchronous/async copies in other regions → **durability + DR**.
- **Replication factor:** how many copies exist (e.g., 3 in MongoDB Atlas) → the higher, the more durable.

```mermaid
flowchart TD
    subgraph ClientTier["Application Clients & Connection Pooler"]
        ClientApp["Client Application Workload"]
        Proxy["Database Proxy / Router (pgBouncer / Mongos)"]
        ClientApp --> Proxy
    end

    subgraph ShardedCluster["Horizontal Database Topology"]
        subgraph PrimaryShard["Primary Node (Write Tier)"]
            PrimaryDB[("Primary Database Node<br/>(Processes All Writes & ACID Transactions)")]
            WAL_Log[("Write-Ahead Log (WAL)")]
            PrimaryDB --- WAL_Log
        end

        subgraph ReadReplicas["Read Replicas Tier (Read Scale-Out)"]
            Replica1[("Read Replica 1 (AZ-1)")]
            Replica2[("Read Replica 2 (AZ-2)")]
            Replica3[("Read Replica 3 (AZ-3)")]
        end
    end

    subgraph FailoverController["High Availability Sentinel"]
        Sentinel["Failover Manager / Consensus Coordinator"]
        Sentinel -. "Heartbeat & Health Checks" .-> PrimaryDB
        Sentinel -. "Promotes Replica on Primary Failure" .-> Replica1
    end

    Proxy -- "Write Traffic (INSERT / UPDATE)" --> PrimaryDB
    Proxy -- "Read Traffic (SELECT)" --> Replica1 & Replica2 & Replica3
    PrimaryDB == "Synchronous / Asynchronous Replication" ==> Replica1 & Replica2 & Replica3
```

---

## 🧠 Deep-Dive Topics

### Deep Dive A: "Justify: data consistency is essential in cloud storage" (s_24 Q.4-b)
With a distributed, replicated store, two readers on different replicas could see different values. If a user pays an invoice (debit) and the system shows the balance unchanged, that's an **inconsistency → financial loss / user trust loss**. **Money transfer (s_26 Q.4-b-alt):** both accounts must reflect the debit *and* credit together — if the ledger is inconsistent, a transfer could appear in one account but not the other, breaking correctness. Hence cloud storage must guarantee strong consistency for such transactions (atomicity across replicas), or apply it at the application level (transactions, idempotency).

### Deep Dive B: "Justify: data durability is essential" (s_24 Q.4-b-alt)
Durability is *data survival*. Storage hardware **will fail** (disk MTBF), so the cloud replicates objects across devices and AZs (S3: 11 nines). If durability is absent, one disk/AZ failure **loses customer data forever** — the worst possible cloud failure (no amount of speed/features compensates). **Backup & DR (s_26 Q.4-b):** versioning, lifecycle copies to other regions, and point-in-time restores turn "survive disk loss" into "survive region loss".

### Deep Dive C: BASE vs ACID in one table
| | ACID (SQL) | BASE (NoSQL) |
|---|---|---|
| A | **Atomicity** | **Basically Available** (system always responds) |
| C | **Consistency** | **Soft state** (state may drift over time) |
| I | **Isolation** | **Eventually consistent** (converges) |
| D | **Durability** | (durability still desired!) |

### Deep Dive D: When to shard — worked example
Orders table = 500 GB, single node saturated at write peak. **Option 1 (vertical):** upgrade to a 64-core machine — costly, still one node. **Option 2 (horizontal):** shard on `customer_id` (hash) across 5 nodes → each node 100 GB, writes split 5 ways. **Option 3:** keep a single primary for writes but add 3 **read replicas** for reporting. The best design usually combines sharding + read replicas — the P06 "how to choose" guide captures this.

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

1. **Object storage is NOT a filesystem** — no in-place edits, no directories (prefixes only), no POSIX. That's why file storage (EFS) exists. A classic exam "why three types?" answer.
2. **Erasure coding > replication at scale** — 3 copies = 3× cost; erasure coding (e.g., 6+3 Reed-Solomon) gives ~11 nines at ~1.5× cost. Hyperscalers use both.
3. **"Eventually consistent" still applies to some NoSQL replicas** — while S3/GCS/Blob are all *strongly consistent* now (post-2020), many NoSQL systems keep eventual consistency for latency — hence the CAP trade-off.
4. **Cloud databases are mostly "just managed open-source"** — RDS wraps MySQL/PostgreSQL; Atlas wraps MongoDB. The differentiator is the *managed features*, not the engine. Great for P06 conclusions.
5. **Durability ≠ availability** — you can be durable (data safe) but unavailable (can't reach it during a failover). Exams love this subtle distinction.

---

## 📝 PYQ Map — UNIT 4 (all available papers)

| Paper | Q. | Topic | Marks |
|---|---|---|---|
| **Summer 2024** | Q.4(a) | Define cloud storage; list major solutions | 3 |
| | Q.4(b) | Justify: data consistency is essential in cloud storage | 4 |
| | Q.4(c) | Explain types of cloud databases in detail | 7 |
| | Q.4(a)-alt | Define database services; features | 3 |
| | Q.4(b)-alt | Justify: data durability is essential | 4 |
| | Q.4(c)-alt | Data scaling and replication in detail | 7 |
| **Winter 2024** | Q.4(a) | Define cloud storage; examples | 3 |
| | Q.4(b) | Data consistency vs durability | 4 |
| | Q.4(c) | Types of cloud storage in detail | 7 |
| | Q.4(a)-alt | Define cloud databases; examples | 3 |
| | Q.4(b)-alt | Data scaling and replication | 4 |
| | Q.4(c)-alt | Types of cloud databases | 7 |
| **Summer 2025** | Q.1(b) | Cloud storage solutions; object storage in detail | 4 |
| | Q.3(c) | Types of cloud databases in detail | 7 |
| | Q.3(c)-alt | Data consistency and durability in detail | 7 |
| | Q.4(a) | Role of data scaling | 3 |
| | Q.4(a)-alt | File storage in the cloud | 3 |
| **Winter 2025** | Q.4(a) | Object storage in the cloud | 3 |
| | Q.4(b) | Managed vs unmanaged cloud storage | 4 |
| | Q.4(c) | Durability in cloud computing | 7 |
| | Q.4(a)-alt | Block storage in the cloud | 3 |
| | Q.4(b)-alt | Data scaling with example | 4 |
| | Q.4(c)-alt | Types of cloud databases: SQL & NoSQL | 7 |
| **Summer 2026** | Q.4(a) | Define database services; two features | 3 |
| | Q.4(b) | Justify: backup & DR are essential | 4 |
| | Q.4(c) | Data scaling and replication in detail | 7 |
| | Q.4(a)-alt | Major cloud storage solutions; explain one | 3 |
| | Q.4(b)-alt | Justify: money transfer must be consistent | 4 |
| | Q.4(c)-alt | Types of cloud databases in detail | 7 |

### ✅ Solved PYQ answers (UNIT 4)

**Q. (w_24 Q.4a / s_26 Q.4a-alt, 3 marks) — Define cloud storage. Write examples / list solutions.**
> Cloud storage is a **managed service for storing data in the cloud**, accessed over the internet through APIs or consoles, where the provider handles capacity, replication, encryption and availability, and you **pay per use** (GB-month + requests). It comes in three models: **object storage** (Amazon S3, Google Cloud Storage, Azure Blob, IBM COS, MinIO), **block storage** (Amazon EBS, Azure Disk, Cinder volumes) and **file storage** (Amazon EFS, Azure Files). The S3-style object model is the dominant one for backups, media and data lakes.

**Q. (w_25 Q.4a, 3 marks) — What is object storage in the cloud?**
> Object storage stores data as discrete **objects** inside **buckets**. Each object = **data + metadata** (content type, tags, timestamps) + a **globally unique ID/ETag**, addressed by an HTTP URL (`bucket/key`). There is no hierarchical filesystem and **no in-place modification** — you PUT/GET/DELETE whole objects. It is massively **scalable** (to exabytes), highly **durable** (11 nines via replication/erasure coding), and accessed with the **S3-style REST API**. Examples: Amazon S3, GCS, Azure Blob, IBM COS and the self-hosted **MinIO** (P09). Ideal for media, backups, static websites and data lakes.

**Q. (w_24 Q.4b, 4 marks) — Differentiate data consistency and durability**
> **Consistency** = whether all readers see the **same (latest) data**. Strong consistency means every read reflects the last write; eventual consistency means reads may briefly be stale and then converge. It is a correctness property, handled by replication/consensus and bounded by the **CAP theorem**. **Durability** = whether data is **safe from loss**; the probability that committed data survives disk/node/AZ failures. It is achieved by **replication** and **erasure coding** (e.g., S3's 99.999999999%). Consistency is about *agreement*, durability about *survival*. A store can be durable but only eventually consistent, and a strongly consistent store can still lose data if it isn't durable. Both are essential: consistency keeps money/accounts correct; durability guarantees data is never lost.

**Q. (w_24 Q.4c, 7 marks) — Explain types of cloud storage in detail**
> Cloud storage has three types. **(1) Object storage:** data as objects (data + metadata + ID) in buckets, HTTP/S3 API, no in-place edit; massively scalable and durable — S3, GCS, Azure Blob, IBM COS, MinIO. Used for media, backups, data lakes. **(2) Block storage:** raw fixed-size volumes attached to a VM like a disk; low latency for OS and databases; formatted with a filesystem — EBS, Azure Disk, Cinder. **(3) File storage:** a POSIX-compliant hierarchical filesystem shared over the network via NFS/SMB; multiple VMs mount the same share — EFS, Azure Files. **Choosing:** databases/OS → block; shared documents/legacy → file; huge unstructured data/media/backup → object. Additionally, storage can be **managed** (service does everything) or **unmanaged** (you operate your own volumes), and uses storage **classes/tiers** (hot → cold/archive) to trade cost for access latency (see P07).

**Q. (w_25 Q.4c-alt / s_24 Q.4c, 7 marks) — Types of cloud databases: SQL & NoSQL (in detail)**
> **SQL databases** use tables with **fixed schemas** and the SQL language, guaranteeing **ACID** transactions (Atomicity, Consistency, Isolation, Durability). They scale **vertically** plus with read replicas, and suit strongly consistent transactional apps (banking, ERP, e-commerce). *Cloud examples:* Amazon RDS, Google Cloud SQL, Azure SQL Database, IBM Db2 on Cloud, Oracle Autonomous Database. **NoSQL databases** use flexible models — **document** (JSON; MongoDB Atlas, Firebase RTDB), **key-value** (DynamoDB, Redis), **wide-column** (Cassandra, Bigtable), **graph** (Neptune). They follow **BASE** (basically available, soft state, eventually consistent), have **flexible schemas**, and scale **horizontally by sharding**, suiting high-volume, variable-schema apps (IoT, real-time chat, catalogs, caching). **Choosing (P06 guide):** strong ACID + fixed schema → SQL; flexible schema + huge scale + eventual consistency acceptable → NoSQL.

**Q. (s_24 Q.4c-alt / s_26 Q.4c, 7 marks) — Explain data scaling and replication in detail**
> **Scaling** increases a database's capacity. **Vertical scaling** upgrades the single server (bigger CPU/RAM) — simple but costly and bounded, with resize downtime. **Horizontal scaling** adds nodes: **sharding** partitions data by a shard key across nodes (spreading writes), and **read replicas** serve read traffic from copies. **Replication** copies data to multiple nodes: **primary–standby (master–slave)** — all writes hit the primary, replicas serve reads and take over on failure (**high availability + read scaling**); **synchronous vs asynchronous** replication trade durability/latency; **multi-region replication** adds disaster recovery. **Benefits:** HA (no single point of failure), durability (multiple copies), performance (parallel reads/writes), scalability (grow by adding nodes). **Trade-offs:** more replicas = more cost + eventual-consistency risk if replication is async (see CAP/BASE). Example (s_25 Q.4-b-alt): a 500 GB orders table sharded by `customer_id` across 5 nodes, plus 3 read replicas for analytics, keeps writes and reads scaling while staying available.

---

## ✍️ Practice Problems (self-test — answers hidden)

1. Differentiate object, block and file storage with one example each.
2. "Consistency vs durability" — give the money-transfer justification for consistency and a disk-loss scenario for durability.
3. Name the SQL and NoSQL services from P06; which two are NoSQL?
4. What does sharding split, and what do read replicas do?
5. Why is object storage "not a filesystem"? Give two consequences.
6. Justify: backup and disaster recovery are essential features of cloud storage.

<details>
<summary>📌 Model solutions</summary>

1. Object: whole objects + metadata in buckets, HTTP API (S3). Block: raw volumes attached to a VM (EBS). File: hierarchical NFS/SMB share (EFS).
2. Consistency: money transfer must show the debit and credit together in every replica immediately; inconsistency → wrong balances. Durability: a disk/AZ failure must never lose committed data → replicate/erasure-code.
3. SQL: RDS, Cloud SQL, Azure SQL DB, Db2, Oracle ATP. NoSQL: Firebase RTDB, MongoDB Atlas.
4. Sharding splits data by a shard key across nodes (spreads writes); read replicas are copies serving reads and providing failover.
5. No in-place edit, no directories/POSIX; objects are whole-unit PUT/GET — consequences: can't append, use prefixes not folders, separate file storage for POSIX apps.
6. Hardware fails; regions fail. Backup (versioning, snapshots) + DR (cross-region copies, restore points) turn "survive a disk loss" into "survive a region loss" — without them a single failure means permanent data loss.
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **Object storage** | Bucket/object (data+metadata+ID), HTTP API, exabyte-scale |
| **Block storage** | Raw volumes attached to VMs (EBS, Cinder) |
| **File storage** | POSIX files shared via NFS/SMB (EFS, Azure Files) |
| **Consistency** | All readers see the same latest data |
| **Durability** | Data never lost (11 nines via replication/erasure coding) |
| **CAP theorem** | Consistency, Availability, Partition tolerance — choose two |
| **Eventual consistency** | Reads converge to latest state over time |
| **ACID / BASE** | Strong transactional guarantees / relaxed NoSQL guarantees |
| **Managed storage/DB** | Provider handles ops; you pay per use |
| **Unmanaged storage/DB** | You operate the resource yourself |
| **SQL / NoSQL** | Relational tables+ACID / flexible-model horizontal DBs |
| **Vertical scaling** | Bigger single machine (scale-up) |
| **Horizontal scaling** | More nodes (scale-out) |
| **Sharding** | Splitting data by key across nodes |
| **Read replicas** | Copies serving reads + failover |
| **Replication factor** | Number of copies of the data |
| **Storage class/tier** | Hot → cold/archive cost-vs-latency tiers |
| **Backup & DR** | Point-in-time copies + cross-region recovery |

---

## 🔗 Curated Resources (per concept)

**Storage fundamentals**
- AWS storage overview (S3/EBS/EFS): https://aws.amazon.com/products/storage/
- Google Cloud storage options: https://cloud.google.com/storage/docs/choosing-a-storage-option
- Azure storage types: https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction

**Consistency & durability**
- CAP theorem (Brewer): https://en.wikipedia.org/wiki/CAP_theorem
- S3 strong consistency announcement: https://aws.amazon.com/blogs/aws/amazon-s3-update-strong-read-after-write-consistency/
- AWS "Data durability" S3 FAQ: https://aws.amazon.com/s3/faqs/

**Cloud databases (P06 links)**
- RDS: https://aws.amazon.com/rds/ · Cloud SQL: https://cloud.google.com/sql · Azure SQL: https://azure.microsoft.com/products/azure-sql/database/ · Db2: https://www.ibm.com/cloud/db2 · Firebase: https://firebase.google.com/docs/database · Atlas: https://www.mongodb.com/products/platform/atlas-database · Oracle ATP: https://www.oracle.com/autonomous-database/

**MinIO (P09)**
- MinIO docs: https://min.io/docs/minio/linux/index.html

**Books (GTU syllabus)**
- Sosinsky, *Cloud Computing Bible* (Wiley) — storage & DB chapters
- Buyya, Vecchiola & Selvi, *Mastering Cloud Computing* — storage chapter

**Videos (high yield)**
- *Object vs Block vs File storage* — IBM Technology / AWS
- *SQL vs NoSQL explained* — IBM Technology
- *Database scaling: sharding & replication* — ByteByteGo

---

## 🎥 Video Study Guide (YouTube)

> Search keywords + trusted channels, in watching order.

### 🧑‍🎓 Step 0 — Pick your learning style
| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short explainers | 1 video per topic (4–10 min each) |
| 🛠️ **Builder** | doing it | Do [[P09 — Minio Secure Object Storage|P09]] (MinIO hands-on) |
| 🧠 **Deep Diver** | the "why" | Watch consistency/durability + CAP deep dives |
| 🎓 **Academic** | exam marks | Nail the two 7-mark monsters from the PYQ map |

### 🎬 Step 1 — Watch by topic
| Topic | YouTube search keywords | Best channels |
|---|---|---|
| Storage types | `object vs block vs file storage` · `s3 vs ebs vs efs` | IBM Technology, AWS, TechTarget |
| Consistency | `strong vs eventual consistency` · `cap theorem for beginners` | ByteByteGo, Martin Kleppmann |
| Durability | `how s3 achieves 11 nines durability` · `erasure coding vs replication` | AWS, ByteByteGo |
| SQL vs NoSQL | `sql vs nosql explained` · `when to use nosql` | IBM Technology, ByteByteGo |
| Database services | `amazon rds vs aurora` · `managed databases explained` | AWS Online Tech Talks, ByteByteGo |
| Scaling & replication | `database sharding explained` · `read replicas explained` | ByteByteGo, TechWorld with Nana |
| MinIO (P09) | `minio docker s3` · `minio bucket policy sse` | MinIO official, Just me and Opensource |
| Revision (exam) | `cloud storage database unit 4 diploma` · `nosql 10 minute recap` | Gate Smashers, Neso Academy |

### 🎬 Step 2 — Full playlists (Deep Divers & Academics)
1. *Database Scaling* — ByteByteGo (sharding, replication, distributed SQL).
2. *SQL & NoSQL fundamentals* — freeCodeCamp / Neso Academy.
3. NPTEL *Cloud Computing* (storage unit): https://archive.nptel.ac.in/courses/106/105/106105167/

### 🎬 Step 3 — Proof you got it (5 min)
- Give the money-transfer argument for consistency AND a disk-loss argument for durability in one minute.
- Name the 3 storage models and one cloud service each from memory.
- Explain why Atlas (NoSQL) shards horizontally while RDS scales vertically.

---

*Next: [[Unit 5 — Cloud Security and Compliance|UNIT 5 — Cloud Security and Compliance]]*

---



---

## 📖 Historical Context & Motivation

Enterprise data storage historically relied on localized Direct-Attached Storage (DAS) and enterprise Storage Area Networks (SAN) / Network-Attached Storage (NAS) built over expensive Fibre Channel hardware. These monolithic storage arrays provided strict POSIX file systems and strong ACID database guarantees, but proved incapable of scaling to planetary-scale internet workloads. As web applications expanded in the early 2000s, traditional monolithic Relational Database Management Systems (RDBMS) suffered from rigid scale-up limits (vertical scaling), expensive multi-master lock contention, and high failover downtime.

The cloud storage paradigm shift occurred between 2003 and 2007. In 2003, Google published the **Google File System (GFS)** paper, demonstrating that reliable distributed storage could be constructed from thousands of cheap, prone-to-failure commodity disk nodes using master-chunkserver architectures. In 2006, Amazon launched **Amazon S3 (Simple Storage Service)**, introducing RESTful Object Storage decoupled from file system hierarchy overhead. Concurrently, Eric Brewer formulated the **CAP Theorem** (proved formally by Gilbert & Lynch in 2002), asserting that a distributed data store can simultaneously provide at most two of three guarantees: *Consistency*, *Availability*, and *Partition Tolerance*. Recognizing that internet-scale services required 100% availability ($A$) under inevitable network partitions ($P$), Amazon published the seminal **Dynamo** paper in 2007. Dynamo sacrificed strict serializable consistency in favor of eventual consistency (BASE), employing consistent hashing, vector clocks, and quorum replication—giving birth to the modern NoSQL and cloud object storage landscape.

---

## 🔬 Deep Dive: System Architecture

### Distributed Consistent Hashing, LSM-Tree Storage Engines, and Reed-Solomon Erasure Coding

Modern cloud storage platforms (AWS S3, MinIO) and distributed databases (DynamoDB, Cassandra) integrate three core system architectures to guarantee high write throughput, horizontal elasticity, and 11-nines ($99.999999999\%$) durability.

```mermaid
flowchart TB
    subgraph ConsistentHashRing["Distributed Consistent Hashing Ring (Keyspace [0, 2^32 - 1])"]
        NodeA["Node A (Tokens: 0, 90)"]
        NodeB["Node B (Tokens: 30, 120)"]
        NodeC["Node C (Tokens: 60, 150)"]
        NodeA --> NodeB --> NodeC --> NodeA
    end
    subgraph LSMEngine["Node Storage Engine (LSM-Tree Write Path)"]
        MemTable[RAM MemTable]
        WAL[Write-Ahead Log (Disk)]
        SSTable0[SSTable Level 0]
        SSTable1[SSTable Level 1]
        MemTable -- "Flushes when full" --> SSTable0
        SSTable0 -- "Background Compaction" --> SSTable1
    end
    subgraph ErasureCoding["Object Durability (Reed-Solomon 8+4)"]
        DataBlocks["8 Data Shards (D1..D8)"]
        ParityBlocks["4 Parity Shards (P1..P4)"]
        DataBlocks & ParityBlocks --> Disks["12 Disks across 3 Availability Zones"]
    end
    NodeA -- "Local Writes" --> MemTable & WAL
```

#### 1. Consistent Hashing & Quorum Replication ($N, W, R$)
To distribute objects and database partitions across dynamic node clusters without a centralized lookup bottleneck, cloud databases apply **Consistent Hashing**:
- The hash space is mapped to a ring modulo $2^{32} - 1$.
- Physical nodes are assigned multiple **Virtual Nodes (vnodes)** across the ring using cryptographic hash functions (e.g., MurmurHash3), ensuring uniform key distribution.
- A key $k$ is assigned to the first node whose position is greater than or equal to $hash(k)$.

To achieve configurable consistency, data is replicated across $N$ physical nodes. Writes and reads enforce **Sloppy Quorum** equations:
- $N$: Replication factor (number of nodes storing a key copy).
- $W$: Write quorum (number of nodes that must acknowledge a write before returning success).
- $R$: Read quorum (number of nodes that must respond to a read request).

$$\text{Strong Consistency Condition: } W + R > N$$

If $W + R > N$, the read set and write set must overlap in at least one node containing the latest vector clock timestamp, guaranteeing strong consistency. If $W + R \le N$, the system delivers **Eventual Consistency** with read-repair background synchronization.

#### 2. LSM-Tree Write Path Mechanics
Cloud database storage engines (e.g., RocksDB, DynamoDB SSD engine) employ **Log-Structured Merge-trees (LSM-Trees)** instead of traditional B+ Trees to optimize for sequential I/O:
1. **Write-Ahead Log (WAL)**: Incoming writes append sequentially to an on-disk WAL for crash recovery.
2. **MemTable**: Writes update an in-memory sorted skip-list (`MemTable`).
3. **SSTable Flush**: When the `MemTable` reaches capacity (e.g., 64 MB), it is written sequentially to disk as an immutable **Sorted String Table (SSTable)** at Level 0.
4. **Leveled Compaction**: Background threads merge overlapping SSTables from Level $L$ to Level $L+1$, eliminating duplicate/deleted keys and bounding read amplification.

#### 3. Durability via Reed-Solomon Erasure Coding ($k + m$)
Rather than incurring 300% storage overhead via 3-way multi-region replication ($N=3$), cloud object stores (S3, MinIO) use **Reed-Solomon $(k + m)$ Erasure Coding**:
- An object payload is divided into $k$ equal-sized data blocks.
- Galois Field arithmetic ($GF(2^8)$ matrix multiplication) generates $m$ parity blocks.
- The total $k + m$ blocks are distributed across $k + m$ independent drive/rack failure domains.

$$\text{Storage Overhead Ratio} = \frac{k + m}{k}$$

$$\text{Fault Tolerance} = m \text{ drive failures sustained with zero data loss}$$

```mermaid
sequenceDiagram
    autonumber
    actor Client as S3 Client / Application
    participant GW as S3 API Gateway Router
    participant Engine as Erasure Coding Engine (Galois Field)
    participant AZ1 as Storage Node Array (AZ 1)
    participant AZ2 as Storage Node Array (AZ 2)
    participant AZ3 as Storage Node Array (AZ 3)
    participant Meta as Metadata Catalog (DynamoDB)

    Client->>GW: 1. PUT /bucket/object.mp4 (Payload 100MB)
    GW->>Engine: 2. Stream Payload to Erasure Encoder
    Engine->>Engine: 3. Divide into 8 Data Blocks (D1..D8) & Compute 4 Parity Shards (P1..P4)
    
    par Distribute 12 Shards across 3 Availability Zones
        Engine->>AZ1: 4a. Parallel Write Shards D1, D2, D3, P1 (AZ-1 Disks)
    and Distribute to AZ 2
        Engine->>AZ2: 4b. Parallel Write Shards D4, D5, D6, P2 (AZ-2 Disks)
    and Distribute to AZ 3
        Engine->>AZ3: 4c. Parallel Write Shards D7, D8, P3, P4 (AZ-3 Disks)
    end

    AZ1-->>Engine: 5a. Write Ack & CRC32 Checksum
    AZ2-->>Engine: 5b. Write Ack & CRC32 Checksum
    AZ3-->>Engine: 5c. Write Ack & CRC32 Checksum
    
    Engine->>Meta: 6. Commit Object Metadata & Shard Mapping Vector
    Meta-->>Engine: 7. Metadata Persisted (ACID Commit)
    Engine-->>GW: 8. Object Erasure Coding Complete (8+4 Shards Committed)
    GW-->>Client: 9. HTTP 200 OK (ETag Header + MD5 Checksum)
```

For example, an $8 + 4$ Reed-Solomon scheme delivers protection against 4 simultaneous drive failures with only $1.5\times$ (50%) storage overhead, compared to $3.0\times$ (200%) overhead for 3-way replication.

---

## 🏢 Real-World Case Study

### AWS S3 & Amazon DynamoDB: Planetary-Scale Storage Infrastructure

Amazon Web Services built **Amazon S3** (object storage) and **Amazon DynamoDB** (managed NoSQL) to power global enterprise applications. Today, S3 stores over 300 trillion objects and processes tens of millions of requests per second.

```mermaid
flowchart TD
    subgraph DynamoDBSystem["Amazon DynamoDB Distributed NoSQL Platform"]
        ReqRouter["Request Router Tier"]
        
        subgraph PaxosGroup["Storage Partition 1 (Paxos 3-AZ Consensus Group)"]
            LeaderDB[("Leader Node (AZ-1)<br/>[Primary Writes & Reads]")]
            Follower1[("Replica Node (AZ-2)<br/>[Paxos Participant]")]
            Follower2[("Replica Node (AZ-3)<br/>[Paxos Participant]")]
            LeaderDB <== "Paxos Consensus Replicas" ==> Follower1 & Follower2
        end
        ReqRouter --> LeaderDB
    end

    subgraph S3System["AWS S3 Planetary Object Storage Subsystem"]
        S3GW["S3 REST Frontend Gateway"]
        
        subgraph DurabilityEngine["11-Nines Durability Engine"]
            RSEncoder["Reed-Solomon (8+4) Erasure Encoder"]
            Scrubber["Background Storage Scrubber Engine<br/>(Detects Bit-Rot & Rebuilds Lost Shards)"]
        end

        subgraph AZDisks["Multi-AZ Storage Nodes"]
            AZ1_Nodes["AZ-1 Storage Node Array"]
            AZ2_Nodes["AZ-2 Storage Node Array"]
            AZ3_Nodes["AZ-3 Storage Node Array"]
        end

        S3GW --> RSEncoder
        RSEncoder ==> AZ1_Nodes & AZ2_Nodes & AZ3_Nodes
        Scrubber -. "Continuous Verification & Self-Healing" .-> AZ1_Nodes & AZ2_Nodes & AZ3_Nodes
    end
```

#### Architectural Breakthroughs:
1. **DynamoDB Paxos Partitioning**: DynamoDB automatically shards tables into 10 GB partitions based on hash partition keys. Each partition runs a 3-node storage replica group across three Availability Zones (AZs) coordinated by **Paxos Consensus**, ensuring single-digit millisecond latency and seamless failover.
2. **S3 11-Nines Durability Engine**: S3 continuously executes automated background **Scrubber Engines** that hash object shards, detect silent bit rot or disk degradation using CRC checksums, and automatically rebuild degraded parity blocks using Reed-Solomon equations before data loss can occur.

---

## 📝 End-of-Chapter Exercises

### Exercise 1: Distributed Quorum & CAP/PACELC Trade-off Calculation
A global e-commerce cloud database uses a 5-node replica cluster ($N = 5$).
- (a) Evaluate the consistency and availability properties for the following operational configurations:
  - Config A: $W = 3, R = 3$
  - Config B: $W = 5, R = 1$
  - Config C: $W = 2, R = 2$
- (b) Under a network partition where the cluster splits into two network partitions containing 3 nodes and 2 nodes respectively, calculate which partition can accept read and write operations under Config A vs Config B.
- (c) Apply the **PACELC Theorem** (If Partition ($P$), trade Availability ($A$) vs. Consistency ($C$); Else ($E$), trade Latency ($L$) vs. Consistency ($C$)) to classify MongoDB, DynamoDB, and Spanner.

### Exercise 2: Consistent Hashing Ring Rebalancing Math
A distributed storage ring has a keyspace ranging from $0$ to $2^{32}-1$. The cluster contains $N = 4$ physical nodes, each allocated $V = 64$ virtual nodes.
- (a) Calculate the expected percentage of total keys assigned to each physical node under ideal uniform distribution.
- (b) When a 5th physical node is added to the cluster, calculate the exact fraction of total keys that must be migrated across the network to rebalance the ring.
- (c) Compare this result against a naive hash allocation function $h(k) = k \bmod N$, demonstrating why naive hashing causes an catastrophic $80\%$ key migration.

### Exercise 3: LSM-Tree Compaction & Write Amplification Derivation
Consider a Leveled Compaction LSM-Tree storage engine with a size ratio $T = 10$ (each Level $L+1$ is 10 times larger than Level $L$).
- (a) If the `MemTable` size is 64 MB and the LSM-tree contains 4 levels ($L_1$ to $L_4$), calculate the total storage capacity of the database.
- (b) Derive the theoretical **Write Amplification Factor (WAF)** for a write operation that traverses from $L_0$ to $L_4$ during background compaction.
- (c) Explain why random 4 KB write throughput on an LSM-Tree outperforms a B+ Tree by orders of magnitude, but point lookup latency ($GET$) is higher.

### Exercise 4: Reed-Solomon Erasure Coding Availability & Durability Proof
An object storage system implements an $8 + 4$ Reed-Solomon erasure coding scheme across independent storage nodes. Individual disk drives have an annual failure rate (AFR) of $p = 2\% = 0.02$.
- (a) Derive the binomial probability formula for the probability that an object suffers unrecoverable data corruption (defined as $> 4$ simultaneous drive failures out of 12).
- (b) Calculate the resulting annual durability percentage (number of nines) of the storage system.
- (c) Calculate the net storage savings in Terabytes if 1 Petabyte of raw object data is stored using $8 + 4$ Erasure Coding versus 3-way Multi-Region Replication.

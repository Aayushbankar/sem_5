# P07 — Cloud Storage: Study & Comparison

**Subject:** Cloud and Data Center Technology | **Unit:** 4 | **Approx. Hrs:** 2
**PrO (verbatim):** *A study and comparison on various cloud storage like Amazon S3, Google Cloud Storage, Microsoft Azure Blob Storage, IBM Cloud Object Storage for its performance and scalability*

---

## 1. Objective
- Understand the **object storage** model used by all four services.
- Compare **durability, storage classes/tiers, scalability, pricing, performance, consistency**.
- Provide practical guidance on which service/tier to pick.

## 2. Theory (exam-ready)
All four are **object storage** services (Unit 4: object vs block vs file):
- Data is stored as **objects** in **buckets**, addressed by a URL `bucket/key`.
- **Metadata** (HTTP headers) + **globally unique ID (ETag)** per object.
- Highly **durable** by replicating across devices/regions; **scalable** to exabytes; accessed over **HTTPS (REST/S3 API)**.
- **Storage classes/tiers** trade cost vs access frequency: hot (frequent) → cold/archive (rare, cheap).
- **Consistency model:** most S3/GCS object stores are *strongly consistent* for PUT/GET (post-2020), while some earlier NoSQL backends were eventually consistent.

## 3. Comparison table

| Criterion | Amazon S3 | Google Cloud Storage | Azure Blob Storage | IBM Cloud Object Storage |
|---|---|---|---|---|
| **Storage model** | Object (buckets/keys) | Object (buckets/objects) | Object (containers/blobs) | Object (buckets/objects) |
| **Durability** | 99.999999999% (11 nines), 3 AZs by default | 99.999999999% (11 nines) | 99.999999999% (11 nines, RA-GRS) | 99.999999999% (11 nines), erasure-coded |
| **Storage classes / tiers** | S3 Standard, IA, OneZone-IA, Glacier (Flexible, Instant, Deep Archive) | Standard, Nearline, Coldline, Archive | Hot, Cool, Cold, Archive tiers (+ Blob access tiers) | Standard (Regional/Cross-Regional), Vault, Cold Vault, Flexible |
| **Scalability** | Infinite (exabytes); auto-partitioned; S3 + S3 Glacier deep archive | Infinite; dual-region/buckets; GCS buckets auto-scale | Infinite; single blob up to ~5 TB; account limits configurable | Infinite; CRR across regions; single object up to 10 TB |
| **Pricing model** | Per GB-month + PUT/GET requests + data transfer out + optional tier | Per GB-month + operations + network egress (+ early-delete fees) | Per GB-month + operations + data egress; archive early-delete | Per GB-month + requests + egress; flat regional pricing |
| **Performance** | 3,500 PUT / 5,500 GET requests per second per prefix (auto-scale); S3 Express OneZone for microsecond | Comparable; uses anycast + regional buckets; strong SLOs | Per-partition throughput limits; Premium/Block Blob for higher IOPS | S3 API compatible; high throughput via CRR and multipart; good for AI workloads |
| **Consistency** | **Strongly consistent** (all reads see latest writes, after 2020) | **Strongly consistent** | **Strongly consistent** (Blob storage) | **Strongly consistent** |
| **Best-fit** | General-purpose AWS object storage (media, backups, static sites, data lakes) | GCP-native workloads, BigQuery/ML pipelines, media | Windows/.NET + Azure ecosystems, file shares (NFS v3), media | Enterprises on IBM Cloud, regulatory/geographic requirements, AI/analytics |

## 4. Storage classes — the cost/latency trade-off (S3 as the model)
| Class | Use | Typical retrieval |
|---|---|---|
| **Standard** | Frequent access (websites, hot analytics) | milliseconds |
| **Infrequent Access (IA)** | Backups, DR, long-lived media | milliseconds |
| **OneZone-IA** | Regenerable, lower durability (single AZ) | milliseconds |
| **Glacier Instant** | Archived data, rare but instant access | milliseconds |
| **Glacier Flexible** | Archive 90+ days | minutes–hours |
| **Glacier Deep Archive** | 180+ days, compliance archives | ~12 h |

> Guidance: **hot data → Standard**, **rarely read → Glacier/Archive**, **GDPR/compliance → archive with object lock / retention policies**, and keep **at least one cross-region copy** for DR.

## 5. Which one should you choose? (guidance)
1. **Stick to your cloud:** S3 (AWS), GCS (GCP), Blob (Azure), IBM COS (IBM) — avoids egress fees and integrates best.
2. **All four are S3-API friendly:** IBM COS and MinIO (P09) even speak the S3 API, so code is portable.
3. **Performance-critical:** use the hot tier + multipart upload for large objects; regional buckets for latency.
4. **Cost-sensitive archive:** use Glacier/Archive tiers with lifecycle rules (auto-move objects after N days).
5. **Compliance:** enable **versioning + object lock (WORM)** + server-side encryption (see P09 for a hands-on SSE demo).

## 6. Worked example (exam-style justification)
> *"Store 50 TB of CCTV footage, accessed rarely, in AWS, minimum cost."* → S3 Standard → lifecycle rule → **Glacier Deep Archive** after 30 days; **versioning + object lock** enabled for forensic evidence. Cost drops ~80% vs Standard.

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Object-storage theory (§2) with a small diagram (bucket → object → metadata).
3. Comparison table (§3).
4. Storage-class tier table + lifecycle example (§4, §6).
5. Guidance list (§5).
6. Conclusion.

## 8. Viva Q&A
1. **Object vs block vs file storage?** — Object: flat key-value, HTTP API, metadata; Block: raw volumes mounted by VMs; File: NFS/SMB shares.
2. **What is durability?** — Probability data survives (11 nines = extremely high) via replication/erasure coding.
3. **What are storage classes?** — Tiers trading cost for access frequency (Standard → Archive).
4. **Is S3 strongly consistent?** — Yes since December 2020: reads reflect the latest write.
5. **What is multipart upload?** — Uploading large objects in parts in parallel; speeds up big transfers.

## 9. Resources
- Amazon S3: https://aws.amazon.com/s3/
- Google Cloud Storage: https://cloud.google.com/storage
- Azure Blob Storage: https://azure.microsoft.com/products/storage/blobs/
- IBM Cloud Object Storage: https://www.ibm.com/cloud/object-storage
- S3 storage classes: https://aws.amazon.com/s3/storage-classes/

# P06 — Cloud Databases: Study & Comparison

**Subject:** Cloud and Data Center Technology | **Unit:** 4 | **Approx. Hrs:** 4
**PrO (verbatim):** *A study and comparison on various cloud databases like Amazon RDS, Google Cloud SQL, Microsoft Azure SQL Database, IBM Db2 on Cloud, Firebase Realtime Database (NoSQL), MongoDB Atlas (NoSQL), Oracle Cloud Autonomous Database*

---

## 1. Objective
- Understand the two families of cloud databases: **relational (SQL)** and **NoSQL**.
- Compare 7 services over: **type, pricing model, scaling, high availability, best-fit use case**.
- Produce a "how to choose" decision guide.

## 2. Theory (exam-ready)
A **cloud database** is a database hosted and managed by a cloud provider. **Managed services** remove admin burden (backups, patching, HA, scaling) — you pay for the convenience. Two families:

- **SQL (relational):** tables, fixed schema, ACID transactions, SQL. Vertical scaling first.
- **NoSQL:** flexible schema, distributed, typically **eventually consistent**, horizontal scaling. Sub-types: **document** (MongoDB, Firebase), **key-value**, **wide-column**, **graph**.

**Scale & replication (Unit 4):** *vertical scaling* (bigger VM) vs *horizontal scaling* (more nodes, sharding); **replication** copies data to multiple nodes/regions for **availability** and **durability** (see P07).

## 3. Comparison table

| Criterion | Amazon RDS | Google Cloud SQL | Azure SQL Database | IBM Db2 on Cloud | Firebase RTDB | MongoDB Atlas | Oracle Autonomous DB |
|---|---|---|---|---|---|---|---|
| **Provider** | AWS | Google Cloud | Microsoft Azure | IBM Cloud | Google (Firebase) | MongoDB, Inc. | Oracle Cloud |
| **Type** | SQL (MySQL, Postgres, MariaDB, Oracle, SQL Server) | SQL (MySQL, Postgres, SQL Server) | SQL (SQL Server engine) | SQL (Db2) | **NoSQL** (JSON, realtime) | **NoSQL** (document/BSON) | SQL (+ Document API, JSON) |
| **Pricing model** | Pay per instance class + storage + I/O | Pay per instance tier (vCPU/mem) + storage | DTU/vCore tiers + storage | Pay per instance/vCPU + storage | Pay per data + bandwidth (realtime sync) | Pay per cluster tier + RAM + storage (free M0 tier) | Pay per OCPU + storage; "autonomous" auto-tunes |
| **Scaling** | Vertical + read replicas, Aurora serverless option | Vertical + read replicas, Cloud SQL for scaling limits | Vertical (vCore/DTU) + read scale-out; Hyperscale | Vertical + HADR; Db2 Warehouse for analytics | Auto-sharded realtime tree; horizontal | **Horizontal by design** (sharded clusters) | **Autonomous**: auto CPU/storage scaling, no tuning |
| **High availability** | Multi-AZ standby (sync) + cross-region replicas | Regional failover + cross-region read replicas | Built-in SLA; geo-replication (active geo-replication) | HADR (log-shipping), rolling upgrade, multi-region | Multi-region replication, offline cache | Multi-node replica sets; auto-failover | Autonomous (RAC-style), automatic failover, 99.95% SLA |
| **Best-fit use case** | Web/ERP/e-com apps with RDBMS skill base | GCP-hosted apps, G Suite/Dataflow integration | Enterprise .NET/SQL Server shops on Azure | Bank/enterprise analytics, existing Db2 estate | Mobile/live-collaboration apps needing realtime sync | Apps needing flexible documents + horizontal scale, dev teams | Enterprises wanting hands-off, self-tuning mission-critical DBs |

## 4. How to choose (decision guide)

```
Does your app need realtime sync on mobile? ── Yes ─► Firebase RTDB
             │ No
Fixed/rigid schema + heavy SQL + ACID? ──────── Yes ─► (SQL) Which cloud?
             │ No                                                │
Flexible schema, JSON docs, big scale? ──────── Yes ─► MongoDB Atlas
             │ No
Autonomous, zero-DBA tuning required? ────────── Yes ─► Oracle Autonomous
             │ No
Which provider do you already use?
   AWS ─► Amazon RDS     GCP ─► Cloud SQL     Azure ─► Azure SQL     IBM ─► Db2 on Cloud
```

### Key decision factors
1. **Data model:** tables+SQL → SQL family; documents/JSON → NoSQL.
2. **Transaction needs:** strong ACID (banking, orders) → SQL; high-scale append/read-heavy → NoSQL.
3. **Cloud lock-in / existing stack:** pick the provider you already run on to save cost and latency.
4. **Ops effort:** if you have no DBA, prefer **fully managed / autonomous** (Oracle ATP, RDS Multi-AZ, Atlas).
5. **Scaling mode:** unpredictable spikes → horizontal-friendly (Atlas); predictable → vertical (cheaper).
6. **Budget:** start with free/small tiers (Atlas M0, Cloud SQL micro, Firebase Spark) for prototyping.

## 5. Worked example (exam-style justification)
> *"Our startup builds a chat app on GCP with realtime message sync."* → **Firebase Realtime Database** because it pushes changes to clients in real time, stores flexible JSON, and integrates with Firebase Auth — despite being NoSQL (eventually consistent), which is fine for chat.
> *"Our bank needs a highly consistent ledger."* → **Amazon RDS PostgreSQL Multi-AZ** (or Oracle ATP) because ACID transactions and synchronous standby HA outweigh flexible scaling.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Short theory (§2) with the SQL vs NoSQL table.
3. Big comparison table (§3).
4. Two worked scenarios (§5) justifying the choice.
5. Decision guide flowchart (§4).
6. Conclusion.

## 7. Viva Q&A
1. **SQL vs NoSQL?** — SQL: fixed schema, ACID, vertical scale; NoSQL: flexible schema, horizontal scale, eventual consistency.
2. **What is a managed database?** — Provider handles provisioning, patching, backup, HA; you use it via APIs/SQL.
3. **Vertical vs horizontal scaling?** — Bigger machine vs more machines (sharding/replicas).
4. **Why choose Atlas for a document app?** — Native horizontal sharding + free tier + flexible schema.
5. **What does "autonomous" mean in Oracle ATP?** — Self-driving: auto-provisioning, auto-tuning, auto-patching, auto-scaling.

## 8. Resources
- Amazon RDS: https://aws.amazon.com/rds/
- Google Cloud SQL: https://cloud.google.com/sql
- Azure SQL Database: https://azure.microsoft.com/products/azure-sql/database/
- IBM Db2 on Cloud: https://www.ibm.com/cloud/db2
- Firebase Realtime Database: https://firebase.google.com/docs/database
- MongoDB Atlas: https://www.mongodb.com/products/platform/atlas-database
- Oracle Autonomous Database: https://www.oracle.com/autonomous-database/

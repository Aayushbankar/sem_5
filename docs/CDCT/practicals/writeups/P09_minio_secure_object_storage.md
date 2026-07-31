# P09 — Secure Object Storage with MinIO (Access Control + SSE)

**Subject:** Cloud and Data Center Technology | **Unit:** 5 | **Approx. Hrs:** 2
**PrO (verbatim):** *To implement secure object storage with access control and encryption using an open-source cloud storage platform.*

---

## 1. Objective
- Deploy **MinIO** (open-source, S3-compatible object storage) with **Docker Compose**.
- Create buckets, users, and **IAM policies** → demonstrate **access control** (RBAC).
- Enable **server-side encryption (SSE-S3, AES-256)** and verify objects are encrypted at rest.

> ✅ **Ran for real in this environment** — Docker + MinIO were available. The console output below is the **actual captured run**.

## 2. Theory (exam-ready)
**MinIO** is a popular open-source **object storage** server that speaks the **Amazon S3 API** (buckets, objects, IAM policies). Security features used here:

- **Access control (IAM):** users get policies (JSON) describing allowed `s3:Action`s on `arn:aws:s3:::bucket/*` resources — exactly like AWS S3.
- **Server-Side Encryption (SSE-S3):** the server encrypts every object with AES-256-GCM *before* writing to disk; clients need no key handling. With `MINIO_KMS_SECRET_KEY` MinIO runs a built-in single-key KMS.
- **Least privilege:** a *read-only* user can `GET` but **not** `PUT`; an *admin* user can `PUT`.

## 3. Files used
| File | Purpose |
|---|---|
| [`p09_docker-compose.yml`](../code/p09_docker-compose.yml) | MinIO server (ports 9000 API / 9001 console) + KMS key |
| [`p09_readonly_policy.json`](../code/p09_readonly_policy.json) | IAM policy: `GetObject`, `ListBucket` (read-only) |
| [`p09_admin_policy.json`](../code/p09_admin_policy.json) | IAM policy: `PutObject`, `GetObject`, `DeleteObject` |
| [`p09_bucket_policy.json`](../code/p09_bucket_policy.json) | Example *bucket* policy (AWS-style) for reference |
| [`p09_setup.sh`](../code/p09_setup.sh) | End-to-end setup + verification script |

## 4. Steps

### 4.1 Start the server
```bash
cd practicals/code
docker compose -f p09_docker-compose.yml up -d
# MinIO API  → http://localhost:9000   Console → http://localhost:9001
docker ps --filter name=p09-minio
```
Compose sets `MINIO_KMS_SECRET_KEY=cdct-sse-key:<base64-32-byte-key>` which enables the built-in KMS (needed for `mc encrypt set sse-s3`).

### 4.2 Install the `mc` client
```bash
# Linux
wget https://dl.min.io/client/mc/release/linux-amd64/mc && chmod +x mc && sudo mv mc /usr/local/bin/
# macOS
brew install minio/stable/mc
```

### 4.3 Run the setup script
```bash
cd practicals/code
bash p09_setup.sh
```

## 5. Actual console output (captured run)
```
==> [1] Configure mc alias for the MinIO server
Added `cdct` successfully.
==> [2] Create a bucket
Bucket created successfully `cdct/cdct-documents`.
==> [3] Enable server-side encryption (SSE-S3, AES-256) for the bucket
Auto encryption configuration has been set successfully for cdct/cdct-documents
Auto encryption 'sse-s3' is enabled
==> [4] Create users with different privileges
Added user `read-only-user` successfully.
Added user `admin-user` successfully.
==> [5] Create IAM policies (see p09_readonly_policy.json / p09_admin_policy.json)
Created policy `cdct-readonly` successfully.
Created policy `cdct-admin` successfully.
==> [6] Attach policies to the users
Attached Policies: [cdct-readonly]
To User: read-only-user
Attached Policies: [cdct-admin]
To User: admin-user
==> [7] Upload a test file (auto-encrypted by the bucket default)
`/work/secret-report.txt` -> `cdct/cdct-documents/secret-report.txt`
┌───────┬─────────────┬──────────┬────────────┐
│ Total │ Transferred │ Duration │ Speed      │
│ 43 B  │ 43 B        │ 00m00s   │ 3.11 KiB/s │
└───────┴─────────────┴──────────┴────────────┘
--- List objects in the bucket ---
[2026-07-31 11:26:51 UTC]    43B STANDARD secret-report.txt
--- Object metadata (shows Encryption: SSE-S3) ---
Name      : secret-report.txt
Date      : 2026-07-31 11:26:51 UTC
Size      : 43 B
ETag      : f75f60b6dba0a65e0ee7151f52d23305
Type      : file
Encryption: SSE-S3
Metadata  :
  Content-Type: text/plain

==> [8] Access-control checks
--- read-only user: GET should SUCCEED ---
Added `ro` successfully.
Confidential report for CDCT Practical P09
--- read-only user: PUT should be DENIED ---
`/work/secret-report.txt` -> `ro/cdct-documents/should-fail.txt`
mc: <ERROR> Failed to copy `/work/secret-report.txt`. Insufficient permissions to access this path `http://localhost:9000/cdct-documents/should-fail.txt`
EXPECTED: read-only user write is DENIED by IAM policy
--- admin user: PUT should SUCCEED ---
Added `ad` successfully.
`/work/secret-report.txt` -> `ad/cdct-documents/admin-report.txt`
┌───────┬─────────────┬──────────┬────────────┐
└───────┴─────────────┴──────────┴────────────┘
[2026-07-31 11:26:55 UTC]    43B STANDARD admin-report.txt
[2026-07-31 11:26:51 UTC]    43B STANDARD secret-report.txt
==> DONE. Web console: http://localhost:9001  (root creds above)
```

## 6. Interpretation (what was proved)
- **Encryption:** `mc stat` shows `Encryption: SSE-S3` → the object is **encrypted at rest** (AES-256) even though the upload itself was plain HTTP.
- **Access control:** `read-only-user` can **read** the file (`mc cat` succeeds) but **cannot write** (`PUT` → *Insufficient permissions*), while `admin-user` **can** write.
- **Least privilege:** policies grant only the actions each role needs — a textbook RBAC setup, identical in spirit to AWS S3.

## 7. Troubleshooting notes (from the real run)
- `MINIO_KMS_SECRET_KEY` must be `<key-name>:<base64-encoded-32-byte-key>` — a **wrong byte length makes MinIO refuse to start** (`kms: invalid key length`).
- MinIO standalone: for user-level access control use **IAM user policies** (`mc admin policy create/attach`); a **bucket policy** with a specific `Principal` only matches when the ARN account matches the deployment (use `arn:aws:iam::*:user/<name>` in MinIO).

## 8. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. `docker compose up` + `docker ps` evidence.
3. Setup-script output (§5).
4. Explanation: encryption metadata + denied/allowed operations (§6).
5. Screenshot of the console (http://localhost:9001) showing the bucket + object.
6. Conclusion.

## 9. Viva Q&A
1. **What is MinIO?** — Open-source S3-compatible object storage server.
2. **What is SSE-S3?** — Server-side encryption where the server encrypts objects with AES-256; no client key management.
3. **How is access controlled?** — IAM users + JSON policies (`Effect`/`Action`/`Resource`); least privilege.
4. **Why is encryption at rest important?** — Protects data if disks/backups are stolen; satisfies compliance.
5. **MinIO vs AWS S3?** — Same S3 API; MinIO runs on your own hardware (private cloud / on-prem).

## 10. Resources
- MinIO docs: https://min.io/docs/minio/linux/index.html
- MinIO Docker quickstart: https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-single-node-docker.html
- Server-side encryption: https://min.io/docs/minio/linux/operations/server-side-encryption.html
- `mc` client downloads: https://dl.min.io/client/mc/release/
- S3 IAM policies (equivalent concept): https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html

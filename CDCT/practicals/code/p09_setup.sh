#!/usr/bin/env bash
# ============================================================
# P09 - MinIO: secure object storage with access control & SSE
# Run AFTER `docker compose up -d` (see p09_docker-compose.yml)
# Requires the `mc` client:  brew install minio/stable/mc  (macOS)
# or download from https://dl.min.io/client/mc/release/linux-amd64/mc
# ============================================================
set -euo pipefail

ALIAS="cdct"
ENDPOINT="http://localhost:9000"
ROOT_USER="minioadmin"
ROOT_PASSWORD="minioadmin123"

echo "==> [1] Configure mc alias for the MinIO server"
mc alias set $ALIAS "$ENDPOINT" "$ROOT_USER" "$ROOT_PASSWORD"

echo "==> [2] Create a bucket"
mc mb --ignore-existing $ALIAS/cdct-documents

echo "==> [3] Enable server-side encryption (SSE-S3, AES-256) for the bucket"
mc encrypt set sse-s3 $ALIAS/cdct-documents
mc encrypt info $ALIAS/cdct-documents

echo "==> [4] Create users with different privileges"
mc admin user add $ALIAS read-only-user 'ReadOnly#2026'
mc admin user add $ALIAS admin-user 'Admin#2026'

echo "==> [5] Create IAM policies (see p09_readonly_policy.json / p09_admin_policy.json)"
mc admin policy create $ALIAS cdct-readonly ./p09_readonly_policy.json
mc admin policy create $ALIAS cdct-admin ./p09_admin_policy.json

echo "==> [6] Attach policies to the users"
mc admin policy attach $ALIAS cdct-readonly --user read-only-user
mc admin policy attach $ALIAS cdct-admin --user admin-user

echo "==> [7] Upload a test file (auto-encrypted by the bucket default)"
echo "Confidential report for CDCT Practical P09" > ./secret-report.txt
mc cp ./secret-report.txt $ALIAS/cdct-documents/secret-report.txt

echo "--- List objects in the bucket ---"
mc ls --recursive $ALIAS/cdct-documents

echo "--- Object metadata (shows Encryption: SSE-S3) ---"
mc stat $ALIAS/cdct-documents/secret-report.txt

echo "==> [8] Access-control checks"
echo "--- read-only user: GET should SUCCEED ---"
mc alias set ro "$ENDPOINT" read-only-user 'ReadOnly#2026'
mc cat ro/cdct-documents/secret-report.txt

echo "--- read-only user: PUT should be DENIED ---"
if mc cp ./secret-report.txt ro/cdct-documents/should-fail.txt; then
  echo "UNEXPECTED: read-only user could write!"
  exit 1
else
  echo "EXPECTED: read-only user write is DENIED by IAM policy"
fi

echo "--- admin user: PUT should SUCCEED ---"
mc alias set ad "$ENDPOINT" admin-user 'Admin#2026'
mc cp ./secret-report.txt ad/cdct-documents/admin-report.txt
rm -f ./secret-report.txt
mc ls --recursive $ALIAS/cdct-documents

echo "==> DONE. Web console: http://localhost:9001  (root creds above)"

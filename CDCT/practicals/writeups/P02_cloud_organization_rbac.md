# P02 — Cloud Organization with RBAC (AWS IAM)

**Subject:** Cloud and Data Center Technology | **Unit:** 1 | **Approx. Hrs:** 4
**PrO (verbatim):** *Create a Cloud Organization in AWS/Google Cloud/or any equivalent Open Source cloud softwares like Openstack/ Eucalyptus/ OpenNebula with Rolebased access control.*

---

## 1. Objective
- Create a cloud **organization** (AWS Organizations) with a root account.
- Implement **Role-Based Access Control (RBAC)** using **IAM users, groups, and policies**.
- Produce a permission matrix and an example policy JSON.

## 2. Theory (exam-ready)
**RBAC** = users are placed in **groups**; policies are attached to **groups** (not to individual users). A user inherits every policy of its group(s). This is *manageable* because permissions change in one place.

**AWS IAM terms:**
- **Root user:** account owner; full access; should be used only for account setup (MFA mandatory).
- **IAM user:** a person/service with credentials (password + access keys) that acts inside the account.
- **Group:** a collection of users sharing the same permissions.
- **Policy:** a JSON document stating `Effect: Allow/Deny` on `Action`s for `Resource`s.
- **Role:** an identity you *assume* (no long-lived keys) — used for cross-account and service access.
- **Managed policy vs inline policy:** managed = reusable library; inline = embedded in one user/group.

```mermaid
flowchart TB
    Root[Organization root<br/>(management account)] --> OrgA[Org Unit: IT]
    Root --> OrgB[Org Unit: Developers]
    OrgA --> A1[CloudAdmin user]
    OrgA --> A2[NetworkAdmin user]
    OrgB --> B1[DevGroup]
    B1 --> U1[alice]
    B1 --> U2[bob]
    B1 --> P1[Policy: EC2-Control + S3-ReadOnly]
```

## 3. Steps (AWS console)

### 3.1 Create the organization (root account)
1. Sign in to the **root account** (`aws.amazon.com → Sign in as Root`).
2. Enable **MFA** on the root account (Security Credentials → Assign MFA device).
3. Open **AWS Organizations** → *Create organization*. This automatically creates the management account and lets you add child **accounts** (e.g., `prod`, `dev`) under **Organizational Units (OUs)** — this is the "cloud organization" structure.
4. (Optional) Enable **SCPs** (Service Control Policies) at the OU level to cap what child accounts can do.

### 3.2 Create users
`IAM → Users → Create user`
| User | Groups | Purpose |
|---|---|---|
| `alice` | `cloud-team` | Cloud resource admin (start/stop VMs, read backup bucket) |
| `bob` | `cloud-team` | Same as alice (team consistency) |
| `ro-user` | `backup-readers` | Read-only access to the backup bucket |

### 3.3 Create groups
`IAM → User groups → Create group`
| Group | Attached policy |
|---|---|
| `cloud-team` | `CDCT-CloudTeam` (custom, see §4) |
| `backup-readers` | `AmazonS3ReadOnlyAccess` (AWS managed) |
| `admins` | `AdministratorAccess` (restricted to 1-2 people) |

### 3.4 Attach the policy
1. `IAM → Policies → Create policy → JSON` → paste the JSON from [`p02_iam_policy.json`](../code/p02_iam_policy.json).
2. Name it `CDCT-CloudTeam`.
3. `IAM → User groups → cloud-team → Permissions → Add permissions → Attach policies → CDCT-CloudTeam`.

### 3.5 Verify RBAC (important!)
- Log in as `alice` (IAM user) → you can *start/stop* EC2 instances but **cannot** `iam:CreateUser`.
- `aws iam get-user` (CLI) works only for the configured account; `iam:CreateAccessKey` is **Denied** by the policy.

## 4. Example IAM policy JSON
See full file: [`p02_iam_policy.json`](../code/p02_iam_policy.json)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Sid": "CloudTeamEC2Control",
      "Effect": "Allow",
      "Action": ["ec2:DescribeInstances", "ec2:StartInstances",
                 "ec2:StopInstances", "ec2:RebootInstances"],
      "Resource": "*" },
    { "Sid": "CloudTeamS3ReadOnly",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket", "s3:GetBucketLocation"],
      "Resource": ["arn:aws:s3:::cdct-org-backups",
                   "arn:aws:s3:::cdct-org-backups/*"] },
    { "Sid": "DenyIAMChanges",
      "Effect": "Deny",
      "Action": ["iam:CreateUser", "iam:DeleteUser",
                 "iam:AttachUserPolicy", "iam:DetachUserPolicy",
                 "iam:CreateAccessKey"],
      "Resource": "*" }
  ]
}
```
**Why this design:** the group can operate *compute* resources, only *read* backups, and can **never** touch IAM — the classic least-privilege RBAC pattern. An explicit `Deny` beats any `Allow`.

## 5. Permission matrix
| Action | Root | admin group | cloud-team (alice/bob) | backup-readers |
|---|---|---|---|---|
| Start/Stop EC2 instance | ✅ | ✅ | ✅ | ❌ |
| List EC2 instances | ✅ | ✅ | ✅ | ❌ |
| Read S3 backup bucket | ✅ | ✅ | ✅ | ✅ |
| Write/Delete S3 objects | ✅ | ✅ | ❌ | ❌ |
| Create user/access key | ✅ | ✅ | **Deny** | ❌ |
| Billing / organization | ✅ | ✅ | ❌ | ❌ |

## 6. Open-source equivalent (OpenStack Keystone)
| AWS IAM | OpenStack Keystone |
|---|---|
| Account/Org | Project (tenant) |
| User | User |
| Group | Group |
| Policy (JSON) | Role (e.g., `admin`, `member`, `reader`) |
| Attach policy to group | Assign role to user/group on a project |
| SCP (OU level) | Domain-level role assignments |
```bash
# OpenStack CLI equivalent of the AWS steps
openstack user create --password 'ChangeMe!' --domain default alice
openstack group create cloud-team
openstack group add user cloud-team alice
openstack role add --group cloud-team --project cdct-proj member
openstack user list --project cdct-proj
```
Eucalyptus follows the AWS model (EC2/S3 APIs); OpenNebula uses its own `oneuser`/`onegroup` with ACLs. The RBAC idea is identical everywhere: *identity + role + resource + action*.

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Organization tree (3.1) with OUs and accounts.
3. Screenshots: users list, groups list, policy JSON, permissions attached to `cloud-team`.
4. Permission matrix (§5).
5. Proof: log in as `alice`, show an allowed action (stop instance) and a denied action (create user) — note: free tier EC2/CloudShell works without cost.
6. Conclusion: why group-based RBAC beats per-user permissions.

## 8. Viva Q&A
1. **What is RBAC?** — Granting permissions based on roles; users are mapped to roles/groups.
2. **Root user vs IAM user?** — Root = account owner (MFA only); IAM users get least-privilege scoped access.
3. **Why use groups instead of per-user policies?** — Single source of truth; a new employee inherits the right permissions instantly.
4. **What does an explicit Deny do?** — Overrides any Allow; used to block dangerous actions (IAM changes) even for powerful roles.
5. **IAM vs SCP?** — IAM governs what a *user/role* can do; SCP governs what a *child account* can do in an organization.

## 9. Resources
- AWS IAM docs: https://docs.aws.amazon.com/iam/
- AWS Organizations docs: https://docs.aws.amazon.com/organizations/
- IAM policy reference: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
- OpenStack Keystone RBAC: https://docs.openstack.org/keystone/latest/user/rbac.html
- AWS free tier (no-cost lab): https://aws.amazon.com/free/

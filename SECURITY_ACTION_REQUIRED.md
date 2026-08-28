# ⚠️ SECURITY ACTION REQUIRED (Founder Verification Checklist)

**Repository:** `khairulxshafiq/Aura-dashboard`  
**Date:** 28 August 2026  
**Action Required:** Manual Credential Revocation & Rotation  

---

## 1. Exposed Credential Category

A historic GitHub Personal Access Token (PAT) was detected in the local repository remote configuration (`.git/config`). 

In accordance with Phase 0 Security Containment rules, the local remote URL has been immediately sanitized and switched to SSH (`git@github.com:khairulxshafiq/Aura-dashboard.git`). However, because removing a credential from a configuration file does not invalidate it on the remote provider, manual revocation by founder Matrol is mandatory.

---

## 2. Founder Action Instructions

### Step 1: Revoke Historic GitHub Personal Access Token (PAT)
1. Log in to GitHub: [https://github.com](https://github.com)
2. Navigate to **Settings** ➔ **Developer Settings** ➔ **Personal Access Tokens** (Tokens classic / Fine-grained tokens).
3. Locate the token previously generated for `Aura-dashboard` or automated deployment.
4. Click **Revoke** or **Delete**.

### Step 2: Verify Glance Ingest API Write Credentials
1. Check Glance API console / Fly.dev ingest settings.
2. If `GLANCE_WRITE_KEY` was publicly exposed, regenerate the write key via Glance console.
3. Update the new key in the Hermes VPS environment file (`~/.hermes/.env` as `GLANCE_WRITE_KEY`).

---

## 3. Confirmation Checklist

- [ ] GitHub PAT revoked on GitHub Developer Settings
- [ ] SSH key authentication verified for local `git push`
- [ ] Glance API write key regenerated on Glance console (if applicable)
- [ ] New credentials saved safely in `~/.hermes/.env` (Mode 600)

---

**Status:** Pending Founder Manual Revocation  
**Note:** Plaintext secret values are strictly `[REDACTED]` and never recorded in this document.

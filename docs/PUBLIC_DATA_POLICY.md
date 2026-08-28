# Public Data Policy & Sanitization Rules

**Repository:** `khairulxshafiq/Aura-dashboard`  
**Target Surface:** Public GitHub Pages (`khairulxshafiq.github.io/Aura-dashboard/`)  

---

## 1. Classification Matrix

### Category A: Public (Allowed on GitHub Pages)
- Sanitized system status (`HEALTHY`, `DEGRADED`, `OFFLINE`)
- Aggregated hardware utilization percentages (`ram_used_pct`, `cpu_pct`, `disk_pct`)
- Public agent roster (names, aliases, roles, personas, triggers, public status)
- System prompt cache hit percentage
- ISO-8601 generation timestamp (`generated_at`) and version numbers

### Category B: Internal (Restricted — Masked or Excluded from Public Output)
- Specific process IDs (PIDs)
- Local filesystem paths (e.g. `/home/ubuntu/...`)
- Internal port numbers and daemon service names
- Token counts and estimated USD cost figures

### Category C: Confidential (Prohibited on GitHub Pages — Private Surface Only)
- Live stock portfolio holdings, quantities, purchase prices, and P&L figures
- Financial revenue logs, OPEX breakdowns, and sales figures
- Raw Luma AGY execution logs, terminal command traces, and file diffs
- Internal Telegram chat IDs and user IDs

### Category D: Secret (Strictly Forbidden Anywhere)
- API keys (DeepSeek, Replicate, Telegram, Airtable, Groq, Google)
- Service Account credentials and SSH keys
- Database contents and environment secret files (`.env`, `.env.secrets`)

---

## 2. Redaction & Masking Rules

1. **API Keys & Tokens:** Must be masked to prefix or completely omitted (`[REDACTED]`).
2. **Infrastructure IP Addresses:** Raw IP addresses must never be hardcoded into public JSON or HTML files. Use logical node labels (`Hermes VPS`, `Luma GCP VM`).
3. **Paths & Usernames:** Replace absolute paths with generic placeholders (e.g., `~/.hermes/` instead of `/home/ubuntu/.hermes/`).

---

## 3. Data Freshness & Staleness Rules

- Data payload must contain `generated_at` ISO-8601 timestamp.
- Frontend consumers must calculate data age.
- Data older than **30 minutes** must display a visual `STALE` indicator.
- If data generation fails, frontend must display a graceful fallback (`FALLBACK` schema) without exposing raw error traces.

---

## 4. Publication Approval Rule

No new telemetry field, log output, or dataset may be published to GitHub Pages without explicit audit verification against this policy.

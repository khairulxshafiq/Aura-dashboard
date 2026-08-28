# Dashboard Baseline & Architecture Verification

**Date:** 28 August 2026  
**Repository:** `khairulxshafiq/Aura-dashboard`  
**Executed By:** Frontend Platform Architect & DevSecOps Lead  

---

## 1. Frontend Source Code Audit Outcome

- **Frontend Search Performed:** Searched repository recursively for `package.json`, `angular.json`, `tsconfig.json`, and `src/app/`.
- **Finding:** No Angular source code files exist in the repository.
- **Classification Outcome:** **C. Compiled Angular artifacts only** (`index.html`, `main-UOVWRWIQ.js`, `styles-N2ZSMZOP.css`).

---

## 2. Entry-Point Inventory & Disposition Matrix

| Entry Point | File Path | Current Role | Data Source | Last Git Change | Evidence-Based Status | Target Disposition |
|---|---|---|---|---|---|---|
| **Angular SPA Entry** | `index.html` | Deployed GitHub Pages index | `main-UOVWRWIQ.js` | Aug 23, 2026 | **Code Present** | Retain as SPA container pending source rebuild |
| **Static Hero Landing** | `index.v1.html` | Uncompiled HTML5 landing page | Inline static text | Aug 22, 2026 | **Code Present** | Consolidate into SPA in Phase 4 |
| **Telemetry Dashboard** | `dashboard.html` | System consumption monitor | `stats.json`, Canvas 2D | Aug 23, 2026 | **Verified Runtime** | Consolidate into SPA route in Phase 4 |
| **Intelligence Audit** | `intelligence.html` | Luma AGY execution timeline report | Static JSON array | Aug 23, 2026 | **Static** | Consolidate into dynamic route in Phase 4 |
| **Legacy Dashboard v1** | `Aura Dashboard v1.html` | Obsolete v1 design | None | Aug 21, 2026 | **Deprecated** | Safe for retirement in Phase 2 |
| **Subfolder Data** | `data/personas.json`, `data/stats.json` | Redundant copies of root files | Root JSON files | Aug 22, 2026 | **Deprecated** | Safe for deletion in Phase 2 |

---

## 3. Deployment Architecture

- **Hosting Provider:** GitHub Pages (`khairulxshafiq.github.io/Aura-dashboard/`).
- **Publishing Source:** Root directory (`/`) on branch `main`.
- **Publication Method:** Shell script `publish.sh` executing `git` and `gh` CLI.
- **Deployment Model:** Artifact-based deployment (compiled JS bundle and HTML files are checked directly into Git repository).
- **CI/CD Automation:** No automated GitHub Actions workflow (`.github/workflows/`) currently exists.

---

## 4. Runtime Dependency & Data Inventory

| Dependency / Data File | Producer | Consumer | Frequency | Classification | Data Freshness & Status |
|---|---|---|---|---|---|
| `stats.json` | `collect_stats.py` (Hermes VPS) | `dashboard.html` | Every 15 mins (cron) | **Public** (Sanitized) | **Verified Runtime** (Generates hardware & token metrics) |
| `usage_history.json` | `collect_stats.py` (Hermes VPS) | `dashboard.html` (Canvas) | Daily append (60 days) | **Public** (Aggregated) | **Verified Runtime** (Trend chart data) |
| `personas.json` | Manual / `publish.sh` | `index.v1.html`, SPA | Static definition | **Public** | **Configuration Verified** (8-9 agent definitions) |
| `glance_trading_feeds.json` | `glance_trading_push_v2.py` | iOS Glance Widgets | Dynamic push | **Internal** | **Verified Runtime** (Portfolio Glance push) |

---

## 5. Feature Evidence Matrix

| Feature | Evidence Classification | Verification Method / Proof |
|---|---|---|
| **System Consumption Monitor** | **Verified Runtime** | `collect_stats.py` generates valid `stats.json` from Linux proc; rendered by `dashboard.html`. |
| **DeepSeek Balance Tracker** | **Verified Runtime** | `collect_stats.py` queries `https://api.deepseek.com/user/balance`. |
| **Low Balance Telegram Alert** | **Verified Runtime** | `alert_balance.py` uses Telegram Bot API to send balance notifications. |
| **Glance Stock Widget Push** | **Verified Runtime** | `glance_trading_push_v2.py` queries Moomoo OpenD / KlseScreener and pushes to Glance API. |
| **Angular WebMCP SPA** | **Code Present** | Compiled bundle `main-UOVWRWIQ.js` executes in browser; source files unverified. |
| **Luma Intelligence Report** | **Static** | Hardcoded JSON payload inside `intelligence.html` from Aug 21-23, 2026. |
| **Persona Roster Grid** | **Configuration Verified** | `personas.json` schema parsed by `index.v1.html`. |

---

## 6. Baseline Risks & Architecture Unknowns

1. **Missing Frontend Source:** Lack of `src/app/` source code prevents direct TypeScript modifications. Rebuilding clean Angular 19 source is required in Phase 2.
2. **Deployment Risk:** Manual script `publish.sh` can cause accidental deployment overwrites. Transition to GitHub Actions CI/CD is required in Phase 2.
3. **Data Freshness Unknown:** If `collect_stats.py` cron job fails on Hermes VPS, `dashboard.html` falls back to static JSON without flagging data staleness.

---

## 7. Required Founder Decisions

1. **Angular Source Strategy:** Confirm approval to initialize a clean Angular 19 source repository in Phase 2.
2. **GitHub Actions CI/CD:** Confirm replacement of `publish.sh` with automated GitHub Actions workflow.

# Aura Dashboard Master Plan

## 1. Executive Summary

Aura Dashboard serves as the public presentation surface, operational telemetry monitor, and iOS Glance widget integration gateway for the **AuraOne Solopreneur AI Empire** & **Dual-Node Agent Network** (Sakluma.my).

Over the project's evolution, the dashboard accumulated multiple frontend entry points, static report pages, uncompiled legacy assets, and embedded credentials. The purpose of this revamp program is to evolve Aura Dashboard into the **AuraOne Mission Control Center**—a unified, secure, and production-grade operating system interface.

Security containment and architecture baseline verification strictly precede any UI redesign or feature implementation. This controlled approach guarantees zero data exposure, verified runtime state, and architectural stability for long-term solopreneur scaling.

---

## 2. Product Vision

Aura Dashboard is defined as the **AuraOne Mission Control Center**.

Its long-term vision is to provide a single, unified, high-density executive command interface for:
- System health and infrastructure supervision
- Multi-agent ecosystem status and active task routing
- Operational telemetry (hardware, tokens, API expenditure, logs)
- Intelligence summaries and audit reports
- Founder Human-in-the-Loop (HITL) decision workflows
- Stock market & crypto trading analytics visibility
- Solopreneur commercial performance and P&L tracking

### Structural Distinction: Public Surface vs. Private Control Plane

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       SURFACE BOUNDARY MODEL                            │
├────────────────────────────────────┬────────────────────────────────────┤
│ PUBLIC SURFACE (GitHub Pages)      │ PRIVATE CONTROL PLANE (Auth/VPS)   │
├────────────────────────────────────┼────────────────────────────────────┤
│ • Sanitized system health status   │ • HITL decision execution & buttons│
│ • Aggregated non-sensitive metrics │ • Raw logs & SSH execution traces  │
│ • Agent roster & capabilities      │ • Stock portfolio holdings & P&L   │
│ • Redacted telemetry summaries     │ • Revenue, cashflow & sales logs   │
│ • Static architecture specs        │ • Infrastructure IP & API key ops  │
└────────────────────────────────────┴────────────────────────────────────┘
```

---

## 3. Current State

Based on rigorous baseline discovery, the current state of Aura Dashboard includes:
- **Multiple Entry Points:** Coexistence of compiled Angular 19 SPA (`index.html`), static landing page (`index.v1.html`), telemetry dashboard (`dashboard.html`), and intelligence audit (`intelligence.html`).
- **Missing Source Code:** The repository contains compiled Angular JavaScript bundles (`main-UOVWRWIQ.js`) but lacks source files (`src/app/`, `package.json`, `angular.json`).
- **Static Intelligence Data:** `intelligence.html` contains static hardcoded audit logs from August 21–23, 2026 rather than a live execution feed.
- **Runtime Collector Scripts:** Python 3 scripts (`collect_stats.py`, `alert_balance.py`, `glance_trading_push_v2.py`) execute on Hermes VPS via cron to produce telemetry (`stats.json`) and push iOS Glance widgets.
- **Security Exposures:** Exposed credentials in tracked Python scripts, hardcoded tokens, and embedded access tokens in repository remote configuration.
- **Master State Drift:** Model routing descriptions and agent roster details differ from `auraone-notes/core/AURAONE_MASTER_OPERATING_STATE.md`.

---

## 4. Evidence Confidence

Every major current-state capability has been classified using rigorous evidence-based labels:

| Feature / Component | Claimed Purpose | Evidence-Based Classification | Evidence Justification |
|---|---|---|---|
| **Angular Command SPA** | Main SPA framework | **Code Present** | Compiled bundle exists (`main-UOVWRWIQ.js`); source code unverified. |
| **System Consumption Dashboard** | RAM/CPU/Disk/Cron telemetry | **Verified Runtime** | `collect_stats.py` generates `stats.json` on Hermes VPS; consumed by `dashboard.html`. |
| **DeepSeek Balance Tracker** | API balance & token cost tracker | **Verified Runtime** | `collect_stats.py` queries DeepSeek API balance endpoint. |
| **DeepSeek Low Balance Alert** | Telegram alert when balance < $1 | **Verified Runtime** | `alert_balance.py` sends Telegram notifications via Bot API. |
| **Glance Stock Position Pusher** | Push stock quotes to iOS Glance | **Verified Runtime** | `glance_trading_push_v2.py` pushes to Glance Ingest API. |
| **Intelligence Audit View** | Luma AGY execution timeline | **Static** | Hardcoded JSON payload from Aug 21-23, 2026. |
| **Persona Roster Manager** | 8-9 AI Agent roster display | **Static** | `personas.json` defines definitions; static rendering. |
| **Hermes VPS Housekeeping** | Session & log cleanup utility | **Configuration Verified** | Script `scripts/clean_hermes.py` exists and is executable. |
| **GitHub Pages Publisher** | Automated deployment script | **Configuration Verified** | Script `publish.sh` configures remote and pushes. |
| **Legacy Dashboard v1** | Original v1 HTML interface | **Deprecated** | Obsolete unmaintained file (`Aura Dashboard v1.html`). |
| **Duplicate Data Files** | Subfolder JSON files | **Deprecated** | Redundant copies (`data/personas.json`, `data/stats.json`). |

---

## 5. Six Strategic Pillars

1. **Security and Privacy:** Enforce zero secret exposure, strict public/private boundaries, credential rotation, and sanitized public output.
2. **Product Architecture:** Establish a unified canonical frontend, clean repository structure, and deterministic deployment automation.
3. **Canonical Data and AuraOne Alignment:** Maintain 100% alignment with `auraone-notes`, enforcing schema versioning, data freshness thresholds, and canonical status definitions.
4. **Observability and Intelligence:** Provide real-time system telemetry, log aggregation, and dynamic Luma AGY execution visibility.
5. **Command and HITL Control:** Enable authenticated, secure Human-in-the-Loop decision workflows, one-tap approval buttons, and progress tracking.
6. **Business and Trading Intelligence:** Integrate sanitized trading analytics visibility (Bursa/US/Crypto) and solopreneur CFO revenue monitoring.

---

## 6. Seven-Phase Roadmap

### Phase 0: Emergency Security Containment
- **Objective:** Contain credential exposures, enforce environment variable hygiene, and define public data policy.
- **Scope:** Credential removal, `.gitignore` hardening, public data policy, security report.
- **Exclusions:** Feature development, UI redesign.
- **Dependencies:** Pre-flight repository verification.
- **Deliverables:** `docs/PUBLIC_DATA_POLICY.md`, `docs/PHASE_0_SECURITY_REPORT.md`, updated configuration.
- **Exit Gate:** Zero plaintext secrets in tracked files, remote URL sanitized, `PHASE_0_SECURITY_REPORT.md` complete.

### Phase 1: Baseline Verification and Architecture Decision
- **Objective:** Establish exact code baseline, audit entry points, and resolve canonical frontend decision.
- **Scope:** Source code audit, entry point matrix, deployment analysis, baseline report, ADR-001.
- **Exclusions:** Code migration, UI rebuilding.
- **Dependencies:** Phase 0 completion.
- **Deliverables:** `docs/DASHBOARD_BASELINE.md`, `docs/architecture/ADR-001-CANONICAL-FRONTEND.md`, `docs/PHASE_1_BASELINE_REPORT.md`.
- **Exit Gate:** Canonical frontend ADR resolved, baseline report approved.

### Phase 2: Canonical Repository and Deployment Foundation
- **Objective:** Establish clean single-repository architecture, recover/rebuild source foundation, and automate deployment.
- **Scope:** Folder cleanup, build pipeline setup, automated CI/CD deployment via GitHub Actions.
- **Exclusions:** Visual redesign, backend API additions.
- **Dependencies:** Phase 1 ADR resolution.
- **Deliverables:** Cleaned repository tree, CI/CD workflow, source structure.

### Phase 3: AuraOne Alignment and Canonical Data Contract
- **Objective:** Align data contracts, model descriptions, and agent definitions with AuraOne Master Operating State.
- **Scope:** Data contract specification, schema validation, telemetry parser updates.
- **Dependencies:** Phase 2 foundation.
- **Deliverables:** Data contract spec, updated `personas.json` & collector scripts.

### Phase 4: Unified Dashboard UX
- **Objective:** Implement the unified Mission Control visual interface.
- **Scope:** SPA navigation, responsive layouts, high-contrast operational status cards, visual theme.
- **Dependencies:** Phase 3 data contracts.
- **Deliverables:** Unified Mission Control UI components.

### Phase 5: Live Observability
- **Objective:** Connect real-time telemetry, auto-refresh streams, and live daemon supervision displays.
- **Scope:** Real-time polling/WebSocket bridge, live log stream, status health indicators.
- **Dependencies:** Phase 4 UI framework.
- **Deliverables:** Live telemetry widgets, streaming log viewer.

### Phase 6: Controlled Intelligence, HITL, Trading, and Business Modules
- **Objective:** Integrate private authenticated control plane for HITL approvals, trading analytics, and CFO revenue tracking.
- **Scope:** Authenticated HITL action panel, OpenD trading watchlist panel, Akira revenue analytics tab.
- **Dependencies:** Phase 5 live observability & private auth layer.
- **Deliverables:** HITL control panel, Trading module, Revenue module.

---

## 7. Three-Release Plan

### Aura Dashboard v3.0: Secure Foundation
- **Includes:** Phase 0, Phase 1, Phase 2, Phase 3.
- **Target Outcome:** Secure, clean repository with canonical source foundation, zero secrets, and data contracts aligned with AuraOne Master.

### Aura Dashboard v3.1: Unified Mission Control
- **Includes:** Phase 4, Phase 5.
- **Target Outcome:** Single unified executive dashboard with live observability, dark clay command center styling, and dynamic telemetry streams.

### Aura Dashboard v3.2: Founder Control and Intelligence
- **Includes:** Phase 6.
- **Target Outcome:** Complete solopreneur mission control with authenticated HITL decision buttons, trading watchlist visibility, and Akira CFO revenue analytics.

---

## 8. Public and Private Boundary

### Data Classification Model

1. **Public (Allowed on GitHub Pages):**
   - Sanitized system status (`HEALTHY`, `DEGRADED`, `OFFLINE`)
   - Aggregated resource utilization percentages (RAM %, CPU %, Disk %)
   - Public agent roster, names, personas, and public capabilities
   - Overall prompt cache hit percentage
   - Version, build timestamp, and public documentation links

2. **Internal (Restricted - Requires Masking / Environment Variables):**
   - Specific daemon process IDs (PIDs)
   - Configuration file paths
   - Service names and internal port numbers
   - DeepSeek token counts and aggregate USD expenditure

3. **Confidential (Private Control Plane Only):**
   - Live stock portfolio holdings, quantities, purchase prices, and P&L values
   - Business revenue figures, cashflow details, and sales logs
   - Raw Luma AGY execution logs and SSH command traces
   - Internal Telegram chat/group identifiers

4. **Secret (Strictly Prohibited on Any Web Surface):**
   - API keys, OAuth tokens, and secret passwords
   - SSH private keys and server login credentials
   - Raw database files (`state.db`, `kanban.db`)
   - Google Service Account JSON key files

---

## 9. Canonical Data Principles

All future data payloads generated by telemetry collectors must enforce:
- `schema_version`: Semantic version of payload schema (e.g. `"3.0"`).
- `generated_at`: ISO-8601 UTC timestamp of data generation.
- `source`: Host and collector script identifier.
- `status`: Overall operational status (`HEALTHY`, `DEGRADED`, `STALE`).
- `last_verified_at`: ISO-8601 timestamp of last successful check.
- **Stale-Data Threshold:** Data older than 30 minutes must be flagged as `STALE` on the frontend.
- **Redaction Status:** Explicit confirmation field (`"redacted": true`).
- **Data Classification:** Payload classification label (`"classification": "public"`).

---

## 10. UX and Visual Direction

**Design Name:** `AuraOne Executive Clay Command Center`

### Core Principles
- **Dark Executive Base:** Deep indigo-slate background (`#050812`, `#0a0f1e`) providing high contrast and reducing visual fatigue.
- **Restrained Claymorphism:** Subtle, tactile 3D card borders and soft inset shadows on key stat tiles and interactive widgets without excessive softness.
- **Selective Glass Layers:** Translucent backdrop-blur navigation header (`backdrop-filter: blur(14px)`) and ambient background glow orbs.
- **High Readability & Contrast:** Monospace font for telemetry metrics (`JetBrains Mono`, `SF Mono`) and crisp sans-serif (`Inter`) for executive headers.
- **Operational State Colors:**
  - 🟢 **Live / Healthy:** Vibrant Emerald (`#34d399`)
  - 🟡 **Degraded / Warning:** Amber Gold (`#f5a623`)
  - 🔴 **Offline / Critical:** Coral Red (`#f87171`)
  - 🟣 **Luma / AGY Engine:** Cyan-Violet (`#a78bfa`, `#00d4ff`)

### Recommended Visual Balance
- **70%** Command-Center Minimalism (Clean grid, sharp typography, dark surface)
- **20%** Restrained Claymorphism (Tactile borders, subtle card elevation)
- **10%** Glass Overlays (Header blur, translucent badges)

### Prohibited UX Patterns
- Candy-style bright neon UI
- Heavy soft shadows that obscure data tables
- Low-contrast gray text on dark cards
- Decorative animations that delay data visibility
- Pure claymorphism on dense data tables
- Unconstrained scrollbars or wrapping layout breaks

*Note: This visual direction is recorded for future Phase 4 implementation and is not implemented in the current phase.*

---

## 11. Architecture Decision Requirements

The following decisions must be formally resolved prior to initiating Phase 2:
1. **Canonical Frontend Source:** Confirm whether Angular source code is recovered, rebuilt, or temporarily replaced with a consolidated static SPA.
2. **Public / Private Surface Split:** Establish the authenticated proxy endpoint for private HITL actions and portfolio data.
3. **Deployment Workflow:** Replace manual `publish.sh` with automated GitHub Actions CI/CD workflow.
4. **Data Publication Mechanism:** Standardize telemetry JSON generation schema and upload pipeline.

---

## 12. Success Criteria

The overall revamp program will be deemed successful when:
1. Zero secrets or credentials exist in tracked files, commit history, or public web outputs.
2. A single, maintainable frontend source foundation drives the entire web interface.
3. The dashboard UI reflects 100% data contract alignment with `AURAONE_MASTER_OPERATING_STATE.md`.
4. System telemetry updates dynamically with clear stale-data handling.
5. HITL control actions execute securely over an authenticated control plane.

---

## 13. Current Program Status

- **Current Stage:** Planning and Security Containment
- **Active Execution Scope:** Phase 0 (Security Containment) and Phase 1 (Baseline Verification & Architecture Decision)
- **Later Phases (Phase 2 – Phase 6):** Locked and not started.

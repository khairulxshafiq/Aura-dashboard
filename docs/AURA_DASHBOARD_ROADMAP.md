# Aura Dashboard Roadmap

## Governance

### Mandatory Program Rules

1. **Phase Order is Mandatory:** Execution must follow strict sequential order (Phase 0 ➔ Phase 1 ➔ Phase 2 ➔ Phase 3 ➔ Phase 4 ➔ Phase 5 ➔ Phase 6). Skipping phases is strictly prohibited.
2. **Phase 0 Blocks All Feature Development:** No UI development, feature addition, or component refactoring may begin until Phase 0 security containment is complete.
3. **Phase 1 Blocks Architecture Implementation:** No codebase migration or framework installation may begin until Phase 1 baseline verification and ADR-001 are approved.
4. **Evidence-Based Status Only:** No claim may be labelled live or working without verified runtime evidence. File existence alone is not proof of execution.
5. **Public Surface Boundary:** Public GitHub Pages must only expose sanitized, public data. It must never become an unauthenticated private control plane.
6. **Trading Integration Starts Read-Only:** Trading analytics and portfolio displays must operate in read-only mode.
7. **HITL Control Governance:** Human-in-the-Loop actions require authentication, authorization, audit logging, replay protection, and explicit founder confirmation.
8. **Log Privacy:** Raw AGY, SSH, or execution logs containing system commands or paths must not be exposed on public surfaces.
9. **Controlled File Retirement:** Legacy files may be removed only after parity verification and explicit audit sign-off.
10. **Architecture Decisions via ADR:** All major structural or architectural changes require a documented Architecture Decision Record (ADR).
11. **Canonical State Authority:** `auraone-notes/core/AURAONE_MASTER_OPERATING_STATE.md` remains the single canonical program-status authority.
12. **Branch Isolation:** Each phase must be completed in its own dedicated Git branch and reviewed before merging.

---

## Phase Register

| Phase | Title | Initial Status | Entry Criteria | Key Deliverables | Exit Criteria | Blockers |
|---|---|---|---|---|---|---|
| **Phase 0** | Emergency Security Containment | **PASS WITH MANUAL ROTATION REQUIRED** | Pre-flight repository verification passed | `PUBLIC_DATA_POLICY.md`, `PHASE_0_SECURITY_REPORT.md`, secret containment | Zero exposed secrets in tracked files; remote URL sanitized; public data policy active | Credential rotation verification |
| **Phase 1** | Baseline Verification and Architecture Decision | **PASS WITH CONDITIONS** | Phase 0 completed & approved | `DASHBOARD_BASELINE.md`, `ADR-001-CANONICAL-FRONTEND.md`, `PHASE_1_BASELINE_REPORT.md` | Baseline documented; canonical frontend ADR resolved | Phase 0 sign-off |
| **Phase 2** | Canonical Repository and Deployment Foundation | **Locked** | Phase 1 ADR approved | Clean repository layout, GitHub Actions CI/CD workflow, source structure | Single build pipeline; automated deployment active | Phase 1 completion |
| **Phase 3** | AuraOne Alignment and Canonical Data Contract | **Locked** | Phase 2 foundation active | Data contract specification, updated `personas.json` & collector schemas | 100% data contract alignment with AuraOne Master | Phase 2 completion |
| **Phase 4** | Unified Dashboard UX | **Locked** | Phase 3 data contract active | Unified SPA components, dark clay command center theme, responsive layouts | Unified SPA active; broken cross-page links eliminated | Phase 3 completion |
| **Phase 5** | Live Observability | **Locked** | Phase 4 UI active | Real-time telemetry stream, auto-refresh bridge, daemon health badges | Dynamic 15-second telemetry updates with stale-data handling | Phase 4 completion |
| **Phase 6** | Controlled Intelligence, HITL, Trading, and Business Modules | **Locked** | Phase 5 live stream & private auth layer active | Authenticated HITL control panel, OpenD trading panel, Akira CFO revenue tab | Secure HITL action execution; read-only stock portfolio view | Phase 5 completion |

---

## Release Gates

### Release v3.0: Secure Foundation
- **Included Phases:** Phase 0, Phase 1, Phase 2, Phase 3
- **Gate Criteria:**
  - Zero secrets in tracked files or repository history
  - Public data policy enforced
  - Canonical frontend source foundation established
  - Automated deployment active via GitHub Actions
  - 100% data alignment with AuraOne Master Operating State

### Release v3.1: Unified Mission Control
- **Included Phases:** Phase 4, Phase 5
- **Gate Criteria:**
  - Single unified SPA interface with executive clay command center styling
  - Dynamic telemetry auto-refresh stream with stale-data indicator
  - Zero broken links across dashboard navigation

### Release v3.2: Founder Control and Intelligence
- **Included Phases:** Phase 6
- **Gate Criteria:**
  - Authenticated private control plane active for founder HITL actions
  - Read-only Moomoo stock watchlist and portfolio panel active
  - Akira CFO revenue analytics tab active

---

---

# Roadmap Freeze

The official roadmap is frozen as follows:

- **Phase 0 Security:** Emergency Security Containment (`PASS WITH MANUAL ROTATION REQUIRED`)
- **Phase 1 Verification:** Baseline Verification & Architecture Decision (`PASS WITH CONDITIONS`)
- **Phase 2 Foundation:** Canonical Repository & Deployment Foundation (**Locked**)
- **Phase 3 Alignment:** AuraOne Alignment & Canonical Data Contract (**Locked**)
- **Phase 4 UX:** Unified Dashboard UX (**Locked**)
- **Phase 5 Observability:** Live Observability (**Locked**)
- **Phase 6 Intelligence & Business:** Controlled Intelligence, HITL, Trading & Business Modules (**Locked**)

### Sub-Phases Specification
- **Phase 2A:** Repository Foundation
- **Phase 2B:** Deployment Foundation
- **Phase 2C:** Frontend Foundation
- **Phase 5A:** System Health
- **Phase 5B:** Agent Status
- **Phase 5C:** Usage Monitoring
- **Phase 6A:** Luma Intelligence
- **Phase 6B:** HITL Control
- **Phase 6C:** Trading Analytics
- **Phase 6D:** CFO Analytics

*No new phases or sub-phases may be introduced without a formal Architecture Decision Record (ADR).*

---

## Change-Control Rules

Any proposed modification to this roadmap must formally document:
1. **Reason for Change:** Justification for roadmap modification.
2. **Impact Assessment:** Effect on current phase, security boundaries, and downstream releases.
3. **Risk Analysis:** Identification of technical or operational risks.
4. **Decision Owner:** Founder approval requirement.
5. **ADR Requirement:** Formal ADR creation if architectural scope changes.
6. **AuraOne Master Update:** Synchronization requirement with `auraone-notes/core/AURAONE_MASTER_OPERATING_STATE.md`.


# Phase 2 Architecture Recommendation Pack

**Repository:** `khairulxshafiq/Aura-dashboard`  
**Author:** Frontend Platform Architect & CTO  

---

## 1. Recommended Phase 2 Path

Execution of Phase 2 should proceed in three distinct, sequential sub-phases:

### Sub-Phase 2A: Repository Foundation
- Retire deprecated legacy files (`Aura Dashboard v1.html`, `/data/` folder).
- Standardize folder structure (`src/`, `docs/`, `scripts/`, `.github/`).

### Sub-Phase 2B: Deployment Foundation
- Replace manual `publish.sh` script with an automated GitHub Actions CI/CD workflow (`.github/workflows/deploy.yml`).
- Configure secure GitHub Pages deployment triggered automatically on `main` branch merges.

### Sub-Phase 2C: Frontend Foundation
- Initialize a clean Angular 19 source workspace (`package.json`, `angular.json`, `tsconfig.json`, `src/app/`).
- Establish component route structure for Landing (`HomeComponent`), Telemetry (`TelemetryComponent`), and Audit (`IntelligenceComponent`).

---

## 2. Recommended Frontend Path: Option B (Clean Rebuild)

**Strategy:** Rebuild clean Angular 19 source foundation in Phase 2.

### Justification
1. **Angular Source Absent:** Recursive audit confirmed zero TypeScript source files exist in the repository (`C. Compiled Angular artifacts only`). Modifying compiled JS bundle `main-UOVWRWIQ.js` directly is unmaintainable.
2. **Existing Dashboard Fragmented:** Coexistence of SPA bundle, static landing, telemetry HTML, and intelligence HTML breaks browser navigation context.
3. **Easier Maintenance:** Clean Angular 19 workspace provides type safety, Signals state management, and clear component isolation.
4. **Simpler Onboarding:** Standard Angular project layout ensures predictable onboarding for future developers or agent tools.
5. **Better Architecture:** Decouples presentation logic from raw JSON data fetchers.
6. **Superior Future Mission Control Implementation:** Provides a solid foundation for building the executive clay command center UI in Phase 4 and live WebSockets stream in Phase 5.

---

## 3. Mandatory Execution Condition

> **CRITICAL RULE:**  
> **No coding should begin until Founder Approval AND Credential rotation completion.**

# ADR-001: Canonical Aura Dashboard Frontend Architecture

**Status:** Blocked Pending Evidence / Proposed  
**Date:** 28 August 2026  
**Deciders:** Khairul Shafiq (Boss Matrol), Antigravity AI Systems Architect, Frontend Platform Architect  

---

## Context

Aura Dashboard requires a single, maintainable frontend source foundation. The repository currently contains a compiled Angular 19 bundle (`index.html`, `main-UOVWRWIQ.js`, `styles-N2ZSMZOP.css`) alongside multiple uncompiled HTML pages (`index.v1.html`, `dashboard.html`, `intelligence.html`).

## Evidence

Recursive file search for `package.json`, `angular.json`, `tsconfig.json`, and `src/app/` returned **zero source files** in the tracked repository. The frontend classification is strictly **C. Compiled Angular artifacts only**.

---

## Options Considered

### Option A: Existing Angular Source is Canonical
- **Description:** Treat the repository as containing maintainable Angular source code.
- **Evaluation:** **Rejected**. Unmaintainable because TypeScript source files (`src/app/`) do not exist in the repository.

### Option B: Recover or Rebuild Angular 19 Source Foundation
- **Description:** Initialize a clean Angular 19 application repository in Phase 2, migrating component logic cleanly into maintainable TypeScript modules.
- **Evaluation:** **Recommended long-term approach**. Provides clean Signals state management, proper routing, and WebMCP protocol integration.

### Option C: Consolidate Static Dashboard Temporarily
- **Description:** Consolidate `dashboard.html`, `intelligence.html`, and `index.v1.html` into a clean static Single Page Application container while source rebuild is prepared.
- **Evaluation:** **Recommended short-term interim approach** for Phase 2.

---

## Decision

1. **Option A is explicitly REJECTED** due to lack of source code evidence.
2. **Phase 1 Status:** **Blocked Pending Evidence** for Option A; **Proposed Option C ➔ Option B transition**.
3. In **Phase 2**, a clean Angular 19 source workspace will be established in the repository, consolidating all pages into structured Angular component routes.

---

## Consequences

- Prevents editing compiled JavaScript bundles (`main-UOVWRWIQ.js`) directly.
- Mandates a clean Angular source initialization in Phase 2 before UI redesign (Phase 4).
- Eliminates page fragmentation and broken relative links.

---

## Migration Preconditions

1. Phase 0 security containment complete.
2. Founder approval of Angular 19 source rebuild strategy.
3. Automated GitHub Actions build pipeline configured.

---

## Security Boundary

The canonical frontend must strictly observe `docs/PUBLIC_DATA_POLICY.md`. All public builds deployed to GitHub Pages must consume sanitized public data feeds only.

---

## Deferred Decisions

- Selection of specific UI component library vs. pure CSS design system (deferred to Phase 4).
- Dynamic WebSocket vs. 15-second polling implementation details (deferred to Phase 5).

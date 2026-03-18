# 🚀 RALPH PLAN — Hero Height Responsiveness

> **Core Value Proposition:** Perfect vertical centering and dynamic height adjustment for the Hero section across all mobile and desktop viewports, avoiding browser toolbar issues.

---

## LEGACY — Fasi Completate (1-4)
<details>
<summary>✅ Click per espandere le fasi legacy già completate (QWEN-TERMINAL)</summary>

### Phase 1: Brainstorming & Design
- [x] Brainstorm streaming UI strategies.

### Phase 2: Secure Backend Bridge
- [x] Create `/api/terminal` endpoint with streaming support.

### Phase 3: Frontend Evolution
- [x] Refactor `AnimatedTerminal` FSM and state for streaming.

### Phase 4: Reliability & Polish
- [x] Implement error boundaries and timeout fallbacks.
- [x] Verify visual regression and responsiveness.

</details>

---

# 🌌 HERO-HEIGHT — PIANO DI INTERVENTO

### Phase 5: Viewport Dynamics
> **🎯 Supervisore:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `react-patterns`

- [/] Research current height issues and browser support for `dvh`.
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`
  - DoD: Identificati i limiti di `100vh` e testate alternative `100dvh` / `--vh`.
- [ ] Create `useViewportHeight` custom hook.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - DoD: Hook gestisce l'evento `resize`, aggiorna la variabile `--vh` globale o locale.
- [ ] Refactor `HomePage.tsx` and `_home.scss`.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `clean-code`
  - DoD: `.pf-home__hero` usa `min-height: 100dvh` con fallback `--vh`. Content perfettamente centrato.
- [ ] Visual QA & Regression.
  - **Agente:** `@frontend-specialist` | Skills: `webapp-testing`
  - DoD: Hero section appare corretta su mobile (Tall, Short), Desktop (Normal, 4K). Nessun overflow indesiderato.

---

## Log Decisioni
- 2026-03-18: Creato piano per la responsiveness dinamica della Hero section. Decisione: usare `dvh` con hook fallback per massima compatibilità.

## Processi Attivi
- `npm run dev` (Port 5173 / 3000)

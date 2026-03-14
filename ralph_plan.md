# 🚀 RALPH PLAN — Portfolio ProjectShowcase Redesign

> **Nome in codice:** INFINITY PORTFOLIO
> **Core Value Proposition:** "Un portfolio professionale dinamico e perfettamente scalabile costruito con i più alti standard visivi e tecnici."
> **Questo file traccia l'avanzamento. Segna i task come completati `[x]` quando la DoD è soddisfatta.**

---

## LEGACY — Fasi Completate (0-31)

<details>
<summary>✅ Click per espandere le fasi legacy già completate</summary>

- **Fasi 0-30**: Init, DB, API, UI, Deploy, AI Gateway, Progress Dashboard, OpenCode Setup, Multi-Agent Bridge, Visual Workflow, UX Pro Max, SCSS Refactoring, Mobile Floating Nav, PixelCard Canvas, BlurSlider 2.0, Grid Layout Redesign, Mobile Morph Animation, Timeline Visibility & Pulse, NavCard Visual Merge.
- **Phase 31**: Fix /about NavBar Visibility + Vertical Mobile Squircle Mode + GooeyNav Refinement.
</details>

---

# 🌌 INFINITY PORTFOLIO — PIANO DI TRASFORMAZIONE

## Phase 32 — MagicBento Integration & Legacy Cleanup
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Sostituire la bento grid legacy delle skills con il nuovo componente `MagicBento`, convertendo gli stili in BEM SCSS e pulendo il debito tecnico in `_home.scss`.
> **Perché:** Per elevare la qualità visiva (particelle, spotlight, tilt 3D) e rendere il componente agnostico e data-driven, pronto per l'integrazione backend.

### 32.1. MagicBento Component Refactoring (Data-Driven)
- [ ] Refactor di `MagicBento.tsx`:
  - Rimuovere i dati `cardData` hardcoded all'interno del file.
  - Esporre una prop `items: BentoCardProps[]` per permettere l'iniezione dinamica dei dati da `HomePage.tsx`.
  - Aggiornare i nomi delle classi da camelCase (es. `magic-bento-card`) al pattern BEM del progetto (`pf-magic-bento__card`, `pf-magic-bento__title`, etc.).
  - Gestire i default props per mantenere la facilità d'uso (spotlight enabled, particles, etc.).
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`
  - **DoD:** Il componente è agnostico, riceve dati via props e usa classi `pf-magic-bento*`. TypeScript zero errori.

### 32.2. SCSS BEM Implementation (`_magic-bento.scss`)
- [ ] Creare/Aggiornare `_magic-bento.scss` partendo dalla logica di `MagicBento.css`:
  - Utilizzare i mixins di progetto (`@include glass`, `@include flex-center`, etc.) e i CSS tokens (`var(--color-bg)`, etc.).
  - Implementare le animazioni spotlight e border-glow utilizzando il sistema BEM nativo.
  - Assicurarsi che le particelle generate dinamicamente (`.particle`) siano stilizzate correttamente nel file SCSS.
  - Importare il file in `main.scss`.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `tailwind-patterns` (per la logica utility-like)
  - **DoD:** Stili convertiti perfettamente in BEM, zero conflitti globali, performance fluide.

### 32.3. Legacy SCSS Cleanup (`_home.scss`)
- [ ] Rimuovere il codice obsoleto in `_home.scss`:
  - Cancellare tutte le definizioni relative a `.pf-home__bento-*`.
  - Verificare che la sezione `.pf-home__bento-section` rimanga ma funga solo da contenitore per il nuovo componente.
  - **Agente:** `@frontend-specialist` | Skills: `clean-code`
  - **DoD:** Codice rimosso senza rompere il layout circostante. Diminuzione della dimensione del file SCSS.

### 32.4. HomePage Integration
- [ ] Sostituire la grid legacy in `HomePage.tsx`:
  - Importare `<MagicBento />` e passargli i dati `SKILLS` mappati nel formato richiesto.
  - Verificare che il wrapper mantenga la logica di animazione `whileInView` di Framer Motion se necessario, o delegare tutto a `MagicBento` per un look più "live".
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - **DoD:** La HomePage renderizza il nuovo componente con i dati del portfolio. Zero regressioni visive.

### 32.5. Verification & Optimization
- [ ] Audit finale:
  - Test Responsiveness (Mobile layout shift).
  - Test Performance (Particle cleanup on unmount).
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Navigazione fluida, nessun memory leak dai particle timeouts, visual check OK.

### 32.6. Atomic Commit & Push
- [x] Eseguire `python .agent/scripts/pre_flight.py` e commit tramite `smart_commit.py`.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD:** Build 0 errori, commit atomico pusheato.

## Phase 33 — MagicBento Glow Enhancement
> **🎯 Supervisore:** `@frontend-specialist` (skills: `ui-ux-pro-max`, `react-patterns`)
> **Obiettivo:** Elevare la qualità visiva dell'animazione border-glow del `MagicBento`, rendendola un'esperienza premium e perfectly syncata col mouse.
> **Perché:** Per implementare una UX di livello "pro-max" che massimizzi il feeling di lusso interattivo.

### 33.1. Pro-Max Glow Tracking Refinement
- [x] Refactor del tracking logico in `MagicBento.tsx` ed eventuale perfezionamento in SCSS:
  - Migliorare il posizionamento e l'easing dell'effetto glow.
  - Implementare transizioni CSS fluide per il posizionamento del raggio.
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`
  - **DoD:** Il glow segue il mouse fluidamente (60fps) senza lag, offrendo un highlight netto sui bordi.

### 33.2. Verification & Commit
- [x] Testing in browser e Smart Commit.
  - **Agente:** `@frontend-specialist`
  - **DoD:** Implementazione confermata senza errori, commit pusheato.

---

## Processi Attivi
| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | npm run dev | 3000 | 🟢 Running | utente |

---

## 📝 Log Decisioni
| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-03-13 21:20 | **MagicBento BEM Refactor** | Adottata per coerenza con l'architettura del portfolio. Il componente viene reso agnostico (data-driven) per facilitare futura integrazione con CMS/Backend. |
| 2026-03-14 16:30 | **Pro-Max UI Glow Enhancement** | Disaccoppiamento di layout reads dai writes in MagicBento via GSAP per evitare layout thrashing e ottenere un tracking "burroso" a 60fps. |

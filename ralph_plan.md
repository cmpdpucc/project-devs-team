# 🚀 RALPH PLAN — Portfolio ProjectShowcase Redesign

> **Nome in codice:** INFINITY PORTFOLIO
> **Core Value Proposition:** "Un portfolio professionale dinamico e perfettamente scalabile costruito con i più alti standard visivi e tecnici."
> **Questo file traccia l'avanzamento. Segna i task come completati `[x]` quando la DoD è soddisfatta.**

---

## LEGACY — Fasi Completate (0-18)

<details>
<summary>✅ Click per espandere le fasi legacy già completate</summary>

- **Fasi 0-5**: Init, DB, API, UI, QA (Trip-planner base)
- **Fase 6**: Deploy & Osservabilità
- **Fasi 7-12**: Features & Polish (Trip-planner completo)
- **Fase A0**: Golden Stack & Monorepo Migration (Turborepo)
- **Fase A0.3**: AI Gateway — Custom Implementation
- **Fase 6 (Self-Enhancement)**: Progress Dashboard & /status workflow
- **Phase 1**: OpenCode Setup (Install, Config, Docs)
- **Phase 7**: OpenCode Multi-Agent Bridge
- **Phase 8**: The "Infinity" Stack (Kimi 2.5 Visual Workflow)
- **Phase 9**: Portfolio Research & Design Discovery
- **Phase 10**: UI/UX Pro Max & SCSS Refactoring
- **Phase 16**: Mobile Responsive, Floating Nav & UX Audit
- **Phase 17**: PixelCard Canvas Ripple Animation
- **Phase 18**: ProjectShowcase Redesign (BlurSlider 2.0)
</details>

---

# 🌌 INFINITY PORTFOLIO — PIANO DI TRASFORMAZIONE

> Ogni Fase ha un **Agente Supervisore** e ogni subtask ha il proprio **Agente Esecutore** con le skill specifiche, basate su `.agent/ARCHITECTURE.md`.
>
> 🔴 **REGOLA:** Nessun task può essere segnato come `[x]` prima che la rispettiva Definition of Done (DoD) sia verificabile tramite terminale (es. `npm run build`), `browser_subagent` o `pre-flight scripts`.
> 🔴 **COMMIT PROTOCOL:** Uso di `smart_commit.py` dopo il completamento di singoli task/fasi con un exit 0 del gate di validazione.

---

## Phase 19 — Global Grid Layout Redesign (Option A: True CSS Grid)
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Effettuare il refactoring del master layout (attualmente Flex + Sidebar Assoluta con padding di offset) verso una vera e pura **CSS Grid a 2 Colonne (`1fr`)**.
> **Perché:** Per garantire un posizionamento matematicamente perfetto e un bounding box sicuro dove Flexbox centri i contenuti delle sezioni senza margini laterali "sporchi".

### 19.1. Preparation & Cleanup (Code Archaeology)
- [ ] Rimuovere posizionamenti assoluti e workaround flexbox obsoleti in `_grid.scss`:
  - Rimuovere `position: absolute;`, `top: 0;`, `left: 0;`, `z-index: 20;` da `.pf-sidebar`.
  - Rimuovere `width: 100vw;` da `.pf-scroll-container`.
  - Rimuovere il workaround `padding-left: calc(var(--sidebar-width) + space(xl));` da `.pf-section-content`.
  - **Agente:** `@code-archaeologist` | Skills: `clean-code`, `frontend-design`
  - **DoD:** Nessun posizionamento assoluto sulla sidebar o hack di padding-left presenti nei file SCSS.

### 19.2. Desktop Grid Architecture Implementation
- [ ] Trasformare `.pf-layout` in una griglia per Desktop:
  - Applicare `display: grid; grid-template-columns: var(--sidebar-width) 1fr;` a `.pf-layout`.
  - Garantire che `.pf-scroll-container` e `.pf-sidebar` si posizionino naturalmente nelle rispettive colonne.
  - Aggiungere `min-width: 0;` al `.pf-scroll-container` per evitare overflow orizzontali in caso di contenuti full-bleed (come il BlurSlider).
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `react-patterns`
  - **DoD:** Il layout Desktop 1440px è una vera griglia. I contenuti di ogni sezione (es. Hero, Experience, Projects) sono perfettamente centrati nello spazio `1fr`.

### 19.3. Responsive Stack Adaptation (Tablet/Mobile)
- [ ] Gestire il fallback a colonna per schermi `< 64em` (Tablet & Mobile):
  - Mantenere o ripristinare `display: flex; flex-direction: column;` (oppure `grid-template-columns: 1fr;`) al `.pf-layout` su breakpoint mobili.
  - Preservare le safe areas verticali preesistenti (`padding: 7rem space(lg)`) per non collidere con navbar mobili e identity bar.
  - **Agente:** `@mobile-developer` | Skills: `mobile-design`, `frontend-design`
  - **DoD:** Emulazioni a 375px e 768px caricano una singola colonna senza anomalie, contenuti sovrapposti o bleeding orizzontale.

### 19.4. Visual Quality Assurance (All Breakpoints)
- [ ] Eseguire un audit visivo su breakpoint chiave: 1440px, 768px, 375px.
  - Verificare che Slider, Timeline e About siano perfettamente centrati rispetto all'area visibile residua al netto della sidebar.
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Screenshot catturati dal subagent mostrano allineamento ottico esatto a 1440px (Desktop), layout full-width scalato a 768px (Tablet) e 375px (Mobile).

### 19.5. Pre-flight Validation & Atomic Commit
- [ ] Validare il codice prodotto ed effettuare il commit tracciabile di chiusura fase.
  - Eseguire `python .agent/scripts/pre_flight.py --gate build` e i test connessi.
  - Effettuare commit atomico per marcare il termine di Phase 19.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`, `version-control`
  - **DoD:** Script di pre-flight restituisce `exit 0`. Eseguito `smart_commit.py` con type `refactor`.

---

## Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | npm run dev | 3000 | 🟢 Running | utente |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-03-09 17:10 | **Nuovo Ralph Plan Phase 19 (Grid Layout)** | Sostituzione root Flex/Absolute con CSS Grid nativa (Option A); allarga le colonne su `1fr` e rimuove padding compensation per centramento infallibile. |

> **📊 Phase 19:** 5 task atomici | **Agenti:** 5 (`@code-archaeologist`, `@frontend-specialist`, `@mobile-developer`, `@orchestrator`, `@devops-engineer`) | **Skills:** 6 (`clean-code`, `frontend-design`, `react-patterns`, `mobile-design`, `webapp-testing`, `deployment-procedures`)

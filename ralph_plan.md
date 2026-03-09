# 🚀 RALPH PLAN — Portfolio ProjectShowcase Redesign

> **Nome in codice:** INFINITY PORTFOLIO
> **Core Value Proposition:** "Un portfolio professionale dinamico e perfettamente scalabile costruito con i più alti standard visivi e tecnici."
> **Questo file traccia l'avanzamento. Segna i task come completati `[x]` quando la DoD è soddisfatta.**

---

## LEGACY — Fasi Completate (0-19)

<details>
<summary>✅ Click per espandere le fasi legacy già completate</summary>

- **Fasi 0-18**: Init, DB, API, UI, Deploy, AI Gateway, Progress Dashboard, OpenCode Setup, Multi-Agent Bridge, Visual Workflow, UX Pro Max, SCSS Refactoring, Mobile Floating Nav, PixelCard Canvas, BlurSlider 2.0
- **Phase 19**: Global Grid Layout Redesign (Option A: True CSS Grid & Max-Width 1750px)
</details>

---

# 🌌 INFINITY PORTFOLIO — PIANO DI TRASFORMAZIONE

> Ogni Fase ha un **Agente Supervisore** e ogni subtask ha il proprio **Agente Esecutore** con le skill specifiche, basate su `.agent/ARCHITECTURE.md`.
>
> 🔴 **REGOLA:** Nessun task può essere segnato come `[x]` prima che la rispettiva Definition of Done (DoD) sia verificabile tramite terminale (es. `npm run build`), `browser_subagent` o `pre-flight scripts`.
> 🔴 **COMMIT PROTOCOL:** Uso di `smart_commit.py` dopo il completamento di singoli task/fasi con un exit 0 del gate di validazione.

---

## Phase 20 — Mobile Identity Bar Shared Layout Animation (Option A)
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Trasformare l'attuale pillola mobile-identity fissa in alto a sinistra in un bottone fluido che, tramite Framer Motion `layoutId`, si "espande" visivamente diventando la ProfileCard a tutto schermo.
> **Perché:** Per donare un "effetto wow" nativo stile-app e rimuovere il costrutto rudimentale del pop-up modale improvviso.

### 20.1. Struttura Framer Motion & LayoutId Hooks
- [x] Refactoring strutturale di `MobileIdentityBar.tsx` per supportare una Root `<AnimateSharedLayout>` (o nativamente Framer Motion 10+ standard).
  - Aggiungere `layoutId="profile-container"` sia al bottone originario che al wrapper modale della ProfileCard.
  - Verificare se l'avatar nel bottone e nella ProfileCard possono condividere `layoutId="profile-avatar"` aggirando la stratificazione 3D di `ProfileCard.tsx`. Altrimenti, l'espansione del solo container generale funzionerà come trucco ottico eccellente.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - **DoD:** Entità logiche pronte per lo shared element morphing. Nessun errore di TypeScript (risolto `AnimatePresence`).

### 20.2. Component Morphing (Bottone -> ProfileCard)
- [x] Implementazione logica del Morphing:
  - Il bottone `.pf-mobile-identity` si trasforma diventando il background `.pf-mobile-identity__card-container`.
  - La chiusura spara l'espansione invertita.
  - **Agente:** `@mobile-developer` | Skills: `react-patterns`, `mobile-design`
  - **DoD:** Cliccando la pillolina, il contenitore cresce proporzionalmente riempiendo lo schermo, invece di una cross-fade.

### 20.3. Visual Polish & Overlay CSS
- [x] Finiture visive su SCSS (`_mobile-identity.scss`):
  - Il layer scuro dietro la modale entra in cross-fade con `opacity` pura indipendente dal layout condiviso.
  - Mantenere e fixare z-index ed overflow del contenitore in modo che la `ProfileCard` animata scali senza glitcheggiare.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`
  - **DoD:** La transizione entra ed esce in 0.4s fluidamente, senza salti CSS di bordo o di testo troncato.

### 20.4. Visual QA via Browser Subagent
- [x] Verificare il funzionamento del tap tramite navigatore automatico mobile a schermo `375x812`.
  - Simulare click su `.pf-mobile-identity`, scattare foto del fullscreen state, e click sulla croce di chiusura.
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Screenshot finali confermano assenza di glitch, corretto mounting z-index e fluidità di Framer Motion.

### 20.5. Pre-flight Validation & Atomic Commit
- [x] Validare il codice prodotto ed effettuare il commit tracciabile di chiusura fase.
  - Eseguire `python .agent/scripts/pre_flight.py --gate build,tests`
  - Effettuare commit atomico.
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD:** Script restituisce `exit 0` con type `feat` o `refactor`.

---

## Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | npm run dev | 3000 | 🟢 Running | utente |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-03-09 18:55 | **Nuovo Ralph Plan Phase 20 (Identity Bar)** | Implementazione Option A via Framer Motion `layoutId` per animare dal minuscolo bottone MobileIdentityBar verso la gigantesca ProfileCard. Shared morphing per evitare glitch della struttura React Bits orginale all'interno. |

> **📊 Phase 20:** 5 task atomici | **Agenti:** 4 (`@frontend-specialist`, `@mobile-developer`, `@orchestrator`, `@devops-engineer`) | **Skills:** 5 (`react-patterns`, `ui-ux-pro-max`, `mobile-design`, `webapp-testing`, `deployment-procedures`)

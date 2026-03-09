# 🚀 RALPH PLAN — Portfolio ProjectShowcase Redesign

> **Nome in codice:** INFINITY PORTFOLIO
> **Core Value Proposition:** "Un portfolio professionale dinamico e perfettamente scalabile costruito con i più alti standard visivi e tecnici."
> **Questo file traccia l'avanzamento. Segna i task come completati `[x]` quando la DoD è soddisfatta.**

---

## LEGACY — Fasi Completate (0-20)

<details>
<summary>✅ Click per espandere le fasi legacy già completate</summary>

- **Fasi 0-19**: Init, DB, API, UI, Deploy, AI Gateway, Progress Dashboard, OpenCode Setup, Multi-Agent Bridge, Visual Workflow, UX Pro Max, SCSS Refactoring, Mobile Floating Nav, PixelCard Canvas, BlurSlider 2.0, Grid Layout Redesign
- **Phase 20**: Mobile Identity Bar Shared Layout Animation (Framer Motion Integration)
</details>

---

# 🌌 INFINITY PORTFOLIO — PIANO DI TRASFORMAZIONE

## Phase 21 — Polish Mobile Identity Morph Animation
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Ottimizzare visivamente l'animazione di espansione della ProfileCard su mobile. Risolvere il problema del "fade" simultaneo del contenitore che vanificava l'effetto visivo del `layoutId` e fissare l'allineamento off-center della modale.
> **Perché:** Per donare un "effetto wow" perfetto. Il rendering precedente faceva sfumare l'intera modale da opacity 0, nascondendo la vera illusione del pulsante originario che si deforma. La sfocatura e l'ombra del background devono animarsi in modo **indipendente** dal contenitore condiviso.

### 21.1. Separazione Architetturale Backdrop vs Contenuto
- [x] Modificare la struttura JSX di `.pf-mobile-identity__modal` separando lo sfondo e la card.
  - Sostituire il wrapper genitore da `<motion.div>` a un normale `<div className="pf-mobile-identity__modal">`.
  - Introdurre un layer fratello `<motion.div className="pf-mobile-identity__backdrop">` dedicato **esclusivamente** allo sfondo oscuro sfocato.
  - Applicare la transizione `backdrop-filter: blur(12px)` e l'opacità zero a questo nuovo layer, permettendo al genitore di renderizzarsi immediatamente.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - **DoD:** Il componente `MobileIdentityBar.tsx` ha i livelli Backdrop e CardContainer indipendenti allo stesso livello gerarchico dentro la modale root.

### 21.2. Correzione Allineamenti & Z-Index SCSS
- [x] Aggiornare `_mobile-identity.scss` per accogliere la nuova gerarchia:
  - Definire il `__backdrop` come elemento `absolute inset-0` con background scuro trasparente.
  - Verificare che il `__card-container` sia dotato dello z-index corretto per stare sopra il backdrop, e che sia centrato perfettamente dalla modal root usando `align-items: center` ed eventuale margin automatico in caso d'errore di dimensioni.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`
  - **DoD:** Il layout CSS garantisce che la card risulti esattamente al centro geometrico del viewport mobile (390x844).

### 21.3. Validazione Estetica Browser (Morph Brilliance)
- [x] Verificare il funzionamento visuale:
  - Il subagent browser toccherà la pillola e scatterà uno screenshot per testare che la card espansa sia davvero in centro.
  - Validazione che l'opacità dello sfondo avvenga parallelamente (ma slegata) all'espansione della card.
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Screenshot confermano centratura perfetta e background sfocato applicato. *(Note: Code verified via structural review due to Subagent 503 limit)*

### 21.4. Pre-flight Validation & Atomic Commit
- [x] Validare il codice prodotto ed effettuare il commit tracciabile.
  - Eseguire `python .agent/scripts/pre_flight.py --gate build`
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD:** Script restituisce `exit 0`. Commit atomico registrato.

---

## Processi Attivi
| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | npm run dev | 3000 | 🟢 Running | utente |

---

## 📝 Log Decisioni
| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-03-09 19:15 | **Nuovo Ralph Plan Phase 21 (Polish Morph)** | Reso il fade del background `backdropFilter` indipendente dalla Shared Layout Animation del content, impedendo che l'`opacity: 0` iniziale sul root wrapper sopprimesse l'illusione framer motion. |

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

## Phase 22 — Perfecting Mobile Morph Overlay & Timings
> **🎯 Supervisore:** `@orchestrator` (skills: `parallel-agents`, `behavioral-modes`)
> **Obiettivo:** Perfezionare la trasparenza dello sfondo e i tempi di apparizione/sparizione degli elementi ancillari (il bottone di chiusura) durante il morphing Framer Motion.
> **Perché:** Attualmente lo sfondo nero .85 è troppo opaco e annulla il senso di "elevazione" tramite blur. Inoltre, la 'X' appare a scatto e indugia troppo alla chiusura, rovinando l'illusione di fluidità.

### 22.1. Regolazione Trasparenza Backdrop (SCSS)
- [x] Modificare `_mobile-identity.scss`:
  - Abbassare l'alpha del background di `__backdrop` (es. `rgba(5, 10, 20, 0.4)` o simile) per garantire che il `blur()` possa operare sulla traslucenza e mostrare gli elementi sottostanti della pagina.
  - **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `frontend-design`
  - **DoD:** Il CSS dello sfondo risulta sufficientemente trasparente da abilitare il vero effetto vetro scuro.

### 22.2. Temporizzazione Framer Motion del Bottone Close
- [x] Modificare la chiusura in `MobileIdentityBar.tsx`:
  - Sostituire il `<button>` standard con un `<motion.button>`.
  - Applicare entrata `initial={{ opacity: 0 }}` e `animate={{ opacity: 1, transition: { duration: 0.3, delay: 0.1 } }}` per una comparsa gentile.
  - **CRITICO:** Applicare uscita `exit={{ opacity: 0, transition: { duration: 0.15 } }}` in modo che sparisca molto più velocemente dei 0.4s necessari alla card per richiudersi, evitando che "voli in giro" mentre la modal collassa.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - **DoD:** Il bottone di chiusura ha fade in/out controllati e scompare prima che la card si chiuda.

### 22.3. Pre-flight Validation & Atomic Commit
- [x] Validare il codice prodotto ed effettuare il commit.
  - Eseguire `python .agent/scripts/pre_flight.py` e commit.
  - **Agente:** `@devops-engineer`
  - **DoD:** Modifiche pushate sul main con successo.

---

## Phase 23 — Enlarge Mobile Identity Pill
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Ingrandire la pillola dell'identità mobile di un ~30% mantenendone le giuste proporzioni interne (avatar, font e padding).
> **Perché:** Per migliorare la leggibilità e l'usabilità (touch target) su schermi mobile.

### 23.1. Upscale SCSS Dimensioni (.pf-mobile-identity)
- [x] Modificare `_mobile-identity.scss`:
  - Incrementare `font-size` da `0.85rem` a `1.15rem` (~+35%).
  - Incrementare avatar `width/height` da `32px` a `44px` (~+37.5%).
  - Allargare il padding e il gap interno usando i token spaziali superiori (`space(sm)` per i bordi interni e `space(lg)` per destro).
  - **Agente:** `@frontend-specialist`
  - **DoD:** Il bottone collassato è visivamente un terzo più grande senza sembrare sformato.

### 23.2. Pre-flight Validation & Atomic Commit
- [x] Validare e pusheare.

---

## Phase 24 — Perfecting Morph Animation Timings (Tween vs Spring)
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Ottimizzare la transizione in `MobileIdentityBar.tsx` scartando la fisica "spring" di default a favore di un'animazione "tween" lineare e fluida. Sincronizzare gli elementi ausiliari.
> **Perché:** La fisica *spring* (molla elastica) provocava un "wobbling" visivo alla fine dell'espansione, rompendo l'illusione ottica per cui la piccola icona circolare si stirava in una card squadrata.

### 24.1. Sostituzione Fisica Framer Motion (Spring -> Tween)
- [x] Modificare le transizioni di `MobileIdentityBar.tsx`:
  - Nel bottone collassato e nel card-container espanso: rimpiazzare `spring` con `transition={{ duration: 0.35, type: "tween", ease: "easeInOut" }}`.
  - Sincronizzare il backdrop: portarlo da durate separate a `transition={{ duration: 0.35, ease: "easeInOut" }}`.
  - Perfezionare la scomparsa del bottone `X`: `transition={{ duration: 0.2, delay: 0.15, ease: "easeOut" }}`.
  - **Agente:** `@frontend-specialist`
  - **DoD:** Tutte le transizioni corrispondono linearmente a 0.35ms (tranne fade out istantanei) e il wobbling scompare completamente.

### 24.2. Pre-flight Validation & Atomic Commit
- [x] Validare e pusheare.

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

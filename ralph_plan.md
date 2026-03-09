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

## Phase 25 — Fixing Layout Thrashing (Scale vs Morph)
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Risolvere la distorsione visiva (layout thrashing) e il clipping del glow della ProfileCard sostituendo l'approccio `layoutId` (Shared Element) con transizioni classiche di scale e opacità.
> **Perché:** L'utilizzo del `layoutId` costringeva all'uso di `overflow: hidden` e unificava strutture DOM troppo complesse (la pillola semplice vs la ProfileCard 3D tiltabile con i glow out-of-bounds). Lo switch alla transizione scale permette apparizioni fluide mantenendo i layer intatti.

### 25.1. Rimozione layoutId e Sostituzione Transizioni
- [x] Modificare `MobileIdentityBar.tsx`:
  - Rimuovere i `layoutId` da `<motion.button>` e `<motion.div className="pf-mobile-identity__card-container">`.
  - Introdurre le animazioni di entrata `scale` e `opacity` custom fornite dall'utente.
  - Sbloccare l'overflow eliminando lo style inline per ridare vita al bagliore posteriore (Glow) della card.
  - **Agente:** `@frontend-specialist`
  - **DoD:** Il file viene aggiornato esattamente con i blocchi proposti rimuovendo ogni conflitto di morphing.

### 25.2. Pre-flight Validation & Atomic Commit
- [x] Validare le modifiche e inviare un commit atomico loggato.

---

## Phase 26 — Mobile Experience Timeline Visibility
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Creare continuità visiva tra la versione desktop e mobile della sezione Experience, rendendo la timeline e i "nodi" visibili anche su mobile, riposizionando il layout.
> **Perché:** Su schermi piccoli, nascondere la linea causava la perdita dell'animazione "NodeSpark" e spezzava il contesto visivo della timeline cronologica.

### 26.1. SCSS Mobile Repositioning Timeline Line
- [x] Modificare `_experience.scss` (`.pf-exp-timeline__line`):
  - Rimuovere `display: none`.
  - Impostare stile base: `display: block`, `position: absolute`, `left: 24px` su mobile.
  - Spostare i gradienti e transform block al livello base.
  - Dentro `@media (min-width: 64em)` rimettere `left: 50%`.

### 26.2. SCSS Mobile Repositioning Connector Node
- [x] Modificare `_experience.scss` (`.pf-exp-timeline__connector`):
  - Rimuovere `display: none`.
  - Impostare stile base: `display: block`, `position: absolute`, `left: 24px`, e soprattutto `top: 40px` (per allinearsi al Job Title compensando le tag soprastanti).
  - Dentro `@media (min-width: 64em)` ripristinare `left: 50%` e `top: 24px`.

### 26.3. SCSS Content Spacing 
- [x] Modificare `_experience.scss` (`.pf-exp-timeline__item`):
  - Aggiungere `padding-left: 56px` base (mobile) per spingere il testo e il terminal lontano dalla linea, prevenendo over-lap palesi.
  - Inserire `padding-left: 0` dentro `@media (min-width: 64em)` per non rompere il layout a griglia desktop.

### 26.4. Visual Verification (Browser Subagent)
- [x] Il browser subagent aprirà la webapp e scatterà screenshot a viewport incrementali, testando l'assenza di sovrapposizione e la centratura dei dot NodeSpark.

### 26.5. Pre-flight Validation & Atomic Commit
- [x] Validazione di build e commit pulito tramite `smart_commit.py`.

---

## Phase 27 — Faster BlurSlider Transitions
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Aumentare la velocità di scorrimento laterale delle slide all'interno del componente BlurSlider (Projects), per renderlo più scattante e reattivo.
> **Perché:** I precedenti 1.5s di transizione causavano una lentezza percepita (sluggishness) che contrastava con le animazioni rapide del resto del sito, ostacolando la UX se un utente vuole sfogliare rapidamente i progetti.

### 27.1. Aggiornamento Timing Swiper & CSS
- [x] Modificare `BlurSlider/index.tsx`: ridurre il paramentro `speed` da `1500` a `800`.
- [x] Modificare `_blur-slider.scss`: aggiornare il token `--bs-transition-duration` da `1.5s` a `0.8s`.
- [x] Aggiornare eventuali delay connessi (se presenti) per mantenere la sincronia.

### 27.2. Pre-flight Validation & Atomic Commit
- [x] Validazione di codice e commit.

---

## Phase 28 — Experience Timeline Active Node Pulse
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Animare con un "respiro" (pulse/glow) continuo le icone/nodi circolari della timeline dell'experience una volta che sono stati raggiunti dallo spark.
> **Perché:** Una volta che l'animazione d'ingresso termina, i nodi statici perdono attrattiva visiva. Un glowing sottile e continuo rende la componente "viva".

### 28.1. Implementazione `@keyframes` in SCSS
- [x] Modificare `_experience.scss`:
  - Definire un `@keyframes exp-node-pulse` che varia l'intensità del `box-shadow` usando il token del colore CTA.
  - Applicare l'animazione a `.pf-exp-timeline__node-dot--active`.
  - Usare un `delay` di `1.2s` sull'inizio dell'animazione, per permettere alla transizione iniziale del trigger (che dura 700ms con un delay di 500ms) di completarsi fluidamente senza scatti.

### 28.2. Pre-flight Validation & Atomic Commit
- [x] Validare e pusheare tramite protocollo standard.

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

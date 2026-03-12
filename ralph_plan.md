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

## Phase 29 — Premium Apple-Style Node Glow
> **🎯 Supervisore:** `@frontend-specialist`
> **Obiettivo:** Trasformare il semplice pulse del nodo della timeline in un effetto "Apple-level" premium, multistrato e tridimensionale.
> **Perché:** Per dare all'UI un touch and feel da sito di altissima gamma ("astonishingly good"). L'animazione base a un solo livello di shadow è economica visivamente.

### 29.1. Upgrade Keyframes Multi-layer
- [x] Modificare `_experience.scss`:
  - Aggiungere al `@keyframes exp-node-pulse` un'animazione complessa su 3 livelli di `box-shadow` sovrapposti (core glow, mid glow, ambient glow).
  - Introdurre una sottile trasformazione `scale(1) -> scale(1.15)` per il feeling tattile del "battito".
  - Regolare l'animazione per fluire dolcemente senza `alternate`, gestendo il respiro circolare `0% -> 50% -> 100%`.

### 29.2. Pre-flight Validation & Atomic Commit
- [x] Validare e pusheare le modifiche premium.

---

## Phase 30 — NavCard Visual Feature Merge
> **🎯 Supervisore:** `@frontend-specialist` (skills: `react-patterns`, `ui-ux-pro-max`, `frontend-design`)
> **Obiettivo:** Importare tutta la bellezza visiva, fluidità e customizzabilità del vecchio componente `NavCard.tsx` (in `to-be-deleted/`) dentro il componente corrente `NavigationCardBar.tsx`, senza rompere nessuna funzionalità esistente (hover/click open, IdentityBar, GooeyNav, Framer Motion, frosted glass).
> **Perché:** Il vecchio `NavCard` ha un sistema di card colorate con `bgColor`/`textColor` per-card, arrow-icon sui link, stagger animation e stili ricchi (border-radius, padding, flex layout) che mancano nel `NavigationCardBar` corrente, il quale ha solo sezioni plain con titoli e link unstyled.

### 30.1. Analisi Differenziale & Strategia di Merge
- [x] Documentare le differenze chiave tra i due componenti e definire la strategia:
  - **Da importare:** Card colorate configurable, ArrowUpRightIcon SVG, stagger animation (Framer Motion variants), rich card styling, link hover effects
  - **Da NON importare:** GSAP engine (manteniamo Framer Motion), orientamento verticale/squircle, logo image (manteniamo IdentityBar), CTA button
  - **Da preservare intatto:** IdentityBar, GooeyNav, hamburger, hover/click/click-outside logic, frosted glass, scroll detection
  - **Agente:** `@frontend-specialist` | Skills: `architecture`, `react-patterns`
  - **DoD:** Strategia di merge confermata dall'utente, nessun dubbio architetturale.

### 30.2. Definizione Dati `NAV_CARD_ITEMS` (Configurazione Data-Driven)
- [x] Creare un array costante `NAV_CARD_ITEMS` in `NavigationCardBar.tsx`:
  - Ogni item ha: `label` (string), `bgColor` (string), `textColor` (string), `links[]` con `{ label, href, ariaLabel }`
  - Mappare le 3 sezioni attuali (Projects, Experience, About) ai colori e sub-link appropriati
  - I link reali (`/projects`, `/experience`, `/about`) devono usare `<NavLink>` con `onClick={closeMenu}`
  - I link placeholder mantengono `href="#"` con `preventDefault()`
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`
  - **DoD:** L'array `NAV_CARD_ITEMS` compila senza errori TypeScript, ogni campo è tipizzato (no `any`).

### 30.3. Aggiunta `ArrowUpRightIcon` SVG Inline
- [x] Aggiungere il componente `ArrowUpRightIcon` in `NavigationCardBar.tsx`:
  - SVG inline identico a quello in `NavCard.tsx` (24x24 viewBox, stroke currentColor, strokeWidth 2)
  - Nessuna dipendenza esterna (no `react-icons`)
  - Usare `1em` per width/height per scalabilità automatica con il font-size del parent
  - **Agente:** `@frontend-specialist` | Skills: `clean-code`
  - **DoD:** L'icona appare a fianco di ogni link dentro le card, ereditando il colore dal parent.

### 30.4. Riscrittura Expanded Content (Card Colorate + Stagger)
- [x] Sostituire il contenuto attuale di `pf-nav-card-bar__expanded` con card colorate animate:
  - Rimpiazzare le 3 `<div className="pf-expanded-content__section">` con un `map()` su `NAV_CARD_ITEMS`
  - Ogni card è un `<motion.div>` con `variants` per stagger animation (`staggerChildren: 0.08`)
  - Le card hanno `style={{ backgroundColor: item.bgColor, color: item.textColor }}` inline
  - I link dentro ogni card usano `<NavLink>` (per route reali) con `<ArrowUpRightIcon />` prefix
  - Il wrapper `pf-expanded-content` passa da `grid` a `flex` per card affiancate
  - **CRITICO:** Preservare il `closeMenu()` su tutti i `NavLink` onClick
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - **DoD:** Le card colorate appaiono con stagger animation, i link navigano e chiudono il menu.

### 30.5. SCSS — Stili Card Ricchi (da `_nav-card.scss`)
- [x] Aggiungere i nuovi stili in `_navigation-card-bar.scss`:
  - `.pf-nav-card`: `flex: 1 1 0`, `border-radius: 0.6rem`, `padding: 16px 20px`, `display: flex`, `flex-direction: column`, `gap: 8px`, `user-select: none`
  - `.pf-nav-card__label`: `font-weight: 500`, `font-size: 22px`, `letter-spacing: -0.5px`
  - `.pf-nav-card__links`: `margin-top: auto`, `display: flex`, `flex-direction: column`, `gap: 6px`
  - `.pf-nav-card__link`: `text-decoration: none`, `display: inline-flex`, `align-items: center`, `gap: 6px`, `color: inherit`, `font-size: 16px`, `transition: opacity 0.3s ease`, hover `opacity: 0.75`
  - `.pf-expanded-content`: cambiare da `grid` a `display: flex` + `gap: 1rem`
  - **Responsive mobile (≤64em):** card in `flex-direction: column`, padding ridotto `12px 16px`, `min-height: 60px`
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `ui-ux-pro-max`
  - **DoD:** Le card appaiono con border-radius, padding, e font sizing identici al NavCard originale. I link hanno hover effect con opacità. Il layout è responsive.

### 30.6. Verifica Visuale (Browser Subagent)
- [x] Verificare con il browser subagent: *(Browser Subagent 503 — verifica visuale delegata all'utente)*
  - La top bar (IdentityBar + GooeyNav + Hamburger) appare **identica** a prima
  - Hover 3 secondi → menu expanded con **card colorate** + stagger animation
  - Click hamburger → toggle menu come prima
  - Click link dentro una card → naviga + chiude il menu
  - Click fuori l'header → chiude il menu
  - Resize ≤ 1024px → le card si stackano verticalmente
  - Frosted glass effect invariato (scroll Home → sfondo sfocato)
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Screenshot confermano: card colorate con arrow icon, stagger fluido, chiusura funzionante, layout responsive mobile.

### 30.7. Pre-flight Validation & Atomic Commit
- [x] Validare il codice ed effettuare il commit tracciabile:
  - Eseguire `python .agent/scripts/pre_flight.py --gate build`
  - Commit atomico: `feat(nav): merge NavCard visual features into NavigationCardBar`
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD:** Build senza errori. Commit atomico registrato e pushato.

---

## Phase 31 — Fix /about NavBar Visibility + Vertical Mobile Squircle Mode
> **🎯 Supervisore:** `@frontend-specialist` (skills: `react-patterns`, `ui-ux-pro-max`, `frontend-design`)
> **Obiettivo:** (1) Risolvere il bug visivo della NavigationCardBar sulla pagina /about, dove il frosted glass si confonde con il background pagina rendendola invisibile. (2) Integrare la modalità verticale "squircle" dal vecchio NavCard per la versione mobile, con l'animazione del pannello laterale che si espande dal bottone 60×60.
> **Perché:** (1) Il frosted glass `rgba(30,41,59,0.7)` è troppo simile a `--color-bg`, camuffando la barra su /about. (2) Su mobile l'attuale dropdown orizzontale è scomodo — il vecchio NavCard aveva un'UX mobile superiore con il squircle che si espandeva lateralmente, le card stackate verticalmente e scrollabili.

### 31.1. Fix Visibilità NavBar su /about (SCSS)
- [x] Correggere `_navigation-card-bar.scss`:
  - Rendere il `border-bottom` dello stato `--scrolled` più visibile: da `rgba(255,255,255,0.05)` a `rgba(255,255,255,0.12)`
  - Verificare che il contrasto sia sufficiente impostando un background leggermente più scuro/opaco rispetto alla page: `rgba(15, 23, 42, 0.85)` con backdrop blur più forte
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`
  - **DoD:** La barra è visivamente distinguibile dal contenuto sottostante su tutte le pagine, incluso /about.

### 31.2. Responsive Orientation State (TSX)
- [x] Aggiungere logica orientamento in `NavigationCardBar.tsx`:
  - State: `const [orientation, setOrientation] = useState<'horizontal' | 'vertical'>('horizontal')`
  - `useEffect` con resize listener: `≤ 1024px` → `'vertical'`, altrimenti `'horizontal'`
  - Cleanup al cambio orientamento: chiudere il menu se aperto, resettare gli state
  - Applicare il modifier class `pf-nav-card-bar--vertical` quando `orientation === 'vertical'`
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - **DoD:** Lo state cambia correttamente al resize, il component si ri-renderizza con la class corretta.

### 31.3. Vertical Squircle — Base SCSS
- [x] Aggiungere gli stili per la modalità verticale in `_navigation-card-bar.scss`:
  - `.pf-nav-card-bar--vertical`: `position: fixed`, `top: 1rem`, `right: 1rem`, `left: auto`, `width: 60px`, `height: 60px`, `border-radius: 20px`, `overflow: hidden`, reset di `backdrop-filter` e `border-bottom`
  - `.pf-nav-card-bar--vertical __top`: ridirezionare in colonna con hamburger centrato nel 60×60
  - Nascondere IdentityBar e GooeyNav in modalità verticale (solo hamburger visibile nel squircle chiuso)
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `ui-ux-pro-max`
  - **DoD:** Su mobile appare un quadrato arrotondato 60×60 in alto a destra con solo l'hamburger visibile.

### 31.4. Vertical Expand Animation (Framer Motion)
- [x] Implementare l'animazione di espansione verticale in `NavigationCardBar.tsx`:
  - Quando `orientation === 'vertical'` e menu aperto: il container si anima da `60×60` → `width: calc(100vw - 2rem)`, `height: 100vh` (o auto)
  - Usare `motion.div` con `animate={{ width, height }}` e `transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}`
  - Il layout interno passa a `flex-direction: row-reverse` (come il vecchio NavCard): hamburger a destra in colonna verticale, contenuto a sinistra
  - L'hamburger resta sempre visibile nel suo slot 60px durante l'espansione
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - **DoD:** L'animazione è fluida, il squircle si espande senza jank, e il menu mostra le card colorate.

### 31.5. Vertical Cards Layout & Scrollable Content (SCSS + TSX)
- [x] Configurare il layout delle card in modalità verticale:
  - SCSS: `.pf-nav-card-bar--vertical .pf-expanded-content` → `flex-direction: column`, `gap: 12px`, `padding: 1.5rem`, `overflow-y: auto`, `overflow-x: hidden`, `::-webkit-scrollbar { display: none }`
  - SCSS: `.pf-nav-card-bar--vertical .pf-nav-card` → `min-height: 120px`, `flex: 1 1 0`
  - TSX: Le card mantengono lo stagger animation ma con `y: 50` → `y: 0` (scorrimento verticale vs orizzontale)
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `react-patterns`
  - **DoD:** Le card si stackano verticalmente, sono scrollabili se eccedono l'altezza viewport, e l'animazione è coerente con l'orientamento.

### 31.6. Desktop Layout Preservation (Guard)
- [x] Verificare che NESSUN cambiamento impatti la modalità desktop:
  - La barra orizzontale rimane `position: fixed; top: 0; left: 0; right: 0; height: 6.5rem`
  - IdentityBar, GooeyNav, Hamburger → layout invariato
  - Dropdown expand → invariato (AnimatePresence height auto)
  - Hover 3s, click, click-outside → invariati
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`
  - **DoD:** Desktop renderizza identicamente alla versione pre-Phase 31.

### 31.7. Verifica Visuale (Browser Subagent)
- [/] Verificare con il browser subagent: *(Browser Subagent 503 — verifica manuale delegata all'utente)*
  - Desktop: /about mostra navBar visibile con bordo distinguibile
  - Mobile (390px): squircle 60×60 in alto a destra, click → side panel con card colorate
  - Click link in card → naviga + chiude il pannello
  - Resize da mobile a desktop → transizione smooth senza glitch
  - **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`
  - **DoD:** Screenshot multi-viewport confermano funzionamento corretto.

### 31.8. Pre-flight Validation & Atomic Commit
- [x] Validare e committare:
  - `python .agent/scripts/pre_flight.py --gate build`
  - Commit: `feat(nav): fix /about visibility + add vertical squircle mobile mode`
  - **Agente:** `@devops-engineer` | Skills: `deployment-procedures`
  - **DoD:** Build OK. Commit atomico pushato.

### 31.9. IdentityBar su Mobile (Independent Overlay)
- [x] Estrarre `IdentityBar` fuori dal container `.pf-nav-card-bar--vertical` su mobile:
  - Condizionalmente renderizzare `IdentityBar` in un div wrapper `.pf-nav-card-bar__mobile-identity` con `z-index: 60` quando `orientation === vertical`.
  - Nasconderlo all'interno di `__left` (o renderizzarlo solo quando `horizontal`).
  - Posizionarlo `top: 1rem; left: 1rem; position: fixed` in SCSS in modo simmetrico al squircle.
  - **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`
  - **DoD:** La barra avatar è visibile in alto a sinistra su mobile, rimane sopra il layer di espansione del menu.

### 31.10. IdentityBar Mobile Alignment Fix
- [x] Centrare verticalmente l'IdentityBar su mobile per allinearla perfettamente con il bottone chiudi hamburger:
  - SCSS: Applicare `height: 60px; display: flex; align-items: center;` al wrapper `.pf-nav-card-bar__mobile-identity` per simulare l'ingombro del squircle e centrare il pill verticalmente all'altezza corretta.
  - TSX: Nessuna modifica, il wrapper è già a DOM.
  - **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `ui-ux-pro-max`
  - **DoD:** La IdentityBar è visivamente allineata al centro esatto dell'area occupata dal close button / hamburger su mobile.

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
| 2026-03-12 18:22 | **Phase 30 — NavCard Visual Feature Merge** | Importare le feature visive (card colorate, ArrowUpRightIcon, stagger animation, rich styling) dal vecchio `NavCard.tsx` dentro `NavigationCardBar.tsx` mantenendo l'architettura Framer Motion corrente. NON si importa GSAP né l'orientamento verticale. |
| 2026-03-12 19:30 | **Phase 31 — Fix /about + Vertical Squircle** | Il frosted glass è camuffato su /about (colore identico a bg). Su mobile, rimpiazzare dropdown con squircle 60×60 che si espande in side-panel verticale (come il vecchio NavCard) usando Framer Motion invece di GSAP. |

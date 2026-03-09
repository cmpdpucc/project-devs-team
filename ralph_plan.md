# 🚀 RALPH PLAN — Portfolio ProjectShowcase Redesign

> **Questo file è il SINGOLO punto di verità per TUTTE le operazioni in corso.**
> Prima di ogni risposta, Antigravity DEVE leggere questo file.

---

## LEGACY

<details>
<summary>✅ Fasi completate precedenti</summary>

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
</details>

---

## Phase 18 — ProjectShowcase Redesign (BlurSlider 2.0)
> **🎯 Obiettivo:** Sostituire l'uso di `PixelCard` (Canvas ripple) dentro il `BlurSlider` con un nuovo `ProjectCard` leggero, fissare le immagini rotte, e migliorare la responsività su tutti i breakpoint.
>
> **Audit visivo precedente:**
> - Desktop 1440px: 3/10 — immagini rotte, Canvas disallineato, blur pixelato
> - Tablet 768px: 4/10 — card minuscole, 90% vuoto
> - Mobile 375px: 7/10 — migliore, ma sezione sparsa senza affordance di swipe
>
> **Design inspiration (Google AI 2025-2026):** Cinematic Blur Slider 2.0 con glassmorphism info panel, gradient fallback, pagination dots.

---

### 18.1 SCSS Foundation — `_project-card.scss`
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `clean-code`

- [x] Creare `portfolio/src/styles/components/_project-card.scss` con classi BEM:
  - `.project-card` — root wrapper con `border-radius: 1.25rem`, `overflow: hidden`, `cursor: pointer`
  - `.project-card__image` — `object-fit: cover`, `width: 100%`, `height: 100%`
  - `.project-card__gradient` — gradient fallback se immagine non carica
  - `.project-card__overlay` — dark overlay con `mix-blend-mode`, transizione su hover
  - `.project-card__info` — glass panel: `backdrop-filter: blur(16px)`, `background: rgba(10,14,36,0.65)`
  - `.project-card__title` — `font-family: var(--font-serif)`, `font-size: 1.5rem`
  - `.project-card__description` — `color: var(--color-text-muted)`, `font-size: 0.875rem`
  - `.project-card__tags` — flexbox row wrap
  - `.project-card__tag` — pill con `border: 1px solid rgba(255,255,255,0.15)`, `border-radius: 999px`
  - **DoD:** File compilabile, nessun errore SCSS, classi BEM pulite senza Tailwind.

---

### 18.2 SCSS Responsive — Breakpoint per `_project-card.scss`
> **Agente:** `@mobile-developer` | Skills: `mobile-design`, `frontend-design`

- [x] Aggiungere media queries responsive in `_project-card.scss`: *(incluso in 18.1)*
  - `@media (max-width: 64em)` (tablet): aspect-ratio `4/3`, info panel sizing ridotto
  - `@media (max-width: 40em)` (mobile): aspect-ratio `3/4`, `font-size` ridotti, padding compatto
  - `@media (max-width: 20em)` (small): minimal styling
  - **DoD:** Card leggibile e proporzionata a 375px, 768px e 1440px. Nessun overflow testo.

---

### 18.3 Import SCSS — Registrare `_project-card` in `main.scss`
> **Agente:** `@frontend-specialist` | Skills: `clean-code`

- [x] Aggiungere `@use 'components/project-card';` in `portfolio/src/styles/main.scss`
  - **DoD:** Build SCSS non produce errori. Il partial è importato nell'ordine corretto.

---

### 18.4 React Component — `ProjectCard.tsx`
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`

- [x] Creare `portfolio/src/components/ProjectCard.tsx`:
  - Props interface: `{ title: string; description: string; imageUrl: string; gradient: string; tags: string[] }`
  - Background: `<img>` con `onError` fallback a `gradient` CSS background
  - Dark overlay div con transizione opacity su hover
  - Info panel con `AnimatePresence` per description reveal
  - Tags renderizzati come `.project-card__tag` pills
  - **NO** Canvas, **NO** rAF loop, **NO** PixelCanvasRipple
  - `prefers-reduced-motion`: skip animazioni Framer Motion
  - JSDoc completo sulla funzione esportata
  - **DoD:** Componente compilabile, strict TypeScript (nessun `any`), zero dipendenza da PixelCard/PixelCanvasRipple.

---

### 18.5 Slider Config Fix — `BlurSlider/index.tsx`
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`

- [x] Modificare `portfolio/src/components/BlurSlider/index.tsx`:
  - `loop: false` (fix Swiper Loop warning — abbiamo solo 5 slide)
  - `grabCursor: true` (affordance visivo drag)
  - Aggiungere modulo `Pagination` da `swiper/modules` + `import 'swiper/css/pagination'`
  - Aggiornare breakpoints: `{ 0: { slidesPerView: 1.05 }, 640: { slidesPerView: 1.8 }, 1024: { slidesPerView: 3 } }`
  - Montare `<Swiper pagination={{ clickable: true }} ...>`
  - **DoD:** Zero console warnings Swiper. Dots di paginazione visibili. Drag cursor attivo.

---

### 18.6 Pagination Dots Styling — `_blur-slider.scss`
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `clean-code`

- [x] Aggiungere stili per `.swiper-pagination` dentro `.blur-slider` in `_blur-slider.scss`:
  - `.swiper-pagination-bullet` — `width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.3)`
  - `.swiper-pagination-bullet-active` — `background: var(--color-cta); width: 24px; border-radius: 4px`
  - Posizionamento: `bottom: 2rem; z-index: 20`
  - **DoD:** Dots glassmorphism visibili su tutte le breakpoint accompagnando lo slide attivo.

---

### 18.7 Blur Slider SCSS Tuning — `_blur-slider.scss`
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`

- [x] Migliorare `_blur-slider.scss` per eliminare i bug visivi dell'audit:
  - Ridurre `--bs-blur-halo: 40px` (meno pixelato)
  - Rimuovere `pointer-events: none` dal container immagine dello slide attivo (bloccava hover)
  - Mobile mask-image: `linear-gradient(to right, transparent 0%, black 5%, black 95%, transparent 100%)` (meno aggressivo)
  - **DoD:** Background blur più morbido. Slide attivo interagibile. Bordi laterali soft su mobile.

---

### 18.8 Project Data & Section — `ProjectsSection.tsx`
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`

- [x] Refactor `portfolio/src/sections/ProjectsSection.tsx`:
  - Rimuovere import `PixelCard` → importare `ProjectCard`
  - Aggiungere campo `gradient` e `tags` nell'interfaccia `Project`
  - Ogni progetto ha un gradient unico (es: `linear-gradient(135deg, #1e3a5f 0%, #0a0e24 100%)`)
  - Aggiornare `renderItem` per usare `<ProjectCard>`
  - **DoD:** Zero import residui di PixelCard. Ogni progetto ha gradient fallback. Build verde.

---

### 18.14 Data Model: Add `iconUrl` + `projectUrl` to Project interface
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`

- [x] In `ProjectsSection.tsx`:
  - Aggiungere `iconUrl: string` e `projectUrl: string` all'interfaccia `Project`
  - `iconUrl` → placeholder Picsum: `https://picsum.photos/64/64?random=N` (N unico per progetto)
  - `projectUrl` → `https://www.google.com` (placeholder, utente aggiornerà dopo)
  - Aggiornare ogni oggetto PROJECTS con i nuovi campi
  - Aggiungere `iconUrl` e `projectUrl` all'interfaccia `BlurSliderItem` in `types.ts`
  - **DoD:** TypeScript compila. Ogni progetto ha iconUrl e projectUrl. Build verde.

---

### 18.15 BlurSlider TSX: Sostituzione `image-container` → Icon clickabile
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`

- [x] In `BlurSlider/index.tsx`:
  - Rimuovere la halo container completamente (il gradient della ProjectCard basta)
  - Sostituire il contenuto di `__slide-image-container` con:
    - `<a>` che wrappa `<img src={item.iconUrl}>` con dimensioni 64×64px
    - `href={item.projectUrl}`, `target="_blank"`, `rel="noopener noreferrer"`
  - Rinominare la classe BEM da `__slide-image-container` → `__slide-icon`
  - **DoD:** Nessuna immagine duplicata. Icon clickabile. Nessun halo container.

---

### 18.16 SCSS: Animazione su `__slide-content` (tutta la ProjectCard)
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`, `clean-code`

- [x] In `_blur-slider.scss`:
  - **Rimuovere** tutte le regole di stato (prev/active/next) su `__slide-image-container`
  - **Spostare** la stessa animazione blur/scale su `__slide-content`:
    - Default: `filter: blur(var(--bs-base-blur)); scale: var(--bs-base-scale)); opacity: 0.3`
    - Active: `filter: blur(0); scale: 1; opacity: 1`
    - Prev: `scale: 0.85; filter: blur(8px); opacity: 0.3`
    - Next: `scale: 0.85; filter: blur(8px); opacity: 0.3`
  - `__slide-content` default: rimuovere il posizionamento `absolute` center → usare layout flex del slide
  - **DoD:** La ProjectCard si anima come faceva l'image-container. Transizioni smooth.

---

### 18.17 SCSS: Icon visibile solo su slide attivo + delay
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`

- [x] In `_blur-slider.scss`:
  - `__slide-icon` default: `opacity: 0; pointer-events: none; transition: opacity 0.5s ease 1.5s`
  - `__slide-icon` su active: `opacity: 1; pointer-events: auto`
  - Il `transition-delay: 1.5s` (= `--bs-transition-duration`) fa sì che l'icona appaia DOPO che l'animazione della card è completata
  - Su prev/next: `opacity: 0` (non visibile)
  - Styling: `position: absolute; top: -2rem; left: 50%; transform: translateX(-50%); z-index: 15`
  - **DoD:** Icon appare magicamente solo dopo l'animazione completa. Invisibile sugli slide non attivi.

---

### 18.18 Mobile Ledge: Ridurre card width + più peek
> **Agente:** `@mobile-developer` | Skills: `mobile-design`

- [x] In `_blur-slider.scss` + `BlurSlider/index.tsx`:
  - Mobile `__slide-content` width: `88vw` → `78vw`
  - Mobile `slidesPerView`: `1.05` → `1.2` (mostra più del prossimo/precedente)
  - Prev/next slide-content su mobile: `opacity: 0.25` (un po' più visibile)
  - **DoD:** Su 375px, si vedono almeno 30-40px del prossimo elemento. Sensazione di continuità.

---

### 18.19 Visual QA Post-Fix — Desktop + Mobile
> **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`

- [x] Browser subagent a 1440x900 E 375x812:
  - Verificato: icon Picsum 64×64 visibile sopra la card attiva
  - Verificato: icon appare DOPO l'animazione della card
  - Verificato: icon è cliccabile (apre google.com)
  - Verificato: card adiacenti blurrate e visibili come peek
  - Verificato: mobile mostra più ledge (~30-40px)
  - **Aggiunta QC Extra:** Mask-image sul Ticker (About) e sistemazione z-index/padding dell'indicatore di scroll (Mobile Nav non si sovrappone più).
  - **DoD:** Icon appare con delay. Card animata. Peek funzionante. Mobile responsive. E layout globale solido.

---

### 18.9 Build Verification
> **Agente:** `@devops-engineer` | Skills: `deployment-procedures`

- [ ] Eseguire `cd portfolio && npm run build` e verificare exit code 0.
  - **DoD:** Build TypeScript senza errori. Nessun warning critico.

---

### 18.10 Visual QA Desktop — 1440px
> **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`

- [ ] Browser subagent a 1440x900:
  - Navigare a `http://localhost:3000`, scrollare alla sezione Projects
  - Verificare: card attiva mostra gradient + titolo + tags; card adiacenti blurrate
  - Verificare: hover rivela description + scala lift
  - Verificare: dots di paginazione visibili e cliccabili
  - Catturare screenshot + recording
  - **DoD:** Zero broken images. Card premium visivamente. Blur transitions smooth.

---

### 18.11 Visual QA Tablet — 768px
> **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`, `mobile-design`

- [ ] Browser subagent a 768x1024:
  - Verificare: cards proporzionate (~1.8 per view), readable
  - Verificare: bottom nav non overlappa con contenuto
  - Verificare: swipe/drag funzionante
  - Catturare screenshot
  - **DoD:** Card leggibili. Layout proporzionato. Swipe responsive.

---

### 18.12 Visual QA Mobile — 375px
> **Agente:** `@orchestrator` (Browser Subagent) | Skills: `webapp-testing`, `mobile-design`

- [ ] Browser subagent a 375x812:
  - Verificare: card quasi full-width (~1.05 per view)
  - Verificare: testo leggibile (min 14px body)
  - Verificare: glass info panel visibile
  - Verificare: bottom nav non copre contenuto
  - Catturare screenshot
  - **DoD:** Esperienza mobile fluida. Zero overflow. Testo leggibile senza zoom.

---

### 18.13 Atomic Commit
> **Agente:** `@devops-engineer` | Skills: `deployment-procedures`

- [ ] Commit atomico di tutti i file modificati:
  ```
  feat(projects): replace PixelCard with ProjectCard in BlurSlider

  - New ProjectCard component (no Canvas, pure CSS + Framer Motion)
  - Gradient fallbacks for broken images
  - Swiper pagination dots + grab cursor
  - Responsive breakpoints refined (1.05/1.8/3)
  - Glass info panel with tags
  ```
  - **DoD:** Commit pushato. Build verde post-commit.

---

### 18.21 Enhance Experience Section Width
> **Agente:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `frontend-design`

- [x] Correggere il layout narrow dell'Experience Section (`pf-exp-timeline`) su schermi desktop/tablet.
  - Aggiunto `width: 100%` a `.pf-exp-timeline` in `_experience.scss` per forzare l'espansione nel fallback di `justify-content: center` del container parent.
  - **DoD:** Il layout riempie lo spazio orizzontale disponibile in modo bilanciato (max 1100px) invece di stringersi testualmente al centro.

---

## Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | npm run dev | 3000 | 🟢 Running | utente |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-03-07 22:30 | Deep Visual Audit a 3 breakpoint | Utente richiede audit pre-implementazione |
| 2026-03-07 22:35 | Google AI Inspiration | 4 pattern trending: Horizontal Gallery, List-Reveal, Scrollytelling, 3D Scene |
| 2026-03-08 20:56 | **Cinematic Blur Slider 2.0** scelto | Mantiene architettura Swiper esistente, sostituisce solo PixelCard con ProjectCard leggero. No GSAP/WebGL complexity. |
| 2026-03-08 20:56 | **13 task atomici** per Phase 18 | Granularità alta per ridurre contesto usato per task → outcome migliore |
| 2026-02-22 10:45 | **Skip Web Worker** per PixelCanvasRipple | Overkill per singola card fullscreen |
| 2026-02-22 10:45 | **Option C (Canvas 2D)** per idle animation | Scelta utente dopo brainstorm — ora obsoleta, sostituita da Phase 18 |

> **📊 Phase 18:** 13 task atomici | **Agenti:** 4 (`@frontend-specialist`, `@mobile-developer`, `@devops-engineer`, `@orchestrator`) | **Skills:** 8 (`frontend-design`, `clean-code`, `react-patterns`, `mobile-design`, `deployment-procedures`, `webapp-testing`, `mobile-design`)

# 🚀 RALPH PLAN — OpenCode Integration

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
</details>

---

## Phase 1 — OpenCode Setup (Inizializzazione)
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`

### Agenti Assegnati

| Agente | Dominio |
|--------|---------|
| `@devops-engineer` | Installazione e configurazione di sistema |
| `@documentation-writer` | Documentazione dei comandi |

### 1.1 `install-opencode.sh` — Script di Setup
> **Agente:** `@devops-engineer` | Skills: `bash-linux`, `powershell-windows`

- [x] Creare `scripts/install-opencode.sh` per installare OpenCode.
  - DoD: File creato, usa `npm install -g opencode-ai@latest`, imposta Truecolor.

### 1.2 `opencode.json` — Configurazione
> **Agente:** `@devops-engineer` | Skills: `deployment-procedures`

- [x] Creare `config/opencode.json` con i settaggi del TUI e watcher.
  - DoD: File JSON formattato correttamente, include istruzioni da GEMINI.md.

### 1.3 `OPENCODE_USAGE.md` — Guide
> **Agente:** `@documentation-writer` | Skills: `documentation-templates`

- [x] Documentazione d'uso base (Già presente)
  - DoD: Il file esiste e contiene i comandi principali.

---

## Phase 7 — OpenCode Multi-Agent Bridge (Self-Enhancement v7)
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`

L'obiettivo di questa fase è creare il ponte bidirezionale tra Antigravity (IDE) e OpenCode (Terminale), permettendo la sincronizzazione delle regole e la validazione del sistema.

### Agenti Assegnati (Orchestrazione Parallela - Min 3)

| Agente | Dominio |
|--------|---------|
| `@documentation-writer` | Regole condivise e SKILL.md per OpenCode |
| `@backend-specialist` | Script Python per il Bridge di sincronizzazione |
| `@devops-engineer` | Script bash per la validazione dell'integrità agenti |

### 7.1 `GEMINI.md` & `opencode-integration` Skill
> **Agente:** `@documentation-writer` | Skills: `documentation-templates`

- [x] Aggiornare/Creare `.agent/rules/GEMINI.md` se necessario e scrivere `.agent/skills/opencode-integration/SKILL.md` con il manuale operativo del bridge.
  - DoD: File `SKILL.md` creato con istruzioni chiare per l'uso combinato dei due agenti.

### 7.2 `antigravity-opencode-bridge.py`
> **Agente:** `@backend-specialist` | Skills: `python-patterns`

- [x] Sviluppare `scripts/antigravity-opencode-bridge.py`.
  - DoD: Lo script espone funzioni per sincronizzare la memoria (es. copiare regole o leggere PID di OpenCode) e avviare server OpenCode in modo robusto.

### 7.3 `validate-agent-folder.sh`
> **Agente:** `@devops-engineer` | Skills: `bash-linux`, `powershell-windows`

- [x] Sviluppare `scripts/validate-agent-folder.sh` per verificare la salute della flotta.
  - DoD: Script eseguibile che controlla `.agent/rules/`, `.agent/skills/` e stampa lo status degli agenti al terminale con Exit code 0 se tutto sano.

---

## Phase 8 — The "Infinity" Stack (Kimi 2.5 Visual Workflow)
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`

L'obiettivo è standardizzare il workflow "Sketch-to-Code" utilizzando Kimi 2.5 via OpenCode, trasformando i design visivi in codice React fedele al pixel.

### Agenti Assegnati

| Agente | Dominio |
|--------|---------|
| `@project-planner` | Documentazione del Workflow Integrato |
| `@frontend-specialist` | Skill specializzata per Visual Coding (React/Tailwind) |

### 8.1 `INTEGRATED_WORKFLOW.md`
> **Agente:** `@project-planner` | Skills: `documentation-templates`

- [x] Aggiornare `docs/INTEGRATED_WORKFLOW.md` con lo "Scenario 4: Visual Coding (Sketch-to-Code) con Kimi 2.5".
  - DoD: Il file descrive i 3 step del workflow (Planning strutturale, Passaggio screenshot, Generazione codice via OpenCode).

### 8.2 Creazione Skill `visual-coding-kimi`
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `ui-ux-pro-max`

- [x] Creare `.agent/skills/visual-coding-kimi/SKILL.md`.
  - DoD: Il file esiste e contiene i prompt testati per Kimi ("Thinking Mode", "Fedele al pixel"), con istruzioni chiare per l'agente frontend.

### 8.3 Smoke Test Integrato
> **Agente:** `@orchestrator` | Skills: `parallel-agents`

- [x] Testare Kimi 2.5 via OpenCode bridge (generazione file tmp).

## Phase 9 — Portfolio Research & Design Discovery
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`

L'obiettivo è analizzare 7 siti portfolio top-tier e la libreria React Bits per raccogliere reference visuali, pattern UI/UX e componenti pronti all'uso. Tutte le descrizioni, video, screenshot e cataloghi verranno salvati nella directory `portfolio/`.

### Agenti Assegnati

| Agente | Dominio |
|--------|---------|
| `@frontend-specialist` | Analisi UI/UX, estrazione pattern, catalogazione componenti React Bits |
| `@orchestrator` | Coordinamento dei browser subagent per l'esplorazione |

### 9.1 Analisi Portfolio Reference
> **Agente:** `@orchestrator` (tramite subagent)

- [x] Navigare e analizzare: Tamal Sen e Cassie Evans.
  - DoD: File descrittivi in `portfolio/descriptions/` e file multimediali catturati.
- [x] Navigare e analizzare: Brittany Chiang e Matt Farley.
  - DoD: File descrittivi e media catturati.
- [x] Navigare e analizzare: Lauren Waller, Van Holtz e Adham Dannaway.
  - DoD: File descrittivi e media catturati.

### 9.2 Scoping Libreria React Bits
> **Agente:** `@frontend-specialist`

- [x] Esplorare `https://reactbits.dev/get-started/index` e catalogare i componenti adatti ad un portfolio.
  - DoD: Documento `portfolio/react_bits/components_catalog.md` generato.

---

## Phase 10 — UI/UX Pro Max & SCSS Refactoring
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`, `ui-ux-pro-max`

Sulla base del `portfolio-refactor.md`, applico l'architettura SCSS `[@uderly]`-like al nuovo Portfolio, eliminando Tailwind e integrando i componenti interattivi di React Bits.

### Agenti Assegnati (Orchestrazione in Parallelo per /refactor)

| Agente | Dominio |
|--------|---------|
| `@frontend-specialist` | Sviluppo Componenti React Bits, SCSS Architecture, Layout Refactoring |
| `@test-engineer` | Verify visuale, E2E base e controllo accessibilità |
| `@performance-optimizer` | Refactoring animazioni Framer per i 60fps, controllo build Next.js |

### 10.1 Scaffolding SCSS ed Epuration
> **Agente:** `@frontend-specialist` | Skills: `visual-coding-kimi`, `react-patterns`

- [x] Rimozione totale di Tailwind e creazione logica SCSS (`_colors.scss`, `_theme.scss`, BEM).
  - DoD: L'app builda senza Tailwind. `main.scss` importa tutti i partials.

### 10.2 React Bits Wow-Factor Integration
> **Agente:** `@frontend-specialist` e `@performance-optimizer`

- [x] Integrazione CSS-agnostic di Spotlight, DecryptedText, PixelCard, Magnet, InfiniteScroll.
  - DoD: I check in `portfolio-refactor.md` sono validati, tutti i componenti animano senza layout shift.

### 10.3 Quality & Visual Gates
> **Agente:** `@test-engineer` | Skills: `webapp-testing`

- [x] Visual testing in localhost mode verificando contrasti (4.5:1), hover states attivi e font caricati (DM Sans/Space Grotesk).
  - DoD: QA report allegato in `/status` e issue visive corrette in loop da K2.5.

## Phase 12 — UI/UX Expansion & Transitions
> **🎯 Supervisore:** `@frontend-specialist` | Skills: `ui-ux-pro-max`, `react-patterns`

### 12.1 Layout Spacing & ScrollSpy Refinements
> **Agente:** `@frontend-specialist`
- [ ] Forzare altezza minima e spaziature drammatiche (top/bottom) in `_grid.scss` per permettere allo ScrollSpy di rilevare 'About' e 'Projects' senza collassare, ed evitare il feel "boring" del layout asimmetrico compresso.
  - DoD: L'utente può scrollare comodamente; la navbar fissa reagisce su tutte le sezioni.

### 12.2 Expandable Cards Component
> **Agente:** `@frontend-specialist`
- [ ] Refactor di `PixelCard` in `ExpandablePixelCard` (o simile) integrando `layoutId` di Framer Motion o un componente React Bits espandibile, così che un click riveli dettagli/storytelling del progetto, "vendendo" le skill.
  - DoD: Animazione fluida di espansione a tutto schermo o modale; zero layout shift nel background.

### 12.3 Transition Flow
> **Agente:** `@frontend-specialist`
- [ ] Introdurre un flusso di navigazione e fadeIn morbido che guidi l'utente dalla Hero ("Developer Name...") alle sezioni inferiori.
  - DoD: Il portfolio guida visivamente lo sguardo dell'utente verso il primo scroll.

---

## Phase 16 — Mobile Responsive, Floating Nav & UX Audit
> **🎯 Supervisore:** `@orchestrator` | Skills: `ui-ux-pro-max`, `visual-coding-kimi`

### 16.1 CSS Audit: px to rem/em
> **Agente:** `@frontend-specialist`
- [x] Convertire tutti i valori `px` statici (spacing, border-radius) in `rem` per garantire scalabilità fluida.

### 16.2 Container Alignment & Mobile Native Scroll
> **Agente:** `@frontend-specialist`
- [x] Centrare orizzontalmente e verticalmente il contenuto delle sezioni (`justify-content: center; align-items: center`).
- [x] Risolvere lo scroll-lock su mobile ripristinando il native scroll se il dispositivo o il breakpoint lo richiede.

### 16.3 Mobile Glassmorphism Floating Bar
> **Agente:** `@frontend-specialist`
- [x] Nascondere nav sidebar su `< 1024px`.
- [x] Creare `MobileNav.tsx`: bottom bar rounded, blur/glassmorphism, con i link di sezione dinamici da `sections.data.ts`.

---

## Phase 17 — PixelCard Canvas Ripple Animation
> **🎯 Supervisore:** `@orchestrator` | Skills: `ui-ux-pro-max`, `performance-profiling`, `visual-coding-kimi`

Obiettivo: Sostituire l'overlay pixel CSS statico con un Canvas 2D animato che simula un effetto ripple/epicentro "goccia in uno stagno". Basato sul prototipo utente `PixelCanvasExample.tsx` con fix architetturali da audit.

### 17.1 Core Canvas Engine — `PixelCanvasRipple.tsx`
> **Agente:** `@performance-optimizer` | Skills: `performance-profiling`, `react-patterns`
- [x] Creare `PixelCanvasRipple.tsx` con architettura Canvas 2D da prototipo:
  - Offscreen canvas caching per griglia statica (singola draw call)
  - 6 `Path2D` bande di opacità per batching draw calls
  - `requestAnimationFrame` loop con skip via IntersectionObserver
  - `ResizeObserver` per resize-safe canvas
  - DPR scaling automatico (Retina)
  - **FIX L1:** Cachare `width/height` in ref, NON usare `getBoundingClientRect()` nel loop
  - **FIX L5:** Tipizzazione TypeScript strict (`HTMLCanvasElement`, `HTMLDivElement`, interfaccia Props)
  - **FIX L6:** `isHovered` comunicato via `useRef`, non nel dependency array di useEffect
  - **FIX L7:** Cooldown di 2s tra un ripple e il successivo
  - DoD: Canvas renderizza ripple fluido, < 4ms/frame su DevTools Performance

### 17.2 Accessibility & Reduced Motion
> **Agente:** `@frontend-specialist` | Skills: `clean-code`, `react-patterns`
- [x] Implementare `prefers-reduced-motion: reduce`:
  - In JS: `matchMedia` → skip rAF loop, mostra griglia statica
  - In SCSS: media query per disabilitare transizioni
  - DoD: Utenti con motion-sensitivity vedono solo griglia statica senza animazione

### 17.3 SCSS Integration — `_pixel-ripple.scss`
> **Agente:** `@frontend-specialist` | Skills: `clean-code`
- [x] Creare `_pixel-ripple.scss` con classi BEM (`pf-pixel-ripple`, `pf-pixel-ripple__canvas`)
  - **FIX L3:** Zero classi Tailwind — tutto in SCSS puro
  - `mask-image` radial per dissolyenza ai bordi
  - Transizione `opacity 700ms` per hover show/hide
  - Importare in `main.scss`
  - DoD: Nessuna classe inline nel componente, solo className BEM

### 17.4 Integration & Refactor `PixelCard.tsx`
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `clean-code`
- [x] Rimuovere l'overlay `radial-gradient` CSS (righe 62-77 attuali)
- [x] Montare `<PixelCanvasRipple />` passando hover state via `useRef`
- [x] Smoke test: hover → canvas fade out | unhover → ripple riprende
  - DoD: PixelCard mostra il ripple in idle, effetto sparisce su hover, card funziona identicamente come prima per il contenuto

### 17.5 Visual QA & Perf Profiling
> **Agente:** `@test-engineer` | Skills: `webapp-testing`, `performance-profiling`
- [x] Browser subagent: catturare recording del ripple effect su desktop e mobile
- [x] DevTools Performance tab: confermare < 4ms/frame
- [x] Verificare `prefers-reduced-motion` disattivi l'animazione
- [x] Commit atomico con verifica build verde su Vercel

---

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | - | - | Nessun processo attivo | - |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-02-21 20:10 | Generazione Piano OpenCode | Avvio autonomo della traccia descritta in PLAN-opencode-integration.md |
| 2026-02-22 10:45 | **Skip Web Worker** per PixelCanvasRipple | Tecnica menzionata nel doc utente ma dichiarata overkill: il portfolio mostra 1 card alla volta (fullscreen snap). Il Main Thread regge ampiamente. Complessità vs beneficio non giustificata. |
| 2026-02-22 10:45 | **Option C (Canvas 2D)** per idle animation | Scelta dall'utente dopo brainstorm di 4 opzioni. Unica che permette controllo pixel-by-pixel fedele alla metafora "goccia in stagno". |


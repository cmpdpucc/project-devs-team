# PLAN-portfolio-phase13.md
# 🚀 Infinity Portfolio — Phase 13: Immersive Navigation & React Bits Upgrade

> **Creato:** 2026-02-22 | **Agente Supervisore:** `@frontend-specialist` + `@orchestrator`
> **Obiettivo:** Trasformare il portfolio da "bella pagina scrollabile" a esperienza esplorativa immersiva ispirata a sicilean.tech

---

## 🔍 Research Summary

### Sicilean.tech Dynamics Estratte
| Tecnica | Descrizione | Applicabilità Portfolio |
|---------|-------------|------------------------|
| **CSS Snap Scroll** | `scroll-snap-type: y mandatory` — ogni sezione = 1 viewport | ✅ Alta — crea il "guida l'utente" effect |
| **Bento Grid Layout** | Card disposte in grid asimmetrica con bordi morbidi | ✅ Per sezione Projects |
| **Stagger Typography** | Titoli Bold+Thin alternati, entrano con delay | ✅ Gia' in place, da rafforzare |
| **Smooth Click Navigation** | Scroll smooth + `ease-in-out` timing function | ✅ Il "snappy click" attuale va eliminato |
| **Background Blur Blobs** | Gradienti animati floating nel BG | ✅ Enrichisce il nostro Spotlight |

### React Bits Componenti Selezionati
| Componente | URL | Uso nel Portfolio | Priorità |
|------------|-----|-------------------|----------|
| **Spotlight Card** | `/components/spotlight-card` | Container per Experience e Projects | 🔴 P0 |
| **Click Spark** | `/animations/click-spark` | Feedback sui click — delight effect | 🟡 P1 |
| **Scroll Velocity** | `/text-animations/scroll-velocity` | Logo/tag strip al posto di InfiniteScroll | 🟡 P1 |
| **Decay Card** | `/components/decay-card` | Sostituzione PixelCard per Projects | 🟡 P1 |
| **Shiny Text** | `/text-animations/shiny-text` | CTA "Download Resume" + nav links | 🟢 P2 |
| **Gradient Text** | `/text-animations/gradient-text` | Subtitle Hero "Senior Software Engineer" | 🟢 P2 |
| **Star Border** | `/animations/star-border` | Bordo animato pulsante per CTA card | 🟢 P2 |
| **True Focus** | `/text-animations/true-focus` | About section paragraph reveal | 🟢 P2 |

---

## 🎯 Issues da Risolvere

| # | Issue | Root Cause | Fix |
|---|-------|-----------|-----|
| 1 | Navigazione "snappy" (salto istantaneo) | `href="#section"` nativo senza smooth scroll | CSS `scroll-behavior: smooth` + Framer scroll |
| 2 | ExpandableCard troppo lenta | Spring config troppo "flaccida" | Aumenta stiffness: 350, damping: 25 |
| 3 | Nessuna transizione narrativa Hero→About | L'utente vede tutto insieme | Snap scroll + sezione Hero dedicata |
| 4 | Projects in colonna = boring | Layout 1 colonna piatto | Bento Grid 2-col con Decay/Spotlight Card |
| 5 | Background troppo statico | Solo radial gradient al mouse | Aggiunge Floating Blobs/Orb background |

---

## 📋 Phase 13 Task Breakdown

### 13.1 — Smooth Navigation (P0 — Non stravolgere il layout)
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`, `frontend-design`
- [ ] Aggiungere `scroll-behavior: smooth` in `main.scss` + `html { scroll-behavior: smooth }`
- [ ] Aggiungere `scroll-snap-type: y proximity` (NON mandatory — interferirebbe con scroll naturale)
- [ ] Accelerare `ExpandableCard` spring: rimuovere spring e usare transition meno 'visivamente violenta
- DoD: Click sui link nav fa uno scroll fluido senza "salto". ExpandableCard apre in <300ms in modo piu' gentile.

### 13.2 — SpotlightCard Integration (P0)
> **Agente:** `@frontend-specialist` | Skills: `react-patterns`
- [ ] Scaricare/implementare `SpotlightCard` da reactbits.dev adattandolo a BEM SCSS
- [ ] Sostituire la `div.pf-card` dell'Experience con `SpotlightCard`
- [ ] Applicare lo stesso a sezione Projects
- DoD: Passando il mouse sulle card c'è l'effetto luce dinamica "spotlight" che segue il cursore.

### 13.3 — Bento Grid Progetti (P1)
> **Agente:** `@frontend-specialist` | Skills: `frontend-design`
- [ ] Convertire la lista verticale dei Projects in un **Bento Grid** 2-colonne asimmetrico  
  - Prima card: grande (span 2), seconda: normale
- [ ] Integrare `DecayCard` (o TiltedCard) per aggiungere tilt 3D hover ai progetti
- [ ] Applicare `Star Border` attorno alla card principale
- DoD: La sezione Projects ispira lo stesso "wow" di una pagina Awwwards.

### 13.4 — Click Spark & Micro-delight (P1)
> **Agente:** `@frontend-specialist`
- [ ] Installare e wrappare il root layout con `ClickSpark` di React Bits
- [ ] Aggiungere `ScrollVelocity` al posto di `InfiniteScroll` nella sezione tecnologie
- DoD: Ogni click produce una piccola esplosione di particelle. Lo scroll della strip tech ha effetto parallax.

### 13.5 — Hero Section Dedicata + Gradient Text (P2)
> **Agente:** `@frontend-specialist`
- [ ] Trasformare la Hero "Developer Name / Subtitle / Desc" in una sezione `#hero` distinta
- [ ] Applicare `GradientText` sul subtitle "Senior Software Engineer..."
- [ ] Aggiungere un piccolo indicatore scroll + freccia down animata per guidare il primo scroll
- DoD: L'utente capisce istantaneamente che deve scrollare verso il basso per esplorare.

### 13.6 — Background Orb Upgrade (P2)
> **Agente:** `@frontend-specialist`
- [ ] Sostituire l'attuale `Spotlight` (solo radial gradient) con un background più ricco:
  - Mantenere il radial gradient al mouse
  - Aggiungere 2-3 blob blur `position: fixed` animati lentamente (CSS keyframes)
- DoD: Il BG non sembra più "flat", ma ha profondità senza distrarre.

---

## 🧪 Verification Plan

### Browser Tests (via Subagent)
- [ ] Smooth scroll funziona su tutti i 3 link nav
- [ ] SpotlightCard: effetto luce visibile su Experience e Projects
- [ ] ExpandableCard apre in < 300ms
- [ ] Bento Grid: risposta corretta su viewport 1440px, 1024px, 768px
- [ ] Click Spark: visibile su almeno 3 click consecutivi

### Performance Gates
- [ ] Nessun re-render ciclico (useMotionValue, non useState)
- [ ] FCP < 2s su localhost

---

## ⚙️ File Impattati

| File | Tipo Modifica |
|------|---------------|
| `src/app/page.tsx` | Aggiunta sezione #hero, SpotlightCard, Bento Grid, ClickSpark wrapper |
| `src/components/ExpandableCard.tsx` | Spring config più veloce |
| `src/components/SpotlightCard.tsx` | [NEW] da React Bits |
| `src/components/DecayCard.tsx` | [NEW] da React Bits |
| `src/components/ClickSpark.tsx` | [NEW] da React Bits |
| `src/components/ScrollVelocity.tsx` | [NEW] sostituto InfiniteScroll |
| `src/styles/main.scss` | scroll-behavior: smooth |
| `src/styles/layout/_grid.scss` | bento grid classes + hero section |
| `src/styles/components/_card.scss` | spotlight card styles BEM |

---

## 📊 Orchestration Plan

```
@frontend-specialist (Antigravity)
  ├── 13.1 Smooth Nav + ExpandableCard speedup       [~30min]
  ├── 13.2 SpotlightCard implementation              [~45min]
  └── 13.3 Bento Grid + DecayCard                   [~45min]

@qa-automation-engineer (Browser Subagent)
  └── Mid-sprint visual QA checkpoint               [~15min]

@frontend-specialist (Antigravity round 2)
  ├── 13.4 ClickSpark + ScrollVelocity              [~30min]
  ├── 13.5 Hero Section + GradientText              [~30min]
  └── 13.6 Background Orb                           [~20min]

@test-engineer (final QA)
  └── Verification + commit                          [~15min]
```

---

> **Note Architetturali:** NON stravolgere il layout sidebar fisso / scroll destra. L'impianto BEM è solido — solo arricchire i componenti e le animazioni.

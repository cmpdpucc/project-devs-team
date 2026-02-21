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

## 🛡️ Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | - | - | Nessun processo attivo | - |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-02-21 20:10 | Generazione Piano OpenCode | Avvio autonomo della traccia descritta in PLAN-opencode-integration.md |

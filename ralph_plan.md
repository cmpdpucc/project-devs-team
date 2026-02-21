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

## Phase 2 — Antigravity Integration (Il Ponte)
> **🎯 Supervisore:** `@backend-specialist` | Skills: `api-patterns`

### 2.1 File delle Regole Unificate
> **Agente:** `@documentation-writer` | Skills: `documentation-templates`

- [ ] Aggiornare/Creare `.agent/rules/GEMINI.md` e `.agent/skills/opencode-integration/SKILL.md`.
  - DoD: File creati con le regole per Antigravity/OpenCode.

### 2.2 Bridge Script
> **Agente:** `@backend-specialist` | Skills: `python-patterns`

- [ ] Aggiornare `scripts/antigravity-opencode-bridge.py` per sincronizzare la memoria.
  - DoD: Lo script espone `sync_gemini_rules()` e `start_opencode_server()`.

---

## Phase 3 — Agent Structure & Validation
> **🎯 Supervisore:** `@devops-engineer` | Skills: `scripting`

### 3.1 Validatore Struttura
> **Agente:** `@devops-engineer` | Skills: `bash-linux`, `powershell-windows`

- [ ] Creare `scripts/validate-agent-folder.sh` per verificare la presenza di agenti e skill.
  - DoD: Script eseguibile, controlla `rules/`, `skills/` e stampa totali.

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

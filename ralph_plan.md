# 🚀 RALPH PLAN — Self-Enhancement v5: Context Guardian

> **Questo file è il SINGOLO punto di verità per TUTTE le operazioni in corso.**
> Prima di ogni risposta, Antigravity DEVE leggere questo file.

---

## LEGACY

<details>
<summary>✅ Fasi completate precedenti</summary>

- **Self-Governance Framework v1** — `ralph_plan.md`, kill-switch, `self-governance.md`
- **Self-Enhancement v2: Memory** — `.agent/memory/` con 6 file, `memory-loader.md`
- **Self-Enhancement v2: Auto-Recovery** — `error-recovery.md`, `ERROR_PATTERNS.md`
- **Self-Enhancement v3: Pre-Flight Gate** — `pre_flight.py`, `pre-flight.md`, `/preflight`
- **Self-Enhancement v4: Smart Commit Protocol** — `smart_commit.py`, `commit-protocol.md`, `/commit`, 20 commit atomici su GitHub

</details>

---

## Phase 5 — 🔐 Context Guardian
> **🎯 Supervisore:** `@orchestrator`
> **🎯 Agente Esecutore:** `@documentation-writer` + `@backend-specialist`

### Problema
In sessioni lunghe (> ~20 tool calls) o troncate, il contesto si perde:
- Lezioni apprese non vengono scritte (problema di oggi)
- Decisioni prese mid-session non vengono registrate
- Se la sessione si tronca, il lavoro successivo riparte da zero

### Soluzione
Un sistema di checkpoint automatici che scrive stato intra-sessione e permette recovery.

---

### 5.1 `session_checkpoint.py` — Script Checkpoint
- [x] Funzione `write_checkpoint()`: scrive snapshot in `SESSION_LOG.md`
  - **Agente:** `@backend-specialist` | Skills: `python-patterns`, `clean-code`
  - Fields: `timestamp`, `last_task_done`, `files_modified[]`, `decisions[]`, `open_questions[]`, `next_step`
  - DoD: script eseguibile standalone, aggiorna SEC senza sovrascrivere storico
- [x] Funzione `read_last_checkpoint()`: legge ultimo checkpoint per recovery
  - DoD: output strutturato (JSON + pretty print), usabile da regola memory-loader
- [x] Funzione `diff_since_checkpoint()`: mostra cosa è cambiato dall'ultimo checkpoint
  - DoD: usa `git diff --stat` + lista file modificati recentemente
- [x] CLI: `python .agent/scripts/session_checkpoint.py --write "desc"` / `--read` / `--diff`
  - DoD: exit 0 su successo, exit 1 su errore con messaggio leggibile

### 5.2 Aggiornamento `self-governance.md` — Checkpoint nel Ciclo
- [x] Aggiungere regola: ogni ~10 tool calls → `session_checkpoint.py --write`
  - **Agente:** `@documentation-writer` | Skills: `plan-writing`
  - DoD: regola chiara con trigger, skip conditions, formato checkpoint
- [x] Allineare `memory-loader.md` Step 4: leggi checkpoint se esiste e < 24h
  - DoD: Step 4 aggiornato con comando esplicito e logica "offri recovery"

### 5.3 `SESSION_LOG.md` — Formato Checkpoint
- [x] Definire formato: YAML frontmatter + sezioni markdown
  - **Agente:** `@documentation-writer` | Skills: `documentation-templates`
  - DoD: file leggibile da `view_file`, parseable da script, max 100 righe per checkpoint
- [x] Aggiungere `SESSION_LOG.md` al sistema memory (già esiste vuoto → va strutturato)

### 5.4 `/checkpoint` Workflow — Slash Command
- [x] Creare `.agent/workflows/checkpoint.md`
  - **Agente:** `@documentation-writer` | Skills: `plan-writing`
  - `// turbo` step: `python .agent/scripts/session_checkpoint.py --write "manual checkpoint"`
  - Include: `--read` per recovery, `--diff` per vedere cosa è cambiato
  - DoD: usabile come `/checkpoint` slash command

### 5.5 Memory + Commit
- [x] Aggiornare `DECISIONS.md` con ADR-007 (Context Guardian design)
- [x] Aggiornare `LESSONS_LEARNED.md` con lezione su checkpoint manuale vs automatico
- [x] Commit atomico: `feat(memory): add context guardian checkpoint system`

---

## 🛡️ Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | - | - | Nessun processo attivo | - |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-02-19 22:28 | Python script (non rule-only) | Script permette lettura/scrittura programmatica + CLI testabile |
| 2026-02-19 22:28 | Checkpoint ogni ~10 tool calls | Bilanciamento overhead vs granularità recovery |
| 2026-02-19 22:28 | SESSION_LOG.md già esiste | Si struttura file esistente invece di crearne uno nuovo |

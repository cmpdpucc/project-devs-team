# 🚀 RALPH PLAN — Self-Enhancement v6: Progress Dashboard

> **Questo file è il SINGOLO punto di verità per TUTTE le operazioni in corso.**
> Prima di ogni risposta, Antigravity DEVE leggere questo file.

---

## LEGACY

<details>
<summary>✅ Fasi completate precedenti</summary>

- **v1: Self-Governance** — `ralph_plan.md`, kill-switch, `self-governance.md`
- **v2: Memory** — `.agent/memory/` con 6 file, `memory-loader.md`, `error-recovery.md`
- **v3: Pre-Flight Gate** — `pre_flight.py`, `pre-flight.md`, `/preflight`
- **v4: Smart Commit Protocol** — `smart_commit.py`, `commit-protocol.md`, `/commit`, 20+ commit atomici
- **v5: Context Guardian** — `session_checkpoint.py`, `SESSION_LOG.md`, `/checkpoint`

</details>

---

## Phase 6 — 📊 Progress Dashboard
> **🎯 Supervisore:** `@orchestrator` | Skills: `parallel-agents`, `behavioral-modes`

### Agenti Assegnati (Orchestrazione Parallela — Min 3)

| Agente | Dominio | Tasks |
|--------|---------|-------|
| `@backend-specialist` | Python/Logic | `progress_reporter.py` — parsing + metriche |
| `@documentation-writer` | Output/Format | `/status` workflow upgrade + report format |
| `@test-engineer` | QA | Test del parser + verifica exit codes |

**OpenCode delegate:** analisi `ralph_plan.md` per pattern comuni → generazione test fixtures

---

### 6.1 `progress_reporter.py` — Core Parser
> **Agente:** `@backend-specialist` | Skills: `python-patterns`, `clean-code`

- [x] Parse `ralph_plan.md` → conteggio `[x]` / `[/]` / `[ ]` / `[-]` per fase
  - DoD: output dizionario `{phase: {done, in_progress, todo, cancelled}}`
- [x] Calcolo % completamento per fase e totale
  - DoD: float 0.0–100.0, arrotondato a 1 decimale
- [x] Rilevamento task bloccati `[!]` e in progress `[/]`
  - DoD: lista `{task, line_number, context}` per ciascuno
- [x] Progress bar ASCII + colored terminal output
  - DoD: `████░░░░ 60% (3/5 tasks)` con colori ANSI
- [x] CLI: `python .agent/scripts/progress_reporter.py` + `--json` + `--phase <n>`
  - DoD: exit 0 su successo, JSON machine-readable con `--json`

### 6.2 Upgrade `/status` Workflow
> **Agente:** `@documentation-writer` | Skills: `documentation-templates`, `plan-writing`

- [x] Aggiornare `.agent/workflows/status.md` con `/status` che chiama `progress_reporter.py`
  - DoD: `// turbo` step, mostra dashboard completo, link a `ralph_plan.md`
- [x] Aggiungere sezione "Commit Recenti" — `git log --oneline -5`
  - DoD: incluso nel report `/status`
- [x] Aggiungere sezione "Processi Attivi" — from ralph_plan tabella
  - DoD: estratto dalla sezione `🛡️ Processi Attivi`

### 6.3 Test Suite
> **Agente:** `@test-engineer` | Skills: `testing-patterns`, `tdd-workflow`
> **OpenCode delegate:** `opencode run "genera fixture ralph_plan.md con edge cases"`

- [x] Test parser con piano completo (all `[x]`) → deve dare 100%
  - DoD: exit 0, output `100.0%`
- [x] Test con piano vuoto / senza tasks → graceful fallback
  - DoD: exit 0, output `0.0%`
- [x] Test `--json` output machine-readable
  - DoD: `json.loads()` non genera eccezioni
- [x] Test progress bar rendering corretto
  - DoD: lunghezza barra = 20 caratteri, % corretto

### 6.4 Memory + Atomic Commits
> **Step 7.5 protocol:** commit per ogni `[x]`

- [x] `DECISIONS.md` → ADR-008 (progress dashboard design)
- [x] `PROJECT_CONTEXT.md` → aggiunge `progress_reporter.py` a script inventory
- [x] Commit: `feat(scripts): add progress_reporter.py with ASCII dashboard`
- [x] Commit: `feat(workflows): upgrade /status with progress dashboard`
- [x] Commit: `test: add progress reporter test suite`
- [x] Commit: `docs(memory): ADR-008 and PROJECT_CONTEXT update`

---

## 🛡️ Processi Attivi

| PID | Tipo | Porta | Stato | Lanciato Da |
|-----|------|-------|-------|-------------|
| - | - | - | Nessun processo attivo | - |

---

## 📝 Log Decisioni

| Timestamp | Decisione | Motivazione |
|-----------|-----------|-------------|
| 2026-02-19 22:40 | Orchestrazione parallela 3 agenti | User request: agenti + skills per velocità e parallelismo |
| 2026-02-19 22:40 | OpenCode per fixture generation | Lettura large context `ralph_plan.md` → test patterns |
| 2026-02-19 22:40 | ASCII progress bar (no external deps) | Zero dipendenze extra, funziona in qualsiasi terminale |
| 2026-02-19 22:40 | `/status` come entry point unico | Un solo comando per vedere tutto il progetto |

---
description: Display agent and project status. Progress tracking and status board.
---

# /status — Project Status Dashboard

> **Dual Use:**
> 1. **User Dashboard:** Vista sintetica per l'umano (`/status`)
> 2. **Orchestrator Tool:** Checkpoint strumentale per l'agente (Pre/Mid/Post run)

---

## 🤖 Uso Interno Orchestratore

### PRE-RUN Snapshot (Baseline)
Da eseguire PRIMA di lanciare agenti in parallelo (Phase 2):
```powershell
python .agent/scripts/progress_reporter.py --compact
# Salva questo output mentalmente per confrontare i progressi
```

### MID-RUN Check (Monitoraggio)
Da eseguire tra un batch e l'altro:
```powershell
python .agent/scripts/progress_reporter.py --phase <N>
```

### POST-RUN Gate (Verifica Finale)
Da usare nel COMPLETION GATE. Se `pct != 100.0`, la fase NON è finita.
```powershell
python .agent/scripts/progress_reporter.py --json
```

---

## 👤 User Dashboard

### Dashboard Completo

// turbo
```powershell
python .agent/scripts/progress_reporter.py
```

---

## Output JSON (machine-readable)

```powershell
python .agent/scripts/progress_reporter.py --json
```

---

## Filtra per Fase Specifica

```powershell
python .agent/scripts/progress_reporter.py --phase 6
```

---

## Compact Mode (solo progress bar, no task details)

```powershell
python .agent/scripts/progress_reporter.py --compact
```

---

## Esempio Output

```
┌──────────────────────────────────────────────────────────────┐
│                      📊  PROJECT STATUS                       │
├──────────────────────────────────────────────────────────────┤
  Phase 6                ████████░░░░░░░░░░░░░░░░   40.0%  (2/5)
  ↻ progress_reporter.py in sviluppo
  ──────────────────────────────────────────────────────────
  TOTAL                  ████████████████░░░░░░░░   75.0%  (15/20)
├──────────────────────────────────────────────────────────────┤
│  📝  RECENT COMMITS                                           │
  fc6a304  feat(memory): Context Guardian checkpoint system
  e08f483  chore(governance): mark Phase 5 complete
  96be9e9  docs(agents): add IDE/OpenCode documentation
├──────────────────────────────────────────────────────────────┤
│  🛡️  ACTIVE PROCESSES                                         │
  Nessun processo attivo
└──────────────────────────────────────────────────────────────┘
```

---

## Integrazioni

| Script | Funzione |
|--------|---------|
| `progress_reporter.py` | Parse ralph_plan.md → % per fase |
| `session_checkpoint.py` | Ultimo checkpoint timestamp |
| `git log --oneline -5` | Commit recenti |

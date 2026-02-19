---
trigger: task_complete
priority: high
---

# COMMIT PROTOCOL — Atomic Commits After Every [x]

> **Regola attiva ogni volta che segni un task come `[x]` in `ralph_plan.md`.**

---

## 🔴 REGOLA: UN TASK = UN COMMIT

Quando completi un task (segni `[x]`), **prima di passare al successivo**:

```bash
python .agent/scripts/smart_commit.py "descrizione" --type <type> --scope <scope> --all --push
```

---

## 📋 Conventional Commits Cheatsheet

| Type | Quando usarlo | Esempio |
|------|--------------|---------|
| `feat` | Nuova feature, nuovo file di funzionalità | `feat(memory): add SESSION_LOG checkpoint` |
| `fix` | Bug fix, correzione errore | `fix(pre-flight): handle missing npm correctly` |
| `docs` | Solo regole .md, README, walkthrough | `docs(rules): add commit-protocol rule` |
| `refactor` | Ristrutturazione senza cambiare behavior | `refactor(scripts): extract GitContext class` |
| `test` | Aggiunta/modifica test | `test(pre-flight): add green and fail path tests` |
| `chore` | Config, .gitignore, tooling, setup | `chore: update .gitignore with __pycache__` |
| `perf` | Ottimizzazione performance | `perf(runner): parallelize gate execution` |

**Scope consigliati:**
- `memory` — `.agent/memory/`
- `rules` — `.agent/rules/`
- `scripts` — `.agent/scripts/`
- `workflows` — `.agent/workflows/`
- `pre-flight` — tutto legato a pre_flight.py
- `governance` — self-governance, ralph-loop, task-tracking

---

## 🔄 Ciclo Post-Task (Integrazione con self-governance.md)

```
STEP 6:   Esegui il lavoro (scrivi il codice)
STEP 7:   Aggiorna ralph_plan.md → segna [x]
STEP 7.5: Commit atomico per questo task  ← NUOVO
STEP 8:   Procedi al prossimo task
```

**Esempio completo:**
```bash
# Task completato: "Add error-recovery.md rule"
python .agent/scripts/smart_commit.py \
  "add error recovery rule with 15 patterns" \
  --type docs --scope rules --all --push
```

---

## ✅ Skip Conditions

Il commit può essere differito (non skippato, solo raggruppato) se:
1. I task sono molto piccoli (< 5 righe cambiate) → raggruppa in unico commit
2. Non c'è ancora un remote → fare i commit locali e pushare alla fine
3. Il pre-flight (Step 0.5) ha dato exit 1 → prima fix, poi commit

---

## ⛔ Anti-Pattern da Evitare

1. ❌ **Mega-commit** con tutti i file — rende la storia illeggibile
2. ❌ **Commit message vago** — "update files", "misc changes"
3. ❌ **Saltare il commit** dopo un `[x]` senza push
4. ❌ **Hardcodare user/email** nel commit — usa sempre `git config`
5. ❌ **Force push su main** — mai senza consenso esplicito

---

## 🤖 Auto-Mode: `--from-plan`

Per commit automatici basati sull'ultimo task completato:
```bash
python .agent/scripts/smart_commit.py --from-plan --all --push
```
Legge l'ultimo `[x]` da `ralph_plan.md` e genera il messaggio corretto.

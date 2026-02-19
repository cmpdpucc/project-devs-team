---
description: Save session context checkpoint. Use to preserve state mid-session or recover from interruption.
---

# /checkpoint — Context Guardian

Salva un checkpoint del contesto corrente in `SESSION_LOG.md`. Permette recovery se la sessione viene troncata.

---

## Uso rapido — Salva checkpoint

// turbo
```powershell
python .agent/scripts/session_checkpoint.py --write "descrizione stato corrente"
```

---

## Leggi ultimo checkpoint (recovery)

```powershell
# Human-readable
python .agent/scripts/session_checkpoint.py --read

# Machine-readable JSON
python .agent/scripts/session_checkpoint.py --read --json
```

---

## Mostra diff da ultimo checkpoint

```powershell
python .agent/scripts/session_checkpoint.py --diff
```

---

## Checkpoint con decisioni e domande aperte

```powershell
python .agent/scripts/session_checkpoint.py `
  --write "completato pre-flight gate, avviato smart commit" `
  --decision "usare script Python invece di bash per portabilità" `
  --decision "commit atomico per ogni [x] in ralph_plan" `
  --question "come gestire progetti senza git init?"
```

---

## Recovery flow (sessione troncata)

```powershell
# Step 1: Leggi ultimo checkpoint
python .agent/scripts/session_checkpoint.py --read

# Step 2: Controlla cosa è cambiato
python .agent/scripts/session_checkpoint.py --diff

# Step 3: Leggi ralph_plan.md per task in sospeso
# (poi riprendere da dove si era rimasti)
```

---

## Quando usare

| Situazione | Comando |
|-----------|---------|
| Ogni ~10 tool calls | `--write "stato corrente"` |
| Prima di `notify_user` | `--write "sessione completa"` |
| Inizio nuova sessione | `--read` per vedere se c'è recovery |
| Dubbio su cosa è cambiato | `--diff` |

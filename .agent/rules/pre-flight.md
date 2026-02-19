---
trigger: always_on
---

# PRE-FLIGHT VALIDATION GATE — Step 0.5

> **Questa regola è ATTIVA prima di qualsiasi operazione di scrittura su codice.**
> Posizione nel ciclo: **DOPO Step 0** (leggi piano) e **PRIMA di Step 6** (esegui).

---

## 🚦 REGOLA SUPREMA: VERIFICA L'AMBIENTE PRIMA DI SCRIVERE

**Prima di chiamare `write_to_file`, `replace_file_content`, `multi_replace_file_content`:**

```
python .agent/scripts/pre_flight.py
```

- **Exit 0 → VERDE** — Procedi normalmente.
- **Exit 1 → ROSSO** — **STOP.** Non scrivere nulla. Leggi il report. Applica recovery.

---

## 📋 Gates in Sequenza

| Gate | Cosa Controlla | Tempo stimato |
|------|----------------|---------------|
| **A — Git** | Working tree pulita (no modified tracked files) | < 2s |
| **B — Build** | Build/compile viene completato senza errori | < 60s |
| **C — Tests** | Unit tests passano (no E2E, timeout 60s) | < 90s |
| **D — Deps** | Dipendenze installate corrispondono al lockfile | < 10s |

---

## ✅ Skip Conditions (Quando NON eseguire il gate)

Il gate può essere bypassato **solo** in questi casi:

1. **Progetto Generic** (no package.json, no requirements.txt) — Gates B/C/D sono auto-SKIP
2. **Prima sessione su progetto nuovo** — non ha ancora build script. Fai solo Gate A.
3. **L'utente ha esplicitamente approvato il bypass** — documenta il motivo nel Log Decisioni
4. **Modifica è solo ai file `.md`** — Gate B/C/D sono irrilevanti. Fai solo Gate A.

Per gate singolo:
```bash
python .agent/scripts/pre_flight.py --gate git    # Solo Gate A
python .agent/scripts/pre_flight.py --gate build  # Solo Gate B
```

---

## 🔴 Recovery Actions se Exit 1

### Gate A (git) FAIL → Tracked files modified
```bash
# Opzione 1: Salva lavoro corrente
git stash

# Opzione 2: Commit come WIP
git commit -am "wip: [descrizione]"

# Opzione 3: Review cosa è cambiato
git diff
```

### Gate B (build) FAIL → Build rotto
```bash
# Delega analisi a OpenCode (context ampio per leggere errori)
opencode run "Fix build error in [progetto]. Error: [stderr dal last_preflight.json]"
```
Leggi `.agent/memory/last_preflight.json` per l'errore completo.

### Gate C (tests) FAIL → Test che rompono
```bash
# Attiva @debugger agent
# Leggi il detail nel report per capire quale test fallisce
python .agent/scripts/pre_flight.py --gate tests
```

### Gate D (deps) FAIL → Dipendenze mancanti o conflitti
```bash
# Node
npm install

# Python
pip install -r requirements.txt

# Verifica dopo
python .agent/scripts/pre_flight.py --gate deps
```

---

## 🧠 Output del Gate (Machine-Readable)

Il gate scrive sempre `.agent/memory/last_preflight.json`:
```json
{
  "passed": false,
  "project_type": "node",
  "timestamp": "...",
  "total_duration_s": 12.4,
  "failed_gates": ["build"],
  "recovery_actions": {
    "build": "opencode"
  },
  "gates": [...]
}
```

Usa questo file per capire cosa è fallito senza rilanciare il gate.

---

## 🔄 Integrazione nel Ciclo di Risposta

Il ciclo aggiornato di `self-governance.md`:

```
STEP 0:   Leggi ralph_plan.md
STEP 0.5: [QUESTO STEP] Esegui pre_flight.py → se exit 1, STOP
STEP 1-5: Analisi richiesta utente, aggiornamento piano
STEP 6:   Esegui il lavoro (scrittura codice)
STEP 7:   Aggiorna ralph_plan.md
STEP 8:   Registra processi attivi
```
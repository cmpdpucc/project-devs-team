---
description: Run pre-flight environment check before writing code. Fast gate: git + build + tests + deps.
---

# /preflight — Pre-Flight Validation Gate

Esegue il gate di validazione dell'ambiente prima di qualsiasi modifica al codice.

---

## Step 1: Esegui tutti i gate

// turbo
```powershell
python .agent/scripts/pre_flight.py
```

Oppure gate singolo:
```powershell
python .agent/scripts/pre_flight.py --gate git
python .agent/scripts/pre_flight.py --gate build
python .agent/scripts/pre_flight.py --gate tests
python .agent/scripts/pre_flight.py --gate deps
```

---

## Step 2: Leggi il risultato

Il report è disponibile in `.agent/memory/last_preflight.json`.

```powershell
Get-Content .agent/memory/last_preflight.json
```

---

## Step 3: Recovery Actions (se exit 1)

### 🔴 Gate A — Git Dirty
```powershell
# Stash il lavoro in corso
git stash

# oppure commit come WIP
git commit -am "wip: salvataggio pre-flight"

# Poi rilanciare:
python .agent/scripts/pre_flight.py --gate git
```

### 🔴 Gate B — Build Failure
```powershell
# Leggi l'errore specifico
$json = Get-Content .agent/memory/last_preflight.json | ConvertFrom-Json
$buildGate = $json.gates | Where-Object { $_.gate -eq "build" }
Write-Host $buildGate.detail
```

Poi delega a OpenCode per diagnosi in contesto ampio:
```powershell
opencode run "Fix build error in this project. Error output: $($buildGate.detail)"
```

### 🔴 Gate C — Tests Failing
```powershell
# Visualizza quali test falliscono
python .agent/scripts/pre_flight.py --gate tests

# Attiva @debugger agent con systematic-debugging skill
```

### 🔴 Gate D — Missing Dependencies
```powershell
# Node
npm install

# Python
pip install -r requirements.txt

# Verifica
python .agent/scripts/pre_flight.py --gate deps
```

---

## Step 4: Conferma ambiente pulito

Quando tutti i gate sono verdi (exit 0), procedi con il task originale.

```
🟢 ENVIRONMENT IS CLEAN — OK to proceed.
```

---

## Note

- **Tempo stimato:** < 30s per progetti Generic/Markdown, < 90s per Node/Python con test
- **Output JSON:** sempre in `.agent/memory/last_preflight.json`
- **Integrabile come git pre-commit hook:** `python .agent/scripts/pre_flight.py --gate git`

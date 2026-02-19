---
trigger: always_on
priority: highest
---

# SELF-GOVERNANCE - Protocollo Obbligatorio

> **Questa regola è ATTIVA per OGNI singola risposta di Antigravity.**

## 🔴 REGOLA SUPREMA: LEGGI IL PIANO

**Prima di rispondere ALL'UTENTE, DEVI:**

1. **LEGGI** `ralph_plan.md` nella root del progetto
2. **VERIFICA** lo stato dei task attivi
3. **AGGIORNA** il piano se la richiesta dell'utente lo modifica

> ⚠️ **VIOLAZIONE:** Rispondere senza aver letto `ralph_plan.md` = FALLIMENTO.

---

## 📋 Ciclo Per Ogni Risposta

```
STEP 0:   Leggi ralph_plan.md
STEP 0.5: Pre-Flight Gate → python .agent/scripts/pre_flight.py → se exit 1, STOP
STEP 1:   Identifica task attivi [/] e bloccati [!]
STEP 2:   Analizza la richiesta dell'utente
STEP 3:   Se la richiesta è un NUOVO task → Aggiungilo al piano
STEP 4:   Se la richiesta MODIFICA un task → Aggiorna il piano
STEP 5:   (riserva)
STEP 6:   Esegui il lavoro
STEP 7:   Aggiorna ralph_plan.md con i risultati
STEP 7.5: Commit atomico → python .agent/scripts/smart_commit.py --from-plan --all --push
STEP 8:   Se hai lanciato processi → Registrali nella tabella "Processi Attivi"
```

---

## 🔄 Piano Lifecycle — Rotazione Automatica

### Quando il piano corrente è COMPLETATO (tutti `[x]`):

1. **ARCHIVIA** il piano completato:
   - Copia `ralph_plan.md` → `docs/ralph_plan_history/ralph_plan_YYYY-MM-DD_HHMMSS.md`
   - Questo è lo storico verificabile di ciò che è stato fatto
2. **ATTENDI** la prossima richiesta dell'utente

### Quando arriva un NUOVO messaggio dell'utente:

1. **LEGGI** `ralph_plan.md`
2. **SE ci sono task `[ ]` o `[/]` pendenti** → Completa quelli prima
3. **SE tutti i task sono `[x]`** (o il piano non esiste) → **GENERA un nuovo `ralph_plan.md`**:
   - Usa il formato di `example.ralph_plan.md` come template
   - Consulta `ARCHITECTURE.md` per la matrice Agente → Skills
   - Assegna **Agente Supervisore** per ogni Fase
   - Assegna **Agente Esecutore + Skills** per ogni subtask
   - Definisci **DoD** (Definition of Done) per ogni task
   - Includi la sezione LEGACY con le fasi precedenti in `<details>`

---

## 🧠 Assegnazione Agenti (Consulta ARCHITECTURE.md)

Per ogni task nel piano, DEVI specificare:

```markdown
- [ ] Descrizione del task
  - **Agente:** `@nome-agente` | Skills: `skill-1`, `skill-2`
  - DoD: Criteri oggettivi di completamento
```

### Matrice di Riferimento Rapida (da ARCHITECTURE.md):

| Dominio | Agente | Skills |
|---------|--------|--------|
| Planning | `@project-planner` | `brainstorming`, `plan-writing`, `architecture` |
| Frontend | `@frontend-specialist` | `react-patterns`, `frontend-design`, `ui-ux-pro-max` |
| Backend | `@backend-specialist` | `api-patterns`, `nodejs-best-practices`, `database-design` |
| Database | `@database-architect` | `database-design` |
| Testing | `@test-engineer` | `testing-patterns`, `tdd-workflow`, `webapp-testing` |
| Security | `@security-auditor` | `vulnerability-scanner`, `red-team-tactics` |
| DevOps | `@devops-engineer` | `deployment-procedures`, `server-management` |
| Performance | `@performance-optimizer` | `performance-profiling` |
| SEO | `@seo-specialist` | `seo-fundamentals`, `geo-fundamentals` |
| Debug | `@debugger` | `systematic-debugging` |
| Docs | `@documentation-writer` | `documentation-templates` |
| Mobile | `@mobile-developer` | `mobile-design` |
| E2E | `@qa-automation-engineer` | `webapp-testing`, `testing-patterns` |
| Orchestration | `@orchestrator` | `parallel-agents`, `behavioral-modes` |

---

## 🛡️ Kill Switch Verification Protocol

**Quando termini un processo, DEVI:**

1. **Cattura il PID** prima della terminazione
2. **Esegui il kill** (`process.terminate()` o `process.kill()`)
3. **VERIFICA** che il processo sia effettivamente morto:
   - Windows: `tasklist /FI "PID eq {PID}"`
   - Linux/Mac: `ps -p {PID}`
4. **Solo se il PID NON appare più**, segna come terminato in `ralph_plan.md`

> 🔴 **MAI dichiarare "processo terminato" senza Step 3!**

---

## 🔄 Refactor del Piano

Quando l'utente fa una nuova richiesta:

1. Leggi `ralph_plan.md`
2. Valuta se la richiesta è:
   - **NUOVO task** → Aggiungi alla sezione corretta
   - **MODIFICA a task esistente** → Aggiorna la riga
   - **CANCELLAZIONE** → Segna con `[-]` e motivazione
3. Aggiorna il timestamp "Ultimo Aggiornamento"
4. Se la richiesta tocca >3 file → Usa `/orchestrate`
5. Se la richiesta è un refactor → Usa `/refactor`

---

## 🧠 Consapevolezza dell'Orchestrazione

**Sei l'Orchestrator.** Prima di ogni task complesso:

1. Leggi `.agent/workflows/orchestrate.md`
2. Identifica gli agenti necessari (minimo 3 per orchestrazione)
3. Segui il protocollo 2-fasi (Planning → Implementation)
4. **MAI** lanciare agenti senza supervisione attiva

---

## 📝 Memory Checkpoint Protocol

### Intra-Sessione (ogni ~10 tool calls):
```bash
python .agent/scripts/session_checkpoint.py --write "descrizione stato corrente"
```
Cattura automaticamente: branch, last [x] task, file modificati dall'ultimo commit.

### Post-Sessione (prima di notify_user finale):
```bash
python .agent/scripts/session_checkpoint.py --write "sessione completata"
```
Poi aggiorna manualmente:
- `LESSONS_LEARNED.md` con nuovi errori/fix
- `DECISIONS.md` con nuove decisioni architetturali
- `PROJECT_CONTEXT.md` se la struttura del progetto è cambiata
- `USER_PREFERENCES.md` se hai osservato nuovi pattern

> 🔴 **MAI chiudere una sessione senza aggiornare la memoria.**
> 🔴 **"Registrato" significa SCRITTO nel file, non solo detto.**

---
trigger: session_start
priority: highest
---

# MEMORY LOADER — Caricamento Conoscenza All'Avvio

> **Questa regola si attiva ALL'INIZIO di ogni nuova conversazione/sessione.**

## 🔴 REGOLA: LEGGI LA MEMORIA PRIMA DI AGIRE

All'avvio di OGNI nuova sessione (= primo messaggio dell'utente in una nuova conversazione), Antigravity DEVE:

### Step 1: Carica Contesto Progetto
```
Leggi .agent/memory/PROJECT_CONTEXT.md
→ Ora sai cos'è il progetto, tech stack, file critici
```

### Step 2: Carica Lezioni Apprese
```
Leggi .agent/memory/LESSONS_LEARNED.md
→ Ora sai quali errori NON ripetere
```

### Step 3: Carica Preferenze Utente
```
Leggi .agent/memory/USER_PREFERENCES.md
→ Ora sai come l'utente vuole lavorare
```

### Step 4: Recupera Sessione Interrotta (se esiste)
```
Se .agent/memory/SESSION_LOG.md esiste E last_checkpoint è recente (< 24h):
→ Leggi per recuperare contesto della sessione precedente
→ Offri all'utente: "Ho trovato una sessione interrotta. Vuoi continuare?"
```

### Step 5: Consulta Decisioni
```
Leggi .agent/memory/DECISIONS.md
→ Ora sai PERCHÉ le scelte architetturali sono state fatte
```

---

## 📝 Checkpoint Periodico (Intra-Sessione)

**Ogni ~10 tool calls**, aggiorna `.agent/memory/SESSION_LOG.md` con:
- Decisioni prese dall'ultimo checkpoint
- File modificati
- Focus corrente
- Domande aperte

Questo garantisce che se la sessione si tronca, il contesto è recuperabile.

---

## 🔄 Aggiornamento Memoria Post-Sessione

Alla FINE del lavoro (prima di notify_user finale), aggiorna:
- `LESSONS_LEARNED.md` con nuovi errori/fix
- `DECISIONS.md` con nuove decisioni architetturali
- `PROJECT_CONTEXT.md` se la struttura del progetto è cambiata
- `USER_PREFERENCES.md` se hai osservato nuovi pattern

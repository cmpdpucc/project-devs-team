---
trigger: always_on
priority: high
---

# TASK TRACKING - Protocollo di Tracciamento

> **Ogni operazione DEVE lasciare una traccia verificabile.**

## 📋 Regole di Tracciamento

### 1. Processi Esterni
Ogni processo lanciato (OpenCode, server, agente):
- **REGISTRA** PID, porta, tipo in `ralph_plan.md` → Tabella "Processi Attivi"
- **MONITORA** stato con loop attivo (NO fire-and-forget)
- **VERIFICA** terminazione con controllo PID effettivo
- **RIMUOVI** dalla tabella solo dopo verifica positiva

### 2. File Modificati
Per ogni file toccato:
- **ANNOTA** in `ralph_plan.md` → Log Decisioni
- **MOTIVA** il cambiamento (perché, non solo cosa)

### 3. Errori e Fallimenti
Se un'operazione fallisce:
- **NON NASCONDERE** l'errore
- **CLASSIFICA** tipo di errore (vedi `.agent/rules/error-recovery.md`)
- **TENTA** auto-fix (max 3 tentativi)
- **REGISTRA** pattern in `.agent/memory/ERROR_PATTERNS.md`
- **REGISTRA** in `ralph_plan.md` → Lezioni Apprese
- **ANALIZZA** root cause prima di riprovare
- **ESCALA** all'utente solo dopo 3 tentativi falliti (o per errori pericolosi)

### 4. Piano Lifecycle
- **Piano completato?** → Archivia in `docs/ralph_plan_history/ralph_plan_YYYY-MM-DD_HHMMSS.md`
- **Nuovo messaggio utente?** → Leggi il piano PRIMA di rispondere
- **Piano inesistente?** → Genera nuovo piano con formato `example.ralph_plan.md`

---

## 🔴 Anti-Pattern Vietati

1. ❌ Dichiarare "fatto" senza verifica
2. ❌ Lanciare processi senza registrarli
3. ❌ Ignorare exit code != 0 senza classificare l'errore
4. ❌ Passare al task successivo con errori aperti
5. ❌ Dimenticare di aggiornare `ralph_plan.md`
6. ❌ Rispondere senza aver letto `ralph_plan.md`
7. ❌ Generare un piano senza consultare `ARCHITECTURE.md`
8. ❌ Assegnare agenti senza specificare le skills
9. ❌ Riprovare >3 volte senza escalation all'utente
10. ❌ Auto-recover da PermissionError o file `.env`

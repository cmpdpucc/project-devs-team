---
last_updated: 2026-02-16T04:42:00+09:00
patterns: 4
---

# Error Patterns Database

> **Database vivente.** Ogni errore risolto = nuovo pattern qui. Consultato durante auto-recovery.

## Pattern: NameError after multi-line replace_file_content
- **Trigger:** `NameError: name 'X' is not defined`
- **Signature:** Variabile usata ma mai definita, solo dopo un edit
- **Root Cause:** `replace_file_content` ha rimosso un blocco che conteneva la definizione della variabile. Il replacement era incompleto.
- **Fix Protocol:**
  1. `view_file` l'intero file dopo ogni replacement
  2. Verificare che tutte le variabili referenziate siano ancora definite
  3. Se mancano, ripristinare il blocco mancante
- **Prevention:** SEMPRE fare `view_file` full dopo `replace_file_content` su blocchi >10 righe
- **Occurrences:** 1 (`demo_orchestrator.py`, 2026-02-16)

## Pattern: Port already in use (EADDRINUSE)
- **Trigger:** `EADDRINUSE` / `address already in use` / `Only one usage of each socket address`
- **Signature:** Server non riesce a fare bind su una porta
- **Root Cause:** Processo precedente non terminato che occupa la porta
- **Fix Protocol:**
  1. Windows: `netstat -ano | findstr :<PORT>`
  2. Identificare il PID
  3. `taskkill /F /PID <PID>`
  4. Verificare: `tasklist /FI "PID eq <PID>"`
  5. Retry il comando originale
- **Prevention:** Kill-switch verification protocol su OGNI processo
- **Occurrences:** Comune in sviluppo locale

## Pattern: Subprocess flags — Windows-only constants
- **Trigger:** Linting error su `subprocess.CREATE_NEW_PROCESS_GROUP`, `subprocess.CREATE_NO_WINDOW`
- **Signature:** Type checker non riconosce costanti Windows-only di subprocess
- **Root Cause:** Pyre2/mypy non supporta platform-conditional type definitions
- **Fix Protocol:**
  1. Opzione A: `# type: ignore` annotation
  2. Opzione B: `if sys.platform == 'win32':` conditional import
  3. Opzione C: Definire la costante localmente: `CREATE_NEW_PROCESS_GROUP = 0x00000200`
- **Prevention:** Usare Opzione B per codice cross-platform
- **Occurrences:** Persistente in `process_manager.py`

## Pattern: Git push fails — remote rejected
- **Trigger:** `remote: error:` / `! [rejected]` / `non-fast-forward`
- **Signature:** Push rifiutato dal remote
- **Root Cause:** Remote ha commit che il locale non ha
- **Fix Protocol:**
  1. `git fetch origin`
  2. `git rebase origin/main` (o branch corrente)
  3. Risolvere conflitti se presenti
  4. `git push`
- **Prevention:** Sempre `git pull --rebase` prima di lavorare
- **Occurrences:** Comune in team

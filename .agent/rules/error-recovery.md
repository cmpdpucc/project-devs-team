---
trigger: command_exit_code_nonzero
priority: high
---

# ERROR RECOVERY — Automatic Diagnosis & Retry Protocol

> **Questa regola si attiva quando QUALSIASI comando termina con exit code != 0.**

## 🔴 REGOLA: NON IGNORARE MAI UN ERRORE

Quando un comando fallisce, **NON** procedere al task successivo. Segui questo protocollo:

---

## Step 1: CLASSIFY — Identifica il tipo di errore

Analizza `stderr` e `stdout`. Cerca pattern noti:

| Pattern in Output | Tipo Errore | Strategia Auto-Fix |
|-------------------|------------|-------------------|
| `ModuleNotFoundError` / `Cannot find module` | Missing dependency | `pip install X` o `npm install X` |
| `SyntaxError` / `Unexpected token` | Errore sintassi | Rileggi file, trova e correggi il syntax error |
| `EADDRINUSE` / `address already in use` | Porta occupata | `netstat -ano \| findstr :PORT` → kill processo → retry |
| `TypeError` / `AttributeError` | Type mismatch | Leggi file sorgente, correggi tipi/attributi |
| `ENOENT` / `FileNotFoundError` / `No such file` | File mancante | Verifica path, crea file se necessario |
| `PermissionError` / `EPERM` / `Access is denied` | Permessi | ⛔ **ESCALATE** — non toccare permessi automaticamente |
| `ETIMEOUT` / `TimeoutError` / `ECONNREFUSED` | Rete/timeout | Retry con backoff: 1s → 3s → 10s |
| `git` + `conflict` / `CONFLICT` | Git conflict | `git status`, analizza conflitto, risolvi |
| `git` + `not a git repository` | Git non init | Verifica directory corrente |
| `tsc` + `error TS` | TypeScript error | Leggi errore, correggi tipo/import/export |
| `ESLint` / `Parsing error` | Lint error | Leggi file, correggi lint violation |
| `npm ERR!` / `ERESOLVE` | NPM dependency | `npm install --legacy-peer-deps` o risolvi versioni |
| `ENOMEM` / `heap out of memory` | Memoria esaurita | ⛔ **ESCALATE** — serve intervento sistema |
| `BUILD FAILED` / `webpack` / `vite` | Build failure | Leggi errore specifico, correggi sorgente |
| `AssertionError` / `test failed` | Test failure | Leggi test output, correggi codice o test |

---

## Step 2: ATTEMPT FIX — Massimo 3 tentativi

```
Tentativo 1: Applica strategia primaria dalla tabella
  ↓ Ancora errore?
Tentativo 2: Prova strategia alternativa (es. path diverso, versione diversa)
  ↓ Ancora errore?
Tentativo 3: Analisi approfondita — leggi TUTTO il contesto, cerca in LESSONS_LEARNED.md + ERROR_PATTERNS.md
  ↓ Ancora errore?
STOP → ESCALATE all'utente
```

**Tra un tentativo e l'altro:**
- Verifica che il fix sia stato applicato (`view_file`)
- Ri-esegui il comando originale
- NON cambiare strategia senza capire perché la precedente ha fallito

---

## Step 3: LOG — Registra in memoria

Indipendentemente dall'esito:

1. **Se risolto:** Aggiungi pattern in `.agent/memory/ERROR_PATTERNS.md`
2. **Se non risolto:** Aggiungi in `.agent/memory/LESSONS_LEARNED.md` con stato "UNRESOLVED"
3. **Sempre:** Registra tentativo nel `ralph_plan.md` → Log Decisioni

---

## Step 4: ESCALATE — Quando chiedere all'utente

**ESCALATE immediatamente (zero retry) per:**
- `PermissionError` — potrebbe essere sicurezza
- Qualsiasi errore che tocca `.env` o file sensibili
- Comandi distruttivi (`rm -rf`, `drop table`, etc.)
- Pattern di errore **mai visto prima** e non classificabile
- Errori di memoria/sistema (`ENOMEM`, `SIGKILL`)

**ESCALATE dopo 3 retry per:**
- Qualsiasi altro errore che non riesci a risolvere

**Formato escalation:**
```
🔴 Errore non risolvibile automaticamente.
Tipo: [TIPO]
Comando: [COMANDO]
Output: [STDERR primi 500 char]
Tentativi: 3/3
Strategie provate: [LISTA]
→ Serve intervento manuale.
```

---

## ⛔ NEVER Auto-Recover From

1. **PermissionError** — potrebbe essere un security gate intenzionale
2. **Qualsiasi cosa con `.env`** — contiene segreti
3. **`rm -rf` o comandi distruttivi** — danni irreversibili
4. **Errori di autenticazione** — credenziali dell'utente
5. **Errori di memoria/sistema** — richiedono intervento OS
6. **Pattern sconosciuti** — se non classificabile, chiedi

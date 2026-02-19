---
name: opencode-integration
description: Integra comandi OpenCode nel workflow Antigravity per operazioni terminale avanzate.
---

# OpenCode Integration Skill

## Quando usare questa Skill
Se rilevi `opencode` installato nel path (`which opencode` o `where opencode`), usa questa skill per delegare task pesanti.

### 1. Operazioni Complesse (Asincrone)
Usa `opencode run` per analisi o refactoring che richiedono tempo, senza bloccare l'IDE.

```bash
# Esempio: Analisi architetturale
opencode run "Analizza pattern architetturali in src/ e genera report in docs/ARCH_REPORT.md"
```

### 2. Sessioni Persistenti
Mantenere il contesto attivo tra diverse sessioni di lavoro.

1.  **Avvia Server**: `opencode serve --port 4096`
2.  **Collega**: `opencode attach http://localhost:4096`

### 3. CI/CD & Automation
Integrazione in script di pipeline o hook git.

```yaml
# GitHub Action example
- name: AI Review
  run: opencode run "Analizza questo PR per vulnerabilità"
```

## Best Practices
- **Large Context**: OpenCode gestisce contesti più ampi di Antigravity chat. Usalo per "leggere tutto il progetto".
- **Refactoring**: Per rinominare variabili in 100 file, usa OpenCode.
- **Sincronizzazione**: Esegui `make sync` per assicurare che OpenCode abbia le ultime regole GEMINI.

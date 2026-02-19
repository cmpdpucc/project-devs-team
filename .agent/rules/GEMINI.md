---
version: 1.0
applies_to: [antigravity, opencode]
---

# GEMINI.md - Unified Agent Protocols

> **Identity**: Senior Full-Stack Developer specialized in modern architecture and best practices.

## 🛑 REGOLE UNIVERSALI

### File System
- **SEMPRE** rispetta `.gitignore`.
- **SEMPRE** crea backup prima di operazioni distruttive massiva.
- **USA** `rg` (ripgrep) per esplorazioni efficienti del codice.
- **NON toccare**: `node_modules/`, `.git/`, `dist/`, `.env`.

### Coding Standards
- Segui le convenzioni rilevate nel progetto (`.editorconfig`, `eslint`).
- **TypeScript**: Obbligatorio per nuovi file, strict typing.
- **Testing**: Ogni nuova feature DEVE avere test unitari.
- **Docs**: JSDoc obbligatorio per funzioni pubbliche ed esportate.

## 🤖 Workflow OpenCode (Terminal Agent)
- **Token Management**: Usa `/compact` ogni 10 messaggi.
- **Task Boundaries**: Dichiara sempre l'inizio di una operazione complessa.
- **Verifica**: Esegui sempre `npm test` o `npm run build` dopo modifiche sostanziali.
- **Bulk Ops**: Preferisci OpenCode per refactoring su >5 file.

## 🛸 Workflow Antigravity (IDE Agent)
- **Planning**: Genera SEMPRE un Implementation Plan per task che toccano >3 file.
- **Verification**: Usa il browser agent per verificare modifiche UI (visual regression).
- **Knowledge**: Registra lezioni apprese in `.agent/memory/LESSONS_LEARNED.md`.

## 🔒 Sicurezza & Compliance
1.  **Segreti**: NON leggere MAI file `.env` senza permesso esplicito.
2.  **Distruzione**: NON eseguire `rm -rf`, `dd`, `mkfs` senza conferma utente.
3.  **Privacy**: Redigi chiavi API da qualsiasi output di log o console.
4.  **Audit**: Ogni comando eseguito è loggato.

---

> **Nota**: Questo file è sincronizzato automaticamente da Antigravity verso OpenCode via `scripts/antigravity-opencode-bridge.py`.
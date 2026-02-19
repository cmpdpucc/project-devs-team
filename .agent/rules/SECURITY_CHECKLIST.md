# Security Checklist

## Pre-Commit
- [ ] Nessun segreto in codice o config
- [ ] .env non committato
- [ ] Dependencies audit pulito (`npm audit`)

## Agent Permissions
- [ ] Strict Mode abilitato per produzione
- [ ] Browser allowlist configurata
- [ ] Terminal commands whitelist attiva

## OpenCode Specific
- [ ] Non-workspace access disabilitato
- [ ] MCP servers validati
- [ ] Backup policy configurata (undo/redo)

## Antigravity Specific
- [ ] Telemetria configurata secondo policy
- [ ] Artefatti sensibili esclusi da sync
- [ ] Prompt injection filters attivi

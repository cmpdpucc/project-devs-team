# Workflow Integrato Antigravity + OpenCode

## Scenario 1: Feature Development
1. **Antigravity (Planning)**: Genera Implementation Plan
2. **OpenCode (Execution)**: Esegue modifiche multi-file con context massivo
3. **Antigravity (Verification)**: Browser agent verifica UI

## Scenario 2: Legacy Refactoring
1. **OpenCode (Analysis)**: Usa ripgrep per mappare dipendenze
2. **Antigravity (Orchestration)**: Coordina refactoring incrementale
3. **OpenCode (Testing)**: Esegue test suite ad ogni step

## Scenario 3: CI/CD Integration
1. **GitHub Actions**: Trigger su PR
2. **OpenCode CLI**: `opencode run "Review security"`
3. **Antigravity**: Genera walkthrough con evidenze visive

## Best Practices
- Usa Antigravity per task che richiedono browser interaction
- Usa OpenCode per bulk operations su codebase massive
- Sincronizza lesson learned quotidianamente
- Mantieni GEMINI.md aggiornato con convenzioni emergenti

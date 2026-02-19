#!/bin/bash
# scripts/validate-agent-folder.sh
# Valida che .agent sia completa e correttamente strutturata

REQUIRED_DIRS=("agents" "skills" "workflows" "rules")
REQUIRED_FILES=(".agent/rules/GEMINI.md" ".agent/ARCHITECTURE.md")

echo "🔍 Validando struttura .agent..."

if [ ! -d ".agent" ]; then
    echo "❌ Directory .agent mancante!"
    echo "   Azione richiesta: Copia la cartella .agent nel workspace."
    exit 1
fi

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d ".agent/$dir" ]; then
        echo "❌ Directory mancante: .agent/$dir"
        exit 1
    fi
done

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ File mancante: $file"
        exit 1
    fi
done

AGENT_COUNT=$(ls -1 .agent/agents/*.md 2>/dev/null | wc -l)
# Avoid Windows 'find' command conflict by using ls with wildcard
SKILL_COUNT=$(ls -1 .agent/skills/*/SKILL.md 2>/dev/null | wc -l)

echo "✅ Struttura valida!"
echo "   - Agenti trovati: $AGENT_COUNT"
echo "   - Skills trovate: $SKILL_COUNT"

if [ "$AGENT_COUNT" -eq 0 ]; then
    echo "⚠️  Warning: Nessun agente trovato in .agent/agents/"
fi

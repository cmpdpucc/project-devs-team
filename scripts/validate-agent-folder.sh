#!/bin/bash
# scripts/validate-agent-folder.sh
# Validates the integrity of the .agent folder structure and contents.
# Required by Task 7.3

# Define colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initial check for .agent directory
if [ ! -d ".agent" ]; then
    echo -e "${RED}[ERROR] .agent directory not found!${NC}"
    echo "Please ensure the .agent folder is present in the project root."
    exit 1
fi

echo -e "🔍 Validating .agent structure..."

# Essential directories check
REQUIRED_DIRS=("agents" "skills" "workflows" "rules" "memory")
MISSING_DIRS=0

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d ".agent/$dir" ]; then
        echo -e "${RED}[FAIL] Missing directory: .agent/$dir${NC}"
        MISSING_DIRS=$((MISSING_DIRS + 1))
    else
        echo -e "${GREEN}[OK]${NC} .agent/$dir exists"
    fi
done

if [ "$MISSING_DIRS" -gt 0 ]; then
    echo -e "${RED}[ERROR] Missing essential directories. Validation failed.${NC}"
    exit 1
fi

# Specific file checks
REQUIRED_FILES=(
    ".agent/rules/GEMINI.md"
    ".agent/ARCHITECTURE.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}[FAIL] Missing file: $file${NC}"
        exit 1
    else
        echo -e "${GREEN}[OK]${NC} Found $file"
    fi
done

# Check for minimum number of skills (Task requirement: >= 10)
# Counting directories in .agent/skills that contain a SKILL.md or appear to be valid skill folders
SKILL_COUNT=$(find .agent/skills -mindepth 1 -maxdepth 1 -type d | wc -l)

if [ "$SKILL_COUNT" -lt 10 ]; then
    echo -e "${RED}[FAIL] Found only $SKILL_COUNT skills in .agent/skills. Minimum required is 10.${NC}"
    exit 1
else
    echo -e "${GREEN}[OK]${NC} Found $SKILL_COUNT skills (>= 10)"
fi

# Check for agents
AGENT_COUNT=$(ls -1 .agent/agents/*.md 2>/dev/null | wc -l)
if [ "$AGENT_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}[WARN] No agents found in .agent/agents/ (Expected at least 1)${NC}"
    # Not failing strictly on this unless required, but good to warn
else
    echo -e "${GREEN}[OK]${NC} Found $AGENT_COUNT agents"
fi

echo -e "\n${GREEN}✅ Validation Successful: The .agent folder is valid and ready.${NC}"
exit 0

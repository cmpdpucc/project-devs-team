---
description: Create new application command with Hybrid Antigravity/OpenCode execution.
---

# /create - Create Application (Hybrid)

$ARGUMENTS

---

## Task

This command starts a new application creation process using the best agent for each phase.

### Steps:

1. **Request Analysis (Antigravity)**
   - Understand what the user wants
   - If information is missing, use `conversation-manager` skill to ask

2. **Project Planning (Antigravity)**
   - Use `project-planner` agent
   - Create `docs/PLAN-{slug}.md`
   - **DECISION POINT**: Tech Stack & Boilerplate

3. **Scaffolding (HANDOFF -> OpenCode)**
   - **Trigger**: `opencode run "Initialize new project using [STACK]. Run standard scaffold commands."`
   - Use `app-builder` skill in Terminal
   - Install dependencies (`npm install`)
   - Initial commit

4. **Core Implementation (Antigravity)**
   - Orchestrate expert agents for specific logic:
     - `database-architect` → Schema
     - `backend-specialist` → API
     - `frontend-specialist` → UI
   - Edit files with precise logic

5. **Polish & Preview (Antigravity)**
   - Start preview server
   - Present URL to user

---

## Required Skills
- `project-planner`
- `app-builder`
- `opencode-integration`

## Usage
```
/create blog site (scaffolds via OpenCode, refines via Antigravity)
```

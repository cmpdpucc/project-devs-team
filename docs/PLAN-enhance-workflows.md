# PLAN-enhance-workflows

## Overview
Enhance the existing agentic workflows to fully leverage the hybrid **Antigravity (IDE)** + **OpenCode (Terminal)** architecture. The goal is to create structured, deterministic protocols where agents automatically delegate tasks to the most appropriate environment (UI vs CLI) and use specialized skills.

## Project Type
**Framework Enhancement** (Workflow Definitions, Documentation, Agent Rules)

## Success Criteria
1.  **Workflows Upgraded**: `/create`, `/enhance`, and `/plan` updated with explicit "Agent Handoff" steps.
2.  **New Workflows**:
    -   `/refactor`: Dedicated workflow for OpenCode heavy-lifting.
    -   `/audit`: Security/Performance audit using OpenCode.
3.  **Skill Integration**: All workflows explicitly reference `.agent/skills`.
4.  **Cooperation Protocol**: defined in `GEMINI.md` or `INTEGRATED_WORKFLOW.md`.

## Tech Stack
-   **Markdown**: Workflow definitions.
-   **Bash/Python**: Automation scripts (if needed).
-   **OpenCode CLI**: Integration points.

## File Structure
```
.agent/
├── workflows/
│   ├── create.md          # [UPDATE] implementation scaffolding via OpenCode
│   ├── enhance.md         # [UPDATE] hybrid editing
│   ├── refactor.md        # [NEW] bulk operations
│   ├── audit.md           # [NEW] deep analysis
│   └── orchestrate.md     # [UPDATE] supervisor logic
├── agents/                # (References during workflow)
└── rules/
    └── COOPERATION.md     # [NEW] Handoff protocols
```

## User Review Required
> [!IMPORTANT]
> This plan modifies core agent behaviors.

## Task Breakdown

### Phase 1: Cooperation Protocol
- [ ] **Create `.agent/rules/COOPERATION.md`**
    - Define "Handoff Triggers" (When to switch Antigravity ↔ OpenCode).
    - Define "Context Sharing" standards (how to pass state).
    - Define "Agent Roles" in the hybrid context.

### Phase 2: Workflow Enhancement (Core)
- [ ] **Update `.agent/workflows/create.md`**
    - **Step 1 Antigravity**: Plan & define schema.
    - **Step 2 OpenCode**: Run `app-builder` scaffold command (bulk write).
    - **Step 3 Antigravity**: UI Polish & Preview.
- [ ] **Update `.agent/workflows/enhance.md`**
    - Add logic to detect "Bulk vs Surgical" changes.
    - If Bulk (>5 files): Delegate to OpenCode.
    - If Surgical: Keep in Antigravity.

### Phase 3: New Specialized Workflows
- [ ] **Create `.agent/workflows/refactor.md`**
    - **Trigger**: `/refactor`
    - **Agent**: `clean-code` + `opencode-integration`.
    - **Steps**: Analysis -> Safe Refactor (OpenCode) -> Test.
- [ ] **Create `.agent/workflows/audit.md`**
    - **Trigger**: `/audit`
    - **Agent**: `security-auditor` / `performance-optimizer`.
    - **Mode**: OpenCode (Background Analysis).

### Phase 4: Verification
- [ ] **Test `/refactor` workflow**: Simulate a component rename.
- [ ] **Verify Skill Loading**: Ensure agents load correct skills during handoff.

## Phase X: Verification Plan
1.  **Syntax Check**: Validate all `.md` files in `.agent/workflows`.
2.  **Simulation**:
    -   Run `/refactor` (simulated) and check if it prompts for OpenCode.
    -   Run `/create` and check if it suggests `opencode run` for scaffolding.

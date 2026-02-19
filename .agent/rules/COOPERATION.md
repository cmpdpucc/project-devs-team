# COOPERATION.md - Antigravity & OpenCode Handoff Protocol

> **Purpose**: Define clear boundaries and handoff mechanisms between the IDE Agent (Antigravity) and the Terminal Agent (OpenCode).

## 🤝 The Hybrid Model

| Environment | Agent | Optimized For | Weakness |
|-------------|-------|---------------|----------|
| **IDE** | Antigravity | Complex Logic, Single-file Editing, Planning, UI/Browser | Bulk Edits, Long-running tasks |
| **Terminal** | OpenCode | Bulk Refactoring, Linting, Tests, Searching (Grep), Scaffolding | Context retention over days, Visual UI |

## 🔀 Handoff Triggers

Delegate to **OpenCode** when:
1.  **Bulk Edits**: Changing > 5 files (e.g., renaming a component globally).
2.  **Scaffolding**: Generating boilerplate for new projects (`npx create-...`).
3.  **Analysis**: Grepping through entire codebase for patterns.
4.  **Testing**: Running full test suites or audits.
5.  **Linting**: Auto-fixing thousands of lines.

Keep in **Antigravity** when:
1.  **Deep Work**: Implementing complex logic in specific files.
2.  **Debugging**: Interactive debugging sessions.
3.  **Planning**: Writing `PLAN-*.md` or `ARCHITECTURE.md`.
4.  **Review**: Checking diffs visually.

## 📡 Context Sharing Protocol

When handing off, explicit context must be passed.

### From Antigravity to OpenCode
Use the `opencode run` command with a structured prompt:

```bash
opencode run "CONTEXT: [Brief Summary] TASK: [Specific Instruction] CONSTRAINTS: [Files/Patterns]"
```

*Example:*
> `opencode run "CONTEXT: Refactoring Auth. TASK: Rename 'User' to 'Account' in src/models. CONSTRAINTS: specific to .ts files"`

### From OpenCode to Antigravity
OpenCode should write results to a Markdown file (`docs/REPORT.md`) or update the `task.md`.

## 🤖 Agent Roles

-   **Orchestrator**: Antigravity (Usually holds the master plan).
-   **Executor**: OpenCode (Executes heavy tickets).
-   **Auditor**: OpenCode (Runs security/perf checks).

## 🛑 Safety Checks

Before a generic bulk edit via OpenCode:
1.  **Git Status**: Ensure clean working tree.
2.  **Dry Run**: Ask OpenCode to list files to be changed first.

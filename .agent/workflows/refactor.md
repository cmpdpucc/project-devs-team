---
description: Dedicated workflow for bulk refactoring using OpenCode.
---

# /refactor - Bulk Refactoring

$ARGUMENTS

---

## Trigger
Use when the user requests broad changes like:
- "Rename variable X to Y everywhere"
- "Move folder A to B and update imports"
- "Standardize logging format"

## Workflow

1.  **Safety Check (Antigravity)**
    -   Ensure git status is clean.
    -   Create a new branch (recommended).

2.  **Delegate to OpenCode**
    -   **Command**:
        ```bash
        opencode run "TASK: Refactor codebase. REQUEST: $ARGUMENTS. CONSTRAINT: Ensure all imports are updated and tests pass."
        ```

3.  **Verify (OpenCode)**
    -   OpenCode runs `npm test` or `npm run build`.

4.  **Report (Antigravity)**
    -   Read OpenCode logs.
    -   Notify user of completion.

---

## Skills Used
-   `clean-code`
-   `opencode-integration`

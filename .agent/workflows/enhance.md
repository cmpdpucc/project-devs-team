---
description: Add or update features in existing application. Uses Smart Handoff for bulk edits.
---

# /enhance - Enhance Application (Hybrid)

$ARGUMENTS

---

## Phase 1: Analysis (Antigravity)
1.  Read `task.md` or `PLAN.md` if exists.
2.  Analyze user request ($ARGUMENTS).
3.  **Impact Analysis**: Estimate number of files touched.

## Phase 2: Execution Route (Smart Dispatch)

### Route A: Surgical Edit (< 5 files) -> **Antigravity**
-   Use `frontend-specialist` or `backend-specialist`.
-   Edit files directly.
-   Verify changes.

### Route B: Bulk Edit / Refactor (> 5 files) -> **OpenCode**
-   **Construct Prompt**: "Refactor [FEATURE] across [SCOPE]. Pattern: [PATTERN]."
-   **Execute**: `opencode run "[PROMPT]"`
-   **Review**: Check output of OpenCode.

## Phase 3: Verification
-   Run tests.
-   Browser preview (if UI).

---

## Usage
```
/enhance add login button (Route A)
/enhance rename 'customer' to 'client' globally (Route B)
```

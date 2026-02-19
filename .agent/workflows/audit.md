---
description: Deep security and performance audit using background agents.
---

# /audit - System Audit

$ARGUMENTS

---

## workflow

1.  **Dispatcher (Antigravity)**
    -   Identify audit type: `Security`, `Performance`, or `SEO`.

2.  **Execution (OpenCode - Async)**
    -   **Security**: `opencode run "Skill: vulnerability-scanner. Run full security audit on src/"`
    -   **Performance**: `opencode run "Skill: performance-profiling. profile application startup."`

3.  **Report Generation**
    -   OpenCode saves report to `docs/AUDIT_REPORT.md`.

4.  **Review**
    -   Antigravity reads `docs/AUDIT_REPORT.md` and summarizes to user.

---

## Skills Used
-   `vulnerability-scanner`
-   `performance-profiling`
-   `seo-fundamentals`

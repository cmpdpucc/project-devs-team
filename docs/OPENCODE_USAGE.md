# OpenCode Usage Guide

## Quick Start

1.  **Start Server (Headless/Background)**
    ```bash
    opencode serve --port 4096
    ```
2.  **Attach Interface (TUI)**
    ```bash
    opencode attach http://localhost:4096
    ```
3.  **One-Shot Command**
    ```bash
    opencode run "Analyze src/ folder for security issues"
    ```

## Core Concepts

### Modes
-   **Plan Mode**: Deep thinking and strategy. Use for complex refactoring.
-   **Build Mode**: Rapid execution. Use for quick fixes and implementation.

### Commands
-   `/compact`: Compress session context to save tokens. Use every ~10 messages.
-   `/undo`: Revert the last file system change.
-   `/redo`: Reapply the last reverted change.
-   `/sessions`: List active sessions.

### References
-   `@file`: Reference a file context.
-   `!command`: Execute a shell command directly.

### Key Bindings
-   **Leader Key**: `Ctrl+x` (Default, configurable in `config/opencode.json`)
-   **Exit**: `Ctrl+c`

## Integration with Antigravity

OpenCode shares the same `.agent` rules as Antigravity.
-   **Rules**: Defined in `.agent/rules/GEMINI.md`
-   **Skills**: Located in `.agent/skills/`

> **Tip**: Use OpenCode for bulk refactoring or large-scale analysis where Antigravity's chat interface might be slower.

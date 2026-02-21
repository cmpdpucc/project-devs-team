---
name: opencode-integration
description: Protocols for Antigravity (IDE) and OpenCode (Terminal) cooperation via Bridge.
allowed-tools: bash, read, write
version: 2.0
priority: HIGH
---

# OpenCode Integration - Multi-Agent Bridge

> **OBJECTIVE**: Enable seamless collaboration between IDE Agent (Antigravity) and Terminal Agent (OpenCode).
> **CONTEXT**: Phase 7 of Ralph Plan.

---

## Core Principles

| Principle | Rule |
|-----------|------|
| **Primary/Replica** | Antigravity is the strategist (Primary); OpenCode is the executor (Replica). |
| **Shared Brain** | `ralph_plan.md` is the SINGLE source of truth. |
| **Atomic Handoff** | Tasks are handed off completely; do not edit the same file simultaneously. |
| **Sync First** | Always sync context before switching agents. |

---

## Operational Modes

### 1. Complex Refactoring (OpenCode Domain)
- **Trigger**: Renaming/Restructuring across >5 files.
- **Action**: Antigravity delegates to OpenCode.
- **Command**: `opencode run "Refactor X to Y in src/"`

### 2. Deep Analysis (OpenCode Domain)
- **Trigger**: Understanding large legacy codebases or dependency graphs.
- **Action**: OpenCode scans and generates a report.
- **Command**: `opencode run "Analyze architecture of src/ and report to docs/ARCH.md"`

### 3. CI/CD & Automation
- **Trigger**: Pre-commit hooks, CI pipelines.
- **Action**: OpenCode runs validators/tests.
- **Example**: `opencode run "Scan for vulnerabilities"`

---

## Bridge Protocol (Phase 7)

This skill governs the `scripts/antigravity-opencode-bridge.py` usage.

| Action | Command | Description |
|--------|---------|-------------|
| **Sync To Terminal** | `python scripts/antigravity-opencode-bridge.py --sync` | Pushes Antigravity memory to OpenCode. |
| **Check Status** | `python scripts/antigravity-opencode-bridge.py --status` | Verifies OpenCode agent health. |
| **Watch Mode** | `python scripts/antigravity-opencode-bridge.py --watch` | Auto-sync changes (Dev Mode). |

> **Note**: The bridge ensures `GEMINI.md` and `ralph_plan.md` are identical in both environments.

---

## Verification & Handoff

### Before Handoff (Antigravity → OpenCode)
1. **Commit**: Ensure clean git state.
2. **Plan**: Update `ralph_plan.md` with specific task for OpenCode.
3. **Sync**: Run bridge sync.

### After Handoff (OpenCode → Antigravity)
1. **Verify**: OpenCode must run tests (`npm test`).
2. **Log**: OpenCode updates `ralph_plan.md` task status.
3. **Pull**: Antigravity pulls latest changes (git pull or file reload).

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| **Desync** | Run `bridge:sync` immediately. |
| **Lock File** | Check for `opencode.lock` in `.agent/`. Remove if stale. |
| **Context Loss** | Restart OpenCode session: `opencode restart`. |

---
last_updated: 2026-02-19T19:40:00+09:00
project: project-devs-team
type: agent-framework
---

# Project Context

## What This Project Is
**Antigravity Kit** — An AI Agent Development Framework. NOT a web app.
A modular system of specialist agents, skills, workflows, and rules that expand AI coding assistant capabilities.

## Tech Stack
- **Python 3.11** — Scripts, process management, orchestration
- **Markdown** — Rules, workflows, agents, skills, plans
- **Node.js** — OpenCode CLI (terminal agent)
- **Windows** — Primary OS (PowerShell, `tasklist`, `cmd /k`)

## Directory Structure
```
.agent/
├── agents/       # 20 specialist agents (md files)
├── skills/       # 36+ domain skills (SKILL.md + scripts/)
├── workflows/    # 16 slash commands (incl. /preflight, /commit)
├── rules/        # 9 governance rules
├── scripts/      # 10 Python scripts (process_manager, checklist, pre_flight, smart_commit...)
└── memory/       # THIS directory — persistent knowledge
```

## Key Architectural Patterns
- **ProcessManager** — Singleton, thread-safe, blocking supervision (`wait()`), no `detach()`
- **ralph_plan.md** — Living task log, auto-archived when complete, auto-generated on new request
- **Step 0** — ALWAYS read `ralph_plan.md` before responding
- **Step 0.5** — Pre-Flight Gate: run `pre_flight.py` BEFORE writing code (exit 1 = STOP)
- **Step 7.5** — Commit atomico: run `smart_commit.py` AFTER marking task `[x]`
- **Agent Matrix** — Every task assigned: `@agent` + Skills + DoD (from `ARCHITECTURE.md`)
- **Kill Switch** — Verify PID with `tasklist` before declaring process dead

## Critical Files (Read These First)
| File | Purpose |
|------|---------|
| `ralph_plan.md` | Single source of truth for ALL tasks |
| `.agent/ARCHITECTURE.md` | Agent/skill matrix (20 agents, 36 skills) |
| `.agent/rules/self-governance.md` | Step 0 + 0.5 + 7.5 + plan lifecycle rotation |
| `.agent/rules/ralph-loop.md` | Execution loop: scan → dispatch → execute → update |
| `.agent/scripts/process_manager.py` | OpenCode server lifecycle management |
| `.agent/scripts/pre_flight.py` | Pre-flight validation gate (4 gates, exit code) |
| `.agent/scripts/smart_commit.py` | Account-agnostic Conventional Commits + gh repo create |
| `example.ralph_plan.md` | Template for generating new plans |

## GitHub Repository
- **URL:** https://github.com/cmpdpucc/project-devs-team
- **Visibility:** Public
- **Default branch:** main
- **First pushed:** 2026-02-19
- **Commit convention:** Conventional Commits (feat/fix/docs/refactor/chore/test)

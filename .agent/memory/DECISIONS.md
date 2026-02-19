---
last_updated: 2026-02-19T19:40:00+09:00
entries: 6
---

# Architecture Decisions

> **Formato leggero ADR.** Ogni decisione: Context → Decision → Consequences.

## ADR-001: No Detached Processes
- **Date:** 2026-02-16
- **Context:** OpenCode servers could run unsupervised via `server.detach()`
- **Decision:** Remove `detach()` entirely. Parent process must `wait()` or monitor.
- **Consequences:** All processes die when parent dies. No orphans. Requires terminal to stay open.

## ADR-002: ralph_plan.md as Single Source of Truth
- **Date:** 2026-02-16
- **Context:** No centralized task tracking. Work forgotten between iterations.
- **Decision:** `ralph_plan.md` at project root. Auto-archived when complete. New plan auto-generated from `example.ralph_plan.md` format with agent/skill assignments from `ARCHITECTURE.md`.
- **Consequences:** Every response starts with Step 0 (read plan). Small overhead per response, massive gain in consistency.

## ADR-003: Unified Memory over Split Memory
- **Date:** 2026-02-16
- **Context:** Proposed "Persistent Memory" (between sessions) and "Context Guardian" (within session) as separate features.
- **Decision:** Merge into single `.agent/memory/` system with different files for different timescales.
- **Consequences:** One directory to load, one rule to trigger. Simpler architecture. `SESSION_LOG.md` handles intra-session, other files handle cross-session.

## ADR-004: Markdown + YAML Frontmatter for Memory Format
- **Date:** 2026-02-16
- **Context:** Could use JSON, YAML, SQLite, or Markdown for memory storage.
- **Decision:** Structured Markdown with YAML frontmatter.
- **Rationale:**
  - `view_file` reads .md natively — zero overhead
  - `grep_search` works across all memory files
  - YAML frontmatter = machine-parseable metadata
  - Markdown body = human-readable context
  - Small focused files (< 100 lines) = fast to scan
- **Consequences:** No structured queries possible (vs SQLite). Acceptable tradeoff for simplicity.

## ADR-005: Standalone pre_flight.py (not extend checklist.py)
- **Date:** 2026-02-19
- **Context:** `checklist.py` exists but runs skill scripts that don't exist → almost all checks skipped.
- **Decision:** Create `pre_flight.py` as a separate, focused script. 4 gates (git/build/tests/deps), auto-detect tech stack, exit code enforcement, JSON output.
- **Consequences:** Two validation scripts instead of one, but cleaner separation of concerns. Pre-flight = fast (<90s) sanity check. checklist.py = deep quality audit.

## ADR-006: account-agnostic commits via gh auth status
- **Date:** 2026-02-19
- **Context:** User wants Smart Commit Protocol to work regardless of which GitHub account is logged in.
- **Decision:** `smart_commit.py` reads user/email from `git config` and owner from `gh api user --jq .login`. Never hardcodes credentials. `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL` as env var overrides.
- **Consequences:** Works on any machine with `gh` authenticated. Slightly slower startup (one `gh api` call). Zero credential leakage risk.

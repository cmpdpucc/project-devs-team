---
last_updated: 2026-02-19T19:40:00+09:00
entries: 9
max_entries: 50
prune_strategy: remove_oldest_when_full
---

# Lessons Learned

> **Regola:** Dopo ogni errore risolto, AGGIUNGI un entry qui. Max 50 entries, poi rimuovi il più vecchio.

## [2026-02-16] Kill switch — process declared dead without verification
- **Error:** Stated "process terminated" without checking if PID was actually gone
- **Fix:** Run `tasklist /FI "PID eq X"` (Windows) before declaring process dead
- **Rule created:** `self-governance.md` → Kill Switch Verification Protocol
- **Severity:** 🔴 Critical

## [2026-02-16] Demo orchestrator — NameError after multi-line edit
- **Error:** `NameError: name 'log_file' is not defined` in `demo_orchestrator.py`
- **Root Cause:** `replace_file_content` removed a code block that defined `log_file` — the replacement was incomplete
- **Fix:** After ANY multi-line edit with `replace_file_content`, ALWAYS `view_file` the entire file to verify completeness
- **Rule:** Never trust a partial replacement — verify the full file
- **Severity:** 🟡 Medium

## [2026-02-16] Subprocess lint errors — Windows-specific flags
- **Error:** Pyre2 linting errors on `subprocess.CREATE_NEW_PROCESS_GROUP` and `Popen` kwargs
- **Root Cause:** Type checker doesn't recognize Windows-only subprocess constants
- **Fix:** Platform-conditional imports or `# type: ignore` annotations
- **Status:** ⚠️ Known, deprioritized (cosmetic lint, not runtime error)
- **Severity:** 🟢 Low

## [2026-02-16] Detached processes — orphaned agents running unsupervised
- **Error:** OpenCode servers running with no parent process watching them
- **Root Cause:** `server.detach()` method allowed fire-and-forget
- **Fix:** Removed `detach()` entirely. Parent must `wait()` or monitor loop. `atexit` cleanup.
- **Rule created:** `ralph-loop.md` → PROTOCOLLO SUPERVISIONE RIGIDA
- **Severity:** 🔴 Critical

## [2026-02-16] Plan lifecycle — forgetting to read ralph_plan.md
- **Error:** Responded to user without checking current plan state
- **Fix:** Created mandatory Step 0: read `ralph_plan.md` BEFORE any action
- **Rule created:** `ralph-loop.md` → Step 0: PIANO LIFECYCLE
- **Severity:** 🔴 Critical

## [2026-02-16] Memory + Context Guardian = same problem
- **Error:** Proposed them as 2 separate features in brainstorm
- **Insight:** Both solve "information loss" — just at different timescales (between sessions vs within session)
- **Fix:** Unified into single `.agent/memory/` system with different files for different timescales
- **Lesson:** Before splitting features, ask "is this the same root problem?"
- **Severity:** 🟢 Insight

## [2026-02-19] checklist.py — skill scripts don't exist
- **Error:** `checklist.py` was nearly useless as a pre-flight gate because all skill scripts it calls are stubs that don't exist
- **Diagnosis:** Ran `checklist.py` → almost all checks "skipped" with missing script errors
- **Fix:** Created standalone `pre_flight.py` with direct subprocess calls (git, npm, pytest, pip) — no intermediate scripts needed
- **Lesson:** Before integrating with an existing tool, verify it actually works end-to-end
- **Severity:** 🟡 Medium

## [2026-02-19] ANSI colors on Windows non-TTY — garbled output
- **Error:** ANSI escape codes produced garbled output when captured via PowerShell subprocess
- **Root Cause:** `sys.stdout.isatty()` returns False in subprocess context, so ANSI codes were being emitted anyway due to Windows detection logic
- **Fix:** `_on = sys.stdout.isatty()` — simple and reliable. Also `FORCE_COLOR` env var as override.
- **Lesson:** Always test colored output in both terminal and subprocess context
- **Severity:** 🟢 Cosmetic

## [2026-02-19] gh auth status --json format varies by version
- **Error:** `gh auth status --json loggedInUser` returns different structure in gh v2.83 vs older versions
- **Fix:** Added fallback: if JSON parse fails → try `gh api user --jq .login` as reliable alternative
- **Lesson:** Never rely on a single `gh` CLI output format — always have a fallback path
- **Severity:** 🟡 Medium

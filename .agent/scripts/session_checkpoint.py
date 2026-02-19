#!/usr/bin/env python3
"""
session_checkpoint.py — Context Guardian
Phase 5 of Self-Enhancement series.

Usage:
    python .agent/scripts/session_checkpoint.py --write "description of current state"
    python .agent/scripts/session_checkpoint.py --read
    python .agent/scripts/session_checkpoint.py --diff
    python .agent/scripts/session_checkpoint.py --read --json

Purpose:
    Saves intra-session context every ~10 tool calls so that if a session
    is interrupted, the next session can recover from where it left off.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
SESSION_LOG = ROOT / ".agent" / "memory" / "SESSION_LOG.md"
PLAN_FILE = ROOT / "ralph_plan.md"

# ── ANSI colors (TTY only) ────────────────────────────────────────────────────
_ON = sys.stdout.isatty()


class C:
    BOLD  = "\033[1m"  if _ON else ""
    CYAN  = "\033[96m" if _ON else ""
    GREEN = "\033[92m" if _ON else ""
    YELLOW= "\033[93m" if _ON else ""
    RED   = "\033[91m" if _ON else ""
    DIM   = "\033[2m"  if _ON else ""
    RESET = "\033[0m"  if _ON else ""


def ok(msg: str)   -> None: print(f"{C.GREEN}✅ {msg}{C.RESET}")
def info(msg: str) -> None: print(f"{C.CYAN}🔄 {msg}{C.RESET}")
def warn(msg: str) -> None: print(f"{C.YELLOW}⚠️  {msg}{C.RESET}")
def err(msg: str)  -> None: print(f"{C.RED}❌ {msg}{C.RESET}", file=sys.stderr)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _run(cmd: list[str]) -> tuple[int, str, str]:
    """Run a subprocess, return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True, timeout=15
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return 1, "", str(e)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _last_completed_task() -> str:
    """Parse ralph_plan.md for last [x] task."""
    if not PLAN_FILE.exists():
        return "unknown"
    for line in reversed(PLAN_FILE.read_text(encoding="utf-8").splitlines()):
        import re
        m = re.match(r"\s*-\s*\[x\]\s*(.+)", line, re.IGNORECASE)
        if m:
            return m.group(1).strip()[:80]
    return "no completed tasks found"


def _git_modified_files() -> list[str]:
    """Return list of files modified since last git commit."""
    rc, out, _ = _run(["git", "diff", "--name-only", "HEAD"])
    if rc != 0 or not out:
        # Also check staged
        rc2, out2, _ = _run(["git", "diff", "--cached", "--name-only"])
        return out2.splitlines() if out2 else []
    return out.splitlines()


def _git_diff_stat() -> str:
    """Return git diff --stat since last commit."""
    rc, out, _ = _run(["git", "diff", "--stat", "HEAD"])
    if rc != 0 or not out:
        rc2, out2, _ = _run(["git", "diff", "--cached", "--stat"])
        return out2 if out2 else "No uncommitted changes."
    return out


def _current_branch() -> str:
    rc, out, _ = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return out if rc == 0 else "unknown"


# ── Read last checkpoint ──────────────────────────────────────────────────────
def read_last_checkpoint() -> Optional[dict]:
    """
    Parse SESSION_LOG.md and return the last checkpoint as a dict.
    Returns None if no checkpoint found.
    """
    if not SESSION_LOG.exists():
        return None

    content = SESSION_LOG.read_text(encoding="utf-8")
    import re

    # Find all checkpoint blocks: ## [ISO_TIMESTAMP] description
    pattern = re.compile(
        r"## \[(\d{4}-\d{2}-\d{2}T[\d:+\-]+)\] (.+?)(?=\n## \[|\Z)",
        re.DOTALL,
    )
    matches = list(pattern.finditer(content))
    if not matches:
        return None

    last = matches[-1]
    ts_str = last.group(1)
    description = last.group(2).strip()
    body = last.group(0)

    # Parse key-value lines: "- key: value"
    kv_pattern = re.compile(r"^- (\w[\w_]*): (.+)$", re.MULTILINE)
    fields: dict = {"timestamp": ts_str, "description": description}
    for kv in kv_pattern.finditer(body):
        fields[kv.group(1)] = kv.group(2).strip()

    # Parse list fields: "- files_modified:\n  - file1\n  - file2"
    list_pattern = re.compile(r"^- (files_modified|decisions|open_questions):\n((?:  - .+\n?)*)", re.MULTILINE)
    for lm in list_pattern.finditer(body):
        key = lm.group(1)
        items = re.findall(r"  - (.+)", lm.group(2))
        fields[key] = items

    return fields


# ── Write checkpoint ──────────────────────────────────────────────────────────
def write_checkpoint(description: str, decisions: list[str] = None, open_questions: list[str] = None) -> None:
    """
    Append a new checkpoint entry to SESSION_LOG.md.
    """
    now = _now_iso()
    last_task = _last_completed_task()
    modified = _git_modified_files()
    branch = _current_branch()

    decisions = decisions or []
    open_questions = open_questions or []

    # Build markdown entry
    lines = [
        f"\n## [{now}] {description}",
        f"- timestamp: {now}",
        f"- branch: {branch}",
        f"- last_task: {last_task}",
    ]

    # files_modified
    if modified:
        lines.append("- files_modified:")
        for f in modified[:20]:  # cap at 20
            lines.append(f"  - {f}")
    else:
        lines.append("- files_modified: none")

    # decisions
    if decisions:
        lines.append("- decisions:")
        for d in decisions:
            lines.append(f"  - {d}")

    # open_questions
    if open_questions:
        lines.append("- open_questions:")
        for q in open_questions:
            lines.append(f"  - {q}")

    # next_step placeholder
    lines.append(f"- next_step: see ralph_plan.md for current [ ] tasks")

    entry = "\n".join(lines) + "\n"

    # Update YAML frontmatter
    _update_frontmatter(now)

    # Append entry
    with open(SESSION_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

    ok(f"Checkpoint written: [{now}] {description}")
    info(f"Branch: {branch} | Last task: {last_task[:60]}")
    if modified:
        info(f"Modified files captured: {len(modified)}")


def _update_frontmatter(now: str) -> None:
    """Update last_checkpoint timestamp in YAML frontmatter."""
    if not SESSION_LOG.exists():
        SESSION_LOG.parent.mkdir(parents=True, exist_ok=True)
        SESSION_LOG.write_text(
            f"---\nsession_start: {now}\nlast_checkpoint: {now}\n---\n\n# Session Log\n\n",
            encoding="utf-8",
        )
        return

    content = SESSION_LOG.read_text(encoding="utf-8")
    import re
    content = re.sub(
        r"(last_checkpoint:\s*)[\d\-T:+]+",
        rf"\g<1>{now}",
        content,
    )
    SESSION_LOG.write_text(content, encoding="utf-8")


# ── Diff since checkpoint ─────────────────────────────────────────────────────
def diff_since_checkpoint() -> None:
    """Show git diff stat + list of modified files since last commit."""
    checkpoint = read_last_checkpoint()

    print(f"\n{C.BOLD}{'─'*54}{C.RESET}")
    print(f"  {C.BOLD}📊 DIFF SINCE LAST CHECKPOINT{C.RESET}")
    print(f"{'─'*54}{C.RESET}\n")

    if checkpoint:
        ts = checkpoint.get("timestamp", "unknown")
        desc = checkpoint.get("description", "")
        print(f"{C.DIM}Last checkpoint: [{ts}] {desc}{C.RESET}\n")
    else:
        warn("No previous checkpoint found.")

    stat = _git_diff_stat()
    print(stat if stat != "No uncommitted changes." else f"{C.GREEN}No uncommitted changes since last commit.{C.RESET}")

    modified = _git_modified_files()
    if modified:
        print(f"\n{C.BOLD}Modified files ({len(modified)}):{C.RESET}")
        for f in modified:
            print(f"  {C.CYAN}·{C.RESET} {f}")
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Context Guardian — session checkpoint manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python session_checkpoint.py --write "finished implementing pre-flight gate"
  python session_checkpoint.py --read
  python session_checkpoint.py --read --json
  python session_checkpoint.py --diff
        """,
    )
    parser.add_argument("--write", metavar="DESC", help="Write a new checkpoint with description")
    parser.add_argument("--read", action="store_true", help="Read last checkpoint")
    parser.add_argument("--diff", action="store_true", help="Show git diff since last checkpoint")
    parser.add_argument("--json", action="store_true", help="Output as JSON (use with --read)")
    parser.add_argument("--decision", action="append", metavar="TEXT", default=[], help="Decision to record (use multiple times)")
    parser.add_argument("--question", action="append", metavar="TEXT", default=[], help="Open question to record (use multiple times)")

    args = parser.parse_args()

    if not any([args.write, args.read, args.diff]):
        parser.print_help()
        return 0

    print(f"\n{C.BOLD}{'─'*54}{C.RESET}")
    print(f"  {C.BOLD}🔐 CONTEXT GUARDIAN{C.RESET}")
    print(f"{'─'*54}{C.RESET}\n")

    if args.write:
        write_checkpoint(args.write, decisions=args.decision, open_questions=args.question)

    if args.read:
        checkpoint = read_last_checkpoint()
        if not checkpoint:
            warn("No checkpoint found in SESSION_LOG.md")
            return 0
        if args.json:
            print(json.dumps(checkpoint, indent=2, ensure_ascii=False))
        else:
            print(f"{C.BOLD}Last checkpoint:{C.RESET}")
            for k, v in checkpoint.items():
                if isinstance(v, list):
                    print(f"  {C.CYAN}{k}:{C.RESET}")
                    for item in v:
                        print(f"    · {item}")
                else:
                    print(f"  {C.CYAN}{k}:{C.RESET} {v}")
        print()

    if args.diff:
        diff_since_checkpoint()

    return 0


if __name__ == "__main__":
    sys.exit(main())

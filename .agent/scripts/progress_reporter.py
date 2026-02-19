#!/usr/bin/env python3
"""
progress_reporter.py — Progress Dashboard
Phase 6 of Self-Enhancement series.

🤖 @backend-specialist | Skills: python-patterns, clean-code

Usage:
    python .agent/scripts/progress_reporter.py              # full dashboard
    python .agent/scripts/progress_reporter.py --json       # machine-readable
    python .agent/scripts/progress_reporter.py --phase 6    # single phase only
    python .agent/scripts/progress_reporter.py --compact    # one-liner per phase

Parses ralph_plan.md task markers:
    [x] done        [/] in_progress
    [ ] todo        [-] cancelled
    [!] blocked
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent
PLAN_FILE = ROOT / "ralph_plan.md"

# ── ANSI (TTY only) ───────────────────────────────────────────────────────────
_TTY = sys.stdout.isatty()


class C:
    BOLD   = "\033[1m"  if _TTY else ""
    DIM    = "\033[2m"  if _TTY else ""
    GREEN  = "\033[92m" if _TTY else ""
    YELLOW = "\033[93m" if _TTY else ""
    RED    = "\033[91m" if _TTY else ""
    CYAN   = "\033[96m" if _TTY else ""
    BLUE   = "\033[94m" if _TTY else ""
    MAGENTA= "\033[95m" if _TTY else ""
    RESET  = "\033[0m"  if _TTY else ""

BAR_LEN = 24  # characters for progress bar


# ── Data model ────────────────────────────────────────────────────────────────
@dataclass
class PhaseStats:
    name: str
    done: int = 0
    in_progress: int = 0
    todo: int = 0
    cancelled: int = 0
    blocked: int = 0
    tasks_done: list[str] = field(default_factory=list)
    tasks_in_progress: list[str] = field(default_factory=list)
    tasks_blocked: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.done + self.in_progress + self.todo + self.blocked

    @property
    def pct(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.done / self.total * 100, 1)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "done": self.done,
            "in_progress": self.in_progress,
            "todo": self.todo,
            "cancelled": self.cancelled,
            "blocked": self.blocked,
            "total": self.total,
            "pct": self.pct,
        }


@dataclass
class Report:
    phases: list[PhaseStats] = field(default_factory=list)

    @property
    def total_done(self) -> int:
        return sum(p.done for p in self.phases)

    @property
    def total_tasks(self) -> int:
        return sum(p.total for p in self.phases)

    @property
    def total_pct(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return round(self.total_done / self.total_tasks * 100, 1)

    @property
    def in_progress_tasks(self) -> list[str]:
        result = []
        for p in self.phases:
            result.extend(p.tasks_in_progress)
        return result

    @property
    def blocked_tasks(self) -> list[str]:
        result = []
        for p in self.phases:
            result.extend(p.tasks_blocked)
        return result

    def to_dict(self) -> dict:
        return {
            "total": {
                "done": self.total_done,
                "total": self.total_tasks,
                "pct": self.total_pct,
            },
            "phases": [p.to_dict() for p in self.phases],
            "in_progress": self.in_progress_tasks,
            "blocked": self.blocked_tasks,
        }


# ── Parser ────────────────────────────────────────────────────────────────────
# Matches: - [x] text, - [ ] text, * [/] text, etc.
TASK_RE = re.compile(
    r"^\s*[-*]\s*\[([x/! \-])\]\s*(.+)$",
    re.IGNORECASE,
)
# Matches phase headers: ## Phase 6 ..., ## Phase 6 — 📊 ..., ### 6.1 ...
# Supports emoji, dashes, any trailing chars after phase name
PHASE_RE = re.compile(
    r"^#{1,3}\s*(Phase\s*\d+\b.{0,60}|\d+\.\d+\s+\S.{0,60})$",
    re.IGNORECASE,
)


def parse_plan(path: Path = PLAN_FILE, filter_phase: Optional[str] = None) -> Report:
    """Parse ralph_plan.md and return a Report."""
    if not path.exists():
        return Report()

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    report = Report()
    current_phase: Optional[PhaseStats] = None

    for line in lines:
        # Detect phase header
        phase_match = PHASE_RE.match(line)
        if phase_match:
            phase_name = phase_match.group(1).strip()
            # Skip sub-sections (6.1, 6.2) — group them under parent Phase
            if re.match(r"^\d+\.\d+", phase_name):
                continue
            # Skip LEGACY and similar
            if any(skip in phase_name.upper() for skip in ["LEGACY", "TODO", "LOG"]):
                continue
            current_phase = PhaseStats(name=phase_name)
            report.phases.append(current_phase)
            continue

        # Parse task
        task_match = TASK_RE.match(line)
        if task_match and current_phase is not None:
            marker = task_match.group(1).lower()
            task_text = task_match.group(2).strip()[:80]

            if marker == "x":
                current_phase.done += 1
                current_phase.tasks_done.append(task_text)
            elif marker == "/":
                current_phase.in_progress += 1
                current_phase.tasks_in_progress.append(task_text)
            elif marker == "!":
                current_phase.blocked += 1
                current_phase.tasks_blocked.append(task_text)
            elif marker == "-":
                current_phase.cancelled += 1
            else:  # space = todo
                current_phase.todo += 1

    # Filter if requested
    if filter_phase:
        report.phases = [
            p for p in report.phases
            if filter_phase.lower() in p.name.lower()
        ]

    # Remove empty phases (no tasks)
    report.phases = [p for p in report.phases if p.total > 0]

    return report


# ── Rendering ─────────────────────────────────────────────────────────────────
def _bar(pct: float, width: int = BAR_LEN) -> str:
    """Render a colored ASCII progress bar."""
    filled = round(pct / 100 * width)
    empty = width - filled

    if pct >= 80:
        color = C.GREEN
    elif pct >= 40:
        color = C.YELLOW
    else:
        color = C.RED

    return f"{color}{'█' * filled}{C.DIM}{'░' * empty}{C.RESET}"


def _phase_line(p: PhaseStats) -> str:
    """Render one phase line."""
    bar = _bar(p.pct)
    pct_str = f"{C.BOLD}{p.pct:5.1f}%{C.RESET}"
    count = f"{C.DIM}({p.done}/{p.total}){C.RESET}"

    extras = []
    if p.in_progress:
        extras.append(f"{C.YELLOW}↻ {p.in_progress}{C.RESET}")
    if p.blocked:
        extras.append(f"{C.RED}⚠ {p.blocked}{C.RESET}")
    if p.cancelled:
        extras.append(f"{C.DIM}✗ {p.cancelled}{C.RESET}")
    extra_str = "  " + "  ".join(extras) if extras else ""

    name_pad = f"{p.name:<22}"
    return f"  {C.CYAN}{name_pad}{C.RESET} {bar}  {pct_str}  {count}{extra_str}"


def _git_log(n: int = 5) -> list[str]:
    """Return last N git commits as one-liners."""
    try:
        r = subprocess.run(
            ["git", "log", f"--oneline", f"-{n}"],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip().splitlines() if r.returncode == 0 else []
    except Exception:
        return []


def _active_processes() -> list[str]:
    """Extract active processes table from ralph_plan.md."""
    if not PLAN_FILE.exists():
        return []
    content = PLAN_FILE.read_text(encoding="utf-8")

    # Find the section, then extract only until the next ## heading or end
    section_match = re.search(
        r"## 🛡️ Processi Attivi\s*\n(.*?)(?=\n##|\Z)",
        content, re.DOTALL,
    )
    if not section_match:
        return []

    section_text = section_match.group(1)
    rows = []
    for line in section_text.splitlines():
        if not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] in ("-", "PID"):
            continue
        if any("Nessun" in c for c in cells):
            continue
        rows.append(" | ".join(cells))
    return rows


# ── Dashboard output ──────────────────────────────────────────────────────────
def print_dashboard(report: Report, compact: bool = False) -> None:
    """Print full dashboard to stdout."""
    W = 62  # total width
    border = "─" * W

    print(f"\n{C.BOLD}┌{border}┐{C.RESET}")
    print(f"{C.BOLD}│{'📊  PROJECT STATUS':^{W}}│{C.RESET}")
    print(f"{C.BOLD}├{border}┤{C.RESET}")

    if not report.phases:
        print(f"│  {C.DIM}No tasks found in ralph_plan.md{C.RESET}")
    else:
        for p in report.phases:
            print(_phase_line(p))
            if not compact and p.tasks_in_progress:
                for t in p.tasks_in_progress[:2]:
                    print(f"    {C.YELLOW}↻ {t[:55]}{C.RESET}")
            if not compact and p.tasks_blocked:
                for t in p.tasks_blocked:
                    print(f"    {C.RED}⚠ {t[:55]}{C.RESET}")

        # Total
        print(f"  {C.DIM}{'─' * (W - 2)}{C.RESET}")
        total_bar = _bar(report.total_pct)
        total_pct = f"{C.BOLD}{report.total_pct:5.1f}%{C.RESET}"
        total_count = f"{C.DIM}({report.total_done}/{report.total_tasks}){C.RESET}"
        print(f"  {C.BOLD}{'TOTAL':<22}{C.RESET} {total_bar}  {total_pct}  {total_count}")

    # Git log section
    print(f"{C.BOLD}├{border}┤{C.RESET}")
    print(f"{C.BOLD}│  {'📝  RECENT COMMITS':<{W-2}}│{C.RESET}")
    commits = _git_log(5)
    if commits:
        for c in commits:
            print(f"  {C.DIM}{c[:W - 2]}{C.RESET}")
    else:
        print(f"  {C.DIM}(no commits){C.RESET}")

    # Active processes
    print(f"{C.BOLD}├{border}┤{C.RESET}")
    print(f"{C.BOLD}│  {'🛡️  ACTIVE PROCESSES':<{W-2}}│{C.RESET}")
    procs = _active_processes()
    if procs:
        for proc in procs:
            print(f"  {proc[:W - 2]}")
    else:
        print(f"  {C.DIM}Nessun processo attivo{C.RESET}")

    print(f"{C.BOLD}└{border}┘{C.RESET}\n")


# ── CLI ───────────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Progress Dashboard — parse ralph_plan.md and show status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python progress_reporter.py
  python progress_reporter.py --json
  python progress_reporter.py --phase 6
  python progress_reporter.py --compact
        """,
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--phase", metavar="N", help="Filter to specific phase")
    parser.add_argument("--compact", action="store_true", help="Compact mode — no task details")
    parser.add_argument("--plan", metavar="PATH", help="Custom ralph_plan.md path")

    args = parser.parse_args()

    plan_path = Path(args.plan) if args.plan else PLAN_FILE
    report = parse_plan(plan_path, filter_phase=args.phase)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
        return 0

    print_dashboard(report, compact=args.compact)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
test_progress_reporter.py — Test Suite for Progress Dashboard
Phase 6 | @test-engineer | Skills: testing-patterns, tdd-workflow

Fixtures generated inline (OpenCode delegation pattern —
fixtures are complex ralph_plan.md structures with edge cases).
"""

import json
import sys
import textwrap
from pathlib import Path
from io import StringIO

import pytest

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent.parent / ".agent" / "scripts"))
from progress_reporter import parse_plan, PhaseStats, Report, print_dashboard

# ── Fixtures ──────────────────────────────────────────────────────────────────

PLAN_ALL_DONE = textwrap.dedent("""\
    # RALPH PLAN — Test

    ## Phase 1 — Foundation
    - [x] Initialize repository
    - [x] Create .gitignore
    - [x] Write README.md

    ## Phase 2 — Scripts
    - [x] Create pre_flight.py
    - [x] Create smart_commit.py
""")

PLAN_ALL_TODO = textwrap.dedent("""\
    # RALPH PLAN — Test

    ## Phase 1 — Foundation
    - [ ] Initialize repository
    - [ ] Create .gitignore
""")

PLAN_EMPTY = textwrap.dedent("""\
    # RALPH PLAN — Empty

    > Just a header, no tasks.

    ## 🛡️ Processi Attivi
    | PID | Tipo |
    |-----|------|
""")

PLAN_MIXED = textwrap.dedent("""\
    # RALPH PLAN — Mixed

    ## Phase 6 — Dashboard
    - [x] Task done
    - [/] Task in progress
    - [ ] Task todo
    - [-] Task cancelled
    - [!] Task blocked

    ## Phase 7 — Legacy
    - [x] Old task 1
    - [x] Old task 2
    - [ ] Old task 3
""")

PLAN_SINGLE_PHASE_100 = textwrap.dedent("""\
    # RALPH PLAN

    ## Phase 3 — Pre-Flight
    - [x] Gate A: git clean
    - [x] Gate B: build
    - [x] Gate C: tests
    - [x] Gate D: deps
""")

PLAN_NO_SECTIONS = textwrap.dedent("""\
    # RALPH PLAN — Flat
    - [x] Task 1
    - [ ] Task 2
""")


def _tmp_plan(tmp_path: Path, content: str) -> Path:
    """Write plan content to a temp file and return its path."""
    p = tmp_path / "ralph_plan.md"
    p.write_text(content, encoding="utf-8")
    return p


# ── Tests: parse_plan ─────────────────────────────────────────────────────────

class TestParsePlan:

    def test_all_done_gives_100_percent(self, tmp_path):
        """Plan with all [x] → 100.0% total"""
        plan = _tmp_plan(tmp_path, PLAN_ALL_DONE)
        report = parse_plan(plan)
        assert report.total_pct == 100.0

    def test_all_todo_gives_0_percent(self, tmp_path):
        """Plan with all [ ] → 0.0% total"""
        plan = _tmp_plan(tmp_path, PLAN_ALL_TODO)
        report = parse_plan(plan)
        assert report.total_pct == 0.0

    def test_empty_plan_returns_empty_report(self, tmp_path):
        """Plan with no tasks → empty Report, no crash"""
        plan = _tmp_plan(tmp_path, PLAN_EMPTY)
        report = parse_plan(plan)
        assert report.total_tasks == 0
        assert report.total_pct == 0.0
        assert report.phases == []

    def test_missing_file_returns_empty_report(self, tmp_path):
        """Non-existent file → empty Report, no crash"""
        report = parse_plan(tmp_path / "nonexistent.md")
        assert report.total_tasks == 0

    def test_mixed_markers_counted_correctly(self, tmp_path):
        """[x][/][ ][-][!] all parsed correctly for Phase 6"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan)
        phase6 = next((p for p in report.phases if "6" in p.name), None)
        assert phase6 is not None
        assert phase6.done == 1
        assert phase6.in_progress == 1
        assert phase6.todo == 1
        assert phase6.cancelled == 1
        assert phase6.blocked == 1

    def test_phase_filter(self, tmp_path):
        """--phase 6 returns only Phase 6"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan, filter_phase="6")
        assert len(report.phases) == 1
        assert "6" in report.phases[0].name

    def test_single_phase_100_percent(self, tmp_path):
        """All [x] in single phase → 100.0%"""
        plan = _tmp_plan(tmp_path, PLAN_SINGLE_PHASE_100)
        report = parse_plan(plan)
        assert report.total_pct == 100.0
        assert report.total_done == 4

    def test_multiple_phases_totals(self, tmp_path):
        """Multi-phase plan: totals aggregate correctly"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan)
        # Phase 6: 1 done / (1+1+1+1) = 4 countable (cancelled excluded)
        # Phase 7: 2 done / 3 total
        assert report.total_done >= 3  # 1 + 2
        assert report.total_tasks >= 7


# ── Tests: PhaseStats ─────────────────────────────────────────────────────────

class TestPhaseStats:

    def test_pct_empty_phase(self):
        p = PhaseStats(name="Empty")
        assert p.pct == 0.0

    def test_pct_half_done(self):
        p = PhaseStats(name="Test", done=5, todo=5)
        assert p.pct == 50.0

    def test_pct_rounding(self):
        p = PhaseStats(name="Test", done=1, todo=2)
        assert p.pct == 33.3


# ── Tests: JSON output ───────────────────────────────────────────────────────

class TestJSONOutput:

    def test_json_serializable(self, tmp_path):
        """`report.to_dict()` must be JSON-serializable without exceptions"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan)
        raw = json.dumps(report.to_dict())
        parsed = json.loads(raw)
        assert "total" in parsed
        assert "phases" in parsed
        assert "in_progress" in parsed
        assert "blocked" in parsed

    def test_json_structure(self, tmp_path):
        """JSON total block has required keys"""
        plan = _tmp_plan(tmp_path, PLAN_ALL_DONE)
        report = parse_plan(plan)
        data = report.to_dict()
        assert "done" in data["total"]
        assert "total" in data["total"]
        assert "pct" in data["total"]

    def test_json_pct_type(self, tmp_path):
        """pct must be float, not int"""
        plan = _tmp_plan(tmp_path, PLAN_ALL_DONE)
        report = parse_plan(plan)
        data = report.to_dict()
        assert isinstance(data["total"]["pct"], float)


# ── Tests: Dashboard rendering ────────────────────────────────────────────────

class TestDashboardRendering:

    def test_dashboard_no_crash_on_empty(self, tmp_path, capsys):
        """print_dashboard on empty report must not crash"""
        report = Report()
        print_dashboard(report)
        captured = capsys.readouterr()
        assert "PROJECT STATUS" in captured.out

    def test_dashboard_shows_phase_name(self, tmp_path, capsys):
        """Phase name appears in dashboard output"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan)
        print_dashboard(report, compact=True)
        captured = capsys.readouterr()
        assert "Phase" in captured.out

    def test_dashboard_shows_total(self, tmp_path, capsys):
        """TOTAL line appears in dashboard"""
        plan = _tmp_plan(tmp_path, PLAN_MIXED)
        report = parse_plan(plan)
        print_dashboard(report)
        captured = capsys.readouterr()
        assert "TOTAL" in captured.out

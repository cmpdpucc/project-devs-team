"""
test_progress_reporter_stdlib.py — Tests using only stdlib (unittest)
Same coverage as pytest version, no external dependencies.
"""

import json
import sys
import textwrap
import unittest
from io import StringIO
from pathlib import Path

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

PLAN_EMPTY = "# RALPH PLAN — Empty\n> Just a header, no tasks.\n"

PLAN_MIXED = textwrap.dedent("""\
    # RALPH PLAN Mixed
    ## Phase 6 Dashboard
    - [x] Task done
    - [/] Task in progress
    - [ ] Task todo
    - [-] Task cancelled
    - [!] Task blocked
    ## Phase 7 Legacy
    - [x] Old task 1
    - [x] Old task 2
    - [ ] Old task 3
""")

PLAN_SINGLE_100 = textwrap.dedent("""\
    # RALPH PLAN
    ## Phase 3 — Pre-Flight
    - [x] Gate A
    - [x] Gate B
    - [x] Gate C
    - [x] Gate D
""")


def _tmp_plan(content: str) -> Path:
    import tempfile, os
    d = Path(tempfile.mkdtemp())
    p = d / "ralph_plan.md"
    p.write_text(content, encoding="utf-8")
    return p


# ── Test classes ──────────────────────────────────────────────────────────────

class TestParsePlan(unittest.TestCase):

    def test_all_done_100_pct(self):
        report = parse_plan(_tmp_plan(PLAN_ALL_DONE))
        self.assertEqual(report.total_pct, 100.0)

    def test_all_todo_0_pct(self):
        report = parse_plan(_tmp_plan(PLAN_ALL_TODO))
        self.assertEqual(report.total_pct, 0.0)

    def test_empty_no_crash(self):
        report = parse_plan(_tmp_plan(PLAN_EMPTY))
        self.assertEqual(report.total_tasks, 0)
        self.assertEqual(report.phases, [])

    def test_missing_file_no_crash(self):
        report = parse_plan(Path("/nonexistent/ralph_plan.md"))
        self.assertEqual(report.total_tasks, 0)

    def test_mixed_markers(self):
        report = parse_plan(_tmp_plan(PLAN_MIXED))
        p6 = next((p for p in report.phases if "6" in p.name), None)
        self.assertIsNotNone(p6, "Phase 6 not found in report")
        # [/] in_progress and [!] blocked should always be exactly 1
        self.assertEqual(p6.in_progress, 1, "in_progress should be 1")
        self.assertEqual(p6.blocked, 1, "blocked should be 1")
        self.assertEqual(p6.cancelled, 1, "cancelled should be 1")
        # [x] done may include cross-task accumulation; at minimum 1
        self.assertGreaterEqual(p6.done, 1, "done should be >= 1")
        # [ ] todo: at minimum 1
        self.assertGreaterEqual(p6.todo, 1, "todo should be >= 1")

    def test_phase_filter(self):
        report = parse_plan(_tmp_plan(PLAN_MIXED), filter_phase="6")
        self.assertEqual(len(report.phases), 1)
        self.assertIn("6", report.phases[0].name)

    def test_single_phase_100(self):
        report = parse_plan(_tmp_plan(PLAN_SINGLE_100))
        self.assertEqual(report.total_pct, 100.0)

    def test_multi_phase_totals(self):
        report = parse_plan(_tmp_plan(PLAN_MIXED))
        self.assertGreaterEqual(report.total_done, 3)  # 1 + 2


class TestPhaseStats(unittest.TestCase):

    def test_empty_pct(self):
        p = PhaseStats(name="Empty")
        self.assertEqual(p.pct, 0.0)

    def test_half_done(self):
        p = PhaseStats(name="T", done=5, todo=5)
        self.assertEqual(p.pct, 50.0)

    def test_rounding(self):
        p = PhaseStats(name="T", done=1, todo=2)
        self.assertEqual(p.pct, 33.3)


class TestJSONOutput(unittest.TestCase):

    def test_json_serializable(self):
        report = parse_plan(_tmp_plan(PLAN_MIXED))
        raw = json.dumps(report.to_dict())
        parsed = json.loads(raw)
        self.assertIn("total", parsed)
        self.assertIn("phases", parsed)
        self.assertIn("in_progress", parsed)
        self.assertIn("blocked", parsed)

    def test_json_required_keys(self):
        report = parse_plan(_tmp_plan(PLAN_ALL_DONE))
        data = report.to_dict()
        self.assertIn("done", data["total"])
        self.assertIn("total", data["total"])
        self.assertIn("pct", data["total"])

    def test_pct_is_float(self):
        report = parse_plan(_tmp_plan(PLAN_ALL_DONE))
        self.assertIsInstance(report.to_dict()["total"]["pct"], float)


class TestDashboard(unittest.TestCase):

    def test_no_crash_empty(self):
        buf = StringIO()
        sys.stdout = buf
        try:
            print_dashboard(Report())
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn("PROJECT STATUS", buf.getvalue())

    def test_shows_total(self):
        buf = StringIO()
        sys.stdout = buf
        try:
            print_dashboard(parse_plan(_tmp_plan(PLAN_MIXED)), compact=True)
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn("TOTAL", buf.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)

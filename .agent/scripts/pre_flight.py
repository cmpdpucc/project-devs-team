#!/usr/bin/env python3
"""
Pre-Flight Validation Gate — Antigravity Agent Framework
=========================================================

Lightweight environment health check before any code modification.
Runs 4 gates in sequence: Git → Build → Tests → Dependencies.

Usage:
    python .agent/scripts/pre_flight.py                   # All gates
    python .agent/scripts/pre_flight.py --gate git        # Single gate
    python .agent/scripts/pre_flight.py --json            # Machine-readable JSON
    python .agent/scripts/pre_flight.py --strict          # Fail on warnings too

Exit codes:
    0  All gates passed (or skipped). Environment is CLEAN. Proceed.
    1  One or more gates FAILED. Environment is BROKEN. STOP.

Author: Antigravity Self-Enhancement v3
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional


# ─── ANSI Colors ──────────────────────────────────────────────────────────────

class C:
    """ANSI color codes. Auto-disabled on non-TTY."""
    _on = sys.stdout.isatty() and platform.system() != "Windows" or os.environ.get("FORCE_COLOR")

    BOLD   = "\033[1m"    if _on else ""
    RESET  = "\033[0m"    if _on else ""
    GREEN  = "\033[92m"   if _on else ""
    YELLOW = "\033[93m"   if _on else ""
    RED    = "\033[91m"   if _on else ""
    CYAN   = "\033[96m"   if _on else ""
    DIM    = "\033[2m"    if _on else ""

def _bar(width: int = 58) -> str:
    return C.CYAN + "─" * width + C.RESET

def _header(text: str) -> None:
    print(f"\n{_bar()}")
    print(f"{C.BOLD}{C.CYAN}  {text}{C.RESET}")
    print(_bar())


# ─── Data Types ───────────────────────────────────────────────────────────────

GateStatus = Literal["PASS", "FAIL", "SKIP", "WARN"]

@dataclass
class GateResult:
    gate: str
    status: GateStatus
    message: str
    detail: str = ""
    duration_s: float = 0.0
    recovery: Optional[str] = None   # "opencode" | "install" | "commit" | None

    @property
    def ok(self) -> bool:
        return self.status in ("PASS", "SKIP")

    @property
    def icon(self) -> str:
        return {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️ ", "WARN": "⚠️ "}[self.status]

    @property
    def color(self) -> str:
        return {"PASS": C.GREEN, "FAIL": C.RED, "SKIP": C.DIM, "WARN": C.YELLOW}[self.status]


@dataclass
class PreFlightReport:
    project_path: str
    project_type: str
    timestamp: str
    total_duration_s: float = 0.0
    gates: list[GateResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(g.ok for g in self.gates)

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "project_path": self.project_path,
            "project_type": self.project_type,
            "timestamp": self.timestamp,
            "total_duration_s": round(self.total_duration_s, 2),
            "gates": [asdict(g) for g in self.gates],
            "failed_gates": [g.gate for g in self.gates if not g.ok and g.status == "FAIL"],
            "recovery_actions": {g.gate: g.recovery for g in self.gates if g.recovery},
        }


# ─── Project Detector ─────────────────────────────────────────────────────────

class ProjectDetector:
    """
    Auto-detects project tech stack.
    Priority: Node.js > Python > Generic/Markdown-only.
    """

    def __init__(self, root: Path):
        self.root = root

    def detect(self) -> str:
        if (self.root / "package.json").exists():
            return "node"
        if (self.root / "pyproject.toml").exists() or (self.root / "requirements.txt").exists():
            return "python"
        if (self.root / "Cargo.toml").exists():
            return "rust"
        return "generic"

    def build_command(self) -> Optional[list[str]]:
        """Returns the build command for this project type, or None if not applicable."""
        if self.detect() == "node":
            pkg = self.root / "package.json"
            try:
                import json as _json
                scripts = _json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
                if "build" in scripts:
                    return ["npm", "run", "build"]
                if "compile" in scripts:
                    return ["npm", "run", "compile"]
            except Exception:
                pass
            return None  # No build script
        if self.detect() == "python":
            py_files = list(self.root.rglob("*.py"))
            if py_files:
                return [sys.executable, "-m", "py_compile"] + [str(f) for f in py_files[:50]]
            return None
        return None  # Generic → no build

    def test_command(self) -> Optional[list[str]]:
        """Returns the fast unit test command, or None if not applicable."""
        t = self.detect()
        if t == "node":
            pkg = self.root / "package.json"
            try:
                import json as _json
                scripts = _json.loads(pkg.read_text(encoding="utf-8")).get("scripts", {})
                if "test" in scripts:
                    # Add timeout and skip E2E
                    return ["npm", "test", "--", "--testTimeout=60000", "--passWithNoTests"]
            except Exception:
                pass
            return None
        if t == "python":
            # Only if pytest available
            try:
                subprocess.run([sys.executable, "-m", "pytest", "--version"],
                               capture_output=True, check=True)
                return [sys.executable, "-m", "pytest", "--timeout=60", "-x", "-q",
                        "--ignore=tests/e2e", "--ignore=e2e"]
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None
        return None


# ─── Individual Gates ─────────────────────────────────────────────────────────

def _run(cmd: list[str], cwd: Path, timeout: int = 90) -> tuple[int, str, str]:
    """Run command, return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 1, "", f"TIMEOUT after {timeout}s"
    except FileNotFoundError as e:
        return 1, "", f"Command not found: {e}"


def gate_git(root: Path, strict: bool = False) -> GateResult:
    """Gate A: Verify git working tree is clean."""
    t0 = time.monotonic()

    # Check if git repo
    rc, out, err = _run(["git", "rev-parse", "--git-dir"], root, timeout=5)
    if rc != 0:
        return GateResult("git", "SKIP", "Not a git repository", duration_s=time.monotonic() - t0)

    # Get working tree status
    rc, out, _ = _run(["git", "status", "--porcelain"], root, timeout=10)
    lines = [l for l in out.splitlines() if l.strip()]

    # Separate tracked-modified from untracked
    modified  = [l for l in lines if not l.startswith("??")]
    untracked = [l for l in lines if l.startswith("??")]

    dur = time.monotonic() - t0

    if not modified and not untracked:
        return GateResult("git", "PASS", "Working tree clean", duration_s=dur)

    if modified:
        detail = "\n".join(modified[:10])
        return GateResult(
            "git", "FAIL",
            f"{len(modified)} tracked file(s) modified/staged",
            detail=detail,
            duration_s=dur,
            recovery="commit",
        )

    if strict and untracked:
        detail = "\n".join(untracked[:10])
        return GateResult("git", "WARN", f"{len(untracked)} untracked file(s)", detail=detail, duration_s=dur)

    return GateResult("git", "PASS",
                      f"Clean (+ {len(untracked)} untracked, non-blocking)",
                      duration_s=dur)


def gate_build(root: Path, detector: ProjectDetector) -> GateResult:
    """Gate B: Build / compile validation."""
    t0 = time.monotonic()
    cmd = detector.build_command()

    if cmd is None:
        return GateResult("build", "SKIP",
                          f"No build command for '{detector.detect()}' project",
                          duration_s=time.monotonic() - t0)

    rc, stdout, stderr = _run(cmd, root, timeout=120)
    dur = time.monotonic() - t0

    if rc == 0:
        return GateResult("build", "PASS", f"Build succeeded ({cmd[0]})", duration_s=dur)

    # Build failed
    err_preview = (stderr or stdout)[:500].strip()
    return GateResult(
        "build", "FAIL",
        f"Build failed (exit {rc})",
        detail=err_preview,
        duration_s=dur,
        recovery="opencode",
    )


def gate_tests(root: Path, detector: ProjectDetector) -> GateResult:
    """Gate C: Fast unit test check (no E2E, 60s timeout)."""
    t0 = time.monotonic()
    cmd = detector.test_command()

    if cmd is None:
        return GateResult("tests", "SKIP",
                          f"No test runner for '{detector.detect()}' project",
                          duration_s=time.monotonic() - t0)

    rc, stdout, stderr = _run(cmd, root, timeout=90)
    dur = time.monotonic() - t0

    if rc == 0:
        # Extract test count if available
        summary = ""
        for line in (stdout + stderr).splitlines():
            if any(k in line.lower() for k in ("passed", "failed", "test suite", "tests:")):
                summary = line.strip()
                break
        return GateResult("tests", "PASS", f"Tests passed{' — ' + summary if summary else ''}", duration_s=dur)

    out_preview = (stdout + stderr)[:500].strip()
    return GateResult(
        "tests", "FAIL",
        f"Tests failed (exit {rc})",
        detail=out_preview,
        duration_s=dur,
        recovery="debugger",
    )


def gate_deps(root: Path, detector: ProjectDetector) -> GateResult:
    """Gate D: Dependency integrity — lockfile vs installed."""
    t0 = time.monotonic()
    ptype = detector.detect()

    if ptype == "node":
        # Check node_modules exists
        if not (root / "node_modules").exists():
            return GateResult("deps", "FAIL", "node_modules missing — run `npm install`",
                              duration_s=time.monotonic() - t0, recovery="install")
        rc, out, err = _run(["npm", "ls", "--depth=0"], root, timeout=30)
        dur = time.monotonic() - t0
        if rc == 0:
            return GateResult("deps", "PASS", "All Node dependencies satisfied", duration_s=dur)
        # Parse missing packages from npm ls output
        missing = [l for l in (out + err).splitlines() if "UNMET" in l or "missing" in l.lower()]
        return GateResult("deps", "FAIL",
                          f"{len(missing)} dependency issue(s)",
                          detail="\n".join(missing[:10]),
                          duration_s=dur,
                          recovery="install")

    if ptype == "python":
        req_file = root / "requirements.txt"
        if not req_file.exists():
            return GateResult("deps", "SKIP", "No requirements.txt found",
                              duration_s=time.monotonic() - t0)
        # Use pip check for installed consistency
        rc, out, err = _run([sys.executable, "-m", "pip", "check"], root, timeout=30)
        dur = time.monotonic() - t0
        if rc == 0:
            return GateResult("deps", "PASS", "Python dependencies consistent", duration_s=dur)
        return GateResult("deps", "FAIL",
                          "Dependency conflicts detected",
                          detail=(out + err)[:500],
                          duration_s=dur,
                          recovery="install")

    return GateResult("deps", "SKIP", f"No dependency check for '{ptype}' project",
                      duration_s=time.monotonic() - t0)


# ─── Runner ───────────────────────────────────────────────────────────────────

class PreFlightRunner:
    """Orchestrates all gates, produces report, writes JSON artifact."""

    MEMORY_DIR = Path(".agent/memory")
    OUTPUT_FILE = MEMORY_DIR / "last_preflight.json"

    def __init__(self, root: Path, strict: bool = False, gate_filter: Optional[str] = None):
        self.root = root
        self.strict = strict
        self.gate_filter = gate_filter
        self.detector = ProjectDetector(root)

    def run(self) -> PreFlightReport:
        ptype = self.detector.detect()
        report = PreFlightReport(
            project_path=str(self.root),
            project_type=ptype,
            timestamp=datetime.now().isoformat(),
        )

        _header(f"🛡️  PRE-FLIGHT VALIDATION — {self.root.name}")
        print(f"{C.DIM}  Project type : {ptype}{C.RESET}")
        print(f"{C.DIM}  Strict mode  : {'ON' if self.strict else 'OFF'}{C.RESET}")
        print(f"{C.DIM}  Gate filter  : {self.gate_filter or 'all'}{C.RESET}\n")

        t_start = time.monotonic()

        gate_map = {
            "git":   lambda: gate_git(self.root, self.strict),
            "build": lambda: gate_build(self.root, self.detector),
            "tests": lambda: gate_tests(self.root, self.detector),
            "deps":  lambda: gate_deps(self.root, self.detector),
        }

        for name, fn in gate_map.items():
            if self.gate_filter and self.gate_filter != name:
                continue
            result = fn()
            report.gates.append(result)
            self._print_gate(result)

        report.total_duration_s = time.monotonic() - t_start

        self._print_summary(report)
        self._write_json(report)

        return report

    def _print_gate(self, r: GateResult) -> None:
        status_str = f"{r.color}{C.BOLD}{r.status}{C.RESET}"
        dur_str = f"{C.DIM}({r.duration_s:.1f}s){C.RESET}"
        print(f"  {r.icon} Gate [{r.gate.upper():5s}]  {status_str}  {r.message}  {dur_str}")
        if r.detail:
            for line in r.detail.splitlines()[:5]:
                print(f"         {C.DIM}{line}{C.RESET}")

    def _print_summary(self, report: PreFlightReport) -> None:
        print(f"\n{_bar()}")
        total = len(report.gates)
        passed  = sum(1 for g in report.gates if g.status == "PASS")
        failed  = sum(1 for g in report.gates if g.status == "FAIL")
        skipped = sum(1 for g in report.gates if g.status == "SKIP")
        warned  = sum(1 for g in report.gates if g.status == "WARN")

        print(f"  {C.BOLD}RESULT{C.RESET}  "
              f"{C.GREEN}✅ {passed} PASS{C.RESET}  "
              f"{C.RED}❌ {failed} FAIL{C.RESET}  "
              f"{C.DIM}⏭️  {skipped} SKIP{C.RESET}  "
              f"{C.YELLOW}⚠️  {warned} WARN{C.RESET}  "
              f"{C.DIM}({report.total_duration_s:.1f}s total){C.RESET}")

        if report.passed:
            print(f"\n  {C.GREEN}{C.BOLD}🟢 ENVIRONMENT IS CLEAN — OK to proceed.{C.RESET}")
        else:
            failed_gates = [g.gate for g in report.gates if g.status == "FAIL"]
            print(f"\n  {C.RED}{C.BOLD}🔴 ENVIRONMENT IS BROKEN — STOP. Fix: {', '.join(failed_gates)}{C.RESET}")
            for g in report.gates:
                if g.recovery:
                    rec = {
                        "opencode": f"opencode run \"Fix build error: {g.detail[:100]}\"",
                        "install":  "npm install  /  pip install -r requirements.txt",
                        "commit":   "git stash  /  git commit -am 'wip'",
                        "debugger": "Activate @debugger agent to diagnose test failures",
                    }.get(g.recovery, g.recovery)
                    print(f"    {C.YELLOW}→ Recovery [{g.gate}]: {rec}{C.RESET}")
        print(_bar())

    def _write_json(self, report: PreFlightReport) -> None:
        try:
            out_path = self.root / self.OUTPUT_FILE
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
            print(f"\n  {C.DIM}📄 Report saved → {self.OUTPUT_FILE}{C.RESET}")
        except Exception as e:
            print(f"  {C.YELLOW}⚠️  Could not write JSON report: {e}{C.RESET}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="pre_flight",
        description="Pre-Flight Validation Gate — Antigravity Agent Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .agent/scripts/pre_flight.py                   Run all gates
  python .agent/scripts/pre_flight.py --gate git        Git check only
  python .agent/scripts/pre_flight.py --json            JSON output only
  python .agent/scripts/pre_flight.py --strict          Fail on warnings
        """,
    )
    parser.add_argument(
        "project", nargs="?", default=".",
        help="Project root path (default: current directory)"
    )
    parser.add_argument(
        "--gate", choices=["git", "build", "tests", "deps"],
        help="Run a single gate only"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_only",
        help="Print JSON report to stdout (suppresses colored output)"
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as failures"
    )

    args = parser.parse_args()
    root = Path(args.project).resolve()

    if not root.exists():
        print(f"❌ Project path not found: {root}", file=sys.stderr)
        return 1

    if args.json_only:
        # Silent run, just print JSON
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            runner = PreFlightRunner(root, strict=args.strict, gate_filter=args.gate)
            report = runner.run()
        print(json.dumps(report.to_dict(), indent=2))
        return report.exit_code

    runner = PreFlightRunner(root, strict=args.strict, gate_filter=args.gate)
    report = runner.run()
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())

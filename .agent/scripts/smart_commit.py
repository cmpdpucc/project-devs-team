#!/usr/bin/env python3
"""
Smart Commit Protocol — Antigravity Agent Framework
=====================================================

Account-agnostic atomic commit workflow with Conventional Commits format.
Never hardcodes user/email/token — reads everything from git config and gh CLI.

Usage:
    python .agent/scripts/smart_commit.py "message"
    python .agent/scripts/smart_commit.py "message" --type feat --scope memory
    python .agent/scripts/smart_commit.py --from-plan --push
    python .agent/scripts/smart_commit.py --create-remote --push --all
    python .agent/scripts/smart_commit.py --status

Conventional Commit types:
    feat     New feature
    fix      Bug fix
    docs     Documentation only
    refactor Code change that is neither fix nor feature
    test     Adding/fixing tests
    chore    Build, CI, tooling, config
    perf     Performance improvement

Author: Antigravity Self-Enhancement v4
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# Force UTF-8 encoding on Windows (supports emojis)
if sys.platform == "win32":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')



# ─── ANSI colors ──────────────────────────────────────────────────────────────

class C:
    _on = sys.stdout.isatty()
    BOLD  = "\033[1m"  if _on else ""
    RESET = "\033[0m"  if _on else ""
    GREEN = "\033[92m" if _on else ""
    YELLOW= "\033[93m" if _on else ""
    RED   = "\033[91m" if _on else ""
    CYAN  = "\033[96m" if _on else ""
    DIM   = "\033[2m"  if _on else ""

def ok(msg: str)  -> None: print(f"{C.GREEN}✅ {msg}{C.RESET}")
def warn(msg: str)-> None: print(f"{C.YELLOW}⚠️  {msg}{C.RESET}")
def err(msg: str) -> None: print(f"{C.RED}❌ {msg}{C.RESET}", file=sys.stderr)
def info(msg: str)-> None: print(f"{C.CYAN}🔄 {msg}{C.RESET}")
def dim(msg: str) -> None: print(f"{C.DIM}   {msg}{C.RESET}")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _run(
    cmd: list[str],
    cwd: Optional[Path] = None,
    capture: bool = True,
    check: bool = False,
) -> tuple[int, str, str]:
    """Run a subprocess. Returns (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            cwd=cwd or Path.cwd(),
        )
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        return 127, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, "", str(e)


def _run_check(cmd: list[str], cwd: Optional[Path] = None) -> str:
    """Run command and return stdout, raise on failure."""
    rc, out, stderr = _run(cmd, cwd)
    if rc != 0:
        raise RuntimeError(f"`{' '.join(cmd)}` failed (exit {rc}): {stderr}")
    return out


# ─── GitContext ────────────────────────────────────────────────────────────────

@dataclass
class GitContext:
    """
    Reads git repository state without hardcoding any user/email/token.
    Everything comes from git config or environment variables.
    """
    root: Path

    def is_repo(self) -> bool:
        rc, _, _ = _run(["git", "rev-parse", "--git-dir"], self.root)
        return rc == 0

    def init(self) -> None:
        """Initialize git repo if not already initialized."""
        if self.is_repo():
            info("Git repository already initialized.")
            return
        info("Initializing git repository...")
        _run_check(["git", "init", "-b", "main"], self.root)
        ok("git init complete (branch: main)")

    def current_branch(self) -> str:
        rc, out, _ = _run(["git", "branch", "--show-current"], self.root)
        return out or "main"

    def has_remote(self, name: str = "origin") -> bool:
        rc, out, _ = _run(["git", "remote"], self.root)
        return name in out.splitlines()

    def remote_url(self, name: str = "origin") -> Optional[str]:
        rc, out, _ = _run(["git", "remote", "get-url", name], self.root)
        return out if rc == 0 else None

    def dirty_files(self) -> list[str]:
        """Returns list of modified/untracked files."""
        rc, out, _ = _run(["git", "status", "--porcelain"], self.root)
        return [l.strip() for l in out.splitlines() if l.strip()]

    def staged_files(self) -> list[str]:
        rc, out, _ = _run(["git", "diff", "--cached", "--name-only"], self.root)
        return [l for l in out.splitlines() if l]

    def user_name(self) -> str:
        """Read from env or git config — never hardcoded."""
        return (
            os.environ.get("GIT_AUTHOR_NAME")
            or _run(["git", "config", "user.name"], self.root)[1]
            or "Unknown"
        )

    def user_email(self) -> str:
        """Read from env or git config — never hardcoded."""
        return (
            os.environ.get("GIT_AUTHOR_EMAIL")
            or _run(["git", "config", "user.email"], self.root)[1]
            or ""
        )

    def last_commit_hash(self) -> Optional[str]:
        rc, out, _ = _run(["git", "rev-parse", "--short", "HEAD"], self.root)
        return out if rc == 0 else None

    def status_summary(self) -> dict:
        dirty = self.dirty_files()
        staged = self.staged_files()
        return {
            "is_repo": self.is_repo(),
            "branch": self.current_branch(),
            "has_remote": self.has_remote(),
            "remote_url": self.remote_url(),
            "dirty_count": len(dirty),
            "staged_count": len(staged),
            "user": self.user_name(),
            "email": self.user_email(),
            "last_commit": self.last_commit_hash(),
        }


# ─── CommitGenerator ──────────────────────────────────────────────────────────

VALID_TYPES = {"feat", "fix", "docs", "refactor", "test", "chore", "perf", "style", "ci", "build"}

@dataclass
class CommitGenerator:
    """
    Generates Conventional Commit messages.
    Can parse last completed task from ralph_plan.md for auto-messages.
    """
    root: Path

    def build(
        self,
        message: str,
        commit_type: str = "chore",
        scope: Optional[str] = None,
        breaking: bool = False,
    ) -> str:
        """Build a formatted Conventional Commit message."""
        if commit_type not in VALID_TYPES:
            warn(f"Unknown type '{commit_type}', defaulting to 'chore'")
            commit_type = "chore"

        scope_part = f"({scope})" if scope else ""
        breaking_part = "!" if breaking else ""
        header = f"{commit_type}{scope_part}{breaking_part}: {message}"

        # Enforce 72-char limit on header
        if len(header) > 72:
            header = header[:69] + "..."

        return header

    def from_plan(self) -> tuple[str, str, Optional[str]]:
        """
        Read last completed task from ralph_plan.md.
        Returns (message, type, scope).
        """
        plan_path = self.root / "ralph_plan.md"
        if not plan_path.exists():
            return "update agent framework", "chore", None

        content = plan_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Find last [x] task line
        last_done = None
        for line in lines:
            if re.match(r"\s*-\s*\[x\]", line, re.IGNORECASE):
                last_done = line

        if not last_done:
            return "update agent framework", "chore", None

        # Extract task description
        match = re.sub(r"\s*-\s*\[x\]\s*", "", last_done).strip()
        # Remove markdown code backticks
        match = re.sub(r"`([^`]+)`", r"\1", match)
        # Truncate to 50 chars max for message
        msg = match[:50].strip()

        # Infer type from content
        ctype = "chore"
        if any(w in msg.lower() for w in ["creare", "add", "create", "nuov", "new"]):
            ctype = "feat"
        elif any(w in msg.lower() for w in ["fix", "correg", "risolv"]):
            ctype = "fix"
        elif any(w in msg.lower() for w in ["test", "verif"]):
            ctype = "test"
        elif any(w in msg.lower() for w in ["doc", "readme", "rule", "regola"]):
            ctype = "docs"
        elif any(w in msg.lower() for w in ["refactor", "rifattorizza", "restrut"]):
            ctype = "refactor"

        # Infer scope from path/content
        scope = None
        path_match = re.search(r"\.agent/(rules|scripts|workflows|memory|skills)/(\w[\w-]*)", msg)
        if path_match:
            scope = path_match.group(2).replace("-", "_")

        return msg, ctype, scope


# ─── RepoManager ──────────────────────────────────────────────────────────────

@dataclass
class RepoManager:
    """
    Manages GitHub repository creation.
    Account-agnostic: reads current gh CLI authenticated user.
    Never hardcodes owner, token, or credentials.
    """
    root: Path
    ctx: GitContext

    def gh_current_user(self) -> Optional[str]:
        """Get currently authenticated GitHub user from gh CLI."""
        rc, out, _ = _run(["gh", "auth", "status", "--json", "loggedInUser"], self.root)
        if rc == 0:
            try:
                data = json.loads(out)
                # gh auth status --json varies by version
                if isinstance(data, list) and data:
                    return data[0].get("user", {}).get("login")
                return data.get("user", {}).get("login")
            except json.JSONDecodeError:
                pass

        # Fallback: parse plain text output
        rc, out, _ = _run(["gh", "api", "user", "--jq", ".login"], self.root)
        if rc == 0 and out:
            return out.strip()

        return None

    def repo_exists_remote(self, owner: str, name: str) -> bool:
        rc, _, _ = _run(["gh", "repo", "view", f"{owner}/{name}"], self.root)
        return rc == 0

    def create_remote(
        self,
        repo_name: str,
        description: str = "",
        private: bool = False,
        push: bool = False,
    ) -> str:
        """
        Create GitHub repository under the currently authenticated user.
        Returns the remote URL.
        """
        owner = self.gh_current_user()
        if not owner:
            raise RuntimeError(
                "Cannot determine GitHub user. Run `gh auth login` first."
            )

        info(f"GitHub user detected: {C.BOLD}{owner}{C.RESET}")

        if self.repo_exists_remote(owner, repo_name):
            remote_url = f"https://github.com/{owner}/{repo_name}.git"
            warn(f"Repo already exists: {remote_url}")
            return remote_url

        info(f"Creating GitHub repo: {owner}/{repo_name} ({'private' if private else 'public'})...")

        cmd = [
            "gh", "repo", "create", repo_name,
            "--description", description or f"Antigravity Agent Framework — {repo_name}",
        ]
        if private:
            cmd.append("--private")
        else:
            cmd.append("--public")

        # Do NOT use --source or --push here — we want manual control over commits
        rc, out, stderr = _run(cmd, self.root)
        if rc != 0:
            raise RuntimeError(f"gh repo create failed: {stderr}")

        remote_url = f"https://github.com/{owner}/{repo_name}.git"
        ok(f"Repository created: {C.CYAN}https://github.com/{owner}/{repo_name}{C.RESET}")
        return remote_url

    def add_remote(self, url: str, name: str = "origin") -> None:
        """Add or update git remote."""
        if self.ctx.has_remote(name):
            existing = self.ctx.remote_url(name)
            if existing == url:
                dim(f"Remote '{name}' already set to {url}")
                return
            info(f"Updating remote '{name}' to {url}")
            _run_check(["git", "remote", "set-url", name, url], self.root)
        else:
            info(f"Setting remote '{name}' → {url}")
            _run_check(["git", "remote", "add", name, url], self.root)
        ok(f"Remote '{name}' configured.")


# ─── CommitRunner ──────────────────────────────────────────────────────────────

@dataclass
class CommitRunner:
    """
    Executes git add → commit → push with retry logic.
    Retry on network errors (push), not on commit errors.
    """
    root: Path
    ctx: GitContext
    max_retries: int = 3

    def stage(self, mode: str = "all", files: Optional[list[str]] = None) -> int:
        """Stage files. mode: 'all' | 'staged' | 'files'"""
        if mode == "all":
            _run_check(["git", "add", "-A"], self.root)
            staged = self.ctx.staged_files()
            info(f"Staged {len(staged)} file(s)")
            return len(staged)
        elif mode == "files" and files:
            for f in files:
                _run_check(["git", "add", f], self.root)
            info(f"Staged {len(files)} specific file(s)")
            return len(files)
        elif mode == "staged":
            staged = self.ctx.staged_files()
            if not staged:
                warn("Nothing staged. Use --all or stage files manually.")
            return len(staged)
        return 0

    def commit(self, message: str) -> str:
        """Create commit. Returns short hash."""
        staged = self.ctx.staged_files()
        if not staged:
            raise RuntimeError("Nothing to commit — working tree clean or nothing staged.")

        info(f"Committing: {C.BOLD}{message}{C.RESET}")
        _run_check(["git", "commit", "-m", message], self.root)
        commit_hash = self.ctx.last_commit_hash() or "?"
        ok(f"Commit created: {C.DIM}{commit_hash}{C.RESET} — {message}")
        return commit_hash

    def push(self, branch: Optional[str] = None, set_upstream: bool = True) -> None:
        """Push to remote with retry on network failures."""
        if not self.ctx.has_remote():
            raise RuntimeError("No remote configured. Use --create-remote first.")

        branch = branch or self.ctx.current_branch()
        cmd = ["git", "push"]
        if set_upstream:
            cmd += ["-u", "origin", branch]

        for attempt in range(1, self.max_retries + 1):
            info(f"Pushing to origin/{branch}... (attempt {attempt}/{self.max_retries})")
            rc, out, stderr = _run(cmd, self.root)

            if rc == 0:
                ok(f"Pushed to origin/{branch}")
                return

            # Classify error
            if any(e in stderr for e in ["Authentication", "403", "Permission"]):
                raise RuntimeError(f"Auth error — run `gh auth refresh`: {stderr[:200]}")
            if any(e in stderr for e in ["Could not resolve host", "timeout", "ETIMEDOUT"]):
                if attempt < self.max_retries:
                    delay = 2 ** attempt
                    warn(f"Network error. Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Push failed after {self.max_retries} attempts (network): {stderr[:200]}")

            raise RuntimeError(f"Push failed (exit {rc}): {stderr[:300]}")


# ─── Main Orchestrator ────────────────────────────────────────────────────────

class SmartCommit:
    def __init__(self, root: Path):
        self.root = root
        self.ctx = GitContext(root)
        self.gen = CommitGenerator(root)
        self.runner = CommitRunner(root, self.ctx)
        self.repo_mgr = RepoManager(root, self.ctx)

    def run(self, args: argparse.Namespace) -> int:
        print(f"\n{C.BOLD}{C.CYAN}{'─'*54}{C.RESET}")
        print(f"{C.BOLD}{C.CYAN}  🎯 SMART COMMIT PROTOCOL{C.RESET}")
        print(f"{C.BOLD}{C.CYAN}{'─'*54}{C.RESET}\n")

        # ── Status only ───────────────────────────────────────
        if args.status:
            status = self.ctx.status_summary()
            print(json.dumps(status, indent=2))
            return 0

        try:
            # ── Step 1: Ensure git repo ──────────────────────
            self.ctx.init()

            # ── Step 2: Create remote if requested ──────────
            if args.create_remote:
                repo_name = args.repo_name or self.root.name
                url = self.repo_mgr.create_remote(
                    repo_name=repo_name,
                    description=args.description,
                    private=args.private,
                )
                self.repo_mgr.add_remote(url)

            # ── Step 3: Build commit message ─────────────────
            if args.from_plan:
                msg_text, ctype, scope = self.gen.from_plan()
                if not args.message:
                    args.message = msg_text
                if not args.type:
                    args.type = ctype
                if not args.scope:
                    args.scope = scope
                dim(f"Auto-detected from plan: [{args.type}]({args.scope}) {args.message}")

            if not args.message:
                err("No commit message. Provide one or use --from-plan.")
                return 1

            full_message = self.gen.build(
                message=args.message,
                commit_type=args.type or "chore",
                scope=args.scope,
                breaking=args.breaking,
            )

            # ── Step 4: Stage ────────────────────────────────
            mode = "staged"
            files = None
            if args.all:
                mode = "all"
            elif args.files:
                mode = "files"
                files = args.files

            n = self.runner.stage(mode=mode, files=files)
            if n == 0 and mode != "staged":
                warn("Nothing to stage.")
                return 0

            # ── Step 5: Commit ───────────────────────────────
            self.runner.commit(full_message)

            # ── Step 6: Push ─────────────────────────────────
            if args.push:
                self.runner.push(set_upstream=args.create_remote or not self.ctx.has_remote())

            print(f"\n{C.GREEN}{C.BOLD}  ✨ Done!{C.RESET}\n")
            return 0

        except RuntimeError as e:
            err(str(e))
            return 1
        except KeyboardInterrupt:
            warn("\nInterrupted.")
            return 130


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="smart_commit",
        description="Smart Commit Protocol — account-agnostic Conventional Commits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .agent/scripts/smart_commit.py "add error recovery rule" --type feat --scope rules --push
  python .agent/scripts/smart_commit.py --from-plan --all --push
  python .agent/scripts/smart_commit.py "initial commit" --create-remote --all --push
  python .agent/scripts/smart_commit.py --status
        """,
    )

    # Message
    parser.add_argument("message", nargs="?", default=None, help="Commit message body")
    parser.add_argument("--type", "-t",
                        choices=sorted(VALID_TYPES), default=None,
                        help="Conventional commit type (default: chore)")
    parser.add_argument("--scope", "-s", default=None,
                        help="Commit scope, e.g. 'memory', 'rules', 'scripts'")
    parser.add_argument("--breaking", action="store_true",
                        help="Mark as breaking change (adds '!' to header)")

    # Staging
    staging = parser.add_mutually_exclusive_group()
    staging.add_argument("--all", "-a", action="store_true",
                         help="Stage all changes (git add -A)")
    staging.add_argument("--files", nargs="+", metavar="FILE",
                         help="Stage specific files")
    staging.add_argument("--staged", action="store_true",
                         help="Commit what is already staged (default)")

    # Remote
    parser.add_argument("--push", "-p", action="store_true",
                        help="Push after commit")
    parser.add_argument("--create-remote", action="store_true",
                        help="Create GitHub repo and set remote before committing")
    parser.add_argument("--repo-name", default=None,
                        help="Repository name (default: current directory name)")
    parser.add_argument("--description", default="",
                        help="GitHub repo description")
    parser.add_argument("--private", action="store_true",
                        help="Create private repository (default: public)")

    # Automation
    parser.add_argument("--from-plan", action="store_true",
                        help="Auto-generate message from last [x] in ralph_plan.md")
    parser.add_argument("--status", action="store_true",
                        help="Print repository status as JSON and exit")

    # Project root
    parser.add_argument("--root", default=".", help="Project root (default: cwd)")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    sc = SmartCommit(root)
    return sc.run(args)


if __name__ == "__main__":
    sys.exit(main())

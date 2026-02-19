#!/usr/bin/env python3
"""
Master Checklist Runner - Antigravity Kit
==========================================

Orchestrates all validation scripts in priority order.
Use this for incremental validation during development.

Usage:
    python scripts/checklist.py .                    # Run core checks
    python scripts/checklist.py . --url <URL>        # Include performance checks

Priority Order:
    P0: Security Scan (vulnerabilities, secrets)
    P1: Lint & Type Check (code quality)
    P2: Schema Validation (if database exists)
    P3: Test Runner (unit/integration tests)
    P4: UX Audit (psychology laws, accessibility)
    P5: SEO Check (meta tags, structure)
    P6: Performance (lighthouse - requires URL)
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# ANSI colors for terminal output
import concurrent.futures
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# ... (Colors and print functions remain same, omitted for brevity if unchanged, but I need to include imports if I change top of file.
# The previous `replace_file_content` context shows imports at top. I will replace from imports down to main loop.)

# To avoid replacing the whole file and dealing with large context, I'll modify imports first, then the main execution logic.
# Wait, let's just replace the whole main function and imports.

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

# Define priority-ordered checks
CORE_CHECKS = [
    ("Security Scan", ".agent/skills/vulnerability-scanner/scripts/security_scan.py", True),
    ("Lint Check", ".agent/skills/lint-and-validate/scripts/lint_runner.py", True),
    ("Schema Validation", ".agent/skills/database-design/scripts/schema_validator.py", False),
    ("Test Runner", ".agent/skills/testing-patterns/scripts/test_runner.py", False),
    ("UX Audit", ".agent/skills/frontend-design/scripts/ux_audit.py", False),
    ("SEO Check", ".agent/skills/seo-fundamentals/scripts/seo_checker.py", False),
]

PERFORMANCE_CHECKS = [
    ("Lighthouse Audit", ".agent/skills/performance-profiling/scripts/lighthouse_audit.py", True),
    ("Playwright E2E", ".agent/skills/webapp-testing/scripts/playwright_runner.py", False),
]

def check_script_exists(script_path: Path) -> bool:
    """Check if script file exists"""
    return script_path.exists() and script_path.is_file()

def run_script(name: str, script_path: Path, project_path: str, url: Optional[str] = None) -> dict:
    """
    Run a validation script and capture results
    """
    if not check_script_exists(script_path):
        return {"name": name, "passed": True, "output": "", "skipped": True, "warning": f"Script not found: {script_path}"}
    
    # Build command
    cmd = ["python", str(script_path), project_path]
    if url and ("lighthouse" in script_path.name.lower() or "playwright" in script_path.name.lower()):
        cmd.append(url)
    
    # Run script
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        passed = result.returncode == 0
        
        return {
            "name": name,
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr,
            "skipped": False
        }
    
    except subprocess.TimeoutExpired:
        return {"name": name, "passed": False, "output": "", "error": "Timeout", "skipped": False}
    
    except Exception as e:
        return {"name": name, "passed": False, "output": "", "error": str(e), "skipped": False}

def print_result(result: dict):
    """Print result immediately"""
    name = result["name"]
    if result.get("skipped"):
        print_warning(f"{name}: Skipped ({result.get('warning', 'Unknown reason')})")
        return

    if result["passed"]:
        print_success(f"{name}: PASSED")
    else:
        print_error(f"{name}: FAILED")
        if result.get("error"):
            print(f"  Error: {result['error'][:200]}")

def print_summary(results: List[dict]):
    """Print final summary report"""
    print_header("📊 CHECKLIST SUMMARY")
    
    passed_count = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed_count = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped_count = sum(1 for r in results if r.get("skipped"))
    
    print(f"Total Checks: {len(results)}")
    print(f"{Colors.GREEN}✅ Passed: {passed_count}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Failed: {failed_count}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Skipped: {skipped_count}{Colors.ENDC}")
    print()
    
    # Detailed results
    for r in results:
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        print(f"{status} {r['name']}")
    
    print()
    
    if failed_count > 0:
        print_error(f"{failed_count} check(s) FAILED - Please fix before proceeding")
        return False
    else:
        print_success("All checks PASSED ✨")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Run Antigravity Kit validation checklist",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project", help="Project path to validate")
    parser.add_argument("--url", help="URL for performance checks (lighthouse, playwright)")
    parser.add_argument("--skip-performance", action="store_true", help="Skip performance checks even if URL provided")
    
    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        sys.exit(1)
    
    print_header("🚀 ANTIGRAVITY KIT - MASTER CHECKLIST")
    print(f"Project: {project_path}")
    print(f"URL: {args.url if args.url else 'Not provided (performance checks skipped)'}")
    print(f"Mode: Parallel Execution ⚡")
    
    results = []
    
    # Run core checks in parallel
    print_header("📋 CORE CHECKS (Parallel)")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_check = {}
        for name, script_path, required in CORE_CHECKS:
            script = project_path / script_path
            print_step(f"Scheduled: {name}")
            future = executor.submit(run_script, name, script, str(project_path))
            future_to_check[future] = (name, required)
            
        for future in concurrent.futures.as_completed(future_to_check):
            name, required = future_to_check[future]
            try:
                result = future.result()
                results.append(result)
                print_result(result)
            except Exception as e:
                print_error(f"{name}: Exception - {e}")
                results.append({"name": name, "passed": False, "error": str(e)})

    # Verify required checks
    failed_required = [r for r in results if not r["passed"] and not r.get("skipped") and any(c[0] == r["name"] and c[2] for c in CORE_CHECKS)]
    
    if failed_required:
         print_error(f"CRITICAL: {len(failed_required)} required checks failed. Stopping checklist.")
         print_summary(results)
         sys.exit(1)
    
    # Run performance checks (Sequential as they might compete for browser/resources)
    if args.url and not args.skip_performance:
        print_header("⚡ PERFORMANCE CHECKS (Sequential)")
        for name, script_path, required in PERFORMANCE_CHECKS:
            script = project_path / script_path
            print_step(f"Running: {name}")
            result = run_script(name, script, str(project_path), args.url)
            results.append(result)
            print_result(result)
    
    # Print summary
    all_passed = print_summary(results)
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()

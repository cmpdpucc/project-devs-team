# PLAN-audit-remediation

## Overview
Remediate findings from `docs/AUDIT_REPORT.md` (Security & Performance Audit). This plan covers fixing critical shell injection vulnerabilities, securing file operations, and optimizing scanning scripts for performance.

## Project Type
**Security & Performance Refactoring** (Python Scripts)

## Success Criteria
1.  **Critical Fix**: `auto_preview.py` uses `shell=False` and `shlex`.
2.  **Security Fix**: `antigravity-opencode-bridge.py` restricts file modifications to project scope and uses configurable ports.
3.  **Performance Fix**: `security_scan.py` completes in a single file pass ($O(N)$).
4.  **Efficiency**: `checklist.py` runs checks in parallel.
5.  **Verification**: Security scan passes with 0 critical issues; bridge script validates without errors.

## Tech Stack
-   **Python**: Core scripting language.
-   **Libraries**: `subprocess`, `shlex`, `os`, `asyncio` / `concurrent.futures`.

## File Structure
```
.agent/
├── scripts/
│   ├── auto_preview.py           # [MODIFY] remove shell=True
│   ├── check_list.py             # [MODIFY] parallel execution
│   └── verify_all.py             # [MODIFY] parallel execution
└── skills/
    └── vulnerability-scanner/
        └── scripts/
            └── security_scan.py  # [REFACTOR] single-pass scan
scripts/
└── antigravity-opencode-bridge.py # [MODIFY] secure file ops & ports
```

## User Review Required
> [!IMPORTANT]
> **Bridge Script Change**: The bridge script will stop modifying global user config (e.g. `%APPDATA%`) without explicit confirmation or flags. This is a behavior change.

## Task Breakdown

### Phase 1: Security Remediation (Agent: `security-auditor`)
- [ ] **Fix `auto_preview.py`**
    -   Replace `shell=True` with `subprocess.Popen(shlex.split(command), ...)`
    -   Validate input sanitization.
- [ ] **Secure `antigravity-opencode-bridge.py`**
    -   Remove modification of global user paths unless `--global` flag is used.
    -   Replace hardcoded `4096` with `os.getenv('OPENCODE_PORT', '4096')`.

### Phase 2: Performance Optimization (Agent: `performance-optimizer`)
- [ ] **Refactor `security_scan.py`**
    -   Implement single `os.walk` loop.
    -   Route file content to `check_secrets`, `check_patterns`, `check_config` based on extension.
    -   Combine regexes where possible.
- [ ] **Parallelize `checklist.py`**
    -   Use `concurrent.futures.ThreadPoolExecutor` to run P0/P1 checks concurrently.

### Phase 3: Verification (Agent: `test-engineer`)
- [ ] **Run `verify_all.py`**
    -   Ensure all checks pass (Security scan, linting).
- [ ] **Manual Bridge Test**
    -   Run bridge script and verify it respects new constraints.

## Phase X: Verification Plan
1.  **Security Verify**:
    ```bash
    python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
    # Expected: No Critical vulnerabilities found.
    ```
2.  **Performance Verify**:
    ```bash
    time python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
    # Expected: Execution time < previous run.
    ```

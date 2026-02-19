# AUDIT_PRE_REFACTOR

## System State Analysis
**Date**: 2026-02-16
**Scope**: Process Management, Concurrency, & Environment

### 1. Critical Findings (Blocking)
-   **❌ Missing Executable in PATH**: `opencode` command is not accessible in the current shell session.
    -   **Detection**: `concurrency_test.py` failed with `[WinError 2]`.
    -   **Root Cause**: Global npm bin folder (`C:\Program Files\nodejs`) is in system PATH but not picked up by current python process, or `subprocess` requires full `.cmd` extension on Windows.
    -   **Verified Location**: `C:\Program Files\nodejs\opencode.cmd`.
    -   **Impact**: Any automated workflow relying on `opencode` (Audit, Checklists, Refactor) will fail.

### 2. Architecture Limitations
-   **⚠️ Single-Port Bottleneck**: Current `bridge.py` hardcodes port `4096`.
    -   **Impact**: Cannot run parallel tasks (e.g., Security Audit + Refactor). Attempting to do so results in port conflicts or queued execution.
-   **⚠️ No Process Supervision**:
    -   Processes are spawned via `subprocess.Popen` (bridge) or `subprocess.run` (checklist).
    -   If a server crashes, there is no restart logic.
    -   If the parent process dies, orphan `node.exe` processes may linger (though `tasklist` showed clean state for now).

### 3. Concurrency Review
-   **Current State**: `checklist.py` runs python scripts in parallel.
-   **Target State**: Needs to run **OpenCode** commands in parallel.
-   **Gap**: The bridge script is a singleton. The "4/5 terminals" requirement cannot be met with current `antigravity-opencode-bridge.py`.

### 4. Security & Cleanup
-   **Open Ports**: Port 4096 is currently free.
-   **Zombie Processes**: No immediate zombies found, but lack of PID tracking makes this a future risk.

## Recommendations for Refactor
1.  **Robust Path Resolution**:
    -   `ProcessManager` MUST detect the `npm` prefix and construct the full path to `opencode.cmd` if the bare command fails.
    -   Do not rely on system PATH variable alone.
2.  **Dynamic Port Allocation**:
    -   Implement a pool of ports (4096-4105).
    -   Check port availability before binding.
3.  **Process Lifecycle**:
    -   Implement a `ServerPool` that tracks PIDs.
    -   Ensure `atexit` cleanup to kill child processes.
4.  **Health Checks**:
    -   Verify server health (`/health` endpoint) before dispatching tasks.

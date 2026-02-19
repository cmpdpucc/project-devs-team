# PLAN-refactor-process-manager

## Goal
Establish a robust mechanism to manage multiple concurrent OpenCode instances ("terminals") within Antigravity, enabling parallel execution of tasks like audits, refactoring, and checklist verification without blocking the main thread or user UI.

## Problem
Currently, OpenCode integration is handled ad-hoc:
- `antigravity-opencode-bridge.py` starts a single server on port 4096.
- `checklist.py` uses `subprocess` but doesn't leverage OpenCode's capabilities efficiently.
- No central management for multiple "agents" running in parallel (the "4/5 terminals" requirement).

## Proposed Solution
Introduce a `ProcessManager` (or `AgentOrchestrator`) module in `.agent/scripts/process_manager.py` that:
1.  Manages a **pool** of OpenCode servers (ports 4096-4100).
2.  Provides an API to run commands in specific contexts/sessions.
3.  Handles lifecycle (start, stop, restart, health check).
4.  Supports both synchronous and asynchronous execution.

## File Structure Changes
### New Files
- [NEW] `.agent/scripts/process_manager.py`: Core logic for managing server pool.
- [NEW] `.agent/scripts/opencode_client.py`: Wrapper for OpenCode CLI/API interactions.

### Modified Files
- [MODIFY] `scripts/antigravity-opencode-bridge.py`: Update to use `ProcessManager` for initial server start (or deprecate in favor of manager).
- [MODIFY] `.agent/scripts/checklist.py`: Refactor to use `ProcessManager` for parallel execution if applicable (or ensure it doesn't conflict).

## Detailed Design

### `ProcessManager` Class
```python
class ProcessManager:
    def __init__(self, max_workers=5, start_port=4096):
        self.pool = [] # List of ActiveServer instances
        self.max_workers = max_workers
        self.start_port = start_port
        self.opencode_path = self._resolve_opencode_path()

    def _resolve_opencode_path(self) -> str:
        # 1. Check env var OPENCODE_PATH
        # 2. Check shutil.which("opencode")
        # 3. Check npm prefix + /opencode.cmd (Windows) or /bin/opencode (Unix)
        pass

    def get_server(self) -> ActiveServer:
        # Returns an available server or starts a new one
        pass
```

### `ActiveServer` Class
```python
class ActiveServer:
    def __init__(self, port, executable):
        self.port = port
        self.executable = executable
        self.process = None

    def start(self):
        # Spawns `{self.executable} serve --port {self.port}`
        pass
```

## Task Breakdown
1.  **Core Implementation (`process_manager.py`)**:
    -   Implement `_resolve_opencode_path` (Crucial per Audit).
    -   Implement `ServerPool` logic.
2.  **Client Wrapper (`opencode_client.py`)**:
    -   Implement `run_command(cmd, session_id)`.
3.  **Integration**:
    -   Update `bridge.py` to use `ProcessManager`.
    -   Update `checklist.py`.
4.  **Verification**:
    -   Run `tests/concurrency_test.py` (updated to use Manager).

## Verification Plan
### Automated Tests
- `tests/test_process_manager.py`: Unit tests for pool management.
- `tests/concurrency_test.py`: Integration test verifying 5 parallel `opencode run` commands succeed.

### Manual Verification
- Run `python .agent/scripts/checklist.py` and observe parallel execution logs.

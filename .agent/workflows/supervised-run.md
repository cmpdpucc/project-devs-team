# /supervised-run - Strictly Supervised Parallel Agents

Strict execution mode where the orchestrator process remains active to monitor and supervise all child agent processes.

---

## 🛡️ Supervision Protocol

1.  **Parent Process (Orchestrator)**
    -   Must remain **ACTIVE** (blocked/waiting) for the entire duration.
    -   Must hold references/PIDs to all child processes.
    -   Must monitor child health and restart if necessary (unless one-off task).
    -   Must ensure **CLEAN SHUTDOWN** of all children on exit/interrupt.

2.  **Child Processes (Agents)**
    -   Must be spawned by the Orchestrator.
    -   Should not detach or daemonize.
    -   Should exit if the parent connection is lost (ideal) or be killed by parent.

## Workflow

### 1. Launch Orchestrator
```bash
python tests/demo_orchestrator.py
# OR
python scripts/antigravity-opencode-bridge.py
```

### 2. Monitor Output
The orchestrator terminal will display:
- `🔒 STRICT SUPERVISION ACTIVE`
- Status of child agents.
- Logs from the supervision loop.

### 3. Termination
- Press `Ctrl+C` in the Orchestrator terminal.
- Verify: **All child agent windows/processes close immediately.**

---

## Constraints
- **NO DETACHED MODES**: `server.detach()` is BANNED.
- **NO FIRE-AND-FORGET**: `subprocess.Popen` must be followed by management logic.

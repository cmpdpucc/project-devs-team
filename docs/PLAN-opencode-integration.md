# PLAN-opencode-integration

## Overview
Create a comprehensive development framework that integrates **OpenCode** (AI terminal agent) with **Google Antigravity IDE**. This setup aims to provide an optimal environment for advanced agentic development by combining the synchronous editing capabilities of Antigravity with the asynchronous, headless power of OpenCode.

## Project Type
**Tooling / Framework Integration** (Scripts, Configuration, Documentation)

## Success Criteria
1.  **OpenCode Installed & Configured**: `install-opencode.sh` runs successfully; `opencode.json` is deployed.
2.  **Antigravity Integrated**: `GEMINI.md` rules are unified and synced via `antigravity-opencode-bridge.py`.
3.  **Agent Structure Validated**: `validate-agent-folder.sh` confirms the `.agent` structure (populated manually by user).
4.  **Workflow Established**: `Makefile` enables easy orchestration; documentation explains the integrated workflow.
5.  **Security Enforced**: `.gitignore` and security checklists are in place.

## Tech Stack
- **Shell**: Bash (Installation & Validation scripts)
- **Python**: Bridge script (Context synchronization)
- **JSON**: OpenCode configuration
- **Markdown**: Documentation & Rules
- **Makefile**: Automation

## File Structure
```
.
├── .agent/
│   ├── rules/
│   │   ├── GEMINI.md          # Unified rules
│   │   └── SECURITY_CHECKLIST.md
│   ├── skills/
│   │   └── opencode-integration/SKILL.md
│   ├── agents/                # (Placeholder)
│   ├── workflows/             # (Placeholder)
│   ├── ARCHITECTURE.md        # (Placeholder)
│   └── README.md              # Warning/Placeholder
├── config/
│   └── opencode.json          # OpenCode config
├── docs/
│   ├── OPENCODE_USAGE.md      # Usage guide
│   ├── INTEGRATED_WORKFLOW.md # Workflow guide
│   └── PLAN-opencode-integration.md
├── scripts/
│   ├── install-opencode.sh            # Setup script
│   ├── antigravity-opencode-bridge.py # Sync script
│   └── validate-agent-folder.sh       # Validation script
├── .github/workflows/
│   └── ai-review.yml          # CI/CD integration
├── Makefile                   # Orchestration
├── README.md                  # Main entry point
└── .gitignore                 # Extended gitignore
```

## User Review Required
> [!IMPORTANT]
> **Manual Action Required**: The user has confirmed the `.agent` folder is present at `.agent`. The `validate-agent-folder.sh` script will verify this structure.

> [!NOTE]
> OpenCode installation will use `npm install -g opencode-ai@latest` as the primary cross-platform method, falling back to OS-specific methods if npm is unavailable. Windows users are still recommended to use WSL for optimal terminal experience.

## Task Breakdown

### Phase 1: OpenCode Setup
- [ ] **Create `scripts/install-opencode.sh`**
    - usage: `npm install -g opencode-ai@latest`
    - Setup Truecolor support.
    - Verify terminal (WezTerm, etc).
- [ ] **Create `config/opencode.json`**
    - Define model, permissions, TUI settings, watcher ignore list.
    - Include GEMINI.md and ARCHITECTURE.md instructions.
- [ ] **Create `docs/OPENCODE_USAGE.md`**
    - Document formatting: Commands, Slash commands, Leader Key, CLI automation.

### Phase 2: Antigravity Integration
- [ ] **Create `.agent/rules/GEMINI.md`**
    - Unified version 1.0.
    - Universal rules for File System, Coding Standards.
    - Specific workflows for OpenCode and Antigravity.
    - Security rules.
- [ ] **Create `.agent/skills/opencode-integration/SKILL.md`**
    - define `opencode-integration` skill.
    - Instructions for complex terminal operations, session persistence, CI/CD.
- [ ] **Create `scripts/antigravity-opencode-bridge.py`**
    - `sync_gemini_rules()`: Sync GEMINI.md to OpenCode config.
    - `export_antigravity_lessons()`: Copy LESSONS_LEARNED.md to .agent context.
    - `start_opencode_server()`: Check/Start server on port 4096.

### Phase 3: Agent Structure & Validation
- [ ] **Create `.agent` placeholders**
    - Directories: `rules`, `skills`, `agents`, `workflows`, `scripts`.
    - Placeholder `README.md` with warning.
- [ ] **Create `scripts/validate-agent-folder.sh`**
    - Verify existence of required vars.
    - Count agents and skills.

### Phase 4: Workflow Unification
- [ ] **Create `Makefile`**
    - Targets: `setup`, `sync`, `bridge`, `dev`, `clean`, `help`.
- [ ] **Create `docs/INTEGRATED_WORKFLOW.md`**
    - Document Scenarios: Feature Dev, Legacy Refactoring, CI/CD.
    - Best Practices.

### Phase 5: Security & Compliance
- [ ] **Update `.gitignore`**
    - Add `.antigravity/`, `.opencode/`, secrets, build artifacts.
- [ ] **Create `.agent/rules/SECURITY_CHECKLIST.md`**
    - Pre-Commit, Agent Permissions, Tool-specific checks.

### Phase 6: Final Documentation & CI
- [ ] **Create `README.md`**
    - Quick Start, Architecture, Structure, Workflow, Resources.
- [ ] **Create `.github/workflows/ai-review.yml`**
    - Github Action for AI Code Review on PR.

## Phase X: Verification
### Automated Verification
1.  **Structure Validation**:
    ```bash
    ./scripts/validate-agent-folder.sh
    # Expected: Fail initially, Pass after manual copy
    ```
2.  **Bridge Test**:
    ```bash
    python3 scripts/antigravity-opencode-bridge.py
    # Expected: "Synced GEMINI.md", "OpenCode server already active/started"
    ```
3.  **Makefile Check**:
    ```bash
    make help
    # Expected: List of commands
    ```

### Manual Verification
1.  **Install Check**: Run `./scripts/install-opencode.sh` (or verify logic if in non-compatible env).
2.  **Dev Mode**: Run `make dev` and ensure both environments launch/connect.

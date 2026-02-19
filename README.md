# Framework Integrato Antigravity + OpenCode

## Quick Start

1.  **Setup automatico**
    ```bash
    make setup
    ```

2.  **Avvia ambiente**
    ```bash
    make dev
    ```

## Architettura
-   **OpenCode**: Agente terminale per operazioni massive e CI/CD (installa via npm).
-   **Antigravity**: IDE agent-first per orchestrazione e UI.
-   **Bridge**: Sincronizzazione contesto e lesson learned.

## Struttura
```
├── .agent/           # (Popolato manualmente)
├── config/
│   └── opencode.json
├── docs/
│   ├── OPENCODE_USAGE.md
│   └── INTEGRATED_WORKFLOW.md
├── scripts/
│   ├── install-opencode.sh
│   ├── antigravity-opencode-bridge.py
│   └── validate-agent-folder.sh
├── Makefile
└── README.md
```

## Risorse
-   [OpenCode Usage](docs/OPENCODE_USAGE.md)
-   [Integrated Workflow](docs/INTEGRATED_WORKFLOW.md)

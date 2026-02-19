import os
import requests
import json
import time
import subprocess
from typing import Dict, Any, Optional
from pathlib import Path
from .process_manager import ProcessManager

class OpenCodeClient:
    def __init__(self, port: int = None):
        self.explicit_port = port
        if not port:
            self.manager = ProcessManager()
        else:
            self.manager = None
        self.server = None
        self.session_id = None

    def connect(self):
        """Connect to the OpenCode server."""
        if self.explicit_port:
             # connecting to existing port
             # We create a dummy server object to hold the port
             class RemoteServer:
                 def __init__(self, p): self.port = p
                 def is_healthy(self): return True # Assume healthy or check via API
             self.server = RemoteServer(self.explicit_port)
             return

        if not self.server:
            self.server = self.manager.get_server()
            # Wait for server ready
            max_retries = 15
            for _ in range(max_retries):
                if self.server.is_healthy():
                    break
                time.sleep(1)
            else:
                raise ConnectionError(f"Server on port {self.server.port} is not responding.")

    def execute(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a command on the OpenCode server.
        Uses `opencode run` semantic via subprocess since API isn't fully documented here,
        but leverages the server context if possible.
        
        Currently, `opencode run` talks to the default server or spawns its own client?
        Actually `opencode run` is a CLI command that talks to the server if `OPENCODE_PORT` is set?
        Or we use HTTP API directly. Let's assume HTTP API for robustness if supported.
        
        If API not available, fall back to subprocess call using resolved executable.
        """
        self.connect()
        
        # Method 1: HTTP API (Hypothetical, assuming standard agent protocol)
        # url = f"http://localhost:{self.server.port}/api/execute"
        # payload = {"command": command, "cwd": cwd}
        # try:
        #     resp = requests.post(url, json=payload, timeout=30)
        #     return resp.json()
        # except:
        #     pass

        # Method 2: CLI Wrapper (Robust fallback)
        # Configure env to point to specific server port if CLI supports it
        env = os.environ.copy()
        env["OPENCODE_PORT"] = str(self.server.port)
        
        executable = self.manager.opencode_path
        full_cmd = [executable, "run", command]
        
        try:
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=cwd,
                timeout=300
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_health_check(self):
        self.connect()
        return self.server.is_healthy()

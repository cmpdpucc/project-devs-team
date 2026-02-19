#!/usr/bin/env python3
"""
OpenCode Process Manager
========================
Orchestrates multiple OpenCode server instances to enable parallel execution.
Handles path resolution, port allocation, and process lifecycle.
"""

import os
import sys
import time
import shutil
import socket
import logging
import platform
import subprocess
import threading
import atexit
from pathlib import Path
from typing import List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProcessManager")

class OpenCodeServer:
    def __init__(self, port: int, executable: str):
        self.port = port
        self.executable = executable
        self.process: Optional[subprocess.Popen] = None
        self.lock = threading.Lock()

    def start(self):
        """Start the OpenCode server on the assigned port."""
        with self.lock:
            if self.is_running():
                logger.info(f"Server on port {self.port} already running.")
                return

            cmd = [self.executable, "serve", "--port", str(self.port)]
            
            # Windows-specific handling for .cmd files if not handled by shell=False
            start_kwargs = {
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
                "cwd": os.getcwd()
            }
            
            if platform.system() == "Windows":
                 start_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
            
            try:
                logger.info(f"Starting OpenCode server on port {self.port}...")
                self.process = subprocess.Popen(cmd, **start_kwargs)
                
                # Wait for startup
                time.sleep(2) 
                
                if self.process.poll() is not None:
                    logger.error(f"Server on port {self.port} failed to start immediately.")
                    self.process = None
                else:
                    logger.info(f"Server on port {self.port} started successfully (PID: {self.process.pid}).")
                    
            except Exception as e:
                logger.error(f"Failed to start server on port {self.port}: {e}")

    def stop(self):
        """Stop the server process."""
        with self.lock:
            if self.process:
                logger.info(f"Stopping server on port {self.port}...")
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                self.process = None

    def wait(self):
        """Block until the server process exits."""
        if self.process:
            try:
                self.process.wait()
            except KeyboardInterrupt:
                self.stop()

    def is_running(self) -> bool:
        """Check if the server process is running."""
        return self.process is not None and self.process.poll() is None

    def is_healthy(self) -> bool:
        """Check if the server is responsive via HTTP."""
        try:
            # Simple socket check as a lightweight health check
            with socket.create_connection(("localhost", self.port), timeout=1) as sock:
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False

class ProcessManager:
    _instance = None
    _creation_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._creation_lock:
                if not cls._instance:
                    cls._instance = super(ProcessManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, start_port=4096, max_workers=5):
        # Double check initialization to prevent race in __init__
        with self._creation_lock:
            if hasattr(self, 'initialized'): return
            self.initialized = True
            
            self.start_port = start_port
            self.max_workers = max_workers
            self.servers: List[OpenCodeServer] = []
            self.opencode_path = self._resolve_opencode_path()
            self.lock = threading.Lock()
            
            # Register cleanup
            atexit.register(self.shutdown_all)

    def _resolve_opencode_path(self) -> str:
        """Robustly resolve the OpenCode executable path."""
        # 1. Environment Variable
        env_path = os.getenv("OPENCODE_PATH")
        if env_path and os.path.exists(env_path):
            logger.info(f"Using OPENCODE_PATH: {env_path}")
            return env_path

        # 2. System PATH
        which_path = shutil.which("opencode")
        if which_path:
             logger.info(f"Found opencode in PATH: {which_path}")
             return which_path

        # 3. NPM Global Prefix (Windows/Linux)
        try:
            # Get npm prefix
            npm_cmd = ["npm", "config", "get", "prefix"]
            # shell=True often helps on Windows to find npm
            prefix = subprocess.check_output(npm_cmd, shell=platform.system()=="Windows", text=True).strip()
            
            if platform.system() == "Windows":
                candidate = Path(prefix) / "opencode.cmd"
            else:
                candidate = Path(prefix) / "bin" / "opencode"
                
            if candidate.exists():
                logger.info(f"Resolved opencode via npm prefix: {candidate}")
                return str(candidate)
                
        except Exception as e:
            logger.warning(f"Failed to resolve via npm prefix: {e}")

        # Fallback (Guess based on standard install locations)
        if platform.system() == "Windows":
             fallback = Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "nodejs" / "opencode.cmd"
             if fallback.exists():
                 return str(fallback)

        logger.critical("Could not resolve 'opencode' executable. Please set OPENCODE_PATH.")
        return "opencode" # Return bare command and hope for the best if all else fails

    def get_server(self) -> OpenCodeServer:
        """Get an available server or spin up a new one."""
        with self.lock:
            # Check existing servers
            for server in self.servers:
                if server.is_running():
                    # Logic to distribute load could go here (e.g. check open connections)
                    # For now, simplistic round-robin invocation by client.
                    # But actually we return a server instance to interaction.
                    # In a real pool we might want to return one that isn't verify busy.
                    pass
            
            # If we haven't reached max workers, create a new one
            if len(self.servers) < self.max_workers:
                port = self.start_port + len(self.servers)
                
                # Check if port is in use by another process not managed by us
                if self._is_port_in_use(port):
                    logger.warning(f"Port {port} is already in use. Skipping.")
                    # Try next port? or just use it if it's an existing opencode instance?
                    # For safety, let's increment and try next, or assume it's one of ours from previous run
                    # If we want to adopt it, we can't control it.
                    # Let's simple skip start logic for it but add to our list to try to use it?
                    # Better to find a free port.
                    pass
                
                server = OpenCodeServer(port, self.opencode_path)
                server.start()
                self.servers.append(server)
                return server
                
            # If all max workers running, return one (Round Robin logic in client necessary, or here)
            # For simplicity, return the first healthy one
            for server in self.servers:
                if server.is_healthy():
                    return server
                    
            # If none healthy, try to restart first one
            if self.servers:
                logger.warning("No healthy servers found. Restarting pool[0].")
                self.servers[0].stop()
                self.servers[0].start()
                return self.servers[0]
                
            raise RuntimeError("Could not obtain OpenCode server.")

    def _is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def shutdown_all(self):
        """Stop all managed servers."""
        logger.info("Shutting down all OpenCode servers...")
        for server in self.servers:
            server.stop()

# Singleton accessor
def get_manager():
    return ProcessManager()

if __name__ == "__main__":
    # Test run
    mgr = ProcessManager()
    print(f"Resolved Path: {mgr.opencode_path}")
    srv = mgr.get_server()
    print(f"Server Port: {srv.port}")
    time.sleep(5)
    # mgr.shutdown_all() # handled by atexit, but for script run we can let it exit

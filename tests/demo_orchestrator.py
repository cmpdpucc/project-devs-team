
import sys
import time
import subprocess
import threading
from pathlib import Path
import os
import shutil

# Add .agent to sys.path
project_root = Path(__file__).resolve().parent.parent
agent_dir = project_root / '.agent'
sys.path.append(str(project_root))
sys.path.append(str(agent_dir))

try:
    from scripts.process_manager import ProcessManager, OpenCodeServer
except ImportError:
    from agent.scripts.process_manager import ProcessManager, OpenCodeServer

def main():
    print("🚀 LAUNCHING VISUAL PARALLEL AGENT DEMO 🚀")
    print("==========================================")
    
    # 1. Start Process Manager and Spin up Servers
    manager = ProcessManager(start_port=4096, max_workers=5)
    
    print("Initializing servers...")
    servers = []
    
    # Pre-warm 5 servers
    for i in range(5):
        port = 4096 + i
        server = OpenCodeServer(port, manager.opencode_path)
        server.start()
        # REMOVED: server.detach() - Orchestrator MUST remain active
        servers.append(server)
        print(f"Started Server {i+1} on Port {port}")
        time.sleep(1) # Stagger slightly
        
    print("✅ All Servers Ready!")
    
    # 2. Prepare Shared File
    log_file = Path("demo_log.txt")
    if log_file.exists():
        log_file.unlink()
    
    with open(log_file, "w") as f:
        f.write("INIT: DEMO STARTING\n")
        
    # 3. Spawn 5 Visual Terminals via Python Popen
    # Assuming Windows environment as per user OS
    
    workers = []
    
    for i in range(5):
        agent_id = str(i + 1)
        port = 4096 + i
        
        # Build command to launch new terminal
        # "start" is cmd shell command.
        # "python demo_worker.py <ID> <PORT>"
        
        worker_script = Path("tests/demo_worker.py").resolve()
        
        # On Windows, we can use creationflags=subprocess.CREATE_NEW_CONSOLE to open a new window
        # But we need to keep the window open after exit if it crashes
        # So wrapping in cmd /k
        
        full_cmd = f'start "Agent {agent_id}" cmd /k "{sys.executable} {worker_script} {agent_id} {port}"'
        
        print(f"Spawning Agent {agent_id}...")
        subprocess.run(full_cmd, shell=True)
        workers.append(agent_id)
        time.sleep(0.5)
        
    print("✅ All Agents Spawned!")
    print("waiting for agents to connect...")
    time.sleep(5)
    
    # 4. Kick off the chain reaction
    with open(log_file, "a") as f:
        f.write("NEXT: 1\n")
        
    print("📢 TRIGGER SENT to Agent 1!")
    print("Watch the other windows!")
    print("🔒 ORCHESTRATOR MONITORING ACTIVE: Press Ctrl+C to stop all agents.")

    try:
        while True:
            # Monitor server health
            for s in servers:
                if not s.is_running():
                    print(f"⚠️ Server on port {s.port} died! Restarting...")
                    s.start()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Demo...")
    finally:
        manager.shutdown_all()
        # On Windows, killing external terminals is hard without handles, 
        # but we kill the servers, so workers will fail connection and (should) exit.

if __name__ == "__main__":
    main()

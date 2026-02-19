
import sys
import time
import random
import os
from pathlib import Path

# Add .agent to sys.path
project_root = Path(__file__).resolve().parent.parent
agent_dir = project_root / '.agent'
sys.path.append(str(project_root))
sys.path.append(str(agent_dir))

try:
    from scripts.opencode_client import OpenCodeClient
except ImportError:
    from agent.scripts.opencode_client import OpenCodeClient

def main():
    if len(sys.argv) < 3:
        print("Usage: python demo_worker.py <AGENT_ID> <PORT>")
        sys.exit(1)

    agent_id = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"\n🤖 AGENT {agent_id} INITIALIZING...")
    print(f"🔌 Connecting to OpenCode Server on Port {port}...")
    
    try:
        client = OpenCodeClient(port=port)
        client.connect()
        print(f"✅ CONNECTED! (Server PID: {client.server.port})")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        time.sleep(10)
        return

    shared_file = Path("demo_log.txt")
    
    print(f"👀 Watching {shared_file} for instructions...")
    
    last_processed_line = 0
    my_color = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m"][int(agent_id) % 5]
    reset_color = "\033[0m"

    while True:
        if shared_file.exists():
            with open(shared_file, "r") as f:
                lines = f.readlines()
                
            if len(lines) > last_processed_line:
                new_lines = lines[last_processed_line:]
                last_processed_line = len(lines)
                
                for line in new_lines:
                    line = line.strip()
                    if not line: continue
                    
                    print(f"📨 Received: {line}")
                    
                    # Logic: If line says "NEXT: AGENT X", and X is me, I do work
                    parts = line.split(":")
                    if len(parts) >= 2 and parts[0].strip() == "NEXT" and parts[1].strip() == agent_id:
                        print(f"{my_color}⚡ IT'S MY TURN! ⚡{reset_color}")
                        
                        # Simulate "Agent Work"
                        work_time = random.uniform(1.0, 3.0)
                        actions = ["Analyzing code...", "Refactoring module...", "Running tests...", "Optimizing DB...", "Auditing security..."]
                        action = random.choice(actions)
                        
                        for _ in range(int(work_time * 5)):
                            print(f"{my_color}.{reset_color}", end="", flush=True)
                            time.sleep(0.2)
                        print(f"\n{my_color}✅ {action} COMPLETED!{reset_color}")
                        
                        # Trigger next agent
                        next_agent = str((int(agent_id) % 5) + 1)
                        message = f"NEXT: {next_agent}\n"
                        with open(shared_file, "a") as f:
                            f.write(message)
                        print(f"📢 Handing off to Agent {next_agent}...")

        time.sleep(0.5)

if __name__ == "__main__":
    main()


import sys
import time
import concurrent.futures
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

def run_task(i):
    client = OpenCodeClient()
    print(f"[{i}] Connecting...")
    client.connect()
    port = client.server.port
    print(f"[{i}] Connected to port {port}")
    
    # Simulate work
    # In reality we would run a command
    time.sleep(2)
    return port

def main():
    print("Testing OpenCode Pool Concurrency...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_task, i) for i in range(5)]
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    print(f"Used Ports: {sorted(list(set(results)))}")
    # We expect multiple ports to be used if they start simultaneously
    # or if the manager logic spawns new ones.
    
    if len(set(results)) > 1:
        print("✅ SUCCESS: Multiple servers were utilized.")
    else:
        print("⚠️  WARNING: Only one server was used (Sequential reuse?).")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Bridge tra Antigravity e OpenCode per sincronizzare contesto e stato
"""
import os
import json
import subprocess
from pathlib import Path
import platform

import sys

# Add project root and .agent to sys.path to find modules
project_root = Path(__file__).resolve().parent.parent
agent_dir = project_root / '.agent'

sys.path.append(str(project_root))
sys.path.append(str(agent_dir))

try:
    from scripts.process_manager import ProcessManager
except ImportError:
    # Fallback/Debug
    print(f"DEBUG: sys.path: {sys.path}")
    raise

class AntigravityOpenCodeBridge:
    def __init__(self, global_sync=False):
        self.antigravity_home = Path.home() / '.antigravity'
        self.global_sync = global_sync
        self.manager = ProcessManager() # Initialize manager
        
        # Determine OpenCode config path based on OS
        if platform.system() == "Windows":
             self.opencode_config = Path(os.environ['APPDATA']) / 'opencode'
        else:
             self.opencode_config = Path.home() / '.local' / 'share' / 'opencode'
        
    def sync_gemini_rules(self):
        """Sincronizza GEMINI.md tra i due ambienti"""
        if not self.global_sync:
            print("ℹ️  Skipping global rule sync (use --global to enable)")
            return

        project_gemini = Path('.agent/rules/GEMINI.md')
        
        if not project_gemini.exists():
            print("⚠️  Warning: .agent/rules/GEMINI.md not found in current directory.")
            return

        # Ensure target dir exists
        if not self.opencode_config.exists():
            try:
                self.opencode_config.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"⚠️  Could not create OpenCode config dir: {e}")
                return

        target_rules = self.opencode_config / 'project_rules.md'
        
        try:
            # On Windows, symlinks might require admin. Copy is safer fallback.
            if target_rules.exists():
                if target_rules.is_symlink():
                    target_rules.unlink()
                else:
                    target_rules.unlink() # Delete old copy
            
            try:
                target_rules.symlink_to(project_gemini.resolve())
                print(f"✅ Synced GEMINI.md to OpenCode (Symlink)")
            except OSError:
                # Fallback to copy if symlink fails (common on Windows)
                import shutil
                shutil.copy2(project_gemini, target_rules)
                print(f"✅ Synced GEMINI.md to OpenCode (Copy)")
                
        except Exception as e:
            print(f"❌ Error syncing rules: {e}")
            
    def export_antigravity_lessons(self):
        """Esporta lesson learned da Antigravity a OpenCode context"""
        lessons_file = self.antigravity_home / 'memory' / 'LESSONS_LEARNED.md'
        target = Path('.agent/LESSONS_LEARNED.md')

        if lessons_file.exists():
            try:
                target.write_text(lessons_file.read_text(encoding='utf-8'), encoding='utf-8')
                print(f"✅ Exported {lessons_file.stat().st_size} bytes of lessons")
            except Exception as e:
                print(f"❌ Error exporting lessons: {e}")
        else:
            print("ℹ️  No Antigravity lessons found to export.")
            
    def start_opencode_server(self):
        """Avvia OpenCode server pool via ProcessManager"""
        print(f"🚀 Initializing OpenCode Server Pool (Ports {self.manager.start_port}+)...")
        try:
            # Start at least one server to warm up
            server = self.manager.get_server()
            print(f"✅ Primary OpenCode server active on port {server.port} (PID: {server.process.pid if server.process else 'External'})")
            print(f"ℹ️  ProcessManager initialized with max {self.manager.max_workers} workers.")
            print("🔒 STRICT SUPERVISION ACTIVE: Keep this terminal open to maintain the server.")
            
            # BLOCKING LOOP to enforce supervision
            try:
                server.wait()
            except KeyboardInterrupt:
                print("\n🛑 Received shutdown signal. Terminating servers...")
            finally:
                self.manager.shutdown_all()
                
        except Exception as e:
            logger.error(f"Bridge error during OpenCode server initialization: {e}")
            sys.exit(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--global", dest="global_sync", action="store_true", help="Sync rules to global OpenCode config")
    args = parser.parse_args()

    bridge = AntigravityOpenCodeBridge(global_sync=args.global_sync)
    bridge.sync_gemini_rules()
    bridge.export_antigravity_lessons()
    bridge.start_opencode_server()

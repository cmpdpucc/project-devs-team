#!/usr/bin/env python3
"""
Bridge tra Antigravity e OpenCode per sincronizzare contesto e stato.
Questo script gestisce la sincronizzazione delle regole (GEMINI.md) e l'avvio del server OpenCode.
"""
import os
import sys
import io
import json
import shutil
import platform
import subprocess
import argparse
import time
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class OpenCodeProcessManager:
    """Gestore robusto dei processi OpenCode."""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None

    def start_server(self, port: int = 3000, dry_run: bool = False) -> bool:
        """Avvia il server OpenCode su una porta specifica."""
        if dry_run:
            print(f"[DRY-RUN] Would start OpenCode server on port {port}")
            return True

        cmd = ["opencode", "serve", "--port", str(port)]
        # Fallback se 'opencode' non è nel PATH, prova con npx o npm
        if shutil.which("opencode") is None:
             cmd = ["npx", "opencode-ai@latest", "serve", "--port", str(port)]

        try:
            print(f"🚀 Starting OpenCode server on port {port}...")
            # In production usage, we might want to capture output or detach
            # For this bridge, we keep it attached or manage it.
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Check if it crashed immediately
            try:
                stdout, stderr = self.process.communicate(timeout=1)
                if self.process.returncode is not None and self.process.returncode != 0:
                    print(f"❌ Server failed to start: {stderr}")
                    return False
            except subprocess.TimeoutExpired:
                # Still running, good.
                pass
                
            print(f"✅ OpenCode server started (PID: {self.process.pid})")
            return True
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False

    def stop_server(self):
        """Ferma il server gestito."""
        if self.process:
            print(f"🛑 Stopping OpenCode server (PID: {self.process.pid})...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("✅ Server stopped.")
            self.process = None

class AntigravityOpenCodeBridge:
    def __init__(self, global_sync: bool = False):
        self.antigravity_home = Path.home() / '.antigravity'
        self.global_sync = global_sync
        self.manager = OpenCodeProcessManager()
        
        # Determine OpenCode config path based on OS
        if platform.system() == "Windows":
             self.opencode_config = Path(os.environ.get('APPDATA', '')) / 'opencode'
        else:
             self.opencode_config = Path.home() / '.local' / 'share' / 'opencode'
        
    def sync_gemini_rules(self) -> bool:
        """Sincronizza GEMINI.md tra i due ambienti."""
        print("🔄 Syncing GEMINI.md rules...")
        
        project_gemini = Path('.agent/rules/GEMINI.md').resolve()
        
        if not project_gemini.exists():
            print("⚠️  Warning: .agent/rules/GEMINI.md not found in current directory.")
            return False

        if not self.global_sync:
            print("ℹ️  Skipping global rule sync (use --global to enable)")
            # For local context, we might want to ensure a local config exists
            # but usually OpenCode looks at global config.
            return True

        # Ensure target dir exists
        if not self.opencode_config.exists():
            try:
                self.opencode_config.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"❌ Could not create OpenCode config dir: {e}")
                return False

        target_rules = self.opencode_config / 'project_rules.md'
        
        try:
            # On Windows, symlinks might require admin. Copy is safer fallback for robustness.
            if target_rules.exists():
                if target_rules.is_symlink():
                    target_rules.unlink()
                else:
                    try:
                        os.remove(target_rules)
                    except PermissionError:
                         print(f"❌ Permission denied removing old rules: {target_rules}")
                         return False
            
            # Try symlink first, then copy
            try:
                target_rules.symlink_to(project_gemini)
                print(f"✅ Synced GEMINI.md to OpenCode (Symlink)")
            except (OSError, AttributeError):
                shutil.copy2(project_gemini, target_rules)
                print(f"✅ Synced GEMINI.md to OpenCode (Copy)")
            
            return True
                
        except Exception as e:
            print(f"❌ Error syncing rules: {e}")
            return False
            
    def export_antigravity_lessons(self):
        """Esporta lesson learned da Antigravity a OpenCode context."""
        print("🔄 Exporting Antigravity lessons...")
        lessons_file = self.antigravity_home / 'memory' / 'LESSONS_LEARNED.md'
        target = Path('.agent/LESSONS_LEARNED.md')

        if lessons_file.exists():
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(lessons_file.read_text(encoding='utf-8'), encoding='utf-8')
                print(f"✅ Exported {lessons_file.stat().st_size} bytes of lessons")
            except Exception as e:
                print(f"❌ Error exporting lessons: {e}")
        else:
            print("ℹ️  No Antigravity lessons found to export.")

    def start_opencode_server(self, port: int = 3000, dry_run: bool = False):
        """Avvia OpenCode server pool via ProcessManager."""
        success = self.manager.start_server(port=port, dry_run=dry_run)
        if not success:
            print("❌ Failed to start OpenCode server.")
            sys.exit(1)
        
        if not dry_run:
            print("🔒 STRICT SUPERVISION ACTIVE: Keep this terminal open to maintain the server.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Received shutdown signal.")
            finally:
                self.manager.stop_server()

def main():
    parser = argparse.ArgumentParser(description="Antigravity-OpenCode Bridge")
    parser.add_argument("--global", dest="global_sync", action="store_true", help="Sync rules to global OpenCode config")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no blocking server)")
    parser.add_argument("--port", type=int, default=3000, help="Port for OpenCode server")
    
    args = parser.parse_args()

    print("🌉 Initializing Antigravity-OpenCode Bridge...")
    bridge = AntigravityOpenCodeBridge(global_sync=args.global_sync)
    
    # Run sync tasks
    bridge.sync_gemini_rules()
    bridge.export_antigravity_lessons()
    
    # Start server logic
    if args.test:
        print("🧪 Running in TEST mode (skipping blocking server start)")
        # In test mode, we just verify the manager *can* be invoked in dry-run
        bridge.start_opencode_server(port=args.port, dry_run=True)
        print("✅ Bridge Test Completed Successfully.")
    else:
        bridge.start_opencode_server(port=args.port)

if __name__ == '__main__':
    main()

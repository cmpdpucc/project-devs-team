
import sys
import textwrap
from pathlib import Path
import json

# Add scripts to path
sys.path.insert(0, str(Path.cwd() / ".agent" / "scripts"))
from progress_reporter import parse_plan

PLAN_MIXED = textwrap.dedent("""\
    # RALPH PLAN — Mixed

    ## Phase 6 — Dashboard
    - [x] Task done
    - [/] Task in progress
    - [ ] Task todo
    - [-] Task cancelled
    - [!] Task blocked

    ## Phase 7 — Legacy
    - [x] Old task 1
    - [x] Old task 2
    - [ ] Old task 3
""")

tmp_plan = Path("debug_plan.md")
tmp_plan.write_text(PLAN_MIXED, encoding="utf-8")

report = parse_plan(tmp_plan)
print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))

# Check Phase 6 specifically
p6 = next((p for p in report.phases if "6" in p.name), None)
if p6:
    print(f"\nPhase 6 Done: {p6.done}")
    print(f"Phase 6 Tasks: {p6.tasks_done}")
else:
    print("Phase 6 not found")

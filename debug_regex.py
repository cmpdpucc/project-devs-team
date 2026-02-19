
import re
from pathlib import Path

# The regex in progress_reporter.py
PHASE_RE = re.compile(
    r"^#{1,3}\s*(Phase\s*\d+\b.*|\d+\.\d+\s+\S.*)",
    re.IGNORECASE,
)

# Read test file
content = Path("tests/test_progress_reporter.py").read_text(encoding="utf-8")

# Extract PLAN_MIXED block (hacky but works for debug)
start = content.find('PLAN_MIXED = textwrap.dedent("""\\')
if start == -1:
    print("Could not find PLAN_MIXED")
    exit(1)

end = content.find('""")', start)
block = content[start:end]
lines = block.splitlines()

print(f"Testing {len(lines)} lines from PLAN_MIXED...")

for i, line in enumerate(lines):
    # Remove \"""\ and indentation is handled by textwrap in real code, 
    # but here we just look at lines that look like headers.
    # In the file, it is indented.
    stripped = line.strip()
    # textwrap.dedent removes common whitespace. 
    # The block inside """\ ... """ has 4 spaces indentation in the file?
    
    # Let's just test matches on stripped lines to be sure
    if stripped.startswith("##"):
        match = PHASE_RE.match(stripped)
        print(f"Line {i}: '{stripped}' -> {bool(match)}")
        if match:
            print(f"   Group 1: '{match.group(1)}'")
        else:
            print(f"   NO MATCH! Hex: {stripped.encode('utf-8').hex()}")

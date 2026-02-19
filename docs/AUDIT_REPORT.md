# Security & Performance Audit Report

**Date:** February 16, 2026  
**Auditor:** OpenCode Agent  
**Scope:** `scripts/`, `config/`, `.agent/`

---

## 1. Executive Summary

The audit of the project's agent configuration and support scripts reveals a generally well-structured environment but identifies specific security risks related to shell execution and file system access, as well as performance optimizations needed for the scanning tools.

**Key Findings:**
- **High Risk:** Shell injection vulnerability in `auto_preview.py`.
- **Medium Risk:** Unsafe file operations outside project scope in bridge scripts.
- **Performance:** Inefficient file scanning (multiple passes) in security scanner.

---

## 2. Security Analysis

### 2.1 Critical Vulnerabilities

**file:** `.agent/scripts/auto_preview.py`  
**Issue:** **Shell Injection Risk**  
**Location:** Line 81 (`subprocess.Popen(..., shell=True)`)  
**Description:** The script executes commands using `shell=True`. The command construction relies on `package.json` content and environment variables. While `package.json` is typically trusted source code, using `shell=True` allows chained commands (e.g., `npm run dev && rm -rf /`) if the package script is compromised.  
**Recommendation:**  
Use `shell=False` (default) and split the command into a list of arguments manually or using `shlex.split()`.

### 2.2 Medium Risks

**file:** `scripts/antigravity-opencode-bridge.py`  
**Issue:** **External File Modification**  
**Location:** Lines 17-19, 37-54  
**Description:** The script attempts to modify files outside the project repository (e.g., `%APPDATA%` on Windows, `~/.local` on Linux). This behavior is intrusive for a project-scoped script and may fail due to permissions or trigger antivirus heuristics.  
**Recommendation:**  
Limit configuration changes to the local project scope or explicitly ask for user confirmation before modifying global user settings.

**file:** `scripts/antigravity-opencode-bridge.py`  
**Issue:** **Hardcoded Network Call**  
**Location:** Line 77 (`curl ... http://localhost:4096`)  
**Description:** Hardcoded dependencies on port `4096` and `localhost`. While low risk in a dev environment, it assumes port availability and trust.  
**Recommendation:**  
Make the port configurable via environment variables or arguments.

### 2.3 Permissions Model

**file:** `config/opencode.json`  
**Observation:**
- `git push`: Set to `"ask"` (Secure)
- `rm -rf *`: Set to `"deny"` (Secure)
- `read`/`edit`: Set to `"allow"`
**Analysis:** The permissions are reasonable for an autonomous agent. The explicit denial of destructive `rm` commands is a good safety net.

---

## 3. Performance Analysis

### 3.1 Scanning Inefficiency

**file:** `.agent/skills/vulnerability-scanner/scripts/security_scan.py`  
**Issue:** **Multiple File System Passes ($O(3N)$)**  
**Description:** The script walks the entire file tree three separate times:
1. `scan_secrets` (Lines 181-234)
2. `scan_code_patterns` (Lines 236-294)
3. `scan_configuration` (Lines 296-366)
**Impact:** For large projects, this triples the I/O load and execution time.  
**Recommendation:**  
Refactor to use a single `os.walk` pass that routes file content to appropriate checkers based on file extension.

### 3.2 Sequential Execution

**file:** `.agent/scripts/checklist.py` & `verify_all.py`  
**Issue:** **Blocking Sequential Checks**  
**Description:** Validations run strictly in series. Independent tasks (e.g., "Lint Check" and "Security Scan") block each other.  
**Impact:** Increases total feedback loop time.  
**Recommendation:**  
Use Python's `asyncio` or `concurrent.futures` to run independent checks in parallel.

### 3.3 Regular Expression Overhead

**file:** `.agent/skills/vulnerability-scanner/scripts/security_scan.py`  
**Issue:** **Potential ReDoS**  
**Location:** Line 75 (`r'["\'][^"\']*\+\s*[a-zA-Z_]+\s*\+\s*["\'].*(?:SELECT...)'`)  
**Description:** Complex regexes are applied line-by-line. Nested quantifiers in the SQL injection detection pattern could lead to catastrophic backtracking on specific malicious inputs.  
**Recommendation:**  
Optimize regex patterns or set a strict timeout for regex operations.

---

## 4. Recommendations Roadmap

1.  **Immediate Fix:** Patch `.agent/scripts/auto_preview.py` to remove `shell=True`.
2.  **Refactor:** Rewrite `security_scan.py` to perform a single-pass scan.
3.  **Enhancement:** Update `checklist.py` to run P0/P1 checks in parallel.

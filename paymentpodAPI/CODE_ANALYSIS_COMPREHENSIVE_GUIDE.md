# Code Analysis Skill - Comprehensive Guide

## 🎯 Purpose
Automated security vulnerability detection in Python and JavaScript code using static analysis (pattern matching)

---

## 📋 Module Structure

### Docstring (Lines 1-4)
```python
"""
Code Analysis Skill
Performs static analysis to detect security vulnerabilities
"""
```
**What it means:**
- Module detects security issues automatically
- Uses static analysis (doesn't run code)
- Works on Python & JavaScript files

---

## 🔧 Core Components

### 1. **SeverityLevel Enum** (Lines 16-21)
Classifies vulnerability risk levels:
```
CRITICAL  → Immediate security risk (SQL Injection, Code Injection)
HIGH      → Major vulnerability (Hardcoded secrets, XSS)
MEDIUM    → Moderate risk
LOW       → Minor issues
```

### 2. **CodeAnalysisSkill Class** (Lines 24-140)
Main class with 4 methods:

| Method | Purpose | Input | Output |
|--------|---------|-------|--------|
| `__init__` | Initialize | None | Empty vulnerabilities list |
| `analyze_python` | Scan .py files | file_path | List of vulnerabilities |
| `analyze_javascript` | Scan .js files | file_path | List of vulnerabilities |
| `scan_directory` | Bulk scan | directory | Report dict |

---

## 🐍 Python Analysis Details

**Checks 3 vulnerability types:**

1. **SQL Injection (CRITICAL)**
   - Regex: `execute\s*\(\s*["\'].*%s`
   - Example: `execute("SELECT * FROM users WHERE id = %s")`

2. **Hardcoded Secrets (HIGH)**
   - Patterns: `password=`, `api_key=`, `secret=`
   - Example: `api_key = "sk_123456789"`

3. **Insecure Deserialization (CRITICAL)**
   - Patterns: `pickle.load()`, `yaml.load()`
   - Risk: Arbitrary code execution

---

## 📜 JavaScript Analysis Details

**Checks 2 vulnerability types:**

1. **Eval Usage (CRITICAL)**
   - Pattern: `eval(`
   - Risk: Code injection

2. **innerHTML Assignment (HIGH)**
   - Pattern: `.innerHTML =`
   - Risk: XSS vulnerability

---

## 📂 Directory Scanning Process

```
scan_directory("/project")
  ↓
os.walk() → Walk all subdirectories
  ↓
Find .py files → analyze_python() for each
Find .js/.jsx files → analyze_javascript() for each
  ↓
Aggregate all vulnerabilities
  ↓
Return summary report
```

---

## 📊 Report Structure

```python
{
    "total_files": 42,              # Total .py + .js files
    "total_vulnerabilities": 5,     # Total issues found
    "vulnerabilities": [
        {
            "file": "src/app.py",
            "line": 15,
            "type": "SQL Injection",
            "severity": "CRITICAL",
            "code": "execute(...)"
        }
    ]
}
```

---

## ⚡ Key Features

✅ **Pattern-based detection** - Uses regex for speed
✅ **Multi-language support** - Python & JavaScript
✅ **Recursive scanning** - Walks entire directory tree
✅ **Error handling** - Continues on file read errors
✅ **Severity classification** - 4-level risk assessment
✅ **Precise line numbers** - Exact vulnerability location
✅ **Logging** - Tracks analysis progress & errors

---

## 🚀 Quick Start

```python
from skills.code_analysis_skill import CodeAnalysisSkill

# Create analyzer
analyzer = CodeAnalysisSkill()

# Scan directory
report = analyzer.scan_directory("./src")

# Print summary
print(f"Files: {report['total_files']}")
print(f"Issues: {report['total_vulnerabilities']}")

# Process each vulnerability
for vuln in report['vulnerabilities']:
    print(f"{vuln['severity']}: {vuln['type']} at {vuln['file']}:{vuln['line']}")
```

---

## 🔍 Vulnerability Detection Examples

| Vulnerability | Code | Status |
|---------------|------|--------|
| SQL Injection | `execute("SELECT %s")` | ✅ DETECTED |
| Hardcoded API Key | `api_key = "sk_xxx"` | ✅ DETECTED |
| Pickle Load | `pickle.load(f)` | ✅ DETECTED |
| Eval Usage | `eval(user_input)` | ✅ DETECTED |
| innerHTML XSS | `el.innerHTML = html` | ✅ DETECTED |

---

## 📁 See Also
- `CODE_ANALYSIS_SKILL_FLOW.md` - Detailed flow explanation
- `CODE_ANALYSIS_EXAMPLES.md` - Real-world examples
- `vulnerability_fixer_skill.py` - Auto-fix vulnerabilities

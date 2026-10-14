# Code Analysis Skill - Complete Flow Explanation

## Overview
**Purpose:** Static code analysis to detect security vulnerabilities in Python and JavaScript files

## Module Docstring
```python
"""
Code Analysis Skill
Performs static analysis to detect security vulnerabilities
"""
```
- Describes what this module does
- Performs automated security scanning
- Detects multiple vulnerability types

---

## 1️⃣ Imports & Dependencies

### Core Libraries
```python
import os           # File system operations
import re           # Regular expression pattern matching
import json         # Data serialization (optional)
from typing import Dict, List  # Type hints for better code clarity
from enum import Enum          # Create severity level categories
import logging      # Track errors and information
```

### Logger Setup
```python
logger = logging.getLogger(__name__)  # Logs analysis results and errors
```

---

## 2️⃣ SeverityLevel Enum (Lines 16-21)

Defines vulnerability severity categories:
- **CRITICAL:** Most severe (SQL injection, insecure deserialization)
- **HIGH:** Major issues (hardcoded secrets, XSS)
- **MEDIUM:** Moderate risks
- **LOW:** Minor issues

---

## 3️⃣ CodeAnalysisSkill Class

### Initialization (Lines 27-29)
```python
def __init__(self):
    self.vulnerabilities = []  # Stores found vulnerabilities
```

---

## 4️⃣ Python Analysis Method (Lines 31-81)

### Flow:
1. **Read file** → Open Python file and load content
2. **Pattern matching** → Use regex to detect issues
3. **SQL Injection check**
   - Pattern: `execute("... %s")`
   - Pattern: `query("... %")`
   - Severity: CRITICAL

4. **Hardcoded Secrets check**
   - Pattern: `password = "..."`
   - Pattern: `api_key = "..."`
   - Severity: HIGH

5. **Insecure Deserialization**
   - Pattern: `pickle.load()` or `yaml.load()`
   - Severity: CRITICAL

6. **Return results** → List of all vulnerabilities

---

## 5️⃣ JavaScript Analysis Method (Lines 83-108)

### Flow:
1. **Read JS file** → Load JavaScript content
2. **Check eval() usage**
   - Pattern: `eval(...)`
   - Severity: CRITICAL
   - Risk: Code injection

3. **Check innerHTML assignments**
   - Pattern: `.innerHTML = `
   - Severity: HIGH
   - Risk: XSS vulnerability

4. **Return vulnerabilities**

---

## 6️⃣ Directory Scanning (Lines 110-129)

### Flow:
```
scan_directory(path)
    ↓
Walk through all folders
    ↓
Find .py files → Call analyze_python()
Find .js/.jsx files → Call analyze_javascript()
    ↓
Aggregate results
    ↓
Return Report:
{
    "total_files": count,
    "total_vulnerabilities": count,
    "vulnerabilities": [list]
}
```

---

## 7️⃣ Vulnerability Reporter (Lines 131-140)

```python
_create_vuln(file, line, type, severity, code)
    ↓
Returns Dict:
{
    "file": "/path/to/file.py",
    "line": 42,
    "type": "SQL Injection",
    "severity": "CRITICAL",
    "code": "execute(\"SELECT %s\")"
}
```

---

## Usage Example

```python
skill = CodeAnalysisSkill()

# Analyze single Python file
results = skill.analyze_python("app.py")

# Analyze entire directory
report = skill.scan_directory("./src")
print(f"Found {report['total_vulnerabilities']} issues")
```

---

## Vulnerability Types Detected

| Type | File Type | Severity | Pattern |
|------|-----------|----------|---------|
| SQL Injection | Python | CRITICAL | `execute()`, `query()` with %s |
| Hardcoded Secret | Python | HIGH | `password=`, `api_key=`, `secret=` |
| Insecure Deserialization | Python | CRITICAL | `pickle.load()`, `yaml.load()` |
| Eval Usage | JavaScript | CRITICAL | `eval()` |
| XSS Vulnerability | JavaScript | HIGH | `.innerHTML =` |

---

## Error Handling
- Try-except blocks catch file read errors
- Logs errors without stopping analysis
- Returns empty list if file cannot be analyzed

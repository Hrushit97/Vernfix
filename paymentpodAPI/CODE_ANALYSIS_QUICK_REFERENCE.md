# Code Analysis Skill - Quick Reference

## 📖 Docstring Explanation
```python
"""
Code Analysis Skill
Performs static analysis to detect security vulnerabilities
"""
```

**Translation:** This module automatically scans code files to find security problems without running the code.

---

## 🎯 What It Does

| Component | Function |
|-----------|----------|
| **SeverityLevel** | Classifies vulnerability risk (CRITICAL, HIGH, MEDIUM, LOW) |
| **analyze_python()** | Scans Python files for 3 types of vulnerabilities |
| **analyze_javascript()** | Scans JS files for 2 types of vulnerabilities |
| **scan_directory()** | Recursively scans entire folder structure |
| **_create_vuln()** | Formats vulnerability data into report |

---

## 🔍 What It Detects

### Python Files (.py)
```
1. SQL Injection
   Pattern: execute/query with %s
   Severity: CRITICAL
   Example: execute("SELECT * FROM users WHERE id = %s")

2. Hardcoded Secrets
   Pattern: password=, api_key=, secret=
   Severity: HIGH
   Example: api_key = "sk_12345"

3. Insecure Deserialization
   Pattern: pickle.load(), yaml.load()
   Severity: CRITICAL
   Example: data = pickle.load(file)
```

### JavaScript Files (.js, .jsx)
```
1. Eval Usage
   Pattern: eval()
   Severity: CRITICAL
   Example: eval(userInput)

2. innerHTML XSS
   Pattern: .innerHTML =
   Severity: HIGH
   Example: el.innerHTML = htmlContent
```

---

## 📊 Output Format

**Single File Analysis:**
```python
[
    {
        "file": "/path/to/app.py",
        "line": 15,
        "type": "SQL Injection",
        "severity": "CRITICAL",
        "code": "execute(\"...%s\")"
    }
]
```

**Directory Scan:**
```python
{
    "total_files": 42,
    "total_vulnerabilities": 7,
    "vulnerabilities": [...]
}
```

---

## 🚀 Usage

### Simple File Analysis
```python
analyzer = CodeAnalysisSkill()
issues = analyzer.analyze_python("app.py")
print(f"Found {len(issues)} issues")
```

### Entire Project Scan
```python
analyzer = CodeAnalysisSkill()
report = analyzer.scan_directory("./src")
print(f"Total vulnerabilities: {report['total_vulnerabilities']}")
```

### Process Results
```python
for vuln in report['vulnerabilities']:
    severity = vuln['severity']
    issue_type = vuln['type']
    file_path = vuln['file']
    line_no = vuln['line']
    print(f"[{severity}] {issue_type} at {file_path}:{line_no}")
```

---

## 🔧 How It Works

1. **Read file** → Load code content
2. **Pattern match** → Use regex to find vulnerable patterns
3. **Calculate line number** → Find exact location
4. **Create report** → Format vulnerability details
5. **Return results** → List of vulnerabilities

For directories:
1. Walk through all subdirectories
2. Find .py and .js files
3. Analyze each file
4. Aggregate all findings
5. Return summary report

---

## ⚠️ Important Notes

✅ **Strengths:**
- Fast pattern-based detection
- Multi-language support
- Precise line numbers
- Error tolerant

❌ **Limitations:**
- Pattern-based (may miss edge cases)
- No runtime analysis
- False positives possible
- Limited to predefined patterns

---

## 📚 Related Files
- `vulnerability_fixer_skill.py` - Auto-fixes detected vulnerabilities
- `test_skills.py` - Unit tests (73% coverage)
- `vulnerability_orchestrator.py` - Orchestrates the analysis

# Code Analysis Skill - Practical Examples

## Example 1: Detecting SQL Injection

### Vulnerable Code (detected as CRITICAL)
```python
# app.py
def get_user(user_id):
    execute("SELECT * FROM users WHERE id = %s")  # ❌ DETECTED!
```

### Analysis Output
```json
{
    "file": "app.py",
    "line": 2,
    "type": "SQL Injection",
    "severity": "CRITICAL",
    "code": "execute(\"SELECT * FROM users WHERE id = %s\")"
}
```

---

## Example 2: Detecting Hardcoded Secrets

### Vulnerable Code
```python
# config.py
api_key = "sk_live_1234567890abcdef"  # ❌ DETECTED!
password = "admin123"                   # ❌ DETECTED!
```

### Analysis Output
```json
[
    {
        "file": "config.py",
        "line": 1,
        "type": "Hardcoded API Key",
        "severity": "HIGH",
        "code": "api_key = \"sk_live_1234567890abcdef\""
    },
    {
        "file": "config.py",
        "line": 2,
        "type": "Hardcoded Secret",
        "severity": "HIGH",
        "code": "password = \"admin123\""
    }
]
```

---

## Example 3: Detecting Insecure Deserialization

### Vulnerable Code
```python
# data_loader.py
import pickle
data = pickle.load(file)  # ❌ DETECTED!
```

### Analysis Output
```json
{
    "file": "data_loader.py",
    "line": 2,
    "type": "Insecure Deserialization",
    "severity": "CRITICAL",
    "code": "pickle/yaml.load usage"
}
```

---

## Example 4: Detecting JavaScript XSS

### Vulnerable Code
```javascript
// app.js
document.getElementById('output').innerHTML = userInput;  // ❌ DETECTED!
```

### Analysis Output
```json
{
    "file": "app.js",
    "line": 1,
    "type": "XSS Vulnerability",
    "severity": "HIGH",
    "code": "innerHTML assignment"
}
```

---

## Example 5: Directory Scan Report

### Scanning a Project
```python
skill = CodeAnalysisSkill()
report = skill.scan_directory("./src")
```

### Full Report Output
```json
{
    "total_files": 42,
    "total_vulnerabilities": 7,
    "vulnerabilities": [
        {
            "file": "src/database.py",
            "line": 15,
            "type": "SQL Injection",
            "severity": "CRITICAL",
            "code": "execute(\"UPDATE users SET name = %s\")"
        },
        {
            "file": "src/config.py",
            "line": 5,
            "type": "Hardcoded Secret",
            "severity": "HIGH",
            "code": "password = \"SuperSecret123\""
        },
        {
            "file": "src/utils.js",
            "line": 42,
            "type": "XSS Vulnerability",
            "severity": "HIGH",
            "code": "innerHTML assignment"
        }
    ]
}
```

---

## Complete Usage Flow

```python
from skills.code_analysis_skill import CodeAnalysisSkill

# 1. Initialize analyzer
analyzer = CodeAnalysisSkill()

# 2. Analyze single Python file
python_issues = analyzer.analyze_python("app.py")
print(f"Found {len(python_issues)} issues in app.py")

# 3. Analyze single JavaScript file
js_issues = analyzer.analyze_javascript("script.js")
print(f"Found {len(js_issues)} issues in script.js")

# 4. Scan entire directory
report = analyzer.scan_directory("./project")
print(f"Scanned {report['total_files']} files")
print(f"Found {report['total_vulnerabilities']} vulnerabilities")

# 5. Process results
for vuln in report['vulnerabilities']:
    print(f"⚠️  {vuln['severity']} - {vuln['type']} in {vuln['file']}:{vuln['line']}")
```

---

## Pattern Reference

| Vulnerability | Python Pattern | JavaScript Pattern |
|--------------|----------------|-------------------|
| SQL Injection | `execute()`, `query()` with `%s` | N/A |
| Hardcoded Secrets | `password=`, `api_key=`, `secret=` | N/A |
| Code Execution | `pickle.load()`, `yaml.load()` | `eval()` |
| XSS | N/A | `.innerHTML =` |

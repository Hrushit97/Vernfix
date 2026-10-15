# Quick Reference: End-to-End Flow

## 🚀 30-Second Overview

**What:** How data flows from your code through Jira and back
**Where:** 7 levels/files involved
**Time:** ~200-750ms total
**Result:** Dict with security issues

---

## 📋 The Flow (Simplified)

```
YOUR CODE
  ↓
Orchestrator (logs + validates)
  ↓
JiraSkill (builds query)
  ↓
Jira Library (makes HTTP request)
  ↓
Jira API (authenticates + searches)
  ↓
Jira Database (finds issues)
  ↓ (returns data back up, 6 steps)
YOUR CODE (gets dict result)
```

---

## 🎯 7 Levels Breakdown

| # | File | Method | Does What |
|---|------|--------|-----------|
| 1 | main.py | `orchestrator.get_existing_security_issues('PAYMENT')` | Calls method |
| 2 | vulnerability_orchestrator.py | `get_existing_security_issues()` | Logs, calls JiraSkill |
| 3 | jira_skill.py | `get_issues_by_labels()` | Builds JQL, calls Jira |
| 4 | jira library | `search_issues()` | Makes HTTP POST |
| 5 | Jira API | REST endpoint | Validates, queries DB |
| 6 | Jira Database | -- | Finds matching issues |
| 1 | YOUR CODE | -- | Receives dict |

---

## 📤 Input & Output

### Input
```python
project_key = 'PAYMENT'
```

### Output
```python
{
    'success': True,
    'count': 2,
    'issues': [
        {'key': 'PAYMENT-123', 'summary': '...', 'status': 'Open'},
        {'key': 'PAYMENT-124', 'summary': '...', 'status': 'In Progress'}
    ]
}
```

---

## 🔄 Data Types at Each Level

```
Level 1: Input str
Level 2: str + adds logging
Level 3: str → JQL str → HTTP request
Level 4: HTTP request → HTTP response
Level 5: Query DB → Issue objects
Level 3: Issue objects → Dict list
Level 2: Wrap in dict
Level 1: Receive dict
```

---

## 🔐 Authentication

Done automatically by Jira library using:
- `jira_url`: https://domain.atlassian.net
- `jira_username`: email@example.com
- `jira_api_token`: YOUR_TOKEN

---

## ⏱️ Performance

- Orchestrator: < 1ms
- JiraSkill: < 10ms
- Network: 100-500ms
- Jira query: 50-200ms
- Response: 10-50ms
- **Total: 200-750ms**

---

## 📚 Documentation Map

| Need | Read |
|------|------|
| Complete flow | END_TO_END_CALLING_FLOW.md |
| Code details | CODE_WALKTHROUGH_GUIDE.md |
| Real examples | PRACTICAL_EXAMPLES.md |
| Quick ref | This file |

---

## 💡 Key Points

1. **Only 1 HTTP request** made at level 4
2. **Automatic authentication** via Jira library
3. **Fresh data** every call (no caching)
4. **Error handling** at each level (try-catch)
5. **Logging** at levels 2 & 3
6. **Data conversion** at level 3 (Jira objects → dicts)

---

## 🧪 Quick Test

```python
# Check it works
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

config = {...}  # Your config
orchestrator = VulnerabilityOrchestrator(config)

result = orchestrator.get_existing_security_issues('PAYMENT')

print(f"Success: {result['success']}")
print(f"Count: {result['count']}")
print(f"Issues: {len(result['issues'])}")
```

---

## 🎯 Common Tasks

### Check Before Running Workflow
```python
existing = orchestrator.get_existing_security_issues('PAYMENT')
if existing['count'] > 5:
    print("Many issues exist already")
```

### List All Issues
```python
result = orchestrator.get_existing_security_issues('PAYMENT')
for issue in result['issues']:
    print(f"{issue['key']}: {issue['status']}")
```

### Count by Status
```python
issues = result['issues']
open_count = sum(1 for i in issues if i['status'] == 'Open')
```

---

## ⚠️ Error Handling

```python
result = orchestrator.get_existing_security_issues('PAYMENT')

# Always check success first!
if result['success']:
    count = result['count']
    issues = result['issues']
else:
    error = result['error']
    print(f"Failed: {error}")
```

---

## 📁 Files Involved

```
paymentpodAPI/
├── main.py .......................... User code (Level 1)
├── orchestrator/
│   └── vulnerability_orchestrator.py  (Level 2)
├── skills/
│   └── jira_skill.py ................ (Level 3)
└── jira library ..................... (Level 4)
        ↓
    Jira API ......................... (Level 5)
        ↓
    Jira Database .................... (Level 6)
```

---

## 🚀 Start Here

1. **Understand:** Read this quick reference
2. **Details:** Read CODE_WALKTHROUGH_GUIDE.md
3. **Practice:** Try PRACTICAL_EXAMPLES.md
4. **Reference:** Use END_TO_END_CALLING_FLOW.md

---

## ✅ What You'll Know After

- How 7 files work together
- What happens at each level
- How data transforms
- How to use in your code
- How to debug issues
- How to test
- Real-world examples

**That's the complete flow! 🎉**

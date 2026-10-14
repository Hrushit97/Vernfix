# Jira Integration Skill - Quick Reference

## 📖 Docstring Translation
```python
"""
Jira Integration Skill
Handles all Jira operations: ticket creation, updates, tracking vulnerabilities
"""
```

**Means:** This module automates Jira ticket management for security vulnerabilities

---

## 🎯 What It Does

- ✅ Create vulnerability tracking tickets
- ✅ Get ticket details
- ✅ Update existing tickets
- ✅ Add comments to tickets
- ✅ Link GitHub PRs to tickets
- ✅ Change ticket status
- ✅ Transition tickets through workflow

---

## 7️⃣ Core Methods

### 1. `__init__(url, username, api_token)`
**Connect to Jira**
```python
jira = JiraSkill(
    "https://your-domain.atlassian.net",
    "your-email@example.com",
    "YOUR_API_TOKEN"
)
```

### 2. `create_issue(project_key, summary, issue_type, description, priority, labels)`
**Create ticket**
```python
issue = jira.create_issue(
    "PAYMENT",
    "SQL Injection in login",
    issue_type="Bug",
    description="Details...",
    priority="Critical",
    labels=["security"]
)
# Returns: issue_key, issue_url
```

### 3. `get_issue(issue_key)`
**Get ticket details**
```python
details = jira.get_issue("PAYMENT-123")
# Returns: key, summary, status, priority, description
```

### 4. `update_issue(issue_key, updates)`
**Modify ticket**
```python
jira.update_issue("PAYMENT-123", {
    "summary": "New title",
    "priority": {"name": "High"}
})
```

### 5. `add_comment(issue_key, comment)`
**Comment on ticket**
```python
jira.add_comment("PAYMENT-123", "Progress update...")
```

### 6. `link_issue_to_pr(issue_key, pr_url)`
**Link PR to ticket**
```python
jira.link_issue_to_pr("PAYMENT-123", "https://github.com/.../pull/42")
# Adds comment with PR link
```

### 7. `transition_issue(issue_key, target_status)`
**Change ticket status**
```python
jira.transition_issue("PAYMENT-123", "In Progress")
# Moves ticket to In Progress
```

---

## 📤 Return Format

All methods return a dictionary:

**Success:**
```python
{
    "success": True,
    "issue_key": "PAYMENT-123",
    "issue_url": "https://..."
}
```

**Error:**
```python
{
    "success": False,
    "error": "Error message from Jira"
}
```

---

## 🔑 Required Credentials

- **Jira URL** - Your Atlassian instance
- **Username** - Email address
- **API Token** - From account settings

```python
url = os.getenv("JIRA_URL")
username = os.getenv("JIRA_USERNAME")
api_token = os.getenv("JIRA_API_TOKEN")
```

---

## 💡 Real-World Workflow

```
Vulnerability Found
    ↓
jira.create_issue("SECURITY", "SQL Injection", priority="Critical")
    ↓
jira.transition_issue(issue_key, "In Progress")
    ↓
Auto-fix code & create PR
    ↓
jira.link_issue_to_pr(issue_key, pr_url)
    ↓
jira.add_comment(issue_key, "Fix deployed ✅")
    ↓
jira.transition_issue(issue_key, "Done")
    ↓
Vulnerability tracked from detection to fix
```

---

## ⚠️ Error Handling

All methods catch exceptions:
- Network errors
- Authentication failures
- Invalid issue keys
- Transition errors
- Jira API errors

Returns error dict with details.

---

## 🔗 Related Files
- `skills/code_analysis_skill.py` - Finds vulnerabilities
- `skills/github_skill.py` - Creates PRs
- `skills/jira_skill.py` - Tracks in Jira ← YOU ARE HERE
- `orchestrator/vulnerability_orchestrator.py` - Orchestrates workflow

---

## 📊 Test Coverage
Currently: **22%** - Needs more integration tests

---

## 🚀 Complete Example

```python
from skills.jira_skill import JiraSkill
import os

# Initialize
jira = JiraSkill(
    os.getenv("JIRA_URL"),
    os.getenv("JIRA_USERNAME"),
    os.getenv("JIRA_API_TOKEN")
)

# Create issue for vulnerability
issue = jira.create_issue(
    "PAYMENT",
    "Security: XSS Vulnerability",
    issue_type="Bug",
    description="Cross-site scripting in payment form",
    priority="High",
    labels=["security", "xss"]
)
print(f"Created: {issue['issue_url']}")

# Mark as in progress
jira.transition_issue(issue['issue_key'], "In Progress")

# Comment with fix details
jira.add_comment(
    issue['issue_key'],
    "Fixed innerHTML assignment. Using textContent instead."
)

# Link to PR with fix
jira.link_issue_to_pr(
    issue['issue_key'],
    "https://github.com/Hrushit97/Vernfix/pull/123"
)

# Mark as done
jira.transition_issue(issue['issue_key'], "Done")
```

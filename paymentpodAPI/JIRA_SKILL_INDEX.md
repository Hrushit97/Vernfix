# Jira Integration Skill - Documentation Index

## 📚 Available Documentation

### 1. **JIRA_SKILL_QUICK_REFERENCE.md** ⭐ START HERE
- One-page overview
- 7 core methods
- Return format
- Complete working example
- **Best for:** Quick lookup & understanding basics

### 2. **JIRA_SKILL_EXPLAINED.md**
- Detailed docstring explanation
- Purpose & imports
- All 7 methods with code examples
- Error handling explained
- Real-world workflow
- **Best for:** Learning how to use it

### 3. **JIRA_SKILL_TECHNICAL_DETAILS.md**
- Line-by-line code breakdown
- Architecture details
- Each method's logic explained
- Authentication requirements
- Integration points
- **Best for:** Understanding implementation

---

## 🎯 Quick Path Based on Your Need

### 👤 I just want to understand what it does
→ Read **QUICK_REFERENCE.md** (5 mins)

### 💻 I want to use it in my code
→ Read **JIRA_SKILL_EXPLAINED.md** (15 mins)

### 🔧 I need to modify or debug it
→ Read **TECHNICAL_DETAILS.md** + view code (30 mins)

---

## 📖 Docstring Explained

```python
"""
Jira Integration Skill
Handles all Jira operations: ticket creation, updates, tracking vulnerabilities
"""
```

**Translation:** This module automates Jira ticket management for security vulnerabilities

---

## 🎯 What It Does (7 Methods)

| Method | Purpose | Use For |
|--------|---------|---------|
| `__init__` | Connect to Jira | Initialize connection |
| `create_issue` | Create new ticket | Report vulnerabilities |
| `get_issue` | Fetch ticket details | Check ticket status |
| `update_issue` | Modify ticket | Update ticket info |
| `add_comment` | Comment on ticket | Post progress updates |
| `link_issue_to_pr` | Link PR to ticket | Connect fix to issue |
| `transition_issue` | Change status | Move through workflow |

---

## 💡 Real-World Use Case

```
Vulnerability Found in Code
    ↓
create_issue("PAYMENT", "SQL Injection")
    ↓
Jira ticket created (PAYMENT-123)
    ↓
transition_issue(→ "In Progress")
    ↓
Auto-fix code & create PR
    ↓
link_issue_to_pr(pr_url)
    ↓
add_comment("Fix deployed ✅")
    ↓
transition_issue(→ "Done")
    ↓
Vulnerability tracked from detection to fix
```

---

## 🔑 Key Concepts

### Jira Tickets
- Vulnerability tracking mechanism
- Has key: "PROJECT-123"
- Properties: title, status, priority

### Issue Types
- Bug (default for vulnerabilities)
- Task
- Story
- Epic

### Priority Levels
- Critical
- High (default)
- Medium
- Low

### Status Workflow
- Open → In Progress → In Review → Done

---

## 🔐 Authentication

Requires:
- **Jira URL** - Your instance
- **Username** - Your Jira email
- **API Token** - From Atlassian account

```python
jira = JiraSkill(
    os.getenv("JIRA_URL"),
    os.getenv("JIRA_USERNAME"),
    os.getenv("JIRA_API_TOKEN")
)
```

---

## 📊 Coverage
Currently: **22%** test coverage
Needed: More integration tests

---

## 🔗 Related Skills

- **code_analysis_skill.py** - Finds vulnerabilities
- **github_skill.py** - Creates PRs with fixes
- **jira_skill.py** - Tracks in Jira ← YOU ARE HERE
- **orchestrator** - Orchestrates all skills

---

## 📁 File Location
`paymentpodAPI/skills/jira_skill.py` (110 lines)

---

## 🚀 Complete Minimal Example

```python
from skills.jira_skill import JiraSkill
import os

# Initialize
jira = JiraSkill(
    os.getenv("JIRA_URL"),
    os.getenv("JIRA_USERNAME"),
    os.getenv("JIRA_API_TOKEN")
)

# Create issue
issue = jira.create_issue(
    "PAYMENT",
    "SQL Injection in login",
    issue_type="Bug",
    priority="Critical",
    labels=["security"]
)

# Link to PR
jira.link_issue_to_pr(issue['issue_key'], "https://github.com/.../pull/42")

# Mark as done
jira.transition_issue(issue['issue_key'], "Done")
```

---

## ✨ Key Features

✅ Full Jira API integration
✅ Ticket creation & management
✅ Status transitions
✅ PR linking capability
✅ Comment posting
✅ Ticket updates
✅ Comprehensive error handling
✅ Logging for all operations

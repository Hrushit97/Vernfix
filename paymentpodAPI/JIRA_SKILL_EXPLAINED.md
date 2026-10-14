# Jira Integration Skill - Complete Explanation

## 📖 Docstring Meaning

```python
"""
Jira Integration Skill
Handles all Jira operations: ticket creation, updates, tracking vulnerabilities
"""
```

**Translation:**
- **Jira Integration** = Connects to Jira project management system
- **Skill** = Reusable component in vulnerability orchestrator
- **Ticket creation** = Creating new issue tickets
- **Updates** = Modifying existing tickets
- **Tracking vulnerabilities** = Managing security issues

---

## 🎯 Purpose

Automate Jira ticket management for security vulnerabilities:
- Create tickets when vulnerabilities are found
- Update tickets as fixes are made
- Link to GitHub PRs that fix vulnerabilities
- Track vulnerability lifecycle

---

## 📚 Imports & Setup

```python
from jira import JIRA              # Jira Python library
from typing import Dict, List, Optional  # Type hints
import logging                      # Error tracking
```

**JIRA Library:** Official Python client for Jira API

---

## 🏗️ Class Architecture

### Initialization (Lines 17-20)
```python
def __init__(self, url: str, username: str, api_token: str):
    self.jira = JIRA(url, basic_auth=(username, api_token))
    logger.info(f"Connected to Jira at {url}")
```

**Parameters:**
- `url` - Jira server URL
- `username` - Jira username
- `api_token` - API authentication token

**Example:**
```python
jira = JiraSkill(
    "https://your-domain.atlassian.net",
    "your-email@example.com",
    "YOUR_API_TOKEN"
)
```

---

## 🔧 7 Methods (Ordered by Usage)

### 1️⃣ **create_issue()** - Lines 22-52
**Create new vulnerability ticket**

```python
def create_issue(self, project_key: str, summary: str, issue_type: str = "Bug",
                description: str = "", priority: str = "High", labels: List[str] = None)
```

**Parameters:**
- `project_key` - Jira project (e.g., "PAYMENT")
- `summary` - Ticket title
- `issue_type` - Bug, Task, etc. (default: "Bug")
- `description` - Ticket details
- `priority` - High, Medium, Low (default: "High")
- `labels` - Tags for filtering

**Returns:**
```python
{
    "success": True,
    "issue_key": "PAYMENT-123",
    "issue_url": "https://...atlassian.net/browse/PAYMENT-123"
}
```

---

### 2️⃣ **get_issue()** - Lines 76-90
**Get ticket details**

```python
def get_issue(self, issue_key: str) -> Dict
```

**Parameters:**
- `issue_key` - Ticket ID (e.g., "PAYMENT-123")

**Returns:**
```python
{
    "success": True,
    "key": "PAYMENT-123",
    "summary": "SQL Injection in login",
    "status": "Open",
    "priority": "High",
    "description": "Details..."
}
```

---

### 3️⃣ **update_issue()** - Lines 54-63
**Modify ticket**

```python
def update_issue(self, issue_key: str, updates: Dict) -> Dict
```

**Parameters:**
- `issue_key` - Ticket ID
- `updates` - Fields to update (dict)

**Example:**
```python
jira.update_issue("PAYMENT-123", {
    "summary": "Updated title",
    "priority": {"name": "Critical"}
})
```

---

### 4️⃣ **add_comment()** - Lines 65-74
**Comment on ticket**

```python
def add_comment(self, issue_key: str, comment: str) -> Dict
```

**Use Cases:**
- Post progress updates
- Link to GitHub PRs
- Add vulnerability details

---

### 5️⃣ **link_issue_to_pr()** - Lines 92-95
**Link PR to ticket**

```python
def link_issue_to_pr(self, issue_key: str, pr_url: str) -> Dict
```

**Internally calls:** `add_comment()` with PR link

**Example:**
```python
jira.link_issue_to_pr("PAYMENT-123", "https://github.com/.../pull/42")
# Creates comment: "Pull Request: https://github.com/.../pull/42"
```

---

### 6️⃣ **transition_issue()** - Lines 97-109
**Change ticket status**

```python
def transition_issue(self, issue_key: str, target_status: str) -> Dict
```

**Status Flow:**
```
Open → In Progress → In Review → Done
```

**Example:**
```python
jira.transition_issue("PAYMENT-123", "In Progress")
# Moves ticket to In Progress status
```

---

### 7️⃣ **Error Handling**
All methods wrap operations in try-except:
```python
except Exception as e:
    logger.error(f"Failed to ...: {e}")
    return {"success": False, "error": str(e)}
```

---

## 💻 Usage Example

```python
from skills.jira_skill import JiraSkill

# Initialize
jira = JiraSkill(
    "https://your-domain.atlassian.net",
    "your-email@example.com",
    "YOUR_API_TOKEN"
)

# 1. Create issue for vulnerability
issue = jira.create_issue(
    "PAYMENT",
    "Security: SQL Injection in login endpoint",
    issue_type="Bug",
    description="SQL injection vulnerability in user authentication",
    priority="Critical",
    labels=["security", "sql-injection"]
)
print(f"Created: {issue['issue_url']}")

# 2. Get issue details
details = jira.get_issue("PAYMENT-123")
print(f"Status: {details['status']}")

# 3. Update issue
jira.update_issue("PAYMENT-123", {
    "assignee": {"name": "developer@example.com"}
})

# 4. Add comment
jira.add_comment("PAYMENT-123", "Started fixing SQL injection")

# 5. Link to PR
jira.link_issue_to_pr("PAYMENT-123", "https://github.com/.../pull/42")

# 6. Transition status
jira.transition_issue("PAYMENT-123", "In Progress")

# 7. Final update
jira.add_comment("PAYMENT-123", "Fix completed and tested")
jira.transition_issue("PAYMENT-123", "Done")
```

---

## 🔄 Real Vulnerability Workflow

```
Vulnerability Detected
    ↓
create_issue("SECURITY", "SQL Injection")
    ↓
JIRA ticket created (SECURITY-42)
    ↓
transition_issue(→ "In Progress")
    ↓
Auto-fix code & create PR
    ↓
link_issue_to_pr(pr_url)
    ↓
add_comment("Fix deployed")
    ↓
transition_issue(→ "Done")
    ↓
Ticket closed
```

---

## 🔐 Authentication

**Required:**
- Jira URL (your instance)
- Username (email)
- API Token (from Atlassian account settings)

**Setup:**
```python
url = "https://your-company.atlassian.net"
username = os.getenv("JIRA_USERNAME")
api_token = os.getenv("JIRA_API_TOKEN")
jira = JiraSkill(url, username, api_token)
```

---

## 📊 Test Coverage
Currently: **22%** - Needs more integration tests

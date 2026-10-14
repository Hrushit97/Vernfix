# Jira Integration Skill - Technical Details

## 📖 Module Docstring (Lines 1-4)

```python
"""
Jira Integration Skill
Handles all Jira operations: ticket creation, updates, tracking vulnerabilities
"""
```

**Components:**
- **Jira Integration** = Bridge to Jira project management
- **Skill** = Reusable component in orchestrator
- **Ticket creation** = Creating new issues
- **Updates** = Modifying issue properties
- **Tracking vulnerabilities** = Managing security tickets

---

## 📚 Dependencies (Lines 6-11)

```python
import json                         # Data serialization
from typing import Dict, List, Optional  # Type hints
from jira import JIRA              # Jira Python library
import logging                      # Error tracking
```

**JIRA Library:** Official Jira Python client for API communication

---

## 🏗️ Class Architecture

### Initialization (Lines 17-20)
```python
def __init__(self, url: str, username: str, api_token: str):
    self.jira = JIRA(url, basic_auth=(username, api_token))
    logger.info(f"Connected to Jira at {url}")
```

**Flow:**
1. Accept Jira connection parameters
2. Create JIRA client with authentication
3. Verify connection
4. Log successful login

---

## 🔧 Method Details

### 1. create_issue() - Lines 22-52
**Purpose:** Create new vulnerability ticket

**Parameters:**
```python
project_key: str              # Jira project (e.g., "PAYMENT")
summary: str                  # Ticket title
issue_type: str = "Bug"       # Default: Bug
description: str = ""         # Ticket details
priority: str = "High"        # Default: High
labels: List[str] = None      # Tags for filtering
```

**Internal Logic:**
```python
# Step 1: Build issue dict
issue_dict = {
    "project": {"key": project_key},
    "summary": summary,
    "description": description,
    "issuetype": {"name": issue_type},
    "priority": {"name": priority},
}

# Step 2: Add labels if provided
if labels:
    issue_dict["labels"] = labels

# Step 3: Create issue via API
issue = self.jira.create_issue(fields=issue_dict)

# Step 4: Return details
return {
    "success": True,
    "issue_key": issue.key,
    "issue_url": f"{self.jira.client_info.url}/browse/{issue.key}",
}
```

---

### 2. get_issue() - Lines 76-90
**Purpose:** Retrieve ticket information

**Logic:**
```python
issue = self.jira.issue(issue_key)  # Get issue object
return {
    "key": issue.key,
    "summary": issue.fields.summary,
    "status": str(issue.fields.status),
    "priority": str(issue.fields.priority),
    "description": issue.fields.description,
}
```

**Returns:** Issue details (key, summary, status, priority, description)

---

### 3. update_issue() - Lines 54-63
**Purpose:** Modify existing ticket

**Logic:**
```python
issue = self.jira.issue(issue_key)  # Get issue
issue.update(**updates)              # Apply updates
```

**Example Updates:**
```python
{
    "summary": "New title",
    "description": "New description",
    "priority": {"name": "Critical"}
}
```

---

### 4. add_comment() - Lines 65-74
**Purpose:** Add comment to ticket

**Logic:**
```python
issue = self.jira.issue(issue_key)
self.jira.add_comment(issue, comment)
```

**Use Cases:**
- Progress updates
- PR links
- Vulnerability details
- Fix confirmation

---

### 5. link_issue_to_pr() - Lines 92-95
**Purpose:** Link GitHub PR to ticket

**Logic:**
```python
comment = f"Pull Request: {pr_url}"
return self.add_comment(issue_key, comment)
```

**Result:** Adds PR link as comment

---

### 6. transition_issue() - Lines 97-109
**Purpose:** Change ticket status

**Logic:**
```python
issue = self.jira.issue(issue_key)
transitions = self.jira.transitions(issue)  # Get available transitions

for transition in transitions:
    if transition["to"]["name"].lower() == target_status.lower():
        self.jira.transition_issue(issue, transition["id"])
        return {"success": True, "new_status": target_status}
```

**Status Flow:**
```
Open → In Progress → In Review → Done
```

---

## ⚠️ Error Handling Pattern

All methods follow:
```python
try:
    # Jira API operation
except Exception as e:
    logger.error(f"Failed to ...: {e}")
    return {"success": False, "error": str(e)}
```

**Catches:**
- Network errors
- Authentication failures (401)
- Invalid issue key (404)
- Transition errors
- Jira API errors

---

## 🔐 Authentication

**Required:**
- `url` - Jira server (e.g., "https://company.atlassian.net")
- `username` - Jira user email
- `api_token` - API token from Atlassian

**JIRA() call:**
```python
self.jira = JIRA(url, basic_auth=(username, api_token))
```

---

## 📊 Return Value Pattern

**Consistent format:**
```python
{
    "success": True/False,
    "specific_key": value,  # Method-specific data
    "error": "message"      # If success=False
}
```

---

## 🚀 Integration Points

Used by:
- `vulnerability_orchestrator.py` - Orchestrates workflow
- `code_analysis_skill.py` - Reports vulnerabilities
- `github_skill.py` - Links PRs to tickets

---

## 📈 Test Coverage
Currently: **22%** coverage
Needs: Integration tests for all methods

---

## 🔄 Typical Workflow

```
1. Code Analysis finds vulnerability
2. create_issue() - Create Jira ticket
3. GitHub creates fix branch
4. GitHub creates PR
5. link_issue_to_pr() - Connect PR to ticket
6. transition_issue() - Mark as "In Progress"
7. add_comment() - Post fix details
8. transition_issue() - Mark as "Done"
9. Ticket closed, vulnerability resolved
```

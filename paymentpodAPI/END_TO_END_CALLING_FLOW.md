# End-to-End File Calling Flow Guide

## 🎯 Overview

This guide explains the **complete calling flow** for `get_existing_security_issues()` from initial user request through all files to Jira and back.

---

## 📊 Complete Call Stack

```
USER CODE
    ↓
main.py or CLI
    ↓
orchestrator/vulnerability_orchestrator.py
    ↓
skills/jira_skill.py
    ↓
Jira REST API
    ↓
Jira Database
    ↓ (response)
Jira REST API
    ↓
skills/jira_skill.py
    ↓
orchestrator/vulnerability_orchestrator.py
    ↓
USER CODE (with results)
```

---

## 🔄 Step-by-Step Flow

### **Level 1: User Code (main.py)**

```python
# File: main.py or your application code
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Step 1: Create configuration
config = {
    'github_token': 'ghp_...',
    'jira_url': 'https://domain.atlassian.net',
    'jira_username': 'email@example.com',
    'jira_api_token': 'YOUR_TOKEN',
    'repo_path': '/path/to/repo',
    'git_username': 'username',
    'git_email': 'email@example.com',
    'github_repo': 'Vernfix',
    'github_owner': 'Hrushit97'
}

# Step 2: Initialize orchestrator
orchestrator = VulnerabilityOrchestrator(config)

# Step 3: CALL THE METHOD ← YOU ARE HERE
existing_issues = orchestrator.get_existing_security_issues('PAYMENT')

# Step 4: Handle results
if existing_issues['success']:
    print(f"Found {existing_issues['count']} issues")
    for issue in existing_issues['issues']:
        print(f"  - {issue['key']}: {issue['summary']}")
else:
    print(f"Error: {existing_issues['error']}")
```

---

### **Level 2: Orchestrator Method**

```python
# File: orchestrator/vulnerability_orchestrator.py

def get_existing_security_issues(self, project_key: str) -> Dict:
    """Get all existing security-related Jira issues"""
    try:
        # Log the request
        logger.info(f"Fetching existing security issues for {project_key}")
        
        # Step 1: CALL JIRA SKILL ↓
        result = self.jira_skill.get_issues_by_labels(
            project_key,
            ['security', 'automated-fix']
        )
        
        # Step 2: Check if call succeeded
        if result.get('success'):
            logger.info(f"Found {result['count']} existing security issues")
            # Step 3: Return result to user ↓
            return result
        else:
            # Step 3: Return error to user ↓
            logger.warning(f"Failed to fetch: {result.get('error')}")
            return {
                'success': False,
                'error': result.get('error'),
                'issues': []
            }
    except Exception as e:
        # Handle exceptions
        logger.error(f"Error getting issues: {e}")
        return {'success': False, 'error': str(e), 'issues': []}
```

---

### **Level 3: Jira Skill Method**

```python
# File: skills/jira_skill.py

def get_issues_by_labels(self, project_key: str, labels: List[str]) -> Dict:
    """Get issues by labels"""
    try:
        # Step 1: Build JQL query
        label_query = " OR ".join([f'labels in ({label})' for label in labels])
        jql = f"project = {project_key} AND ({label_query})"
        
        logger.info(f"Searching with JQL: {jql}")
        
        # Step 2: CALL JIRA API ↓
        issues = self.jira.search_issues(jql, maxResults=100)
        
        # Step 3: Process results
        issues_list = []
        for issue in issues:
            issues_list.append({
                'key': issue.key,
                'summary': issue.fields.summary,
                'status': str(issue.fields.status),
                'labels': issue.fields.labels,
            })
        
        # Step 4: Return to orchestrator ↓
        return {
            'success': True,
            'count': len(issues_list),
            'issues': issues_list
        }
    except Exception as e:
        logger.error(f"Failed to get issues: {e}")
        # Return error ↓
        return {'success': False, 'error': str(e), 'issues': []}
```

---

### **Level 4: Jira API**

```python
# Pseudo-code for Jira REST API call:

# Inside self.jira.search_issues():

# HTTP Request:
POST https://domain.atlassian.net/rest/api/2/search
Headers:
  Authorization: Basic [base64(email@example.com:api_token)]
  Content-Type: application/json

Body:
{
  "jql": "project = PAYMENT AND (labels in (security) OR labels in (automated-fix))",
  "maxResults": 100
}

# HTTP Response:
{
  "issues": [
    {
      "key": "PAYMENT-123",
      "fields": {
        "summary": "[CRITICAL] Fix SQL Injection in app.py",
        "status": { "name": "Open" },
        "labels": ["security", "automated-fix"]
      }
    },
    {
      "key": "PAYMENT-124",
      "fields": { ... }
    }
  ]
}
```

---

## 🔙 Return Value Flow

### **Level 4 → Level 3 (Jira API to Jira Skill)**

```python
{
    'success': True,
    'count': 2,
    'issues': [
        {
            'key': 'PAYMENT-123',
            'summary': '[CRITICAL] Fix SQL Injection in app.py',
            'status': 'Open',
            'labels': ['security', 'automated-fix']
        },
        {
            'key': 'PAYMENT-124',
            'summary': '[HIGH] Fix XSS Vulnerability in form.js',
            'status': 'In Progress',
            'labels': ['security', 'automated-fix']
        }
    ]
}
```

### **Level 3 → Level 2 (Jira Skill to Orchestrator)**

```python
# Same format returned
{
    'success': True,
    'count': 2,
    'issues': [...]
}
```

### **Level 2 → Level 1 (Orchestrator to User Code)**

```python
# Same format returned to your code
{
    'success': True,
    'count': 2,
    'issues': [...]
}
```

---

## 📁 Files Involved

| File | Purpose | Method |
|------|---------|--------|
| `main.py` | Entry point | `orchestrator.get_existing_security_issues()` |
| `orchestrator/vulnerability_orchestrator.py` | Coordination | `get_existing_security_issues()` |
| `skills/jira_skill.py` | Jira operations | `get_issues_by_labels()` |
| `jira` library | REST client | `search_issues()` |
| Jira API | Backend | HTTP endpoint |

---

## 🔐 Authentication Flow

```
User provides credentials:
  - jira_url: https://domain.atlassian.net
  - jira_username: email@example.com
  - jira_api_token: YOUR_TOKEN

JiraSkill.__init__():
  Creates JIRA client with credentials
  
Each API call:
  Automatically includes authentication
  Sends as HTTP Basic Auth header
  
Jira API:
  Validates credentials
  Returns data or error
```

---

## ❌ Error Handling Flow

```
Level 1: User Code
    ↓
Level 2: Orchestrator
    ↓ try-catch
Level 3: Jira Skill
    ↓ try-catch
Level 4: Jira API
    ↓ Connection error or bad response
Level 3: Exception caught
    ↓ Logger.error()
Returns: {'success': False, 'error': 'message'}
    ↓
Level 2: Gets error response
    ↓ Logs warning
Returns: {'success': False, 'error': 'message', 'issues': []}
    ↓
Level 1: User Code
    ↓ Checks success flag
Handles error appropriately
```

---

## 📊 Data Types Through Flow

```
Input: project_key: str = 'PAYMENT'

↓ Orchestrator passes to Jira Skill:
  project_key: str
  labels: List[str] = ['security', 'automated-fix']

↓ Jira Skill builds JQL query:
  jql: str = "project = PAYMENT AND (labels in (security) OR ...)"

↓ Jira API returns:
  issues: List of Jira Issue objects

↓ Jira Skill converts to Dict:
  issues: List[Dict]

↓ Orchestrator returns:
  Dict with 'success', 'count', 'issues'

↓ User code receives:
  Dict[str, Any]
```

---

## 🧪 Testing the Flow

```python
# Verify each level works:

# Level 1: Import
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Level 2: Initialize
orchestrator = VulnerabilityOrchestrator(config)

# Level 3: Call method
result = orchestrator.get_existing_security_issues('PAYMENT')

# Level 4: Check result
assert result['success'] == True
assert result['count'] >= 0
assert 'issues' in result
for issue in result['issues']:
    assert 'key' in issue
    assert 'summary' in issue
    assert 'status' in issue
```

---

## 📈 Performance Notes

| Operation | Time | Notes |
|-----------|------|-------|
| Orchestrator call | < 1ms | Local method call |
| Network latency | 100-500ms | Internet to Jira |
| Jira search | 50-200ms | Database query |
| Response parse | 10-50ms | Convert to Python objects |
| **Total** | **~200-750ms** | Typical response time |

---

## 🎯 Common Use Cases

### **Before Running Workflow**
```python
existing = orchestrator.get_existing_security_issues('PAYMENT')
if existing['count'] > 5:
    print("Many existing issues. Review before fixing.")
```

### **In Conditional Logic**
```python
if orchestrator.get_existing_security_issues('PAYMENT')['count'] > 0:
    print("Security issues exist. Prioritize fixes.")
```

### **For Reporting**
```python
existing = orchestrator.get_existing_security_issues('PAYMENT')
for issue in existing['issues']:
    print(f"{issue['key']}: {issue['status']}")
```

---

## 💾 Data Storage

```
Jira Database
    ↓
Stores: Issues with labels, summaries, status
    ↓
On API call: Searches by JQL
    ↓
Returns: Matching issues
    ↓
JiraSkill: Converts to Python Dict
    ↓
Orchestrator: Passes to user
    ↓
User Code: Uses the data
```

No local caching - always gets fresh data from Jira!

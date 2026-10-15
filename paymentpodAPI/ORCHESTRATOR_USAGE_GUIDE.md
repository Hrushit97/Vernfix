# Vulnerability Orchestrator - Complete Usage Guide

## 📋 Quick Overview

The **VulnerabilityOrchestrator** is the central engine that automates security vulnerability detection, fixing, and tracking through a 9-step workflow.

---

## 🚀 Getting Started

### Step 1: Install Dependencies
```bash
pip install PyGithub jira
```

### Step 2: Create Configuration
```python
config = {
    'github_token': 'ghp_YOUR_TOKEN_HERE',
    'github_repo': 'Vernfix',
    'github_owner': 'Hrushit97',
    'jira_url': 'https://domain.atlassian.net',
    'jira_username': 'email@example.com',
    'jira_api_token': 'YOUR_JIRA_TOKEN',
    'repo_path': '/path/to/local/repo',
    'git_username': 'Hrushit97',
    'git_email': 'email@example.com'
}
```

### Step 3: Initialize Orchestrator
```python
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

orchestrator = VulnerabilityOrchestrator(config)
```

---

## 📊 Execute Workflow

### Basic Usage
```python
result = orchestrator.execute_workflow(
    repo_name='Vernfix',
    repo_owner='Hrushit97',
    project_key='PAYMENT',
    analyze_path='/path/to/src'
)

print(f"Vulnerabilities found: {result['vulnerabilities_found']}")
print(f"Vulnerabilities fixed: {result['vulnerabilities_fixed']}")
print(f"PR created: {result['pr_url']}")
```

### Advanced Options
```python
result = orchestrator.execute_workflow(
    repo_name='Vernfix',
    repo_owner='Hrushit97',
    project_key='PAYMENT',
    analyze_path='/path/to/src',
    base_branch='develop',           # PR base branch
    skip_jira=False,                 # Skip Jira ticket creation
    skip_pr=False                    # Skip PR creation
)
```

---

## 📤 Response Format

### Success Response
```python
{
    'success': True,
    'vulnerabilities_found': 5,
    'vulnerabilities_fixed': 4,
    'vulnerabilities_failed': 1,
    'jira_issues': ['PAYMENT-123', 'PAYMENT-124', ...],
    'pr_url': 'https://github.com/Hrushit97/Vernfix/pull/42',
    'pr_number': 42,
    'failed_fixes': [
        {'vuln': {...}, 'error': 'Error message'}
    ],
    'duration_seconds': 45.3
}
```

### Error Response
```python
{
    'success': False,
    'error': 'Error message',
    'vulnerabilities_found': 0,
    'vulnerabilities_fixed': 0,
    'jira_issues': [],
    'pr_url': None,
    'pr_number': None
}
```

---

## 🔄 The 9-Step Workflow

1. **Get Repository Info** - Fetch GitHub repo details
2. **Analyze Code** - Scan for vulnerabilities
3. **Create Jira Issues** - Track in Jira
4. **Create Branch** - Create feature branch
5. **Fix Vulnerabilities** - Apply auto-fixes
6. **Commit Changes** - Git commit
7. **Push Branch** - Push to remote
8. **Create PR** - Create pull request
9. **Link PR to Jira** - Connect PR to tickets

---

## 💡 Usage Examples

### Example 1: Complete Automated Fix
```python
config = {...}
orchestrator = VulnerabilityOrchestrator(config)

result = orchestrator.execute_workflow(
    'Vernfix', 'Hrushit97', 'PAYMENT', '/src'
)

if result['success']:
    print(f"✓ Fixed {result['vulnerabilities_fixed']} issues")
    print(f"✓ PR: {result['pr_number']}")
else:
    print(f"✗ Error: {result['error']}")
```

### Example 2: Skip PR Creation
```python
result = orchestrator.execute_workflow(
    'Vernfix', 'Hrushit97', 'PAYMENT', '/src',
    skip_pr=True  # Only create Jira tickets & fixes
)
```

### Example 3: Check Workflow Status
```python
status = orchestrator.get_workflow_status()
print(f"Status: {status['status']}")
print(f"All skills ready: {all(status['skills_ready'].values())}")
```

---

## 🛠️ Configuration Details

| Key | Purpose | Example |
|-----|---------|---------|
| `github_token` | GitHub authentication | `ghp_xxx...` |
| `github_repo` | Repository name | `Vernfix` |
| `github_owner` | Repository owner | `Hrushit97` |
| `jira_url` | Jira instance URL | `https://domain.atlassian.net` |
| `jira_username` | Jira user email | `user@example.com` |
| `jira_api_token` | Jira API token | `jira_token` |
| `repo_path` | Local repo path | `/path/to/repo` |
| `git_username` | Git committer name | `Hrushit97` |
| `git_email` | Git committer email | `user@example.com` |

---

## ⚠️ Error Handling

```python
result = orchestrator.execute_workflow(...)

if not result['success']:
    error = result['error']
    # Handle error
    logger.error(f"Workflow failed: {error}")

# Check partial success
if result['vulnerabilities_failed'] > 0:
    for failed in result['failed_fixes']:
        print(f"Failed: {failed['vuln']['file']}")
        print(f"Error: {failed['error']}")
```

---

## 🔐 Security Best Practices

1. **Never hardcode credentials** - Use environment variables
2. **Rotate API tokens** - Regularly update credentials
3. **Validate paths** - Prevent directory traversal
4. **Log securely** - Don't log sensitive data
5. **Use HTTPS** - Encrypt all communications

---

## 🧪 Testing

```bash
python -m unittest tests.test_orchestrator -v
```

---

## 📚 Related Files

- `orchestrator/vulnerability_orchestrator.py` - Main implementation
- `skills/` - Individual skill modules
- `tests/test_orchestrator.py` - Unit tests
- `VULNERABILITY_ORCHESTRATOR_DETAILED.md` - Technical details

---

## 🎯 Next Steps

1. Set up configuration
2. Initialize orchestrator
3. Call `execute_workflow()`
4. Monitor progress via logs
5. Review created PR & Jira tickets
6. Merge PR after review

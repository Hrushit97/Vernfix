# Jira-GitHub Synchronization Guide

## 🔄 Overview

The VulnerabilityOrchestrator now includes built-in **Jira-GitHub synchronization** to prevent duplicate issue creation and keep security tracking consistent across platforms.

---

## ✨ What's New

### Enhanced Jira Skill Methods

#### 1. **search_issues()**
Search for existing Jira issues by project and criteria
```python
result = jira_skill.search_issues(
    project_key='PAYMENT',
    summary_keyword='SQL Injection',
    status='Open'
)
# Returns: {'success': True, 'count': N, 'issues': [...]}
```

#### 2. **find_duplicate_issues()**
Find duplicate/existing issues for a specific vulnerability
```python
result = jira_skill.find_duplicate_issues(
    project_key='PAYMENT',
    file_path='/src/app.py',
    vuln_type='SQL Injection'
)
# Returns: {
#   'success': True,
#   'found_duplicates': True/False,
#   'duplicates': [...]
# }
```

#### 3. **get_issues_by_labels()**
Get all issues with specific labels
```python
result = jira_skill.get_issues_by_labels(
    project_key='PAYMENT',
    labels=['security', 'automated-fix']
)
# Returns: {'success': True, 'count': N, 'issues': [...]}
```

### Enhanced Orchestrator Methods

#### 1. **get_existing_security_issues()**
Retrieve all existing security-labeled issues
```python
issues = orchestrator.get_existing_security_issues('PAYMENT')
# Returns list of all security issues in project
```

#### 2. **sync_jira_to_github()**
Sync Jira issues to GitHub
```python
result = orchestrator.sync_jira_to_github(
    repo_name='Vernfix',
    repo_owner='Hrushit97',
    project_key='PAYMENT'
)
# Returns: {'success': True, 'synced_count': N, 'issues': [...]}
```

---

## 🔄 How Sync Works

### During Vulnerability Fix Workflow

```
Step 3: Create Jira Issues
    ↓
For each vulnerability:
    ↓
Check: Does duplicate issue exist?
    ↓
YES: Use existing issue (link to PR)
NO: Create new issue
    ↓
Result: Prevents duplicate tracking
```

### Duplicate Detection Logic

Issues are considered duplicates if they have:
1. **Same file path** - From vulnerability location
2. **Same vulnerability type** - SQL Injection, XSS, etc.
3. **Same project** - Jira project key

---

## 📊 Usage Examples

### Example 1: Sync During Workflow

```python
result = orchestrator.execute_workflow(
    repo_name='Vernfix',
    repo_owner='Hrushit97',
    project_key='PAYMENT',
    analyze_path='/src'
)

# Output includes:
# - vulnerabilities_found: 10
# - vulnerabilities_fixed: 8
# - jira_issues: [
#     'PAYMENT-123',  # Existing (synced)
#     'PAYMENT-124',  # Existing (synced)
#     'PAYMENT-456',  # New (created)
#   ]
```

### Example 2: Check Existing Issues

```python
# Before running workflow, check what exists
existing = orchestrator.get_existing_security_issues('PAYMENT')
print(f"Found {existing['count']} existing security issues")

for issue in existing['issues']:
    print(f"  - {issue['key']}: {issue['summary']}")
```

### Example 3: Search Specific Issues

```python
# Search for SQL injection issues
result = jira_skill.search_issues(
    project_key='PAYMENT',
    summary_keyword='SQL Injection'
)

for issue in result['issues']:
    print(f"{issue['key']}: {issue['status']}")
```

---

## 📈 Benefits

✅ **No Duplicate Tracking** - Same issue not created twice
✅ **Consistent Status** - Issue status synced across platforms
✅ **Better Collaboration** - Team sees all related issues
✅ **Audit Trail** - Complete history of all fixes
✅ **Smart Linking** - PR linked to correct ticket

---

## 🔍 Sync Logic

### When Sync Occurs

1. **During Workflow Execution**
   - Each vulnerability checked for duplicates
   - Existing issues reused
   - New issues created only if needed

2. **Manual Sync**
   - Call `sync_jira_to_github()` anytime
   - Fetch all security issues
   - Compare with GitHub PRs

---

## ⚙️ Configuration

No additional configuration needed! Sync works automatically with existing config.

The orchestrator uses:
- `project_key` parameter for Jira project
- `github_repo` and `github_owner` for GitHub repo
- Labels: `['security', 'automated-fix']` for filtering

---

## 🧪 Testing Sync

```python
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

config = {...}
orchestrator = VulnerabilityOrchestrator(config)

# Test 1: Check existing issues
existing = orchestrator.get_existing_security_issues('PAYMENT')
print(f"Existing: {existing['count']}")

# Test 2: Manual sync
sync_result = orchestrator.sync_jira_to_github(
    'Vernfix', 'Hrushit97', 'PAYMENT'
)
print(f"Synced: {sync_result['synced_count']}")

# Test 3: Full workflow with sync
result = orchestrator.execute_workflow(
    'Vernfix', 'Hrushit97', 'PAYMENT', '/src'
)
print(f"Issues: {len(result['jira_issues'])}")
```

---

## 📋 Response Format

### get_existing_security_issues()
```python
{
    'success': True,
    'count': 5,
    'issues': [
        {
            'key': 'PAYMENT-123',
            'summary': '[CRITICAL] Fix SQL Injection in app.py',
            'status': 'Open',
            'labels': ['security', 'automated-fix']
        },
        ...
    ]
}
```

### find_duplicate_issues()
```python
{
    'success': True,
    'found_duplicates': True,
    'duplicate_count': 1,
    'duplicates': [
        {
            'key': 'PAYMENT-123',
            'summary': '...',
            'status': '...',
            'url': '...'
        }
    ]
}
```

---

## 🚀 Best Practices

1. **Check First** - Call `get_existing_security_issues()` before workflow
2. **Review Duplicates** - Check found issues before running fixes
3. **Link PRs** - Ensure PRs are linked to Jira issues
4. **Status Tracking** - Keep Jira status updated in GitHub
5. **Label Consistently** - Always use `['security', 'automated-fix']` labels

---

## 🔗 Related Files

- `skills/jira_skill.py` - Enhanced with search methods
- `orchestrator/vulnerability_orchestrator.py` - Enhanced with sync methods
- `tests/test_orchestrator.py` - Test cases for sync
- `VULNERABILITY_ORCHESTRATOR_DETAILED.md` - Workflow details

---

## 💡 Next Steps

1. Review the new Jira skill methods
2. Test sync with your Jira instance
3. Integrate into CI/CD pipeline
4. Monitor duplicate reduction
5. Adjust duplicate detection if needed

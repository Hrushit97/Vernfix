# Skills Reference Documentation

## GitHub Skill

**Module**: `skills/github_skill.py`
**Purpose**: Manages all GitHub operations

### Methods

#### `get_repository(repo_name, owner=None)`
Fetch repository details
```python
result = github_skill.get_repository("paymentpodAPI", "username")
# Returns: {success, repo_url, clone_url, default_branch}
```

#### `create_branch(repo_name, branch_name, owner=None)`
Create a new feature branch
```python
result = github_skill.create_branch("paymentpodAPI", "security/fix-001")
```

#### `create_pull_request(repo_name, title, body, head_branch, base_branch, owner)`
Create a pull request
```python
result = github_skill.create_pull_request(
    "paymentpodAPI",
    "Security: Fix vulnerabilities",
    "Fixes SQL injection and XSS",
    "security/fix-001",
    "main"
)
```

#### `add_comment_to_pr(repo_name, pr_number, comment, owner)`
Add comment to PR

---

## Jira Skill

**Module**: `skills/jira_skill.py`
**Purpose**: Manages Jira issue tracking

### Methods

#### `create_issue(project_key, summary, issue_type, description, priority, labels)`
Create security issue
```python
result = jira_skill.create_issue(
    "PAYMENT",
    "SQL Injection in auth module",
    "Bug",
    "Line 45 uses unparameterized query",
    "High",
    ["security", "critical"]
)
```

#### `update_issue(issue_key, updates)`
Update issue fields

#### `transition_issue(issue_key, target_status)`
Move issue to new status

#### `link_issue_to_pr(issue_key, pr_url)`
Link PR URL to issue

---

## Code Analysis Skill

**Module**: `skills/code_analysis_skill.py`
**Purpose**: Detects security vulnerabilities

### Methods

#### `analyze_python(file_path)`
Scan Python file for vulnerabilities

#### `analyze_javascript(file_path)`
Scan JavaScript file for vulnerabilities

#### `scan_directory(directory)`
Recursively scan all files in directory
```python
result = skill.scan_directory("/path/to/src")
# Returns: {total_files, total_vulnerabilities, vulnerabilities}
```

### Detected Vulnerabilities

1. **SQL Injection** (CRITICAL)
2. **Hardcoded Secrets** (HIGH)
3. **Hardcoded API Keys** (HIGH)
4. **Insecure Deserialization** (CRITICAL)
5. **Eval Usage** (CRITICAL)
6. **XSS Vulnerabilities** (HIGH)

---

## Vulnerability Fixer Skill

**Module**: `skills/vulnerability_fixer_skill.py`
**Purpose**: Automatically fixes vulnerabilities

### Methods

#### `fix_vulnerability(file_path, vuln)`
Fix a specific vulnerability
```python
result = fixer.fix_vulnerability(
    "/path/to/file.py",
    {
        "type": "Hardcoded Secret",
        "line": 5,
        "file": "/path/to/file.py"
    }
)
```

### Fix Strategies

- **SQL Injection**: Parameterized queries
- **Hardcoded Secrets**: Environment variables
- **API Keys**: os.getenv() pattern
- **Deserialization**: json/yaml.safe_load
- **Eval**: JSON.parse alternative
- **XSS**: textContent instead of innerHTML

---

## PR Management Skill

**Module**: `skills/pr_management_skill.py`
**Purpose**: Manages git and PR operations

### Methods

#### `create_feature_branch(branch_name)`
Create local feature branch

#### `commit_changes(files, message)`
Stage and commit changes

#### `push_branch(branch_name)`
Push branch to remote

#### `get_changed_files()`
Get list of modified files

#### `create_pr_description(vulnerabilities)`
Generate PR description from vulnerabilities

---

## Orchestrator

**Module**: `orchestrator/vulnerability_orchestrator.py`
**Purpose**: Coordinates all skills

### Methods

#### `execute_workflow(repo_name, repo_owner, project_key, analyze_path)`
Run complete workflow
```python
result = orchestrator.execute_workflow(
    "paymentpodAPI",
    "username",
    "PAYMENT",
    "/path/to/src"
)
# Returns: {success, pr_url, pr_number, vulnerabilities_fixed, jira_issues}
```

### Workflow Stages

1. Get repository info
2. Analyze code
3. Create Jira issues
4. Create feature branch
5. Fix vulnerabilities
6. Commit changes
7. Push branch
8. Create PR
9. Link to Jira issues

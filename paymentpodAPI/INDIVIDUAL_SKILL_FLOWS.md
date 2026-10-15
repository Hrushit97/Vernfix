# Individual Skill Flows - Detailed

## 📍 Skill 1: CodeAnalysisSkill

### Purpose
Find security vulnerabilities in source code

### File Location
`skills/code_analysis_skill.py`

### Methods
```python
analyze_python(file_path: str) -> List[Dict]
analyze_javascript(file_path: str) -> List[Dict]
scan_directory(directory: str) -> Dict
```

### Flow
```
ORCHESTRATOR (Step 2)
    ↓
CodeAnalysisSkill.scan_directory('/src')
    ↓
Walk directory recursively
    ↓
For each .py or .js file:
  ├─ analyze_python() or analyze_javascript()
  ├─ Apply regex patterns
  ├─ Find vulnerabilities
  └─ Extract line numbers
    ↓
Return: {
  'total_files': 100,
  'total_vulnerabilities': 15,
  'vulnerabilities': [
    {'file': '/src/app.py', 'line': 42, 'type': 'SQL Injection', ...},
    {'file': '/src/db.py', 'line': 156, 'type': 'Hardcoded Secret', ...}
  ]
}
    ↓
ORCHESTRATOR gets list of vulns
```

### Vulnerability Types Detected
- SQL Injection - string concatenation in queries
- Hardcoded Secrets - password = "secret"
- Hardcoded API Keys - api_key = "..."
- Insecure Deserialization - pickle.load(), yaml.load()
- Eval Usage - eval() function
- XSS Vulnerability - .innerHTML = ...

### Key Features
- Regex-based pattern matching
- Python & JavaScript support
- Recursive directory walking
- Severity classification
- Precise line numbers
- Error handling per file

---

## 📍 Skill 2: GitHubSkill

### Purpose
Manage GitHub repositories and pull requests

### File Location
`skills/github_skill.py`

### Methods
```python
get_repository(repo_name, owner) -> Dict
create_branch(repo_name, branch_name, owner) -> Dict
create_pull_request(repo_name, title, body, head, base, owner) -> Dict
add_comment_to_pr(repo_name, pr_number, comment, owner) -> Dict
get_repo_files(repo_name, path, owner) -> Dict
```

### Flow - Step 1 (Get Repository)
```
ORCHESTRATOR (Step 1)
    ↓
GitHubSkill.get_repository('Vernfix', 'Hrushit97')
    ↓
GitHub API: GET /repos/Hrushit97/Vernfix
    ↓
Return: {
  'repo_url': 'https://github.com/...',
  'clone_url': 'https://github.com/...git',
  'description': '...',
  'default_branch': 'paymentAPI'
}
```

### Flow - Step 8 (Create PR)
```
ORCHESTRATOR (Step 8)
    ↓
GitHubSkill.create_pull_request(
  'Vernfix',
  'Security: Fix 5 vulnerabilities',
  'PR body with fixes',
  'security/vulnerability-fixes',
  'paymentAPI'
)
    ↓
GitHub API: POST /repos/Hrushit97/Vernfix/pulls
    ↓
Return: {
  'pr_url': 'https://github.com/.../pull/42',
  'pr_number': 42
}
```

### Data Flow
```
Step 1: Gets repo info
Step 8: Creates PR from feature branch
Step 9: Jira links back to this PR
```

---

## 📍 Skill 3: JiraSkill

### Purpose
Track vulnerabilities in Jira, prevent duplicates

### File Location
`skills/jira_skill.py`

### Methods
```python
create_issue(project_key, summary, ...) -> Dict
find_duplicate_issues(project_key, file, type) -> Dict
get_issues_by_labels(project_key, labels) -> Dict
link_issue_to_pr(issue_key, pr_url) -> Dict
transition_issue(issue_key, target_status) -> Dict
```

### Flow - Step 3 (Create Issues with Sync)
```
ORCHESTRATOR (Step 3)
    ↓
For each vulnerability:
    ├─ JiraSkill.find_duplicate_issues()
    │  ├─ Search: project=PAYMENT AND file=/src/app.py AND type=SQL Injection
    │  ├─ Found existing PAYMENT-123
    │  └─ Return: {found_duplicates: True}
    │
    ├─ IF duplicate exists: Reuse issue_key
    │
    └─ IF NOT exists: JiraSkill.create_issue()
       ├─ Create new issue
       ├─ Return: {issue_key: 'PAYMENT-456', ...}
       └─ Jira API creates ticket
    ↓
Return: ['PAYMENT-123', 'PAYMENT-456', ...]
```

### Flow - Step 9 (Link PR)
```
ORCHESTRATOR (Step 9)
    ↓
For each jira_issue:
    ├─ JiraSkill.link_issue_to_pr()
    │  └─ Add comment: "Pull Request: https://github.com/.../pull/42"
    │
    └─ JiraSkill.transition_issue()
       └─ Change status to "In Progress"
```

### Data Flow
```
Step 3: Create/reuse Jira issues
Step 9: Link PR to issues, update status
```

---

## 📍 Skill 4: VulnerabilityFixerSkill

### Purpose
Automatically fix vulnerabilities in code

### File Location
`skills/vulnerability_fixer_skill.py`

### Methods
```python
fix_vulnerability(file_path, vuln) -> Dict
_fix_sql_injection(file_path, line_num) -> Dict
_fix_hardcoded_secret(file_path, line_num) -> Dict
_fix_hardcoded_api_key(file_path, line_num) -> Dict
_fix_insecure_deserialization(file_path) -> Dict
_fix_eval_usage(file_path) -> Dict
_fix_xss_vulnerability(file_path) -> Dict
```

### Flow - Step 5 (Fix Vulnerabilities)
```
ORCHESTRATOR (Step 5)
    ↓
For each vulnerability:
    ├─ VulnerabilityFixerSkill.fix_vulnerability(file, vuln)
    │
    ├─ IF SQL Injection:
    │  └─ Replace: execute("query %s") → execute("query ?", [params])
    │
    ├─ IF Hardcoded Secret:
    │  └─ Replace: password="secret" → password=os.getenv("PASSWORD")
    │
    ├─ IF Insecure Deserialization:
    │  └─ Replace: pickle.load() → json.load()
    │
    ├─ IF Eval Usage:
    │  └─ Replace: eval() → JSON.parse()
    │
    ├─ IF XSS:
    │  └─ Replace: .innerHTML = → .textContent =
    │
    └─ Return: {success: True, fix: "Fixed SQL Injection"}
    ↓
Return: [fixed_vulns list], [failed_fixes list]
```

### Key Fixes
```
SQL Injection:
  From: execute("SELECT * FROM users WHERE id = %s")
  To:   execute("SELECT * FROM users WHERE id = ?", [id])

Hardcoded Secret:
  From: api_key = "secret_key_12345"
  To:   api_key = os.getenv("API_KEY")

Deserialization:
  From: pickle.load(file)
  To:   json.load(file)

Eval:
  From: eval(user_input)
  To:   JSON.parse(user_input)

XSS:
  From: element.innerHTML = user_data
  To:   element.textContent = user_data
```

### Data Flow
```
Step 5: Modifies source files directly
Step 6: PRManagement commits these changes
```

---

## 📍 Skill 5: PRManagementSkill

### Purpose
Handle Git operations for vulnerability fixes

### File Location
`skills/pr_management_skill.py`

### Methods
```python
create_feature_branch(branch_name) -> Dict
commit_changes(files, message) -> Dict
push_branch(branch_name) -> Dict
get_current_branch() -> str
get_changed_files() -> List[str]
create_pr_description(vulnerabilities) -> str
```

### Flow - Step 4 (Create Branch)
```
ORCHESTRATOR (Step 4)
    ↓
PRManagementSkill.create_feature_branch('security/vulnerability-fixes')
    ↓
Git commands:
  ├─ git fetch origin
  ├─ git checkout -b security/vulnerability-fixes
    ↓
Return: {success: True, branch: 'security/vulnerability-fixes'}
```

### Flow - Step 6 (Commit Changes)
```
ORCHESTRATOR (Step 6)
    ↓
changed_files = PRManagementSkill.get_changed_files()
    ↓ (returns ['src/app.py', 'src/db.py', ...])
    ↓
PRManagementSkill.commit_changes(
  ['src/app.py', 'src/db.py'],
  'Security: Fix 5 vulnerabilities'
)
    ↓
Git commands:
  ├─ git add src/app.py
  ├─ git add src/db.py
  ├─ git commit -m "Security: Fix 5 vulnerabilities"
    ↓
Return: {success: True, message: 'Changes committed'}
```

### Flow - Step 7 (Push Branch)
```
ORCHESTRATOR (Step 7)
    ↓
PRManagementSkill.push_branch('security/vulnerability-fixes')
    ↓
Git command:
  ├─ git push origin security/vulnerability-fixes
    ↓
Return: {success: True, branch: 'security/vulnerability-fixes'}
```

### Flow - Step 8 Helper (PR Description)
```
PR Description generation:
    ↓
PRManagementSkill.create_pr_description(vulns)
    ↓
Output:
## Security Vulnerability Fixes

This PR fixes the following security vulnerabilities:

- **SQL Injection** (CRITICAL)
  - File: `src/app.py`
  - Line: 42

- **Hardcoded Secret** (HIGH)
  - File: `src/db.py`
  - Line: 156

## Changes
- Applied security best practices
- Used parameterized queries for database operations
- Moved secrets to environment variables
```

### Data Flow
```
Step 4: Create feature branch
Step 5: VulnerabilityFixer modifies files
Step 6: Commit all changed files
Step 7: Push to remote
Step 8: GitHub creates PR from this branch
```

---

## 🔄 Skills Working Together

### Example: Fixing SQL Injection

```
Step 1: GitHub
  └─ Get repo info

Step 2: CodeAnalysis
  └─ Find: /src/app.py:42 - SQL Injection

Step 3: Jira
  └─ Create or reuse: PAYMENT-123

Step 4: PRManagement
  └─ Create branch: security/vulnerability-fixes

Step 5: VulnerabilityFixer
  └─ Modify: /src/app.py line 42 (fix SQL)

Step 6: PRManagement
  └─ Commit: "Security: Fix SQL Injection"

Step 7: PRManagement
  └─ Push: security/vulnerability-fixes

Step 8: GitHub
  └─ Create PR #42 with fixes

Step 9: Jira
  └─ Link PAYMENT-123 to PR #42
```

Result: Vulnerability detected, fixed, tracked, and proposed for review!

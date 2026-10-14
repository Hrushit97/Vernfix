# GitHub Integration Skill - Quick Reference

## 📖 Docstring Translation
```python
"""
GitHub Integration Skill
Handles all GitHub operations: cloning, fetching repos, branch management, PRs
"""
```

**Means:** This module automates all GitHub interactions (repos, branches, PRs)

---

## 🎯 What It Does

- ✅ Connect to GitHub with authentication
- ✅ Fetch repository details
- ✅ Create branches
- ✅ Create pull requests
- ✅ Add comments to PRs
- ✅ List repository files

---

## 6️⃣ Core Methods

### 1. `__init__(token)`
**Initialize GitHub connection**
```python
skill = GitHubSkill("ghp_xxx...")  # Your GitHub token
# Authenticates and confirms connection
```

### 2. `get_repository(repo_name, owner)`
**Fetch repo information**
```python
info = skill.get_repository("Vernfix", "Hrushit97")
# Returns: repo_url, clone_url, description, default_branch
```

### 3. `create_branch(repo_name, branch_name, owner)`
**Create new branch**
```python
skill.create_branch("Vernfix", "security/fix-001", "Hrushit97")
# Creates branch from default branch
```

### 4. `create_pull_request(repo, title, body, head, base, owner)`
**Create pull request**
```python
pr = skill.create_pull_request(
    "Vernfix",
    "Fix: SQL Injection",
    "Fixes database vulnerability",
    "security/fix-001",
    "main",
    "Hrushit97"
)
# Returns: pr_url, pr_number
```

### 5. `add_comment_to_pr(repo, pr_number, comment, owner)`
**Comment on PR**
```python
skill.add_comment_to_pr(
    "Vernfix",
    42,
    "Vulnerability fixed and tested",
    "Hrushit97"
)
```

### 6. `get_repo_files(repo, path, owner)`
**List repository files**
```python
files = skill.get_repo_files("Vernfix", "src", "Hrushit97")
# Returns: list of files with name, path, type
```

---

## 📤 Return Format

All methods return a dictionary:

**Success:**
```python
{
    "success": True,
    "data_key": "value"
}
```

**Error:**
```python
{
    "success": False,
    "error": "Error message from GitHub"
}
```

---

## 🔑 Required

- **GitHub Personal Access Token (PAT)**
  - Must have `repo` scope
  - Must have `pull_request` scope
  - Keep it SECRET (use env variables)

---

## 💡 Real-World Workflow

```
Vulnerability Detected
    ↓
skill.create_branch("security/sql-injection-fix")
    ↓
Auto-fix code
    ↓
skill.create_pull_request(..., "security/sql-injection-fix", "main")
    ↓
skill.add_comment_to_pr(..., "Fixed and tested ✅")
    ↓
PR ready for team review
```

---

## ⚠️ Error Handling

All methods catch `GithubException`:
- Network errors
- Authentication failures
- Repository not found
- Permission denied

Returns error dict with details.

---

## 🔗 Related Files
- `skills/vulnerability_fixer_skill.py` - Auto-fixes code
- `skills/jira_skill.py` - Creates JIRA issues
- `orchestrator/vulnerability_orchestrator.py` - Orchestrates workflow
- `tests/test_skills.py` - Unit tests (20% coverage)

---

## 📊 Test Coverage
Currently: **20%** - Needs more integration tests

---

## 🚀 Complete Example

```python
from skills.github_skill import GitHubSkill

# Initialize
github = GitHubSkill(os.getenv("GITHUB_TOKEN"))

# Get repo
repo_info = github.get_repository("Vernfix", "Hrushit97")
print(f"Clone: {repo_info['clone_url']}")

# Create branch
github.create_branch("Vernfix", "fix/xss-vulnerability", "Hrushit97")

# Create PR
pr = github.create_pull_request(
    "Vernfix",
    "Security Fix: XSS Vulnerability",
    "Fixed innerHTML assignment vulnerability in form handler",
    "fix/xss-vulnerability",
    "main",
    "Hrushit97"
)

# Comment
github.add_comment_to_pr(
    "Vernfix",
    pr['pr_number'],
    f"✅ Security scan completed\n- No new vulnerabilities\n- Tests passing",
    "Hrushit97"
)

# List files
files = github.get_repo_files("Vernfix", "src", "Hrushit97")
for f in files['files']:
    print(f"- {f['name']} ({f['type']})")
```

# GitHub Integration Skill - Complete Explanation

## 📖 Docstring Meaning

```python
"""
GitHub Integration Skill
Handles all GitHub operations: cloning, fetching repos, branch management, PRs
"""
```

**Translation:**
- **GitHub Integration** = Connects to GitHub platform
- **Handles all GitHub operations** = Automates GitHub tasks
- **Cloning, fetching repos** = Downloading repository data
- **Branch management** = Creating/managing branches
- **PRs** = Pull Requests - code review mechanism

---

## 🎯 Purpose

Automate GitHub interactions programmatically without using the web interface.
Uses **PyGithub** library to communicate with GitHub API.

---

## 📚 Imports & Setup

```python
from github import Github, GithubException  # PyGithub library
import logging                               # Error tracking
from typing import Dict, List, Optional      # Type hints
```

**Logger:** Tracks all GitHub operations for debugging

---

## 🔧 Core Methods (6 Total)

### 1️⃣ **__init__(token: str)**
```python
def __init__(self, token: str):
    self.client = Github(token)        # Authenticate with GitHub
    self.user = self.client.get_user() # Get current user info
```

**What it does:**
- Connects to GitHub using authentication token
- Initializes client for API calls
- Verifies authentication by fetching user info

**Returns:** Logged in username

---

### 2️⃣ **get_repository(repo_name, owner)**
```python
Fetch complete repository details
```

**Returns:**
```python
{
    "success": True,
    "repo_url": "https://github.com/...",
    "clone_url": "https://github.com/.../xxx.git",
    "description": "Repository description",
    "default_branch": "main"
}
```

---

### 3️⃣ **create_branch(repo_name, branch_name, owner)**
```python
Create new branch from default branch
```

**Process:**
1. Get repository
2. Get default branch commit SHA
3. Create new branch reference
4. Return success status

**Returns:**
```python
{"success": True, "branch": "feature/fix-sql-injection"}
```

---

### 4️⃣ **create_pull_request(repo_name, title, body, head_branch, base_branch)**
```python
Create pull request between branches
```

**Parameters:**
- `title` - PR title
- `body` - PR description
- `head_branch` - Source branch (with changes)
- `base_branch` - Target branch (default: "main")

**Returns:**
```python
{
    "success": True,
    "pr_url": "https://github.com/.../pull/42",
    "pr_number": 42
}
```

---

### 5️⃣ **get_repo_files(repo_name, path, owner)**
```python
List files in repository at given path
```

**Returns:**
```python
{
    "success": True,
    "files": [
        {
            "name": "app.py",
            "path": "src/app.py",
            "type": "file"
        }
    ]
}
```

---

### 6️⃣ **add_comment_to_pr(repo_name, pr_number, comment, owner)**
```python
Add comment to existing pull request
```

**Use cases:**
- Post review feedback
- Notify about vulnerabilities
- Provide analysis results

**Returns:**
```python
{"success": True, "message": "Comment added"}
```

---

## ⚠️ Error Handling

All methods have try-except for `GithubException`:
```python
except GithubException as e:
    logger.error(f"Failed to ...: {e}")
    return {"success": False, "error": str(e)}
```

---

## 💻 Usage Example

```python
from skills.github_skill import GitHubSkill

# 1. Initialize with token
skill = GitHubSkill("ghp_YOUR_TOKEN_HERE")

# 2. Get repo details
repo = skill.get_repository("Vernfix", "Hrushit97")
print(repo['clone_url'])

# 3. Create feature branch
skill.create_branch("Vernfix", "security/fix-001", "Hrushit97")

# 4. Create pull request
pr = skill.create_pull_request(
    "Vernfix",
    "Fix: SQL Injection in login",
    "Fixes vulnerability in database queries",
    "security/fix-001",
    "main",
    "Hrushit97"
)
print(f"PR created: {pr['pr_url']}")

# 5. Add comment to PR
skill.add_comment_to_pr(
    "Vernfix",
    pr['pr_number'],
    "Security scan completed. No new issues found.",
    "Hrushit97"
)

# 6. List files
files = skill.get_repo_files("Vernfix", "src", "Hrushit97")
for f in files['files']:
    print(f"{f['name']} - {f['type']}")
```

---

## 🔗 Workflow Example

```
Security Vulnerability Found
    ↓
create_branch("security/fix-xyz")
    ↓
Auto-fix vulnerability
    ↓
create_pull_request(title, body, "security/fix-xyz", "main")
    ↓
add_comment_to_pr("Vulnerability fixed and tested")
    ↓
PR ready for review on GitHub
```

---

## 🔐 Authentication

Requires GitHub Personal Access Token (PAT):
- Must have `repo` scope
- Must have `pull_request` scope
- Keep token secure in environment variables

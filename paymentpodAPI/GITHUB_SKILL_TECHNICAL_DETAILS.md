# GitHub Integration Skill - Technical Details

## 📖 Module Docstring (Lines 1-4)

```python
"""
GitHub Integration Skill
Handles all GitHub operations: cloning, fetching repos, branch management, PRs
"""
```

**Components:**
- **GitHub Integration** = Bridge between code and GitHub platform
- **Skill** = Reusable component in vulnerability orchestrator
- **Handles all GitHub operations** = Comprehensive GitHub API wrapper
- **Cloning** = Downloading repositories
- **Fetching repos** = Retrieving repository metadata
- **Branch management** = Creating branches
- **PRs** = Pull Requests for code review

---

## 📚 Dependencies (Lines 6-12)

```python
import os                           # File operations
import json                         # Data serialization
from typing import Dict, List, Optional  # Type hints
from github import Github, GithubException  # PyGithub library
import logging                      # Error tracking
```

**PyGithub:** Official GitHub Python library
- Provides: `Github` class for API access
- Provides: `GithubException` for error handling

---

## 🏗️ Class Architecture

### Initialization (Lines 18-22)
```python
def __init__(self, token: str):
    self.client = Github(token)        # Authenticate with GitHub
    self.user = self.client.get_user() # Get current user
```

**Flow:**
1. Accept GitHub Personal Access Token
2. Create authenticated GitHub client
3. Verify auth by fetching user info
4. Log successful connection

**Exceptions:** Raised if token invalid

---

## 🔧 Method Details

### get_repository() - Lines 24-39
**Purpose:** Retrieve repository metadata

**Logic:**
```
If owner not provided:
    Use current user as owner
Get repository object
Extract key info
Return as Dict
Handle GithubException
```

**Data Returned:**
- `repo_url` - Web URL
- `clone_url` - Git clone URL
- `description` - Repository description
- `default_branch` - Default branch name

---

### create_branch() - Lines 41-55
**Purpose:** Create new branch

**Logic:**
```
Get repository
Get default branch commit SHA
Create git reference with that SHA
Return success status
```

**Important:**
- New branch created from default branch
- Uses commit SHA for accuracy
- Ref format: `refs/heads/{branch_name}`

---

### create_pull_request() - Lines 57-84
**Purpose:** Create pull request between branches

**Logic:**
```
Get repository
Use repo.create_pull() method
Pass: title, body, head, base
Return PR details
```

**Parameters:**
- `head_branch` - Source branch (with changes)
- `base_branch` - Target branch (default: "main")
- `title` - PR title (searchable)
- `body` - PR description (markdown)

**Returns:**
- `pr_url` - GitHub PR URL
- `pr_number` - PR identifier for comments

---

### get_repo_files() - Lines 86-106
**Purpose:** List files in repository

**Logic:**
```
Get repository
Get contents at path
Iterate through items
Extract: name, path, type
Return file list
```

**Types:** "file", "dir", "symlink", "submodule"

**Default:** Root directory if path=""

---

### add_comment_to_pr() - Lines 108-125
**Purpose:** Comment on pull request

**Logic:**
```
Get repository
Get pull request by number
Create issue comment
Return success
```

**Use Cases:**
- Security analysis results
- Test status updates
- Vulnerability findings
- Approval messages

---

## ⚠️ Error Handling Pattern

All methods follow this pattern:
```python
try:
    # GitHub API call
except GithubException as e:
    logger.error(f"Failed to ...: {e}")
    return {"success": False, "error": str(e)}
```

**Catches:**
- Network errors
- Authentication failures (401)
- Not found errors (404)
- Permission errors (403)
- Rate limit errors (429)

---

## 🔐 Authentication

**Token Requirements:**
- Scope: `repo` (full repository access)
- Scope: `pull_request` (PR management)
- Type: Personal Access Token (PAT)

**Best Practices:**
```python
token = os.getenv("GITHUB_TOKEN")  # Never hardcode!
skill = GitHubSkill(token)
```

---

## 📊 Return Value Pattern

**Consistent return format:**
```python
{
    "success": True/False,
    "key": value,  # Specific data
    "error": "message"  # If success=False
}
```

**Benefits:**
- Predictable error handling
- Easy to check success
- Detailed error messages

---

## 🚀 Integration Points

Used by:
- `vulnerability_orchestrator.py` - Orchestrates workflow
- `vulnerability_fixer_skill.py` - Creates PRs with fixes
- `jira_skill.py` - Links JIRA issues to PRs

---

## 📈 Test Coverage
Currently: **20%** coverage
Needs: Integration tests for all methods

# GitHubSkill - repo_name Parameter Usage

## 🎯 What is repo_name?

**repo_name** is a parameter used in the GitHubSkill class that specifies **which repository** to perform operations on.

**Example values:**
- `"Vernfix"` - Repository name
- `"paymentpodAPI"` - Another repository name
- `"your-repo-name"` - Any repository you own

---

## 📋 All 5 Methods Using repo_name

### 1️⃣ **get_repository(repo_name, owner)**
**Line 24-39**

```python
def get_repository(self, repo_name: str, owner: Optional[str] = None) -> Dict:
    """Fetch repository details"""
    # Line 29: Uses repo_name here
    repo = self.client.get_user(owner).get_repo(repo_name)
    return {
        "repo_url": repo.html_url,
        "clone_url": repo.clone_url,
        "description": repo.description,
        "default_branch": repo.default_branch,
    }
```

**Usage:**
```python
skill.get_repository("Vernfix", "Hrushit97")
#                     ↑ repo_name
```

**What it does:** Fetches metadata about the specified repository

---

### 2️⃣ **create_branch(repo_name, branch_name, owner)**
**Line 41-55**

```python
def create_branch(self, repo_name: str, branch_name: str, owner=None) -> Dict:
    """Create a new branch"""
    # Line 46: Uses repo_name here
    repo = self.client.get_user(owner).get_repo(repo_name)
    base_branch = repo.get_branch(repo.default_branch)
    repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=base_branch.commit.sha,
    )
```

**Usage:**
```python
skill.create_branch("Vernfix", "security/fix-001", "Hrushit97")
#                    ↑ repo_name where branch will be created
```

**What it does:** Creates a new branch in the specified repository

---

### 3️⃣ **create_pull_request(repo_name, title, body, head_branch, base_branch, owner)**
**Line 57-84**

```python
def create_pull_request(self, repo_name: str, title: str, body: str,
                       head_branch: str, base_branch: str = "main", 
                       owner: Optional[str] = None) -> Dict:
    """Create a pull request"""
    # Line 70: Uses repo_name here
    repo = self.client.get_user(owner).get_repo(repo_name)
    pr = repo.create_pull(
        title=title,
        body=body,
        head=head_branch,
        base=base_branch,
    )
```

**Usage:**
```python
skill.create_pull_request("Vernfix", "Fix SQL", "Details", 
                         "security/fix-001", "main", "Hrushit97")
#                ↑ repo_name where PR will be created
```

**What it does:** Creates a pull request in the specified repository

---

### 4️⃣ **get_repo_files(repo_name, path, owner)**
**Line 86-106**

```python
def get_repo_files(self, repo_name: str, path: str = "", owner=None) -> Dict:
    """Get list of files in repository"""
    # Line 91: Uses repo_name here
    repo = self.client.get_user(owner).get_repo(repo_name)
    contents = repo.get_contents(path)
    files = []
    if isinstance(contents, list):
        for item in contents:
            files.append({
                "name": item.name,
                "path": item.path,
                "type": item.type,
            })
```

**Usage:**
```python
skill.get_repo_files("Vernfix", "src", "Hrushit97")
#                     ↑ repo_name to list files from
```

**What it does:** Lists all files in the specified repository path

---

### 5️⃣ **add_comment_to_pr(repo_name, pr_number, comment, owner)**
**Line 108-125**

```python
def add_comment_to_pr(self, repo_name: str, pr_number: int,
                     comment: str, owner: Optional[str] = None) -> Dict:
    """Add comment to pull request"""
    # Line 119: Uses repo_name here
    repo = self.client.get_user(owner).get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)
```

**Usage:**
```python
skill.add_comment_to_pr("Vernfix", 42, "Comment text", "Hrushit97")
#                       ↑ repo_name where PR exists
```

**What it does:** Adds comment to a PR in the specified repository

---

## 🔗 Internal Usage Pattern

All 5 methods follow the same pattern:

```python
# Step 1: Get repository object
repo = self.client.get_user(owner).get_repo(repo_name)
#                                   ↑ repo_name identifies which repo

# Step 2: Perform operation on that repo
# Different for each method

# Step 3: Return result
return {"success": True, ...}
```

---

## 💡 Complete Example Using repo_name

```python
from skills.github_skill import GitHubSkill
import os

github = GitHubSkill(os.getenv("GITHUB_TOKEN"))

# All these operations happen on "Vernfix" repository
repo_name = "Vernfix"
owner = "Hrushit97"

# 1. Get repo info
info = github.get_repository(repo_name, owner)

# 2. Create branch in this repo
github.create_branch(repo_name, "security/fix-001", owner)

# 3. Create PR in this repo
pr = github.create_pull_request(
    repo_name,  # ← Operations on this repo
    "Security Fix",
    "Description",
    "security/fix-001",
    "main",
    owner
)

# 4. Get files from this repo
files = github.get_repo_files(repo_name, "src", owner)

# 5. Comment on PR in this repo
github.add_comment_to_pr(
    repo_name,  # ← Same repo
    pr['pr_number'],
    "Fixed ✅",
    owner
)
```

---

## 🎯 Key Points

- **repo_name is required** in all 5 methods
- **repo_name specifies which repository** to operate on
- **Same repo_name can be used** across multiple method calls
- **Different repo_name = different repository** (different operations)
- **Works with owner parameter** - specifies repository owner

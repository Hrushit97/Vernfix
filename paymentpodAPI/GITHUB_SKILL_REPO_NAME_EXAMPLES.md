# GitHubSkill repo_name - Practical Examples

## 🎯 What is repo_name?

**repo_name** = The name of the GitHub repository you want to operate on

Examples:
- `"Vernfix"` - Your security fixing repository
- `"paymentpodAPI"` - Your payment API repository
- `"my-project"` - Any other repository

---

## 📋 Examples for Each Method

### Example 1: get_repository

```python
from skills.github_skill import GitHubSkill
import os

github = GitHubSkill(os.getenv("GITHUB_TOKEN"))

# Get details about "Vernfix" repository
result = github.get_repository(
    repo_name="Vernfix",      # ← Which repository?
    owner="Hrushit97"         # ← Who owns it?
)

if result["success"]:
    print(f"Repository: {result['repo_url']}")
    print(f"Clone: {result['clone_url']}")
    print(f"Default Branch: {result['default_branch']}")
```

**Output:**
```
Repository: https://github.com/Hrushit97/Vernfix
Clone: https://github.com/Hrushit97/Vernfix.git
Default Branch: main
```

---

### Example 2: create_branch

```python
# Create branch in "Vernfix" repository
result = github.create_branch(
    repo_name="Vernfix",               # ← In which repository?
    branch_name="security/fix-sql",    # ← New branch name
    owner="Hrushit97"                  # ← Repository owner
)

if result["success"]:
    print(f"Branch created: {result['branch']}")
    print("Ready to commit changes!")
```

**What happens:**
```
"Vernfix" repository
    ↓
Create new branch from 'main'
    ↓
New branch: "security/fix-sql"
    ↓
Ready to commit changes
```

---

### Example 3: create_pull_request

```python
# Create PR in "Vernfix" repository
result = github.create_pull_request(
    repo_name="Vernfix",                    # ← In which repository?
    title="Security Fix: SQL Injection",
    body="Fixed SQL injection vulnerability in database queries",
    head_branch="security/fix-sql",         # ← From this branch
    base_branch="main",                     # ← To this branch
    owner="Hrushit97"
)

if result["success"]:
    print(f"PR created: {result['pr_url']}")
    print(f"PR number: {result['pr_number']}")
```

**What happens:**
```
In "Vernfix" repository:
    ↓
Create PR from "security/fix-sql" → "main"
    ↓
PR opened for review
    ↓
Team can comment and approve
```

---

### Example 4: get_repo_files

```python
# List files in "Vernfix" repository
result = github.get_repo_files(
    repo_name="Vernfix",      # ← From which repository?
    path="src",               # ← In which directory?
    owner="Hrushit97"
)

if result["success"]:
    for file in result["files"]:
        print(f"- {file['name']} ({file['type']})")
```

**Output:**
```
- app.py (file)
- config.py (file)
- utils (dir)
- models (dir)
```

---

### Example 5: add_comment_to_pr

```python
# Add comment to PR in "Vernfix" repository
result = github.add_comment_to_pr(
    repo_name="Vernfix",           # ← In which repository?
    pr_number=42,                  # ← Which PR number?
    comment="✅ Security scan complete\n- No new issues\n- Tests passing",
    owner="Hrushit97"
)

if result["success"]:
    print("Comment added to PR!")
```

**What happens:**
```
In "Vernfix" repository:
    ↓
Find PR #42
    ↓
Add comment to it
    ↓
Team sees the feedback
```

---

## 🔄 Multi-Repository Example

```python
github = GitHubSkill(os.getenv("GITHUB_TOKEN"))

# Work with Repository 1: "Vernfix"
print("=== Working with Vernfix ===")
repo1 = github.get_repository("Vernfix", "Hrushit97")
github.create_branch("Vernfix", "feature-1", "Hrushit97")

# Work with Repository 2: "paymentpodAPI"
print("\n=== Working with paymentpodAPI ===")
repo2 = github.get_repository("paymentpodAPI", "Hrushit97")
github.create_branch("paymentpodAPI", "feature-2", "Hrushit97")

# Work with Repository 3: "SecurityTools"
print("\n=== Working with SecurityTools ===")
repo3 = github.get_repository("SecurityTools", "Hrushit97")
files = github.get_repo_files("SecurityTools", "tools", "Hrushit97")
```

**Key Point:** Same `github` object, different `repo_name` = different repositories

---

## ⚙️ How repo_name Works Internally

```python
# When you call:
github.create_branch("Vernfix", "fix-001", "Hrushit97")

# Inside create_branch method:
repo = self.client.get_user("Hrushit97").get_repo("Vernfix")
#                                                   ↑ repo_name
#      This gets the "Vernfix" repository object

# Then operation uses that repo object:
repo.create_git_ref(ref=f"refs/heads/fix-001", ...)
```

---

## ✅ Common Patterns

### Pattern 1: Using Same repo_name Multiple Times
```python
repo_name = "Vernfix"
owner = "Hrushit97"

# All operations on same repo
github.create_branch(repo_name, "feature-1", owner)
pr = github.create_pull_request(repo_name, ..., owner)
github.add_comment_to_pr(repo_name, pr["pr_number"], ..., owner)
```

### Pattern 2: Different repo_name for Different Repos
```python
# Different repos = different operations
github.create_branch("Vernfix", "feature-1", "Hrushit97")
github.create_branch("SecurityTools", "feature-2", "Hrushit97")
```

---

## ⚠️ Important Notes

- **repo_name is case-sensitive** - "Vernfix" ≠ "vernfix"
- **repo_name must exist** - Will error if repo doesn't exist
- **owner must have access** - Typically your own username
- **All operations need repo_name** - It identifies which repository

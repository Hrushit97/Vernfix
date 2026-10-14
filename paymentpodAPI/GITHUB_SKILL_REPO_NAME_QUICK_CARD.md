# repo_name Parameter - Quick Reference Card

## 🎯 What is repo_name?

**repo_name = Repository name you want to operate on**

Examples:
- `"Vernfix"` ← Your security repository
- `"paymentpodAPI"` ← Your payment API repository
- `"my-project"` ← Any GitHub repository

---

## 5️⃣ Methods Using repo_name

| Method | Purpose | repo_name Used For |
|--------|---------|-------------------|
| `get_repository(repo_name, owner)` | Fetch repo info | Identify which repo |
| `create_branch(repo_name, branch_name, owner)` | Create branch | Which repo to branch |
| `create_pull_request(repo_name, ..., owner)` | Create PR | Which repo for PR |
| `get_repo_files(repo_name, path, owner)` | List files | Which repo's files |
| `add_comment_to_pr(repo_name, pr_num, ...)` | Comment on PR | Which repo's PR |

---

## 📝 Quick Examples

### Example 1: Basic Usage
```python
github = GitHubSkill("token")

# repo_name = "Vernfix"
github.get_repository("Vernfix", "Hrushit97")
```

### Example 2: Create Branch
```python
github.create_branch(
    repo_name="Vernfix",        # ← Which repo?
    branch_name="fix-001",      # ← New branch name
    owner="Hrushit97"
)
```

### Example 3: Create PR
```python
github.create_pull_request(
    repo_name="Vernfix",        # ← Which repo?
    title="Fix SQL Injection",
    body="Details",
    head_branch="fix-001",
    base_branch="main",
    owner="Hrushit97"
)
```

### Example 4: List Files
```python
github.get_repo_files(
    repo_name="Vernfix",        # ← Which repo?
    path="src",
    owner="Hrushit97"
)
```

### Example 5: Comment on PR
```python
github.add_comment_to_pr(
    repo_name="Vernfix",        # ← Which repo?
    pr_number=42,
    comment="Fixed! ✅",
    owner="Hrushit97"
)
```

---

## 🔗 Internal Code

```python
# When you pass repo_name:
github.create_branch("Vernfix", "fix", "Hrushit97")

# Inside method:
repo = self.client.get_user("Hrushit97").get_repo("Vernfix")
#                                                   ↑ repo_name used here
```

---

## ✅ Key Points

✅ repo_name identifies **which repository**
✅ Used in **all 5 methods**
✅ Must be **exact name** (case-sensitive)
✅ Repository must **exist** on GitHub
✅ Works with **owner parameter** to specify whose repo

---

## ⚠️ Common Mistakes

❌ Forgetting repo_name parameter
```python
# WRONG - will error
github.create_branch(branch_name="fix")

# RIGHT
github.create_branch("Vernfix", "fix", "Hrushit97")
```

❌ Wrong repo_name spelling
```python
# WRONG - "vernfix" doesn't exist
github.create_branch("vernfix", "fix", "Hrushit97")

# RIGHT - exact name
github.create_branch("Vernfix", "fix", "Hrushit97")
```

---

## 🚀 Real Workflow

```python
# Setup
github = GitHubSkill(token)
repo_name = "Vernfix"
owner = "Hrushit97"

# Step 1: Create branch
github.create_branch(repo_name, "security/fix-001", owner)

# Step 2: Make changes to code locally
# (not shown here)

# Step 3: Create PR
pr = github.create_pull_request(
    repo_name,
    "Security Fix: SQL Injection",
    "Fixes vulnerability",
    "security/fix-001",
    "main",
    owner
)

# Step 4: Add comment
github.add_comment_to_pr(
    repo_name,
    pr["pr_number"],
    "Fixed and tested ✅",
    owner
)
```

---

## 📊 Summary

**repo_name Purpose:**
- Tells GitHub API which repository to operate on
- Required parameter in all 5 methods
- Must match actual GitHub repository name
- Works together with owner parameter

**repo_name Examples:**
- `"Vernfix"` - main repository
- `"paymentpodAPI"` - API repository
- `"SecurityTools"` - tools repository

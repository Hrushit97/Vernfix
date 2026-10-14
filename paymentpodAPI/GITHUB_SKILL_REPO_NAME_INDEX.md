# GitHub Skill repo_name Parameter - Documentation Index

## 📚 Documentation Files

### 1. **GITHUB_SKILL_REPO_NAME_QUICK_CARD.md** ⭐ START HERE
**5-minute quick reference**
- What is repo_name?
- 5 methods using it
- Quick examples
- Common mistakes
- **Perfect for:** Quick lookup

### 2. **GITHUB_SKILL_REPO_NAME_USAGE.md**
**Detailed usage guide**
- All 5 methods explained
- Line-by-line code examples
- Complete examples
- Key points summary
- **Perfect for:** Understanding usage

### 3. **GITHUB_SKILL_REPO_NAME_EXAMPLES.md**
**Practical examples**
- Example 1: get_repository
- Example 2: create_branch
- Example 3: create_pull_request
- Example 4: get_repo_files
- Example 5: add_comment_to_pr
- Multi-repository example
- **Perfect for:** Learning by example

---

## 🎯 Quick Answer

### What is repo_name?
**Repository name on GitHub that you want to operate on**

### Which methods use it?
All 5 methods:
1. `get_repository(repo_name, owner)`
2. `create_branch(repo_name, branch_name, owner)`
3. `create_pull_request(repo_name, title, body, head, base, owner)`
4. `get_repo_files(repo_name, path, owner)`
5. `add_comment_to_pr(repo_name, pr_number, comment, owner)`

### How is it used?
```python
# Pass repo_name to identify which repository
github.create_branch("Vernfix", "fix-001", "Hrushit97")
#                     ↑ repo_name identifies the repository
```

### Example values
- `"Vernfix"` - Your security repository
- `"paymentpodAPI"` - Your payment API
- `"my-project"` - Any GitHub repo

---

## 📋 5 Methods Breakdown

### 1️⃣ get_repository
```python
github.get_repository("Vernfix", "Hrushit97")
#                      ↑ repo_name = which repo to fetch info about
```

### 2️⃣ create_branch
```python
github.create_branch("Vernfix", "fix-001", "Hrushit97")
#                     ↑ repo_name = which repo to create branch in
```

### 3️⃣ create_pull_request
```python
github.create_pull_request("Vernfix", "Title", "Body", "fix-001", "main", "Hrushit97")
#                          ↑ repo_name = which repo to create PR in
```

### 4️⃣ get_repo_files
```python
github.get_repo_files("Vernfix", "src", "Hrushit97")
#                      ↑ repo_name = which repo's files to list
```

### 5️⃣ add_comment_to_pr
```python
github.add_comment_to_pr("Vernfix", 42, "Comment", "Hrushit97")
#                         ↑ repo_name = which repo's PR to comment on
```

---

## 💡 Real-World Workflow

```python
github = GitHubSkill(token)
repo_name = "Vernfix"    # Repository to work with
owner = "Hrushit97"      # Repository owner

# 1. Get repository info
info = github.get_repository(repo_name, owner)

# 2. Create branch for fix
github.create_branch(repo_name, "security/sql-fix", owner)

# 3. Auto-fix code (done separately)

# 4. Create PR with fix
pr = github.create_pull_request(
    repo_name,
    "Fix: SQL Injection",
    "Fixed SQL injection vulnerability",
    "security/sql-fix",
    "main",
    owner
)

# 5. Comment with results
github.add_comment_to_pr(
    repo_name,
    pr["pr_number"],
    "✅ Fixed and tested",
    owner
)
```

---

## 🔗 How It Works Internally

```python
# You call:
github.create_branch("Vernfix", "fix-001", "Hrushit97")

# Inside method:
owner = "Hrushit97"
repo_name = "Vernfix"

# Get repository object
repo = self.client.get_user(owner).get_repo(repo_name)
#                                           ↑ repo_name used here

# Use repository object
repo.create_git_ref(ref=f"refs/heads/fix-001", sha=...)
```

---

## ✅ Key Points

1. **repo_name = Repository name** (e.g., "Vernfix")
2. **Used in all 5 methods** to specify which repo
3. **Case-sensitive** - "Vernfix" ≠ "vernfix"
4. **Must exist** on GitHub
5. **Works with owner** to identify owner/repo combo

---

## 📖 Full Documentation

- `GITHUB_SKILL_EXPLAINED.md` - Complete explanation
- `GITHUB_SKILL_QUICK_REFERENCE.md` - One-page overview
- `GITHUB_SKILL_TECHNICAL_DETAILS.md` - Code breakdown
- `GITHUB_SKILL_INDEX.md` - Full documentation index

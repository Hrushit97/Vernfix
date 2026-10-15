# Complete Skills Flow - All 5 Skills + Orchestrator

## 🎯 Overview

How all 5 specialized skills work together with VulnerabilityOrchestrator through the complete 9-step workflow.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  VulnerabilityOrchestrator                  │
│              (Main coordinator & workflow engine)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Coordinates
                              ├──────────────────────┬──────────────┬─────────────┬──────────────┐
                              │                      │              │             │              │
                    ┌─────────▼──────────┐  ┌───────▼──────┐  ┌────▼───────┐  ┌─▼────────────┐  ┌──▼──────────────┐
                    │   CodeAnalysisSkill│  │  GitHubSkill │  │JiraSkill   │  │VulnerabilityFix│  │PRManagementSkill│
                    │  (Finds vulns)     │  │(Repos & PRs) │  │(Tracking)  │  │   erSkill      │  │(Git operations) │
                    │                    │  │              │  │            │  │(Auto-fixing)   │  │                 │
                    └────────────────────┘  └──────────────┘  └────────────┘  └────────────────┘  └─────────────────┘
                           ▲                     ▲                ▲                 ▲                     ▲
                           │                     │                │                 │                     │
                    Files on Disk         GitHub API          Jira API       Code Files           Local Git Repo
```

---

## 5️⃣ The Five Skills

### **1. CodeAnalysisSkill** 🔍
**Purpose:** Find vulnerabilities in code

**Methods:**
- `analyze_python(file)` - Scans Python files
- `analyze_javascript(file)` - Scans JS files
- `scan_directory(path)` - Recursive scan

**Detects:**
- SQL Injection
- Hardcoded Secrets
- Insecure Deserialization
- Eval Usage
- XSS Vulnerabilities
- Hardcoded API Keys

**Output:** List of vulnerabilities with:
- File path
- Line number
- Vulnerability type
- Severity level
- Code snippet

---

### **2. GitHubSkill** 🔗
**Purpose:** Manage GitHub repositories and PRs

**Methods:**
- `get_repository(repo, owner)` - Fetch repo info
- `create_branch(repo, branch, owner)` - Create feature branch
- `create_pull_request(repo, title, body, head, base, owner)` - Create PR
- `add_comment_to_pr(repo, pr_num, comment, owner)` - Add PR comment
- `get_repo_files(repo, path, owner)` - List files

**Used For:**
- Getting repository details
- Creating feature branches
- Creating pull requests
- Commenting on PRs
- Listing repository files

**External:** GitHub API

---

### **3. JiraSkill** 📋
**Purpose:** Track vulnerabilities in Jira

**Methods:**
- `create_issue(project, summary, type, desc, priority, labels)` - Create ticket
- `get_issue(key)` - Get ticket details
- `update_issue(key, updates)` - Update ticket
- `add_comment(key, comment)` - Add comment
- `link_issue_to_pr(key, pr_url)` - Link PR
- `transition_issue(key, status)` - Change status
- `search_issues(project, keyword, status)` - Search
- `find_duplicate_issues(project, file, type)` - Find duplicates
- `get_issues_by_labels(project, labels)` - Get by labels

**Used For:**
- Creating security issue tickets
- Linking PRs to tickets
- Tracking issue status
- Preventing duplicates
- Cross-referencing fixes

**External:** Jira API

---

### **4. VulnerabilityFixerSkill** 🔧
**Purpose:** Automatically fix vulnerabilities

**Methods:**
- `fix_vulnerability(file, vuln)` - Main fix method
- `_fix_sql_injection(file, line)` - Use parameterized queries
- `_fix_hardcoded_secret(file, line)` - Use env variables
- `_fix_hardcoded_api_key(file, line)` - Use env variables
- `_fix_insecure_deserialization(file)` - Use safe methods
- `_fix_eval_usage(file)` - Use JSON.parse
- `_fix_xss_vulnerability(file)` - Use textContent

**Fixes Applied:**
- SQL Injection → Parameterized queries
- Hardcoded secrets → Environment variables
- Unsafe deserialization → Safe alternatives
- eval() → JSON.parse
- XSS → innerHTML → textContent

**Modifies:** Source code files directly

---

### **5. PRManagementSkill** 📊
**Purpose:** Handle Git operations and PR preparation

**Methods:**
- `create_feature_branch(branch)` - Create branch locally
- `commit_changes(files, message)` - Git commit
- `push_branch(branch)` - Push to remote
- `get_current_branch()` - Get current branch
- `get_changed_files()` - Get modified files
- `create_pr_description(vulns)` - Generate description

**Used For:**
- Creating feature branches
- Staging and committing changes
- Pushing branches to remote
- Generating PR descriptions
- Tracking changed files

**Manages:** Local Git repository

---

## 🔄 The 9-Step Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  STEP 1: Get Repository Info                                       │
│  └─→ GitHubSkill.get_repository()                                  │
│                                                                     │
│  STEP 2: Analyze Code                                              │
│  └─→ CodeAnalysisSkill.scan_directory()                            │
│                                                                     │
│  STEP 3: Create Jira Issues                                        │
│  └─→ JiraSkill.create_issue() + find_duplicate_issues()           │
│                                                                     │
│  STEP 4: Create Feature Branch                                     │
│  └─→ PRManagementSkill.create_feature_branch()                     │
│                                                                     │
│  STEP 5: Fix Vulnerabilities                                       │
│  └─→ VulnerabilityFixerSkill.fix_vulnerability()                   │
│                                                                     │
│  STEP 6: Commit Changes                                            │
│  └─→ PRManagementSkill.commit_changes()                            │
│                                                                     │
│  STEP 7: Push Branch                                               │
│  └─→ PRManagementSkill.push_branch()                               │
│                                                                     │
│  STEP 8: Create Pull Request                                       │
│  └─→ GitHubSkill.create_pull_request()                             │
│  └─→ PRManagementSkill.create_pr_description()                     │
│                                                                     │
│  STEP 9: Link PR to Jira                                           │
│  └─→ JiraSkill.link_issue_to_pr()                                  │
│  └─→ JiraSkill.transition_issue()                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Skill Usage by Step

| Step | Skill | Method | Input | Output |
|------|-------|--------|-------|--------|
| 1 | GitHub | get_repository() | repo_name, owner | repo_info dict |
| 2 | CodeAnalysis | scan_directory() | path | vulns list |
| 3 | Jira | create_issue() | vuln data | issue_key |
| 4 | PRMgmt | create_feature_branch() | branch_name | success |
| 5 | Fixer | fix_vulnerability() | file, vuln | fix result |
| 6 | PRMgmt | commit_changes() | files, message | commit success |
| 7 | PRMgmt | push_branch() | branch_name | push success |
| 8 | GitHub | create_pull_request() | PR details | pr_url, pr_num |
| 9 | Jira | link_issue_to_pr() | issue_key, pr_url | success |

---

## 🔗 Skill Interactions

### **CodeAnalysis → Fixer**
```
Vuln found at /src/app.py line 10, SQL Injection
    ↓
Pass to VulnerabilityFixer
    ↓
Fix applied, file modified
```

### **Fixer → PRManagement**
```
Files modified by fixer
    ↓
PRManagement gets changed files
    ↓
Commits and pushes to branch
```

### **GitHub → PRManagement**
```
Branch created locally by PRManagement
    ↓
Changes committed and pushed
    ↓
GitHub creates PR from branch
```

### **Jira ↔ GitHub**
```
Jira issues created from vulns
    ↓
GitHub PR created with fixes
    ↓
PR linked to Jira issues
    ↓
Issue status updated
```

---

## 📁 File Operations Summary

**CodeAnalysisSkill:**
- **Reads:** Source files (.py, .js)
- **Modifies:** None
- **Purpose:** Analyze only

**VulnerabilityFixerSkill:**
- **Reads:** Source files
- **Modifies:** Source files (applies fixes)
- **Purpose:** Fix vulnerabilities

**PRManagementSkill:**
- **Reads:** Git status, changed files
- **Modifies:** Git commits, branches
- **Purpose:** Version control operations

**GitHubSkill:**
- **Reads:** GitHub API
- **Modifies:** GitHub (branches, PRs)
- **Purpose:** Remote repository management

**JiraSkill:**
- **Reads:** Jira API
- **Modifies:** Jira (issues, comments)
- **Purpose:** Issue tracking

---

## 🔐 Configuration Requirements

```python
config = {
    # GitHub
    'github_token': 'ghp_...',
    'github_repo': 'Vernfix',
    'github_owner': 'Hrushit97',
    
    # Jira
    'jira_url': 'https://domain.atlassian.net',
    'jira_username': 'email@example.com',
    'jira_api_token': 'YOUR_TOKEN',
    
    # Local
    'repo_path': '/path/to/repo',
    'git_username': 'Hrushit97',
    'git_email': 'email@example.com',
}
```

---

## ✅ Workflow Result

After all 9 steps:
```python
{
    'success': True,
    'vulnerabilities_found': 10,
    'vulnerabilities_fixed': 8,
    'vulnerabilities_failed': 2,
    'jira_issues': ['PAYMENT-123', 'PAYMENT-124', ...],
    'pr_url': 'https://github.com/.../pull/42',
    'pr_number': 42,
    'duration_seconds': 45.3
}
```

All vulnerabilities are:
- ✅ Detected
- ✅ Tracked in Jira
- ✅ Fixed in code
- ✅ Committed to branch
- ✅ Proposed in PR
- ✅ Linked in Jira

# Getting Started with Vulnerability Orchestrator

Welcome! This guide will get you up and running in 10 minutes.

## Prerequisites

- Python 3.8 or higher
- GitHub account with a personal access token
- Jira account with API token
- Git installed on your system

## 5-Minute Setup

### Step 1: Prepare Your Environment (1 minute)

```bash
# Navigate to project directory
cd paymentpodAPI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

### Step 3: Configure Credentials (2 minutes)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
# Add your GitHub token, Jira URL, Jira token, etc.
```

### Step 4: Verify Installation (1 minute)

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected output:
```
Ran 5 tests in 0.124s
OK
```

## 10-Minute First Run

### 1. Test Code Analysis (2 minutes)

```bash
python examples/usage_example.py analysis
```

This scans your code WITHOUT making changes.

### 2. Prepare Repository (3 minutes)

Ensure your Git repository is clean:
```bash
git status
# Should show: "working tree clean"
```

### 3. Run Full Workflow (5 minutes)

```bash
python main.py
```

This will:
- Analyze your code
- Detect vulnerabilities
- Create Jira issues
- Fix vulnerabilities
- Create a pull request

### 4. Review Results

Check GitHub:
- Navigate to your repository
- Look for new branch: `security/vulnerability-fixes`
- Review the pull request

Check Jira:
- Look for new issues labeled "security"
- See PR links in comments

## Understanding Your First Run

### What Got Analyzed?
- All Python and JavaScript files in your code
- Common security vulnerabilities detected

### What Happened?
1. Each vulnerability was assigned severity (CRITICAL, HIGH, MEDIUM, LOW)
2. A Jira issue was created for each vulnerability
3. Code was automatically fixed
4. Changes were committed and pushed
5. A PR was created with all fixes

### What's Next?
1. Review the PR changes
2. Run your security tests
3. Merge the PR when satisfied
4. Monitor the Jira issues

## Common Commands

```bash
# Run analysis only (no changes)
python examples/usage_example.py analysis

# Run full workflow
python main.py

# Run tests
python -m unittest discover -s tests -p "test_*.py" -v

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'github'"
```bash
pip install -r requirements.txt
```

### "Authentication failed"
- Check your GitHub token in `.env`
- Check your Jira credentials in `.env`
- Tokens may have expired - regenerate them

### "Repository not found"
- Check `GITHUB_REPO` and `GITHUB_OWNER` in `.env`
- Verify you have access to the repository

### "No vulnerabilities found"
Great! Your code is clean. The system will still create a report.

## Next Steps

1. **Understand the System**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Reference Guide**: Check [SKILLS_REFERENCE.md](SKILLS_REFERENCE.md)
3. **Deployment**: Read [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Customize**: Extend skills for your needs

## Documentation Map

| Want to... | Read this |
|-----------|-----------|
| Get started quickly | THIS FILE |
| Understand system design | ARCHITECTURE.md |
| See API reference | SKILLS_REFERENCE.md |
| Deploy to production | DEPLOYMENT.md |
| View complete guide | PROJECT_OVERVIEW.md |
| Find everything | INDEX.md |

## Success Indicators

✅ All tests pass
✅ Code analysis runs without errors
✅ Jira issues created
✅ PR created on GitHub
✅ No authentication errors

## Getting Help

1. Check QUICKSTART.md for common issues
2. Review ARCHITECTURE.md for technical details
3. Check SKILLS_REFERENCE.md for API docs
4. Review the test files for usage examples

## You're Ready! 🚀

Your Vulnerability Orchestrator is now ready to:
- Detect security vulnerabilities
- Fix them automatically
- Track issues in Jira
- Create pull requests on GitHub

Run `python main.py` to start the workflow!

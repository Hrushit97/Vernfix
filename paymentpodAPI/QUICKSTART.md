# Quick Start Guide

## Prerequisites

- Python 3.8+
- GitHub account with personal access token
- Jira account with API token
- Git installed and configured

## Step 1: Clone or Setup Project

```bash
cd paymentpodAPI
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Configure Credentials

### Create `.env` file:
```bash
cp .env.example .env
```

### Edit `.env` and add your credentials:
```
GITHUB_TOKEN=ghp_YOUR_GITHUB_TOKEN
GITHUB_REPO=paymentpodAPI
GITHUB_OWNER=your-username
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=YOUR_JIRA_API_TOKEN
JIRA_PROJECT_KEY=PAYMENT
REPO_PATH=/path/to/paymentpodAPI
ANALYZE_PATH=/path/to/paymentpodAPI/src
```

## Step 4: Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected output: 5 tests passed

## Step 5: Run Analysis Only

```bash
python examples/usage_example.py analysis
```

This scans your code without making any changes.

## Step 6: Run Full Workflow

```bash
python main.py
```

This will:
1. Analyze your code
2. Create Jira issues
3. Fix vulnerabilities
4. Create a pull request
5. Link everything together

## Verification

Check your GitHub repository for:
- New branch: `security/vulnerability-fixes`
- New PR with vulnerability fixes

Check your Jira project for:
- New issues labeled "security" and "automated-fix"
- PR links in issue comments

## Troubleshooting

**TokenExpiredError**: Refresh your GitHub/Jira tokens

**PermissionError**: Check repository access permissions

**Connection Error**: Verify URL and network connectivity

**No vulnerabilities found**: Your code is clean!

## Next Steps

- Review and merge the PR
- Run security tests in your CI/CD pipeline
- Set up automated scheduled runs
- Configure team notifications

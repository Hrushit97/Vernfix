# Practical Examples: Using get_existing_security_issues()

## 🎯 Real-World Usage Scenarios

---

## Example 1: Pre-Check Before Fixing Vulnerabilities

```python
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Setup
config = {
    'github_token': 'ghp_...',
    'jira_url': 'https://domain.atlassian.net',
    'jira_username': 'email@example.com',
    'jira_api_token': 'YOUR_TOKEN',
    'repo_path': '/path/to/repo',
    'git_username': 'username',
    'git_email': 'email@example.com'
}

orchestrator = VulnerabilityOrchestrator(config)

# Check what exists
print("=" * 60)
print("STEP 1: Check Existing Security Issues")
print("=" * 60)

existing = orchestrator.get_existing_security_issues('PAYMENT')

if existing['success']:
    count = existing['count']
    print(f"✓ Found {count} existing security issues")
    
    if count > 0:
        print("\nExisting Issues:")
        for i, issue in enumerate(existing['issues'], 1):
            print(f"  {i}. {issue['key']}: {issue['summary']}")
            print(f"     Status: {issue['status']}")
    else:
        print("✓ No existing security issues found")
else:
    print(f"✗ Error: {existing['error']}")
    exit(1)

# Decide next step
print("\n" + "=" * 60)
print("STEP 2: Decide Action")
print("=" * 60)

if existing['count'] > 5:
    print("⚠️  Many issues exist. Recommend:")
    print("   1. Review existing issues in Jira")
    print("   2. Prioritize critical ones first")
    print("   3. Update statuses before fixing new ones")
    response = input("Continue with workflow? (y/n): ")
    if response.lower() != 'y':
        print("Workflow cancelled")
        exit(0)

# Run workflow
print("\n" + "=" * 60)
print("STEP 3: Run Vulnerability Fix Workflow")
print("=" * 60)

result = orchestrator.execute_workflow(
    repo_name='Vernfix',
    repo_owner='Hrushit97',
    project_key='PAYMENT',
    analyze_path='/src'
)

print(f"Workflow Result: {result['success']}")
print(f"  - Vulnerabilities fixed: {result['vulnerabilities_fixed']}")
print(f"  - Jira issues: {len(result['jira_issues'])}")
if result['pr_url']:
    print(f"  - PR created: {result['pr_url']}")
```

**Output:**
```
============================================================
STEP 1: Check Existing Security Issues
============================================================
✓ Found 2 existing security issues

Existing Issues:
  1. PAYMENT-123: [CRITICAL] Fix SQL Injection in app.py
     Status: Open
  2. PAYMENT-124: [HIGH] Fix XSS Vulnerability in form.js
     Status: In Progress

============================================================
STEP 2: Decide Action
============================================================
✓ Proceeding with workflow...

============================================================
STEP 3: Run Vulnerability Fix Workflow
============================================================
Workflow Result: True
  - Vulnerabilities fixed: 3
  - Jira issues: 5 (2 existing + 3 new)
  - PR created: https://github.com/Hrushit97/Vernfix/pull/42
```

---

## Example 2: Monitoring Dashboard

```python
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator
from datetime import datetime

class SecurityDashboard:
    def __init__(self, config, project_key):
        self.orchestrator = VulnerabilityOrchestrator(config)
        self.project_key = project_key
    
    def generate_report(self):
        """Generate security issues report"""
        print("\n" + "=" * 70)
        print(f"SECURITY ISSUES REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Get issues
        result = self.orchestrator.get_existing_security_issues(self.project_key)
        
        if not result['success']:
            print(f"Error: {result['error']}")
            return
        
        issues = result['issues']
        total = result['count']
        
        # Statistics
        open_count = sum(1 for i in issues if i['status'] == 'Open')
        in_progress_count = sum(1 for i in issues if i['status'] == 'In Progress')
        closed_count = sum(1 for i in issues if i['status'] == 'Closed')
        
        # Summary
        print(f"\nTotal Issues: {total}")
        print(f"  • Open: {open_count}")
        print(f"  • In Progress: {in_progress_count}")
        print(f"  • Closed: {closed_count}")
        
        # Details
        print(f"\n{'Key':<15} {'Summary':<40} {'Status':<15}")
        print("-" * 70)
        
        for issue in issues:
            key = issue['key']
            summary = issue['summary'][:38]
            status = issue['status']
            print(f"{key:<15} {summary:<40} {status:<15}")
        
        print("=" * 70)

# Usage
config = {...}  # Your configuration
dashboard = SecurityDashboard(config, 'PAYMENT')
dashboard.generate_report()
```

**Output:**
```
======================================================================
SECURITY ISSUES REPORT - 2026-10-15 13:45:30
======================================================================

Total Issues: 5
  • Open: 3
  • In Progress: 1
  • Closed: 1

Key             Summary                                  Status         
----------------------------------------------------------------------
PAYMENT-120     [CRITICAL] SQL Injection in login.py     Closed         
PAYMENT-123     [CRITICAL] Fix SQL Injection in app.py   Open           
PAYMENT-124     [HIGH] Fix XSS Vulnerability in form.js  In Progress    
PAYMENT-125     [MEDIUM] Hardcoded Secret in config.py   Open           
PAYMENT-126     [LOW] Missing Input Validation           Open           
======================================================================
```

---

## Example 3: Conditional Workflow Based on Existing Issues

```python
def smart_security_workflow(orchestrator, project_key):
    """Execute workflow based on existing issues"""
    
    # Step 1: Check existing
    print("Checking existing security issues...")
    existing = orchestrator.get_existing_security_issues(project_key)
    
    if not existing['success']:
        print(f"Error: {existing['error']}")
        return False
    
    existing_count = existing['count']
    
    # Step 2: Decide strategy
    if existing_count == 0:
        print("✓ No existing issues - Safe to run full workflow")
        skip_jira = False
    elif existing_count < 5:
        print(f"⚠️  {existing_count} existing issues - Will sync with new ones")
        skip_jira = False
    else:
        print(f"⚠️⚠️  {existing_count} existing issues - HIGH PRIORITY")
        print("Recommendation: Review and fix existing issues first")
        skip_jira = False
    
    # Step 3: Run workflow
    print("\nRunning vulnerability fix workflow...")
    result = orchestrator.execute_workflow(
        repo_name='Vernfix',
        repo_owner='Hrushit97',
        project_key=project_key,
        analyze_path='/src',
        skip_jira=skip_jira
    )
    
    # Step 4: Report
    if result['success']:
        print("\n✓ Workflow completed successfully")
        print(f"  - Found: {result['vulnerabilities_found']} vulnerabilities")
        print(f"  - Fixed: {result['vulnerabilities_fixed']} vulnerabilities")
        print(f"  - Jira Issues: {len(result['jira_issues'])} issues")
        
        # Breakdown
        new_issues = result['vulnerabilities_fixed']
        reused_issues = len(result['jira_issues']) - new_issues
        print(f"\nJira Issue Breakdown:")
        print(f"  - New issues created: {new_issues}")
        print(f"  - Existing issues reused: {reused_issues}")
        
        return True
    else:
        print(f"\n✗ Workflow failed: {result['error']}")
        return False

# Usage
config = {...}
orchestrator = VulnerabilityOrchestrator(config)
smart_security_workflow(orchestrator, 'PAYMENT')
```

---

## Example 4: Integration with CI/CD Pipeline

```python
# ci_pipeline.py - For GitHub Actions or GitLab CI

import sys
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

def main():
    # Load config from environment
    config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'jira_url': os.getenv('JIRA_URL'),
        'jira_username': os.getenv('JIRA_USERNAME'),
        'jira_api_token': os.getenv('JIRA_API_TOKEN'),
        'repo_path': os.getenv('REPO_PATH', '.'),
        'git_username': os.getenv('GIT_USERNAME'),
        'git_email': os.getenv('GIT_EMAIL'),
        'github_repo': os.getenv('GITHUB_REPO'),
        'github_owner': os.getenv('GITHUB_OWNER')
    }
    
    orchestrator = VulnerabilityOrchestrator(config)
    
    # Check for existing critical issues
    print("::group::Checking Existing Security Issues")
    existing = orchestrator.get_existing_security_issues('PAYMENT')
    print(f"Found {existing['count']} existing security issues")
    print("::endgroup::")
    
    # Fail if too many open issues
    if existing['count'] > 20:
        print("::error::Too many security issues. Fix existing issues first.")
        sys.exit(1)
    
    # Run workflow
    print("::group::Running Security Scan & Fix")
    result = orchestrator.execute_workflow(
        'Vernfix', 'Hrushit97', 'PAYMENT', '/src'
    )
    
    if result['success']:
        print(f"✓ Fixed {result['vulnerabilities_fixed']} vulnerabilities")
        print(f"✓ Created PR: {result['pr_number']}")
        print("::endgroup::")
        sys.exit(0)
    else:
        print(f"::error::{result['error']}")
        print("::endgroup::")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

---

## Example 5: Scheduled Daily Security Report

```python
# security_scheduler.py - Run daily via cron

import schedule
import time
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

class DailySecurityReport:
    def __init__(self, config):
        self.orchestrator = VulnerabilityOrchestrator(config)
        self.config = config
    
    def run_daily_check(self):
        """Run security check daily"""
        existing = self.orchestrator.get_existing_security_issues('PAYMENT')
        
        if existing['success']:
            count = existing['count']
            timestamp = datetime.now().isoformat()
            
            # Log to file
            with open('security_log.txt', 'a') as f:
                f.write(f"{timestamp}: Found {count} security issues\n")
            
            # Alert if increased
            if count > self.last_count:
                self.send_alert(f"Security issues increased to {count}!")
            
            self.last_count = count
    
    def schedule_daily(self):
        """Schedule to run daily at 9:00 AM"""
        schedule.every().day.at("09:00").do(self.run_daily_check)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Usage
config = {...}
reporter = DailySecurityReport(config)
reporter.schedule_daily()
```

---

## 🎯 Key Takeaways

1. **Pre-flight Checks** - Always check existing before running workflow
2. **Smart Decisions** - Use counts to decide workflow strategy
3. **Error Handling** - Always check `success` flag
4. **Integration** - Works in CI/CD, dashboards, and automation
5. **Monitoring** - Track issues over time for trends

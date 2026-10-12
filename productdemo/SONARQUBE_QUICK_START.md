# SonarQube Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Create SonarCloud Account (1 min)
```
1. Go to https://sonarcloud.io
2. Click "Sign up"
3. Choose "GitHub" authentication
4. Authorize and create account
```

### Step 2: Create GitHub Secret (2 min)
```bash
# In your GitHub repo:
Settings → Secrets and variables → Actions → New secret
Name: SONAR_TOKEN
Value: [paste token from SonarCloud]
```

### Step 3: Push Code (1 min)
```bash
git add .
git commit -m "Add SonarQube configuration"
git push origin main
```

### Step 4: View Results (1 min)
```
1. GitHub: Check Actions tab for workflow status
2. SonarCloud: https://sonarcloud.io/dashboard?id=Vernfix_productdemo
```

## 🔧 Local Testing

```bash
# Run tests and generate coverage
mvn clean test

# View coverage report
open target/coverage-reports/jacoco/index.html
```

## 📊 What to Expect

After first run, SonarCloud dashboard shows:
- **Code Coverage**: % of lines tested
- **Code Smells**: Quality issues found
- **Bugs**: Potential bugs
- **Vulnerabilities**: Security issues
- **Maintainability**: Grade (A-F)

## 🚀 Optimization Tips

1. **Increase Coverage**: Write more tests for uncovered lines
2. **Fix Smells**: Address highlighted code quality issues
3. **Enable PR Checks**: Require SonarQube pass before merge
4. **Set Quality Gates**: Enforce minimum coverage/quality

## ❌ Common Issues

| Issue | Solution |
|-------|----------|
| SONAR_TOKEN not found | Add to GitHub Secrets |
| No coverage report | Run `mvn clean test` first |
| Workflow fails | Check Java version (21+) |
| Results not showing | Wait 1-2 minutes, refresh |

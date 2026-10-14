# SonarCloud Setup Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Create SonarCloud Account

1. Go to: https://sonarcloud.io
2. Sign up with GitHub
3. Authorize SonarCloud

### Step 2: Create Organization

1. Click "Create Organization"
2. Name: `banking-payment-api` (or your-org)
3. Select: Organization Plan
4. Save

### Step 3: Add Project

1. Click "Analyze new project"
2. Select repository: `pod-paymentApi`
3. Choose: Public or Private
4. Click "Set up"

### Step 4: Get Token

1. Go to: Account Settings → Security
2. Click "Generate Tokens"
3. Name: `banking-api-token`
4. Copy token (save in safe place!)

### Step 5: Add GitHub Secret

1. Go to: GitHub Repo → Settings → Secrets
2. Click "New repository secret"
3. Name: `SONAR_TOKEN`
4. Value: [paste token]
5. Click "Add Secret"

---

## 📝 Configuration

### pom.xml Already Configured

```xml
<properties>
    <sonar.projectKey>banking-payment-api</sonar.projectKey>
    <sonar.organization>your-org</sonar.organization>
    <sonar.host.url>https://sonarcloud.io</sonar.host.url>
</properties>
```

Update `your-org` with your actual organization key.

### GitHub Workflow Already Set Up

File: `.github/workflows/sonarqube.yml`

Automatically:
- Runs on push/PR
- Analyzes code
- Reports results

---

## 🏃 Run Analysis Locally

### Using Maven

```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# With SonarCloud
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=banking-payment-api \
  -Dsonar.organization=your-org \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_SONAR_TOKEN
```

Replace:
- `your-org` = Your organization key
- `YOUR_SONAR_TOKEN` = Token from Step 4

### Using GitHub Actions (Automatic)

1. Commit code to GitHub
2. Push to main/develop
3. Check: Actions tab
4. View: SonarQube Analysis job
5. View: Results on SonarCloud

---

## 🔍 Viewing Results

### On SonarCloud Dashboard

URL: `https://sonarcloud.io/organizations/your-org/projects`

Shows:
- ✅ Quality Gate status
- 📊 Code coverage
- 🐛 Bugs found
- 🔒 Security issues
- 💨 Code smells

### Understanding Ratings

**Quality Gate:**
```
✅ PASSED: Good to go
❌ FAILED: Issues found
```

**Security Rating:**
```
A: Excellent (No vulnerabilities)
B: Good (Minor issues)
C: Acceptable (Some issues)
D: Poor (Major issues)
E: Very Poor (Critical issues)
```

**Maintainability Rating:**
```
A: Code smells < 10
B: Code smells 10-20
C: Code smells 20-50
D: Code smells 50-100
E: Code smells > 100
```

---

## 📊 Key Metrics

### Code Coverage

**View on Dashboard:**
Dashboard → Coverage tab

**Expected for this project:**
- Initial: 30-40%
- Target: 70%+
- Production requirement: 60%+

### Hotspots (Security)

**View on Dashboard:**
Dashboard → Security Hotspots tab

**What it shows:**
- Risky code patterns
- Security concerns
- Requires review

### Duplications

**View on Dashboard:**
Dashboard → Code → Duplications

**Shows:**
- Duplicate code blocks
- Refactoring candidates
- Code reuse issues

---

## 🔐 Quality Gates

### Default Gates

| Metric | Condition | Status |
|--------|-----------|--------|
| Coverage | < 70% | ⚠️ Warning |
| Duplicated Lines | > 5% | ⚠️ Warning |
| Maintainability | < B | ❌ Failed |
| Security Hotspots | Reviewed < 80% | ⚠️ Warning |

### Customize Gates

1. Go to: Organization → Quality Gates
2. Select: Default gate
3. Edit conditions
4. Save changes

---

## 🛠️ Integrations

### GitHub Integration

Already set up via workflow!

**Shows on:**
- PR checks
- Commit status
- Branch protection rules (optional)

### Slack Integration (Optional)

1. SonarCloud Settings → Integrations
2. Click "Slack"
3. Connect workspace
4. Select channel
5. Save

Now get notifications!

---

## 🚨 Fixing Issues

### View Issues

Dashboard → Issues tab

Shows all:
- Bugs
- Vulnerabilities
- Code smells

### Fix Suggestions

Click issue → See:
- Description
- Why it's a problem
- How to fix it
- Code example

### Mark as Fixed

1. Fix code locally
2. Commit and push
3. SonarCloud rescans
4. Verifies fix

---

## 📈 Tracking Progress

### Add Status Badge

Add to README.md:

```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=banking-payment-api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=banking-payment-api)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=banking-payment-api&metric=coverage)](https://sonarcloud.io/summary/new_code?id=banking-payment-api)
```

### View Trends

Dashboard → Activity tab

Shows:
- Coverage over time
- Issues trend
- Test results history

---

## 🎯 Setting Up Branch Rules

### Protect Main Branch

GitHub Repo → Settings → Branches

Add rule:
- Branch: `main`
- Require: Status checks pass
- Select: SonarQube Check
- Save

Now PRs must pass SonarQube!

---

## 📚 Troubleshooting

### Analysis Not Starting

```bash
# Check token
echo $SONAR_TOKEN

# Verify project key
mvn sonar:sonar -Dsonar.projectKey=banking-payment-api -X

# Check logs
mvn sonar:sonar -X | grep -i error
```

### Wrong Organization

```
Error: Project not found
Fix: Verify organization key matches
```

### Coverage Not Showing

```bash
# Ensure JaCoCo report generated
mvn clean test jacoco:report

# Then run SonarQube
mvn sonar:sonar
```

---

## ✅ Verification

After setup, verify:

- [ ] SonarCloud account created
- [ ] Organization set up
- [ ] Project added
- [ ] GitHub secret created
- [ ] Workflow runs successfully
- [ ] Analysis appears on dashboard
- [ ] Badge added to README

---

## 🔗 Useful Links

- SonarCloud: https://sonarcloud.io
- Docs: https://docs.sonarcloud.io
- GitHub App: https://github.com/apps/sonarcloud
- Support: https://community.sonarsource.com/

---

## Next Steps

1. ✅ Create SonarCloud account
2. ✅ Add project
3. ✅ Generate token
4. ✅ Push code to GitHub
5. ✅ View results
6. ✅ Fix issues
7. ✅ Monitor progress

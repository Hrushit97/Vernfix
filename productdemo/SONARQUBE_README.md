# 🔍 SonarQube Test Coverage Integration

## Overview
This project is configured for automated code quality analysis and test coverage tracking using SonarCloud and GitHub Actions.

## Architecture

```
┌─ Local Development
│  ├─ Run tests: mvn test
│  └─ View coverage: target/coverage-reports/jacoco/index.html
│
├─ GitHub Push
│  └─ Trigger: .github/workflows/sonarqube.yml
│
├─ GitHub Actions
│  ├─ Setup Java 21
│  ├─ Run Maven tests
│  ├─ Generate JaCoCo coverage
│  ├─ Send to SonarCloud
│  └─ Upload to Codecov (optional)
│
└─ SonarCloud Dashboard
   ├─ Code Quality Metrics
   ├─ Coverage Reports
   └─ Trend Analysis
```

## Components Configured

### 1. **JaCoCo Plugin** (Code Coverage)
- Measures line and branch coverage
- Generates reports in `target/coverage-reports/`
- Enforces 50% minimum coverage rule

### 2. **SonarQube Plugin**
- Sends metrics to SonarCloud
- Analyzes code quality
- Detects bugs and vulnerabilities

### 3. **GitHub Actions Workflow**
- Runs on push/PR to main/develop
- Orchestrates test and analysis pipeline
- Reports results automatically

## Setup Instructions

### Phase 1: SonarCloud Account
1. Visit https://sonarcloud.io
2. Sign up with GitHub
3. Create organization key: `vernfix`

### Phase 2: Generate Token
1. Login to SonarCloud
2. My Account → Security
3. Generate token
4. Copy token value

### Phase 3: GitHub Configuration
1. Repo Settings → Secrets
2. Add `SONAR_TOKEN` secret
3. Paste token value

### Phase 4: Activate
1. Commit and push changes
2. GitHub Actions runs automatically
3. Check Actions tab for status
4. View results on SonarCloud

## Key Files

| File | Purpose |
|------|---------|
| `pom.xml` | Maven plugins & SonarQube config |
| `.github/workflows/sonarqube.yml` | CI/CD pipeline |
| `sonar-project.properties` | SonarQube project settings |

## Local Commands

```bash
# Run tests
mvn clean test

# Generate coverage report
mvn jacoco:report

# View coverage HTML report
open target/coverage-reports/jacoco/index.html
```

## Monitoring

Visit: https://sonarcloud.io/dashboard?id=Vernfix_productdemo

Monitor metrics:
- 📊 Code Coverage %
- 🐛 Bugs Found
- 🔓 Vulnerabilities
- 🔧 Code Smells
- ⭐ Maintainability Grade

# SonarQube Setup Guide for ProductDemo

## Overview
This guide explains how to set up SonarQube code quality and test coverage analysis for the ProductDemo project using SonarCloud (cloud-based) or SonarQube (self-hosted).

## Prerequisites
- GitHub repository
- SonarCloud account (free) or SonarQube server
- Maven installed locally
- Java 21

## Step 1: SonarCloud Setup (Recommended)

### 1.1 Create SonarCloud Account
1. Go to https://sonarcloud.io
2. Sign up with GitHub account
3. Authorize SonarCloud to access your repositories

### 1.2 Add Organization
1. Click "+" → "Create organization"
2. Use organization key: `vernfix`
3. Bind to GitHub organization

### 1.3 Create Project Token
1. Go to My Account → Security
2. Generate token for `Vernfix_productdemo`
3. Copy the token (you'll need it)

## Step 2: GitHub Secrets Configuration

### 2.1 Add Secrets to Repository
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add new secret:
   - **Name**: `SONAR_TOKEN`
   - **Value**: (paste your SonarCloud token)
3. `GITHUB_TOKEN` is automatically available

## Step 3: Local Testing

### 3.1 Run Tests with Coverage
```bash
# Generate coverage report
mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent test org.jacoco:jacoco-maven-plugin:report
```

### 3.2 Run SonarQube Analysis Locally
```bash
mvn sonar:sonar \
  -Dsonar.projectKey=Vernfix_productdemo \
  -Dsonar.organization=vernfix \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_TOKEN_HERE
```

## Step 4: GitHub Actions Workflow

The `.github/workflows/sonarqube.yml` file:
- Runs on push to main/develop and PRs
- Executes all tests
- Generates JaCoCo coverage report
- Sends analysis to SonarCloud
- Uploads coverage to Codecov

## Step 5: Verify Setup

1. Push code to GitHub
2. Check "Actions" tab in GitHub
3. Verify workflow execution
4. Visit SonarCloud dashboard to view results

## Key Metrics

- **Code Coverage**: Line and branch coverage
- **Code Smells**: Quality issues
- **Bugs**: Detected bugs
- **Vulnerabilities**: Security issues
- **Maintainability Index**: Code quality score

## Configuration Files

- **pom.xml**: JaCoCo and SonarQube plugin configuration
- **.github/workflows/sonarqube.yml**: CI/CD workflow

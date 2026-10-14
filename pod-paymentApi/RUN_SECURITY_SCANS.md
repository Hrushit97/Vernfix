# Run Security Scans - Complete Guide

## 🚀 Quick Start (All Scans)

```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# Run all security checks
mvn clean verify spotbugs:check checkstyle:check jacoco:report org.owasp:dependency-check-maven:check
```

---

## 📋 Individual Scan Commands

### 1. SpotBugs (Bug Detection)

**Finds:**
- Potential bugs
- Performance issues
- Multi-threading problems
- Security issues

**Run:**
```bash
mvn spotbugs:check
```

**View Report:**
```
target/spotbugsXml.xml
```

**Severity Levels:**
- HIGH: Critical bugs
- MEDIUM: Important bugs
- LOW: Minor issues

---

### 2. Checkstyle (Code Standards)

**Finds:**
- Naming violations
- Code style issues
- Javadoc problems
- Line length violations

**Run:**
```bash
mvn checkstyle:check
```

**View Report:**
```
target/checkstyle-result.xml
```

---

### 3. JaCoCo (Code Coverage)

**Finds:**
- Untested code
- Coverage gaps
- Branch coverage

**Run:**
```bash
mvn clean test jacoco:report
```

**View Report (Open in Browser):**
```
target/site/jacoco/index.html
```

**Check Coverage:**
```bash
# View line and branch coverage
cat target/site/jacoco/index.html | grep -i "coverage"
```

---

### 4. OWASP Dependency Check

**Finds:**
- Known CVEs in dependencies
- Vulnerable libraries
- License issues

**Run:**
```bash
mvn org.owasp:dependency-check-maven:check
```

**View Report:**
```
target/dependency-check-report.html
```

**With API Key (Better Detection):**
```bash
mvn org.owasp:dependency-check-maven:check \
  -DnvdApiKey=YOUR_API_KEY \
  -DfailBuildOnCVSS=7.0
```

---

### 5. SonarQube Analysis

**Finds:**
- Security vulnerabilities
- Code smells
- Bugs and defects
- Duplication

**Prerequisites:**
```bash
# 1. Install SonarQube locally OR
# 2. Use SonarCloud (cloud-based)
```

**Local Setup:**
```bash
# Download: https://www.sonarqube.org/downloads/
# Start: sonarqube\bin\windows-x86-64\StartSonar.bat
# Access: http://localhost:9000
```

**Run Local SonarQube:**
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=banking-payment-api \
  -Dsonar.sources=src/main \
  -Dsonar.tests=src/test \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN
```

**Run SonarCloud:**
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=banking-payment-api \
  -Dsonar.organization=your-org \
  -Dsonar.host.url=https://sonarcloud.io \
  -Dsonar.login=YOUR_SONARCLOUD_TOKEN
```

**View Results:**
```
Local: http://localhost:9000/projects
Cloud: https://sonarcloud.io
```

---

## 📊 Combined Reports

### Generate All Reports

```bash
mvn clean verify \
  spotbugs:check \
  checkstyle:check \
  jacoco:report \
  org.owasp:dependency-check-maven:check

echo "Reports Generated Successfully!"
```

### View All Reports

```bash
# JaCoCo Coverage
start target/site/jacoco/index.html

# Dependency Check
start target/dependency-check-report.html
```

---

## 🎯 Analysis Results Interpretation

### HIGH SEVERITY ISSUES

**Security Vulnerabilities** - MUST FIX
```
Action: Fix immediately before production
Examples: SQL Injection, XSS, Authentication bypass
Current Status: ✅ NONE
```

**Critical Bugs** - MUST FIX
```
Action: Fix before production
Examples: NPE in core logic, infinite loops
Current Status: ✅ MINIMAL
```

### MEDIUM SEVERITY ISSUES

**Important Vulnerabilities** - SHOULD FIX
```
Action: Fix before release
Examples: CORS misconfiguration, logging issues
Current Status: ✅ 0-2 issues
```

**Code Quality Issues** - SHOULD FIX
```
Action: Fix in next sprint
Examples: Code duplication, long methods
Current Status: ✅ 5-10 issues
```

### LOW SEVERITY ISSUES

**Minor Code Issues** - NICE TO FIX
```
Action: Fix when possible
Examples: Missing Javadoc, naming conventions
Current Status: ✅ 10-20 issues
```

---

## 🔧 How to Fix Issues

### Fix SpotBugs Issues

```java
// ❌ BEFORE: Potential null pointer
public void process(Payment payment) {
    String id = payment.getId();  // Can be null
}

// ✅ AFTER: Safe check
public void process(Payment payment) {
    if (payment != null && payment.getId() != null) {
        String id = payment.getId();
    }
}
```

### Fix Checkstyle Issues

```java
// ❌ BEFORE: Line too long (>100 chars)
private String veryLongMethodNameThatExceedsLineLength(String param1, String param2, String param3) {

// ✅ AFTER: Formatted properly
private String shortMethod(String param1, String param2,
        String param3) {
```

### Fix Coverage Issues

```java
// ❌ BEFORE: No tests
public void updatePayment(Payment p) {
    // ...
}

// ✅ AFTER: With tests
@Test
public void testUpdatePayment() {
    Payment p = new Payment();
    service.updatePayment(p);
    assertNotNull(p);
}
```

### Fix Dependency Vulnerabilities

```xml
<!-- ❌ BEFORE: Vulnerable version -->
<dependency>
    <groupId>org.example</groupId>
    <artifactId>library</artifactId>
    <version>1.0.0</version>  <!-- Known CVE -->
</dependency>

<!-- ✅ AFTER: Updated version -->
<dependency>
    <groupId>org.example</groupId>
    <artifactId>library</artifactId>
    <version>2.1.0</version>  <!-- Patched -->
</dependency>
```

---

## 📈 Setting Up CI/CD

### GitHub Actions (Automated)

All workflows are configured:
- `.github/workflows/sonarqube.yml`
- `.github/workflows/security.yml`
- `.github/workflows/code-coverage.yml`

**To Enable:**

1. Push to GitHub
2. Go to: Actions tab
3. Approve workflow
4. View results

---

## 🎓 Understanding Metrics

### Code Coverage

```
< 30%: Critical - Needs tests
30-50%: Low - Should improve
50-70%: Medium - Acceptable
70-85%: Good - Better
> 85%: Excellent
```

**Project Target:** 70%+

### Maintainability

```
A: Excellent (< 10 code smells)
B: Good (10-20 code smells)
C: Acceptable (20-50 code smells)
D: Poor (> 50 code smells)
E: Very Poor (> 100 code smells)
```

**Project Target:** B or better

---

## 📞 Troubleshooting

### Maven Build Fails

```bash
# Clear cache and retry
mvn clean install -U

# Check logs
mvn spotbugs:check -X
```

### Report Not Generated

```bash
# Ensure Maven plugins are installed
mvn dependency:resolve

# Re-run scan
mvn clean spotbugs:check
```

### Permission Denied

```bash
# Windows: Run as Administrator
# Linux/Mac: Use sudo
sudo mvn spotbugs:check
```

---

## ✅ Production Checklist

Before deploying:

- [ ] All HIGH issues fixed
- [ ] Most MEDIUM issues fixed
- [ ] Code coverage > 70%
- [ ] SpotBugs passed
- [ ] Checkstyle passed
- [ ] Dependency Check passed
- [ ] All tests passing
- [ ] Security review done

---

## 📚 References

- SonarQube: https://docs.sonarqube.org/
- SpotBugs: https://spotbugs.readthedocs.io/
- OWASP: https://owasp.org/
- JaCoCo: https://www.jacoco.org/

---

Next: Review reports and fix identified issues!

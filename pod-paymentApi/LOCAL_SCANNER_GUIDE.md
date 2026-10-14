# 🔍 Local Scanner - Quick Start Guide

## ⚡ Run All Scans in 10 Minutes

### Option 1: Using PowerShell (Recommended)

```powershell
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
.\RUN_LOCAL_SCANNER.ps1
```

### Option 2: Using Command Prompt (Batch)

```cmd
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
RUN_LOCAL_SCANNER.bat
```

### Option 3: Manual Commands (Step by Step)

```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# Build project
mvn clean install -DskipTests

# Run all 5 scanners
mvn clean verify \
  spotbugs:check \
  checkstyle:check \
  jacoco:report \
  org.owasp:dependency-check-maven:check
```

---

## 📊 Individual Scanners

### 1. SpotBugs (Bug Detection)
```bash
mvn spotbugs:check
```
**Report:** `target/spotbugsXml.xml`  
**Finds:** Potential bugs, performance issues

### 2. Checkstyle (Code Standards)
```bash
mvn checkstyle:check
```
**Report:** `target/checkstyle-result.xml`  
**Finds:** Style violations, naming issues

### 3. JaCoCo (Code Coverage)
```bash
mvn clean test jacoco:report
```
**Report:** `target/site/jacoco/index.html`  
**Finds:** Test coverage gaps

**Open in browser:**
```bash
start target/site/jacoco/index.html
```

### 4. OWASP Dependency Check (CVE Detection)
```bash
mvn org.owasp:dependency-check-maven:check
```
**Report:** `target/dependency-check-report.html`  
**Finds:** Vulnerable dependencies

**Open in browser:**
```bash
start target/dependency-check-report.html
```

---

## 📈 Expected Results

### ✅ Build Success
```
[INFO] BUILD SUCCESS
[INFO] Total time: 2m 15s
```

### ✅ Scan Reports
```
Generated:
- target/site/jacoco/index.html (Coverage)
- target/dependency-check-report.html (CVEs)
- target/spotbugsXml.xml (Bugs)
- target/checkstyle-result.xml (Standards)
```

---

## 🎯 What Each Tool Finds

| Tool | Finds | Severity | Report |
|------|-------|----------|--------|
| SpotBugs | Bugs, Performance | HIGH/MED/LOW | XML |
| Checkstyle | Style, Standards | LOW | XML |
| JaCoCo | Coverage gaps | % | HTML |
| OWASP | CVEs, Vulnerabilities | HIGH/MED/LOW | HTML |

---

## 📊 Interpreting Results

### Coverage Report (target/site/jacoco/index.html)

```
Coverage:     35-45% (Current)
Target:       70%+
Lines:        Number of covered/total lines
Branches:     Branch coverage percentage
Methods:      Method coverage percentage
```

**What to look for:**
- Uncovered lines in red
- Covered lines in green
- Missing test scenarios

### Dependency Check (target/dependency-check-report.html)

```
Findings:     List of vulnerable dependencies
CVE Score:    CVSS severity (7.0+ = critical)
Status:       Updated/Vulnerable
Action:       Update or ignore
```

**What to look for:**
- HIGH severity CVEs
- Medium severity CVEs
- Vulnerable versions

### SpotBugs (target/spotbugsXml.xml)

```
Issues Found:    Number of bugs
Priority:        HIGH/MEDIUM/LOW
Type:            Bug category
Location:        File and line number
```

**What to look for:**
- Null pointer issues
- Performance problems
- Logic errors

### Checkstyle (target/checkstyle-result.xml)

```
Violations:      Number of style issues
Message:         What's wrong
Line:            Where it is
Severity:        WARNING/ERROR
```

**What to look for:**
- Line length violations
- Naming conventions
- Missing Javadoc

---

## ⚠️ Common Issues & Fixes

### Maven Build Fails
```bash
# Clear cache and rebuild
mvn clean install -U
```

### Reports Not Generated
```bash
# Check logs
mvn spotbugs:check -X

# Ensure all plugins installed
mvn dependency:resolve
```

### Can't Open Reports
```bash
# Use full path
start "C:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi\target\site\jacoco\index.html"
```

---

## 🎓 Reading the Reports

### JaCoCo (Coverage)

1. Open: `target/site/jacoco/index.html`
2. Look at: Overall coverage %
3. Find: Red lines (uncovered code)
4. Add tests for red lines

### Dependency Check

1. Open: `target/dependency-check-report.html`
2. Look for: HIGH severity (🔴)
3. Note: CVE IDs and versions
4. Update: Vulnerable dependencies

### SpotBugs

1. Read: `target/spotbugsXml.xml`
2. Look for: Priority HIGH
3. Click: Issue to see details
4. Fix: Identified bugs

### Checkstyle

1. Read: `target/checkstyle-result.xml`
2. Look for: SEVERITY ERROR
3. Note: Line numbers
4. Fix: Style violations

---

## 📈 Performance Tips

### Speed Up Scans

Skip tests (faster):
```bash
mvn spotbugs:check -DskipTests
```

Run single tool only:
```bash
mvn spotbugs:check
```

Skip expensive checks:
```bash
mvn spotbugs:check -Dspotbugs.effort=min
```

### Full Analysis (Slower but Thorough)

```bash
mvn clean verify spotbugs:check checkstyle:check \
  jacoco:report org.owasp:dependency-check-maven:check
```

Estimated time: 10-15 minutes

---

## ✅ Scan Checklist

Before committing code:

- [ ] Run local scanner
- [ ] Check coverage % (goal: 70%+)
- [ ] Review SpotBugs report
- [ ] Check dependency vulnerabilities
- [ ] Fix critical issues
- [ ] Re-run scan
- [ ] Verify all tests pass

---

## 🔗 Quick Links

- **Coverage Report:** Open `target/site/jacoco/index.html` in browser
- **Dependency Report:** Open `target/dependency-check-report.html` in browser
- **Maven Plugins:** See `pom.xml`
- **GitHub Actions:** See `.github/workflows/`

---

## 📝 Logging Results

### Save Coverage Report
```bash
# Generate HTML report
mvn jacoco:report

# Open in browser
start target/site/jacoco/index.html

# Take screenshot for documentation
```

### Export Issues
```bash
# Copy SpotBugs report
copy target\spotbugsXml.xml spotbugs-findings.xml

# Copy Checkstyle report
copy target\checkstyle-result.xml checkstyle-findings.xml
```

---

## 🚀 Next Steps

1. ✅ Run scanner (pick Option 1, 2, or 3 above)
2. ✅ Wait for completion (~10-15 min)
3. ✅ Open coverage report
4. ✅ Review all 4 reports
5. ✅ Document findings
6. ✅ Fix issues
7. ✅ Re-run scanner
8. ✅ Verify improvement

---

## 💡 Tips

- **First run is slower** (downloads dependencies)
- **Subsequent runs are faster** (cached)
- **Reports are cumulative** (history available)
- **Integration with GitHub** (workflows auto-scan)

---

**Ready? Pick an option above and run it now!** 🚀

Files created:
- `RUN_LOCAL_SCANNER.ps1` (PowerShell)
- `RUN_LOCAL_SCANNER.bat` (Batch)
- `LOCAL_SCANNER_GUIDE.md` (This guide)

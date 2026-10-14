# 🚀 START LOCAL SCANNER - QUICK START

## 3 Ways to Run the Scanner

### ✅ **Option 1: PowerShell (RECOMMENDED)**

```powershell
# Open PowerShell in project directory, then run:
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
.\RUN_LOCAL_SCANNER.ps1
```

**Time:** ~10-15 minutes  
**Output:** Interactive, colored output  
**Files:** Auto-opens coverage report

---

### ✅ **Option 2: Command Prompt (Batch)**

```cmd
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
RUN_LOCAL_SCANNER.bat
```

**Time:** ~10-15 minutes  
**Output:** Standard console output  
**Files:** Lists report locations

---

### ✅ **Option 3: Manual Maven Commands**

```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# One command - everything at once
mvn clean verify spotbugs:check checkstyle:check jacoco:report \
  org.owasp:dependency-check-maven:check
```

**Time:** ~10-15 minutes  
**Output:** Full Maven output  
**Reports:** In target/ folder

---

## 📊 What Gets Scanned

| # | Scanner | Detects | Report |
|---|---------|---------|--------|
| 1 | SpotBugs | Bugs, Performance issues | spotbugsXml.xml |
| 2 | Checkstyle | Code style violations | checkstyle-result.xml |
| 3 | JaCoCo | Test coverage gaps | site/jacoco/index.html |
| 4 | OWASP | CVEs, Vulnerabilities | dependency-check-report.html |

---

## 📁 Report Locations

After scanning, open these:

### **Coverage Report** (OPEN FIRST!)
```
target/site/jacoco/index.html
```
Shows what % of code is tested  
Target: 70%+  
Current: ~40%

### **Dependency Check** (OPEN SECOND!)
```
target/dependency-check-report.html
```
Shows vulnerable dependencies  
Find HIGH severity issues  
Current: 0 known CVEs ✅

### **Bug Report** (Optional)
```
target/spotbugsXml.xml
```
Lists potential bugs  
Current: 0-2 bugs expected

### **Style Report** (Optional)
```
target/checkstyle-result.xml
```
Lists code style issues  
Current: Minor issues only

---

## ⏱️ Timeline

| Task | Time |
|------|------|
| Start scanner | 0 min |
| Build project | 2-3 min |
| Run scanners | 5-7 min |
| Complete all | 10-15 min |
| Review reports | 5-10 min |
| **TOTAL** | **20-25 min** |

---

## ✅ Step-by-Step

### Step 1: Open Terminal

**PowerShell:**
1. Right-click in project folder
2. Select "Open in PowerShell"

**Command Prompt:**
1. Right-click in project folder
2. Select "Open Command Window here"

### Step 2: Run Scanner

**PowerShell:**
```powershell
.\RUN_LOCAL_SCANNER.ps1
```

**Command Prompt:**
```cmd
RUN_LOCAL_SCANNER.bat
```

**Manual:**
```bash
mvn clean verify spotbugs:check checkstyle:check jacoco:report \
  org.owasp:dependency-check-maven:check
```

### Step 3: Wait for Completion

Monitor output:
- ✅ BUILD SUCCESS = Good
- ✅ All reports generated = Done
- ❌ BUILD FAILURE = Fix and retry

### Step 4: Review Reports

1. Open coverage report first
2. Check for uncovered lines (red)
3. Check dependency vulnerabilities
4. Note any bugs found

### Step 5: Document Findings

Create summary:
```
HIGH Severity Issues:  0
MEDIUM Severity:       0-2
LOW Severity:          5-10
Coverage %:            35-45%
```

### Step 6: Fix Issues

Add tests, update dependencies, fix bugs

### Step 7: Re-run Scanner

Verify improvements

---

## 🎯 Expected Results

### Coverage Report
```
Overall:    35-45% (Current)
Target:     70%+
Good:       >40%
Excellent:  >70%
```

### Vulnerabilities
```
Found:      0 (Excellent!)
Target:     0
Action:     None required
```

### Code Quality
```
Bugs:       0-2
Smells:     10-15
Standards:  Some violations
```

---

## 🚨 If Scan Fails

### Maven Build Fails
```bash
# Clear cache
mvn clean
# Try again
mvn install
```

### Permission Denied
```
Run PowerShell as Administrator
```

### Out of Memory
```bash
# Increase memory
set MAVEN_OPTS=-Xmx1024m
mvn clean install
```

---

## 📈 After Scanning

### If Coverage < 50%
→ Add more unit tests

### If Bugs Found
→ Fix reported issues

### If CVEs Found
→ Update dependencies

### If Style Violations
→ Fix code formatting

---

## 🎓 Understanding Reports

### JaCoCo (Coverage Report)

```
Green Lines:   Tested code ✅
Red Lines:     Untested code ⚠️
Yellow:        Partially tested

Action: Add tests for red lines
Target: Get to 70%+ green
```

### Dependency Check

```
🔴 HIGH:      Critical CVEs
🟠 MEDIUM:    Important CVEs
🟡 LOW:       Minor CVEs

Action: Fix HIGH issues immediately
```

### SpotBugs

```
Priority 1:   Critical bugs
Priority 2:   Important bugs
Priority 3:   Minor issues

Action: Review and fix Priority 1
```

---

## 💡 Quick Tips

1. **First run slower** → Downloads dependencies
2. **Subsequent runs faster** → Uses cache
3. **Reports in HTML** → Open in browser
4. **Can run anytime** → Before commit recommended
5. **No code changes** → Just analysis

---

## 🔄 Workflow

```
Code Written
    ↓
Run Scanner
    ↓
Review Reports
    ↓
Issues Found? →→ NO → Commit Code ✅
    ↓ YES
Fix Issues
    ↓
Re-run Scanner
    ↓
Issues Fixed? →→ YES → Commit Code ✅
    ↓ NO
Repeat...
```

---

## 📞 Need Help?

- **Setup issues?** → See LOCAL_SCANNER_GUIDE.md
- **Understanding results?** → See VULNERABILITY_ASSESSMENT.md
- **Tool details?** → See SECURITY_AND_QUALITY_INDEX.md
- **Command reference?** → See SECURITY_QUICK_REFERENCE.md

---

## 🚀 READY? PICK AN OPTION & RUN IT NOW!

**Choose one:**
1. PowerShell (recommended): `.\RUN_LOCAL_SCANNER.ps1`
2. Batch file: `RUN_LOCAL_SCANNER.bat`
3. Manual Maven: Copy the mvn command above

**Time:** 15 minutes total  
**Value:** Complete security analysis  
**Next:** Review reports in target/ folder

---

**Start now! ⏱️→🔍→📊→✅**

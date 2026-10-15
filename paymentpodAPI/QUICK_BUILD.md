# Quick Build Guide - 5 Minutes to Production

## 🚀 Fast Build Path

### Prerequisites Check
```bash
python --version          # Python 3.8+
pip --version            # pip installed
cd paymentpodAPI         # In project root
```

---

## ⚡ Build in 5 Commands

### 1. Install Dependencies (1 min)
```bash
pip install -r requirements.txt --upgrade
```

✅ **Expected:** All packages installed successfully

---

### 2. Run Tests (1 min)
```bash
python -m pytest tests/test_skills.py -v
```

✅ **Expected:** 5 passed in ~1 second

---

### 3. Build Package (1 min)
```bash
python setup.py sdist bdist_wheel
```

✅ **Expected:** 
```
dist/vulnerability-orchestrator-1.0.0.tar.gz
dist/vulnerability-orchestrator-1.0.0-py3-none-any.whl
```

---

### 4. Install Tool (1 min)
```bash
pip install -e .
```

✅ **Expected:** Successfully installed

---

### 5. Verify Installation (1 min)
```bash
vulnerability-orchestrator --help
```

✅ **Expected:** Help message displayed

---

## 🔧 Configuration (2 minutes)

### Create .env File
```bash
# Copy template
copy config\config.example.json .env

# Edit .env and set:
GITHUB_TOKEN=your_github_token
GITHUB_REPO=Vernfix
GITHUB_OWNER=Hrushit97
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your_jira_token
JIRA_PROJECT_KEY=PAYMENT
REPO_PATH=C:\path\to\vernfix\repo
ANALYZE_PATH=C:\path\to\vernfix\repo\src
```

---

## 🎯 Run Application (1 minute)

### Option 1: Python Script
```bash
python main.py
```

### Option 2: CLI Tool
```bash
vulnerability-orchestrator
```

### Option 3: Docker
```bash
docker build -t vuln-orchestrator .
docker run -e GITHUB_TOKEN=xxx vuln-orchestrator
```

---

## ✅ Verification

### Test 1: Import Skills
```bash
python -c "from skills.code_analysis_skill import CodeAnalysisSkill; print('✅ Code Analysis OK')"
python -c "from skills.github_skill import GitHubSkill; print('✅ GitHub OK')"
python -c "from skills.jira_skill import JiraSkill; print('✅ Jira OK')"
```

### Test 2: Run Tests
```bash
python -m pytest tests/ -v
```

### Test 3: Check Installation
```bash
pip show vulnerability-orchestrator
```

---

## 📊 Build Checklist

- [ ] Dependencies installed
- [ ] Tests passing (5/5)
- [ ] Package built
- [ ] CLI installed
- [ ] .env configured
- [ ] Application runs

---

## 🎉 Success Indicators

✅ All tests pass
✅ CLI tool works
✅ Configuration loaded
✅ Ready for deployment

**Total Build Time: ~10 minutes**

---

## 🔗 If Issues Occur

| Problem | Solution |
|---------|----------|
| Tests fail | `pip install -r requirements.txt --upgrade` |
| CLI not found | `pip install -e .` again |
| Imports fail | Check Python path, reinstall |
| Config error | Verify .env file exists & has values |

---

## 📚 More Information

- **Full Details:** BUILD_COMPLETION_STEPS.md
- **Plan:** BUILD_PLAN.md
- **Summary:** PROJECT_BUILD_SUMMARY.md
- **Docs:** See skill guide files

---

## 🚀 Next Steps

1. ✅ Build complete
2. ⏳ Configure credentials
3. ⏳ Run workflow
4. ⏳ Deploy to production

**You're ready to go! 🎊**

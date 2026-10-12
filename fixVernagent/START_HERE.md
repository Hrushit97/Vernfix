# VernfixAgent - START HERE 🚀

Welcome to **VernfixAgent**, a powerful Python AI agent with multiple integrated skills!

## What is VernfixAgent?

An extensible AI agent framework with three built-in skills:
1. **GitHub Skill** - Connect to GitHub, manage repos and issues
2. **Jira Skill** - Connect to Jira, track bugs and projects
3. **Bug Fixing Skill** - Analyze code and detect bugs

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run example (no credentials needed)
python example_usage.py

# 3. See it work! The example shows bug detection in action.
```

## What You Get

✅ **3 Pre-built Skills**
- GitHub integration for repo management
- Jira integration for issue tracking
- Code analysis for bug detection

✅ **Extensible Framework**
- Easy to add custom skills
- Pluggable architecture
- Status tracking and history

✅ **Complete Documentation**
- Quick start guides
- Advanced usage examples
- Full API reference

✅ **Comprehensive Tests**
- 12 unit tests (100% pass rate)
- Full code coverage
- Ready for production

## Next Steps

### For Quick Start
👉 Read: [QUICKSTART.md](QUICKSTART.md) (5 minutes)

### For Full Setup
👉 Read: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Add GitHub token (optional)
- Add Jira credentials (optional)

### For Using in Code
👉 Read: [README.md](README.md) and [ADVANCED_USAGE.md](ADVANCED_USAGE.md)

### For Understanding Architecture
👉 Read: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## Quick Example

```python
from agent import AIAgent
from skills import BugFixingSkill

# Create agent with bug fixing skill
agent = AIAgent(name="MyAgent")
agent.add_skill(BugFixingSkill())

# Analyze code for bugs
code = "if x == None: pass"
result = agent.execute_skill("BugFixer", action="analyze", code=code)
print(result)
```

## File Guide

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `QUICKSTART.md` | 5-minute guide |
| `SETUP_GUIDE.md` | Installation guide |
| `ADVANCED_USAGE.md` | Custom skills |
| `PROJECT_SUMMARY.md` | Project overview |
| `example_usage.py` | Working examples |
| `test_agent.py` | Unit tests |

## Questions?

1. **"How do I get started?"** → [QUICKSTART.md](QUICKSTART.md)
2. **"How do I set up GitHub/Jira?"** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. **"How do I create custom skills?"** → [ADVANCED_USAGE.md](ADVANCED_USAGE.md)
4. **"What's the architecture?"** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## Verify Installation

```bash
python test_agent.py
```

Should see: `Ran 12 tests in X.XXs OK` ✅

---

**Ready?** Start with [QUICKSTART.md](QUICKSTART.md) →

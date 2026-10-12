# VernfixAgent - Quick Start

Get up and running in 5 minutes!

## 1. Install

```bash
pip install -r requirements.txt
```

## 2. Configure (Optional)

```bash
cp .env.example .env
# Edit .env with your GitHub and Jira tokens
```

## 3. Run Example

```bash
python example_usage.py
```

## 4. Use in Code

### Analyze Code for Bugs

```python
from agent import AIAgent
from skills import BugFixingSkill

agent = AIAgent()
agent.add_skill(BugFixingSkill())

code = """
def process_data(items=[]):
    try:
        process(items)
    except:
        pass
"""

result = agent.execute_skill("BugFixer", action="analyze", code=code)
print(result)
```

### Connect to GitHub

```python
from skills import GitHubSkill

github = GitHubSkill()
agent.add_skill(github)

# Connect
agent.execute_skill("GitHub", action="connect", token="your_token")

# List repos
repos = agent.execute_skill("GitHub", action="list_repos")
print(repos)
```

### Connect to Jira

```python
from skills import JiraSkill

jira = JiraSkill()
agent.add_skill(jira)

# Connect
agent.execute_skill(
    "Jira",
    action="connect",
    server="https://company.atlassian.net",
    email="you@company.com",
    api_token="token"
)

# List projects
projects = agent.execute_skill("Jira", action="list_projects")
print(projects)
```

## Testing

```bash
python test_agent.py
```

Expected: 12 tests pass ✓

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [ADVANCED_USAGE.md](ADVANCED_USAGE.md) for custom skills
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup

## Support

Error? Check:
1. Dependencies installed: `pip install -r requirements.txt`
2. Python 3.8+: `python --version`
3. Credentials in `.env` for GitHub/Jira integration

# VernfixAgent Setup Guide

## Prerequisites

- Python 3.8+
- pip or conda package manager
- GitHub account (for GitHub integration)
- Jira account (for Jira integration)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

### 3. Configure GitHub (Optional)

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select `repo` scope for full repository access
4. Copy the token
5. Add to `.env`:
   ```
   GITHUB_TOKEN=your_token_here
   ```

### 4. Configure Jira (Optional)

1. Go to Jira → Account settings → Security → API tokens
2. Click "Create API token"
3. Copy the token
4. Get your Jira server URL (e.g., https://yourcompany.atlassian.net)
5. Add to `.env`:
   ```
   JIRA_SERVER=https://yourcompany.atlassian.net
   JIRA_EMAIL=your_email@example.com
   JIRA_API_TOKEN=your_token_here
   ```

## Running the Agent

### Run Example Demo

```bash
python example_usage.py
```

### Run Tests

```bash
python test_agent.py -v
```

### Use in Your Code

```python
from agent import AIAgent
from skills import GitHubSkill, JiraSkill, BugFixingSkill

# Create agent
agent = AIAgent(name="MyAgent")

# Add skills
agent.add_skill(GitHubSkill())
agent.add_skill(JiraSkill())
agent.add_skill(BugFixingSkill())

# Use skills
result = agent.execute_skill("BugFixer", action="analyze", code="...")
```

## Troubleshooting

**ModuleNotFoundError**: Run `pip install -r requirements.txt`

**Connection failed**: Check credentials in `.env`

**Import errors**: Ensure you're in the correct directory with proper Python path

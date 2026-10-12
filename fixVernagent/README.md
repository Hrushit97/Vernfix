# VernfixAgent - Python AI Agent with Multiple Skills

A powerful Python AI agent with integrated skills for GitHub connection, Jira management, and automated bug fixing.

## Features

- **GitHub Skill**: Connect to GitHub, list repositories, manage issues, and fetch code
- **Jira Skill**: Connect to Jira, manage projects, track bugs, and create issues
- **Bug Fixing Skill**: Analyze code for bugs and suggest fixes
- **Extensible Architecture**: Easy to add new skills
- **Status Tracking**: Monitor skill execution and history

## Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Add your credentials to `.env`

## Quick Start

### Basic Usage

```python
from agent import AIAgent
from skills import GitHubSkill, JiraSkill, BugFixingSkill

# Initialize agent
agent = AIAgent(name="VernfixAgent")

# Add skills
agent.add_skill(GitHubSkill())
agent.add_skill(JiraSkill())
agent.add_skill(BugFixingSkill())

# Execute skills
result = agent.execute_skill("BugFixer", action="analyze", code="your_code")
```

### Run Example

```bash
python example_usage.py
```

## Skills Documentation

### GitHub Skill

Connect and interact with GitHub repositories:

- **connect**: Authenticate with GitHub token
- **list_repos**: List all accessible repositories
- **get_issues**: Retrieve issues from a repository

### Jira Skill

Manage Jira projects and issues:

- **connect**: Authenticate with Jira server
- **list_projects**: List all accessible projects
- **list_issues**: Get issues from a project
- **create_issue**: Create new issues

### Bug Fixing Skill

Analyze and fix code:

- **analyze**: Detect bugs in code
- **suggest_fix**: Generate fixes for identified bugs

## Configuration

Set environment variables in `.env`:

```
GITHUB_TOKEN=your_token
JIRA_SERVER=https://your-instance.atlassian.net
JIRA_EMAIL=your_email@example.com
JIRA_API_TOKEN=your_token
```

## Project Structure

```
fixVernagent/
├── agent.py                 # Core agent framework
├── skills/
│   ├── __init__.py
│   ├── github_skill.py      # GitHub integration
│   ├── jira_skill.py        # Jira integration
│   └── bug_fixing_skill.py  # Bug analysis and fixing
├── example_usage.py         # Example script
├── requirements.txt         # Dependencies
├── .env.example            # Configuration template
└── README.md               # This file
```

## Adding New Skills

1. Create a new skill class inheriting from `Skill`:

```python
from agent import Skill

class NewSkill(Skill):
    def __init__(self):
        super().__init__(
            name="NewSkill",
            description="Description of your skill"
        )
    
    def execute(self, **kwargs):
        # Implementation
        pass
```

2. Register with agent:
```python
agent.add_skill(NewSkill())
```

## API Tokens and Setup

### GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create token with `repo` scope
3. Copy token to `.env`

### Jira API Token
1. Go to Jira Account settings → Security → API tokens
2. Create token
3. Copy server URL, email, and token to `.env`

## Requirements

- Python 3.8+
- PyGithub 2.1.1
- jira 3.13.0
- python-dotenv 1.0.0
- requests 2.31.0
- langchain 0.1.8
- openai 1.3.0
- anthropic 0.7.0

## License

MIT

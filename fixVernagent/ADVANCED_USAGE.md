# Advanced Usage Guide

## Creating Custom Skills

### Example: Custom Code Review Skill

```python
from agent import Skill

class CodeReviewSkill(Skill):
    def __init__(self):
        super().__init__(
            name="CodeReviewer",
            description="Review code for quality and best practices"
        )
    
    def execute(self, **kwargs):
        code = kwargs.get("code", "")
        review_type = kwargs.get("review_type", "basic")
        
        if review_type == "basic":
            return self._basic_review(code)
        elif review_type == "advanced":
            return self._advanced_review(code)
    
    def _basic_review(self, code):
        # Implementation
        return {"review": "..."}
    
    def _advanced_review(self, code):
        # Implementation
        return {"review": "..."}

# Register with agent
agent.add_skill(CodeReviewSkill())
```

## Chaining Skills

Execute multiple skills in sequence:

```python
# Analyze code for bugs
bug_result = agent.execute_skill(
    "BugFixer",
    action="analyze",
    code=my_code
)

# If bugs found, create Jira issue
if bug_result["result"]["total_bugs"] > 0:
    agent.execute_skill(
        "Jira",
        action="create_issue",
        project_key="PROJ",
        summary="Code bugs detected",
        description=f"Found {bug_result['result']['total_bugs']} bugs"
    )
```

## Working with GitHub Issues

```python
# Connect to GitHub
github = agent.skills["GitHub"]
github.execute(
    action="connect",
    token="your_token"
)

# Get open issues
issues = agent.execute_skill(
    "GitHub",
    action="get_issues",
    repo_name="my-repo",
    state="open"
)

# Process each issue
for issue in issues["result"]["issues"]:
    print(f"Issue #{issue['number']}: {issue['title']}")
```

## Working with Jira Issues

```python
# Connect to Jira
jira = agent.skills["Jira"]
jira.execute(
    action="connect",
    server="https://company.atlassian.net",
    email="user@company.com",
    api_token="token"
)

# Get all bug issues
bugs = agent.execute_skill(
    "Jira",
    action="list_issues",
    project_key="PROJ",
    issue_type="Bug"
)

# Create new bug issue
new_issue = agent.execute_skill(
    "Jira",
    action="create_issue",
    project_key="PROJ",
    summary="Critical security bug",
    description="Potential SQL injection vulnerability",
    issue_type="Bug"
)
```

## Error Handling

```python
try:
    result = agent.execute_skill(
        "GitHub",
        action="list_repos"
    )
    if result["status"] == "failed":
        print(f"Skill failed: {result['error']}")
    else:
        print(f"Success: {result['result']}")
except Exception as e:
    print(f"Exception: {str(e)}")
```

## Monitoring Execution History

```python
# Get full agent status with history
status = agent.get_agent_status()

print(f"Total executions: {len(status['execution_history'])}")

for execution in status['execution_history']:
    print(f"Skill: {execution['skill']}")
    print(f"Status: {execution['status']}")
```

## Environment Variables

Supported environment variables:

- `GITHUB_TOKEN`: GitHub personal access token
- `JIRA_SERVER`: Jira server URL
- `JIRA_EMAIL`: Jira account email
- `JIRA_API_TOKEN`: Jira API token
- `AGENT_NAME`: Custom agent name
- `AGENT_MODEL`: AI model to use
- `OPENAI_API_KEY`: OpenAI API key (for advanced features)

Load with:

```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_TOKEN")
```

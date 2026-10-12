# VernfixAgent - Code Structure

Complete breakdown of the codebase structure and components.

## Core Framework

### agent.py (106 lines)
```
Classes:
  - SkillStatus (Enum)
    * SUCCESS, FAILED, IN_PROGRESS, NOT_EXECUTED
  
  - Skill (ABC - Abstract Base Class)
    * __init__(name, description)
    * execute(**kwargs) - abstract method
    * get_status() - returns skill status dict
  
  - AIAgent
    * __init__(name, model)
    * add_skill(skill) - register skill
    * execute_skill(skill_name, **kwargs) - run skill
    * list_skills() - get all skills
    * get_agent_status() - get agent info
    * execution_history - track all executions
```

## Skills Package

### skills/__init__.py
- Exports: GitHubSkill, JiraSkill, BugFixingSkill

### skills/github_skill.py (87 lines)
```
Class: GitHubSkill(Skill)
  Methods:
    - connect(access_token) -> Dict
    - list_repositories() -> Dict
    - get_issues(repo_name, state) -> Dict
    - execute(action, **kwargs) -> Dict
  
  Actions:
    - "connect" - authenticate with GitHub
    - "list_repos" - list all repositories
    - "get_issues" - get repo issues
```

### skills/jira_skill.py (134 lines)
```
Class: JiraSkill(Skill)
  Methods:
    - connect(server, email, api_token) -> Dict
    - list_projects() -> Dict
    - list_issues(project_key, issue_type) -> Dict
    - create_issue(project_key, summary, ...) -> Dict
    - execute(action, **kwargs) -> Dict
  
  Actions:
    - "connect" - authenticate with Jira
    - "list_projects" - list all projects
    - "list_issues" - get project issues
    - "create_issue" - create new issue
```

### skills/bug_fixing_skill.py (97 lines)
```
Class: BugFixingSkill(Skill)
  Methods:
    - analyze_code(code) -> Dict
    - generate_fix(bug_type, code_line) -> Dict
    - execute(action, **kwargs) -> Dict
    - _check_bare_except(line) -> bool
    - _check_none_comparison(line) -> bool
    - _check_mutable_default(line) -> bool
  
  Actions:
    - "analyze" - detect bugs in code
    - "suggest_fix" - generate fix suggestions
  
  Bug Types Detected:
    - syntax_error (critical)
    - bare_except (high)
    - none_comparison (medium)
    - mutable_default (high)
```

## Example & Test Files

### example_usage.py (103 lines)
- Demonstrates all three skills
- Shows bug analysis in action
- Shows GitHub/Jira integration (with credentials)
- Displays agent status and history

### test_agent.py (168 lines)
```
Test Classes:
  - TestSkillBase
    * test_skill_initialization
  
  - TestAIAgent
    * test_agent_initialization
    * test_add_skill
    * test_list_skills
    * test_execute_nonexistent_skill
  
  - TestBugFixingSkill
    * test_analyze_valid_code
    * test_detect_syntax_error
    * test_detect_bare_except
    * test_detect_none_comparison
    * test_suggest_fix
  
  - TestAgentStatus
    * test_get_agent_status
    * test_execution_history

Tests: 12 total, 100% pass rate
```

## Configuration Files

### requirements.txt
```
PyGithub>=2.1.0
jira>=3.10.5
python-dotenv>=1.0.0
requests>=2.31.0
langchain>=0.1.0
openai>=1.0.0
anthropic>=0.7.0
```

### .env.example
```
GITHUB_TOKEN=
JIRA_SERVER=
JIRA_EMAIL=
JIRA_API_TOKEN=
AGENT_NAME=VernfixAgent
AGENT_MODEL=openai
OPENAI_API_KEY=
```

## Code Statistics

| Component | Files | Lines | Classes | Methods |
|-----------|-------|-------|---------|---------|
| Core | 2 | 123 | 3 | 9 |
| Skills | 4 | 318 | 3 | 19 |
| Tests | 1 | 168 | 4 | 12 |
| Examples | 1 | 103 | 0 | 2 |
| **Total** | **8** | **712** | **10** | **42** |

## Execution Flow

```
User Code
    ↓
AIAgent.execute_skill(name, **kwargs)
    ↓
Skill.execute(**kwargs)
    ↓
Skill-specific method (connect, list, etc.)
    ↓
External API (GitHub, Jira) or local processing
    ↓
Result returned to AIAgent
    ↓
Execution tracked in history
    ↓
Status updated
    ↓
Result returned to user
```

## Design Patterns Used

1. **Strategy Pattern** - Each skill is a strategy
2. **Abstract Factory** - Skill base class defines interface
3. **Status Pattern** - SkillStatus enum for state tracking
4. **History Pattern** - Execution history logging
5. **Chain of Responsibility** - Skills executed in sequence

## Error Handling

- Try/except blocks in all skill methods
- Exception messages propagated to caller
- Execution status set to FAILED on error
- Error stored in skill.error
- History records all failures

## Extensibility Points

1. Create new Skill subclass
2. Implement execute() method
3. Register with agent: agent.add_skill(MySkill())
4. Call: agent.execute_skill("MySkill", action=..., **kwargs)

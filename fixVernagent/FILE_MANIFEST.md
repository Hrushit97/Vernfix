# VernfixAgent File Manifest

Complete list of all project files and their purposes.

## Core Framework

| File | Purpose |
|------|---------|
| `agent.py` | Core AIAgent class, Skill base class, and SkillStatus enum |
| `__init__.py` | Package initialization and exports |

## Skills Package

| File | Purpose |
|------|---------|
| `skills/__init__.py` | Skills package initialization |
| `skills/github_skill.py` | GitHub API integration (connect, list repos, get issues) |
| `skills/jira_skill.py` | Jira API integration (connect, projects, issues, create) |
| `skills/bug_fixing_skill.py` | Code analysis and bug detection |

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation and feature overview |
| `QUICKSTART.md` | 5-minute quick start guide |
| `SETUP_GUIDE.md` | Detailed installation and configuration |
| `ADVANCED_USAGE.md` | Custom skills and advanced features |
| `PROJECT_SUMMARY.md` | Complete project overview and status |
| `FILE_MANIFEST.md` | This file - file reference guide |

## Examples & Testing

| File | Purpose |
|------|---------|
| `example_usage.py` | Comprehensive usage demonstration |
| `test_agent.py` | 12 unit tests for all components |

## Configuration

| File | Purpose |
|------|---------|
| `requirements.txt` | Python package dependencies |
| `.env.example` | Environment variable template |

## Quick Reference

### To Get Started
1. Read: `QUICKSTART.md`
2. Run: `pip install -r requirements.txt`
3. Run: `python example_usage.py`

### For Detailed Setup
- Read: `SETUP_GUIDE.md`
- Add credentials to `.env`

### For Advanced Usage
- Read: `ADVANCED_USAGE.md`
- Create custom skills by extending `Skill` class

### To Understand Architecture
- Read: `PROJECT_SUMMARY.md`
- Review: `agent.py` for core framework
- Review: `skills/*.py` for skill implementations

### To Verify Installation
- Run: `python test_agent.py`
- Should see: 12 tests pass ✓

## File Statistics

- **Total Files**: 13 (code + docs)
- **Lines of Code**: ~1,200
- **Documentation Pages**: 6
- **Test Coverage**: 12 unit tests
- **Skills**: 3 (GitHub, Jira, BugFixer)
- **Dependencies**: 7 major packages

## Key Classes

### Core
- `AIAgent` - Main agent coordinator
- `Skill` - Base skill class

### Skills
- `GitHubSkill` - GitHub integration
- `JiraSkill` - Jira integration
- `BugFixingSkill` - Code analysis

### Enums
- `SkillStatus` - Execution status tracking

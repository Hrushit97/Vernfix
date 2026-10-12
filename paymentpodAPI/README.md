# Vulnerability Orchestrator for Payment Pod API

An automated security vulnerability detection, fixing, and PR management system that integrates with GitHub and Jira.

## Features

- **Code Analysis**: Static analysis to detect security vulnerabilities (SQL injection, hardcoded secrets, XSS, etc.)
- **Automated Fixes**: Automatically fixes common vulnerabilities
- **GitHub Integration**: Creates branches and pull requests automatically
- **Jira Integration**: Creates and tracks vulnerability issues
- **Orchestration**: End-to-end workflow automation

## Architecture

### Skills

1. **GitHub Skill** (`skills/github_skill.py`)
   - Repository management
   - Branch and PR operations
   - File operations

2. **Jira Skill** (`skills/jira_skill.py`)
   - Issue creation and tracking
   - Status transitions
   - PR linking

3. **Code Analysis Skill** (`skills/code_analysis_skill.py`)
   - Security vulnerability detection
   - Multiple language support (Python, JavaScript)
   - Configurable severity levels

4. **Vulnerability Fixer Skill** (`skills/vulnerability_fixer_skill.py`)
   - Automatic vulnerability remediation
   - Safe code transformation
   - Multiple fix strategies

5. **PR Management Skill** (`skills/pr_management_skill.py`)
   - Git operations
   - Commit management
   - Branch lifecycle

### Orchestrator

`orchestrator/vulnerability_orchestrator.py` coordinates all skills through an automated workflow.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Update with your credentials:
   - GitHub token
   - Jira credentials
   - Repository paths

## Usage

```bash
python main.py
```

## Workflow

1. Get repository information
2. Analyze code for vulnerabilities
3. Create Jira issues for each vulnerability
4. Create feature branch
5. Fix identified vulnerabilities
6. Commit changes
7. Push branch
8. Create pull request
9. Link PR to Jira issues

## Supported Vulnerabilities

- SQL Injection
- Hardcoded Secrets/API Keys
- Insecure Deserialization
- Eval Usage
- XSS Vulnerabilities

## Testing

```bash
python -m unittest tests.test_skills -v
```

## Configuration Files

- `config/config.example.json`: Template configuration
- `.env.example`: Environment variables template

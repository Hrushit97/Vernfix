"""MCP resource handlers. Never returns secret values, only variable names."""

import os
from typing import Dict

REQUIRED_ENV_VARS = ['GITHUB_TOKEN', 'JIRA_URL', 'JIRA_USERNAME', 'JIRA_API_TOKEN']
OPTIONAL_ENV_VARS = ['GITHUB_OWNER', 'GITHUB_REPO', 'JIRA_PROJECT_KEY',
                     'SONAR_URL', 'SONAR_TOKEN', 'SONAR_PROJECT_KEY', 'REPO_PATH']

TOOLS = {
    'jira': ['create_jira_issue', 'search_jira_issues', 'find_duplicate_jira_issues',
             'get_existing_security_issues', 'get_jira_issue', 'link_pr_to_issue'],
    'github': ['get_github_repository', 'create_github_pr'],
    'sonar': ['get_sonar_vulnerabilities', 'get_sonar_hotspots',
              'get_sonar_quality_gate', 'get_sonar_findings'],
    'code': ['analyze_code', 'get_vulnerabilities', 'fix_vulnerability',
             'get_workflow_status'],
}
WRITE_TOOLS = ['create_jira_issue', 'link_pr_to_issue', 'create_github_pr',
               'fix_vulnerability']

SKILLS = {
    'CodeAnalysisSkill': ['scan_directory', 'analyze_python', 'analyze_javascript'],
    'VulnerabilityFixerSkill': ['fix_vulnerability'],
    'GitHubSkill': ['get_repository', 'create_branch', 'create_pull_request',
                    'get_repo_files', 'add_comment_to_pr'],
    'JiraSkill': ['create_issue', 'update_issue', 'add_comment', 'get_issue',
                  'link_issue_to_pr', 'transition_issue', 'search_issues',
                  'find_duplicate_issues', 'get_issues_by_labels'],
    'PRManagementSkill': ['local git: branch, commit, push'],
    'SonarSkill': ['get_vulnerabilities', 'get_security_hotspots',
                   'get_quality_gate_status', 'get_all_findings'],
}


def get_config_info() -> Dict:
    """codebase://config - which env vars are needed and whether they are set"""
    return {
        'required_env_vars': {n: bool(os.getenv(n)) for n in REQUIRED_ENV_VARS},
        'optional_env_vars': {n: bool(os.getenv(n)) for n in OPTIONAL_ENV_VARS},
        'setup_instructions': 'Set the variables in your environment or .env file; '
                              'never commit tokens.',
    }


def get_overview(services) -> Dict:
    """codebase://overview - project name, skills, and repo file count"""
    total = 0
    for _, dirs, files in os.walk(services.repo_root):
        dirs[:] = [d for d in dirs if d not in ('.git', '.venv', '__pycache__', 'node_modules')]
        total += sum(1 for f in files if f.endswith(('.py', '.js', '.jsx')))
    return {'project': 'Vulnerability Orchestrator', 'version': '1.0.0',
            'skills': list(SKILLS), 'tool_count': sum(len(t) for t in TOOLS.values()),
            'source_files': total}


def get_skills_overview() -> Dict:
    """codebase://skills - skills and their methods"""
    return {'skills': [{'name': n, 'methods': m} for n, m in SKILLS.items()]}


def get_vulnerability_status(services) -> Dict:
    """codebase://vulnerabilities - counts from the last analyze_code run"""
    last = services.last_analysis
    counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    if last:
        for v in last['vulnerabilities']:
            sev = str(v.get('severity', '')).lower()
            if sev in counts:
                counts[sev] += 1
    return {'analyzed': bool(last),
            'total_found': len(last['vulnerabilities']) if last else 0, **counts}


def get_tools_overview() -> Dict:
    """codebase://tools - tool catalog and which tools need confirm=true"""
    return {'tools': TOOLS, 'write_tools_require_confirm': WRITE_TOOLS}

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
}
WRITE_TOOLS = ['create_jira_issue', 'link_pr_to_issue', 'create_github_pr']


def get_config_info() -> Dict:
    """codebase://config - which env vars are needed and whether they are set"""
    return {
        'required_env_vars': {n: bool(os.getenv(n)) for n in REQUIRED_ENV_VARS},
        'optional_env_vars': {n: bool(os.getenv(n)) for n in OPTIONAL_ENV_VARS},
        'setup_instructions': 'Set the variables in your environment or .env file; '
                              'never commit tokens.',
    }


def get_tools_overview() -> Dict:
    """codebase://tools - tool catalog and which tools need confirm=true"""
    return {'tools': TOOLS, 'write_tools_require_confirm': WRITE_TOOLS}

"""
MCP tool handlers for Jira and GitHub.

Plain functions that take a `services` object (with .jira and .github skills),
so they can be unit-tested without the MCP SDK or network access.
Write operations require confirm=True.
"""

import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

ISSUE_KEY_RE = re.compile(r'^[A-Z][A-Z0-9_]+-\d+$')
PROJECT_KEY_RE = re.compile(r'^[A-Z][A-Z0-9_]+$')
REPO_RE = re.compile(r'^[A-Za-z0-9_.-]{1,100}$')
BRANCH_RE = re.compile(r'^(?!/)(?!.*\.\.)(?!.*//)[A-Za-z0-9._/-]{1,200}(?<![/.])$')
REF_RE = re.compile(r'^[A-Za-z0-9._/-]{1,200}$')   # Sonar branch / pull request id
PRIORITIES = {'Lowest', 'Low', 'Medium', 'High', 'Highest', 'Critical'}


def _error(message: str) -> Dict:
    return {'success': False, 'error': message}


def _check(value: str, pattern: re.Pattern, label: str) -> Optional[Dict]:
    if not isinstance(value, str) or not pattern.match(value):
        return _error(f"Invalid {label}")
    return None


def _need_confirm(confirm: bool, action: str) -> Optional[Dict]:
    if confirm is not True:
        return _error(f"Refusing to {action}: pass confirm=true after a human has approved it")
    return None


def _safe(fn):
    """Return a safe error message instead of leaking exception details"""
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            logger.error(f"{fn.__name__} failed: {e}")
            return _error(f"{fn.__name__} failed; see server log")
    wrapper.__name__ = fn.__name__
    return wrapper


# ---------------- Jira ----------------

@_safe
def create_jira_issue(services, project_key: str, summary: str, description: str = "",
                      priority: str = "High", issue_type: str = "Bug",
                      labels: Optional[List[str]] = None, confirm: bool = False) -> Dict:
    err = (_check(project_key, PROJECT_KEY_RE, 'project_key')
           or _need_confirm(confirm, 'create a Jira issue'))
    if err:
        return err
    if not summary or len(summary) > 255:
        return _error("summary must be 1-255 characters")
    if priority not in PRIORITIES:
        return _error(f"priority must be one of {sorted(PRIORITIES)}")
    return services.jira.create_issue(project_key, summary, issue_type,
                                      description, priority, labels)


@_safe
def search_jira_issues(services, project_key: str, keyword: Optional[str] = None,
                       status: Optional[str] = None) -> Dict:
    err = _check(project_key, PROJECT_KEY_RE, 'project_key')
    if err:
        return err
    return services.jira.search_issues(project_key, keyword, status)


@_safe
def find_duplicate_jira_issues(services, project_key: str, file_path: str,
                               vuln_type: str) -> Dict:
    err = _check(project_key, PROJECT_KEY_RE, 'project_key')
    if err:
        return err
    return services.jira.find_duplicate_issues(project_key, file_path, vuln_type)


@_safe
def get_existing_security_issues(services, project_key: str,
                                 labels: Optional[List[str]] = None) -> Dict:
    err = _check(project_key, PROJECT_KEY_RE, 'project_key')
    if err:
        return err
    return services.jira.get_issues_by_labels(project_key, labels or ['security'])


@_safe
def get_jira_issue(services, issue_key: str) -> Dict:
    err = _check(issue_key, ISSUE_KEY_RE, 'issue_key')
    return err or services.jira.get_issue(issue_key)


@_safe
def link_pr_to_issue(services, issue_key: str, pr_url: str, confirm: bool = False) -> Dict:
    err = (_check(issue_key, ISSUE_KEY_RE, 'issue_key')
           or _need_confirm(confirm, 'comment on a Jira issue'))
    if err:
        return err
    if not pr_url.startswith('https://github.com/'):
        return _error("pr_url must be a https://github.com/ URL")
    return services.jira.link_issue_to_pr(issue_key, pr_url)


# ---------------- GitHub ----------------

@_safe
def get_github_repository(services, repo_name: str, owner: Optional[str] = None) -> Dict:
    err = _check(repo_name, REPO_RE, 'repo_name')
    if not err and owner:
        err = _check(owner, REPO_RE, 'owner')
    return err or services.github.get_repository(repo_name, owner)


@_safe
def create_github_pr(services, repo_name: str, title: str, head_branch: str,
                     body: str = "", base_branch: str = "main",
                     owner: Optional[str] = None, confirm: bool = False) -> Dict:
    err = (_check(repo_name, REPO_RE, 'repo_name')
           or _check(head_branch, BRANCH_RE, 'head_branch')
           or _check(base_branch, BRANCH_RE, 'base_branch')
           or _need_confirm(confirm, 'create a pull request'))
    if not err and owner:
        err = _check(owner, REPO_RE, 'owner')
    if err:
        return err
    if not title or len(title) > 256:
        return _error("title must be 1-256 characters")
    return services.github.create_pull_request(
        repo_name, title, body, head_branch, base_branch, owner)



# ---------------- Sonar (read-only) ----------------

def _check_refs(branch: Optional[str], pull_request: Optional[str]) -> Optional[Dict]:
    if branch and not REF_RE.match(branch):
        return _error("Invalid branch")
    if pull_request and not REF_RE.match(pull_request):
        return _error("Invalid pull_request")
    return None


@_safe
def get_sonar_vulnerabilities(services, branch: Optional[str] = None,
                              pull_request: Optional[str] = None) -> Dict:
    return _check_refs(branch, pull_request) or \
        services.sonar.get_vulnerabilities(branch, pull_request)


@_safe
def get_sonar_hotspots(services, branch: Optional[str] = None,
                       pull_request: Optional[str] = None) -> Dict:
    return _check_refs(branch, pull_request) or \
        services.sonar.get_security_hotspots(branch, pull_request)


@_safe
def get_sonar_quality_gate(services, branch: Optional[str] = None,
                           pull_request: Optional[str] = None) -> Dict:
    return _check_refs(branch, pull_request) or \
        services.sonar.get_quality_gate_status(branch, pull_request)


@_safe
def get_sonar_findings(services, branch: Optional[str] = None,
                       pull_request: Optional[str] = None) -> Dict:
    return _check_refs(branch, pull_request) or \
        services.sonar.get_all_findings(branch, pull_request)

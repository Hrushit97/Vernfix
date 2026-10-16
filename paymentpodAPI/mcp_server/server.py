"""
MCP server exposing the Jira and GitHub skills.

Run:  python -m mcp_server.server      (stdio transport, e.g. for Claude Desktop)
"""

import os
import sys
import logging
from typing import Dict, List, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp.server.mcpserver import MCPServer

from mcp_server import tool_handlers as th
from mcp_server import resource_handlers as rh

# stdio transport uses stdout for protocol messages: log to stderr only
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Services:
    """Creates the Jira/GitHub skills on first use, from environment variables"""

    def __init__(self):
        self._jira = None
        self._github = None
        self._sonar = None

    @property
    def sonar(self):
        if self._sonar is None:
            from skills.sonar_skill import SonarSkill
            self._sonar = SonarSkill(os.environ['SONAR_URL'], os.environ['SONAR_TOKEN'],
                                     os.environ['SONAR_PROJECT_KEY'], os.getenv('REPO_PATH'))
        return self._sonar

    @property
    def jira(self):
        if self._jira is None:
            from skills.jira_skill import JiraSkill
            self._jira = JiraSkill(os.environ['JIRA_URL'], os.environ['JIRA_USERNAME'],
                                   os.environ['JIRA_API_TOKEN'])
        return self._jira

    @property
    def github(self):
        if self._github is None:
            from skills.github_skill import GitHubSkill
            self._github = GitHubSkill(os.environ['GITHUB_TOKEN'])
        return self._github


def create_server(services=None) -> MCPServer:
    """Create the MCP server and register tools and resources"""
    services = services or Services()
    server = MCPServer(
        "vulnerability-orchestrator",
        instructions=("Jira and GitHub tools for security vulnerability tracking. "
                      "Search for duplicates before creating Jira issues. Write tools "
                      "need confirm=true and must only be called after a human approves."),
    )

    @server.tool()
    def create_jira_issue(project_key: str, summary: str, description: str = "",
                          priority: str = "High", issue_type: str = "Bug",
                          labels: Optional[List[str]] = None, confirm: bool = False) -> Dict:
        """Create a Jira issue. Requires confirm=true."""
        return th.create_jira_issue(services, project_key, summary, description,
                                    priority, issue_type, labels, confirm)

    @server.tool()
    def search_jira_issues(project_key: str, keyword: Optional[str] = None,
                           status: Optional[str] = None) -> Dict:
        """Search Jira issues in a project by keyword and/or status."""
        return th.search_jira_issues(services, project_key, keyword, status)

    @server.tool()
    def find_duplicate_jira_issues(project_key: str, file_path: str, vuln_type: str) -> Dict:
        """Find existing Jira issues for the same file and vulnerability type."""
        return th.find_duplicate_jira_issues(services, project_key, file_path, vuln_type)

    @server.tool()
    def get_existing_security_issues(project_key: str,
                                     labels: Optional[List[str]] = None) -> Dict:
        """List Jira issues with security labels (default label: security)."""
        return th.get_existing_security_issues(services, project_key, labels)

    @server.tool()
    def get_jira_issue(issue_key: str) -> Dict:
        """Get details of one Jira issue, e.g. PAYMENT-123."""
        return th.get_jira_issue(services, issue_key)

    @server.tool()
    def link_pr_to_issue(issue_key: str, pr_url: str, confirm: bool = False) -> Dict:
        """Add a pull request link as a comment on a Jira issue. Requires confirm=true."""
        return th.link_pr_to_issue(services, issue_key, pr_url, confirm)

    @server.tool()
    def get_github_repository(repo_name: str, owner: Optional[str] = None) -> Dict:
        """Get GitHub repository details."""
        return th.get_github_repository(services, repo_name, owner)

    @server.tool()
    def create_github_pr(repo_name: str, title: str, head_branch: str, body: str = "",
                         base_branch: str = "main", owner: Optional[str] = None,
                         confirm: bool = False) -> Dict:
        """Create a GitHub pull request. Requires confirm=true."""
        return th.create_github_pr(services, repo_name, title, head_branch, body,
                                   base_branch, owner, confirm)

    @server.tool()
    def get_sonar_vulnerabilities(branch: Optional[str] = None,
                                  pull_request: Optional[str] = None) -> Dict:
        """List open Sonar VULNERABILITY issues (read-only)."""
        return th.get_sonar_vulnerabilities(services, branch, pull_request)

    @server.tool()
    def get_sonar_hotspots(branch: Optional[str] = None,
                           pull_request: Optional[str] = None) -> Dict:
        """List Sonar security hotspots still to review (read-only)."""
        return th.get_sonar_hotspots(services, branch, pull_request)

    @server.tool()
    def get_sonar_quality_gate(branch: Optional[str] = None,
                               pull_request: Optional[str] = None) -> Dict:
        """Get the Sonar quality gate result: passed true/false (read-only)."""
        return th.get_sonar_quality_gate(services, branch, pull_request)

    @server.tool()
    def get_sonar_findings(branch: Optional[str] = None,
                           pull_request: Optional[str] = None) -> Dict:
        """Vulnerabilities and hotspots together, in the orchestrator's format (read-only)."""
        return th.get_sonar_findings(services, branch, pull_request)

    @server.resource("codebase://config")
    def config_resource() -> Dict:
        """Required environment variables and whether they are set (no values)."""
        return rh.get_config_info()

    @server.resource("codebase://tools")
    def tools_resource() -> Dict:
        """Tool catalog and which tools need confirm=true."""
        return rh.get_tools_overview()

    return server


def run_server() -> None:
    """Entry point: run over stdio"""
    from dotenv import load_dotenv
    load_dotenv()
    create_server().run("stdio")


if __name__ == '__main__':
    run_server()

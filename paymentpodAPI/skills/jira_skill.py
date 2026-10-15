"""
Jira Integration Skill
Handles all Jira operations: ticket creation, updates, tracking vulnerabilities
"""

import json
from typing import Dict, List, Optional
from jira import JIRA
import logging

logger = logging.getLogger(__name__)


class JiraSkill:
    """Skill to manage Jira operations"""

    def __init__(self, url: str, username: str, api_token: str):
        """Initialize Jira connection"""
        self.jira = JIRA(url, basic_auth=(username, api_token))
        logger.info(f"Connected to Jira at {url}")

    def create_issue(
        self,
        project_key: str,
        summary: str,
        issue_type: str = "Bug",
        description: str = "",
        priority: str = "High",
        labels: List[str] = None,
    ) -> Dict:
        """Create a Jira issue for vulnerability"""
        try:
            issue_dict = {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
            }
            if labels:
                issue_dict["labels"] = labels

            issue = self.jira.create_issue(fields=issue_dict)
            logger.info(f"Created issue {issue.key}")
            return {
                "success": True,
                "issue_key": issue.key,
                "issue_url": f"{self.jira.client_info.url}/browse/{issue.key}",
            }
        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            return {"success": False, "error": str(e)}

    def update_issue(self, issue_key: str, updates: Dict) -> Dict:
        """Update an existing issue"""
        try:
            issue = self.jira.issue(issue_key)
            issue.update(**updates)
            logger.info(f"Updated issue {issue_key}")
            return {"success": True, "issue_key": issue_key}
        except Exception as e:
            logger.error(f"Failed to update issue: {e}")
            return {"success": False, "error": str(e)}

    def add_comment(self, issue_key: str, comment: str) -> Dict:
        """Add comment to an issue"""
        try:
            issue = self.jira.issue(issue_key)
            self.jira.add_comment(issue, comment)
            logger.info(f"Added comment to {issue_key}")
            return {"success": True, "issue_key": issue_key}
        except Exception as e:
            logger.error(f"Failed to add comment: {e}")
            return {"success": False, "error": str(e)}

    def get_issue(self, issue_key: str) -> Dict:
        """Get issue details"""
        try:
            issue = self.jira.issue(issue_key)
            return {
                "success": True,
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": str(issue.fields.status),
                "priority": str(issue.fields.priority),
                "description": issue.fields.description,
            }
        except Exception as e:
            logger.error(f"Failed to get issue: {e}")
            return {"success": False, "error": str(e)}

    def link_issue_to_pr(self, issue_key: str, pr_url: str) -> Dict:
        """Add PR link to issue"""
        comment = f"Pull Request: {pr_url}"
        return self.add_comment(issue_key, comment)

    def transition_issue(self, issue_key: str, target_status: str) -> Dict:
        """Transition issue to different status"""
        try:
            issue = self.jira.issue(issue_key)
            transitions = self.jira.transitions(issue)
            for transition in transitions:
                if transition["to"]["name"].lower() == target_status.lower():
                    self.jira.transition_issue(issue, transition["id"])
                    return {"success": True, "new_status": target_status}
            return {"success": False, "error": f"Cannot transition to {target_status}"}
        except Exception as e:
            logger.error(f"Failed to transition issue: {e}")
            return {"success": False, "error": str(e)}

    def search_issues(self, project_key: str, summary_keyword: str = None, status: str = None) -> Dict:
        """Search for existing Jira issues in a project"""
        try:
            jql_parts = [f"project = {project_key}"]

            if summary_keyword:
                jql_parts.append(f'summary ~ "{summary_keyword}"')

            if status:
                jql_parts.append(f'status = "{status}"')

            jql = " AND ".join(jql_parts)
            logger.info(f"Searching with JQL: {jql}")

            issues = self.jira.search_issues(jql, maxResults=50)
            issues_list = []
            for issue in issues:
                issues_list.append({
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": str(issue.fields.status),
                    "priority": str(issue.fields.priority),
                    "description": issue.fields.description,
                })

            logger.info(f"Found {len(issues_list)} existing issues")
            return {
                "success": True,
                "count": len(issues_list),
                "issues": issues_list
            }
        except Exception as e:
            logger.error(f"Failed to search issues: {e}")
            return {"success": False, "error": str(e), "issues": []}

    def find_duplicate_issues(self, project_key: str, file_path: str, vuln_type: str) -> Dict:
        """Find duplicate/existing issues for a specific vulnerability"""
        try:
            # Search for issues related to file and vulnerability type
            jql = f'project = {project_key} AND description ~ "{file_path}" AND summary ~ "{vuln_type}"'
            logger.info(f"Searching for duplicates with JQL: {jql}")

            issues = self.jira.search_issues(jql, maxResults=10)
            duplicates = []

            for issue in issues:
                duplicates.append({
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": str(issue.fields.status),
                    "priority": str(issue.fields.priority),
                    "url": f"{self.jira.client_info.url}/browse/{issue.key}",
                })

            return {
                "success": True,
                "found_duplicates": len(duplicates) > 0,
                "duplicate_count": len(duplicates),
                "duplicates": duplicates
            }
        except Exception as e:
            logger.error(f"Failed to find duplicates: {e}")
            return {"success": False, "error": str(e), "duplicates": []}

    def get_issues_by_labels(self, project_key: str, labels: List[str]) -> Dict:
        """Get issues by labels (e.g., 'security', 'automated-fix')"""
        try:
            label_query = " OR ".join([f'labels in ({label})' for label in labels])
            jql = f"project = {project_key} AND ({label_query})"
            logger.info(f"Searching issues with labels: {labels}")

            issues = self.jira.search_issues(jql, maxResults=100)
            issues_list = []

            for issue in issues:
                issues_list.append({
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": str(issue.fields.status),
                    "labels": issue.fields.labels,
                })

            return {
                "success": True,
                "count": len(issues_list),
                "issues": issues_list
            }
        except Exception as e:
            logger.error(f"Failed to get issues by labels: {e}")
            return {"success": False, "error": str(e), "issues": []}

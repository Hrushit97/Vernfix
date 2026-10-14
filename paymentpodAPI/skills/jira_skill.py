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

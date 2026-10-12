"""
Jira Integration Skill
"""

from typing import Dict, List, Any
from jira import JIRA
from agent import Skill


class JiraSkill(Skill):
    """Skill for Jira project and issue management"""
    
    def __init__(self, server: str = None, email: str = None, api_token: str = None):
        super().__init__(
            name="Jira",
            description="Connect to Jira, manage projects, issues, and track bugs"
        )
        self.server = server
        self.email = email
        self.api_token = api_token
        self.client = None
        if all([server, email, api_token]):
            self.client = self._create_client(server, email, api_token)
    
    def _create_client(self, server: str, email: str, api_token: str) -> JIRA:
        """Create Jira client"""
        return JIRA(
            server=server,
            basic_auth=(email, api_token)
        )
    
    def connect(self, server: str, email: str, api_token: str) -> Dict[str, Any]:
        """Connect to Jira server"""
        try:
            self.client = self._create_client(server, email, api_token)
            self.server = server
            self.email = email
            self.api_token = api_token
            
            myself = self.client.myself()
            return {
                "status": "connected",
                "server": server,
                "user": myself["displayName"],
                "email": myself["emailAddress"]
            }
        except Exception as e:
            raise Exception(f"Jira connection failed: {str(e)}")
    
    def list_projects(self) -> Dict[str, Any]:
        """List all accessible projects"""
        if not self.client:
            raise Exception("Not connected to Jira. Call connect() first.")
        
        try:
            projects = []
            for project in self.client.projects():
                projects.append({
                    "key": project.key,
                    "name": project.name,
                    "type": project.projectTypeKey
                })
            return {"projects": projects, "total": len(projects)}
        except Exception as e:
            raise Exception(f"Failed to list projects: {str(e)}")
    
    def list_issues(self, project_key: str, issue_type: str = "Bug") -> Dict[str, Any]:
        """List issues from a project"""
        if not self.client:
            raise Exception("Not connected to Jira.")
        
        try:
            jql = f"project = {project_key} AND type = {issue_type}"
            issues = self.client.search_issues(jql)
            
            issue_list = []
            for issue in issues:
                issue_list.append({
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "priority": issue.fields.priority.name if issue.fields.priority else None,
                    "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
                    "created": str(issue.fields.created)
                })
            return {"issues": issue_list, "total": len(issue_list)}
        except Exception as e:
            raise Exception(f"Failed to list issues: {str(e)}")
    
    def create_issue(self, project_key: str, summary: str, 
                    description: str, issue_type: str = "Bug") -> Dict[str, Any]:
        """Create a new issue"""
        if not self.client:
            raise Exception("Not connected to Jira.")
        
        try:
            issue_dict = {
                'project': {'key': project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type}
            }
            issue = self.client.create_issue(fields=issue_dict)
            return {"issue_key": issue.key, "status": "created"}
        except Exception as e:
            raise Exception(f"Failed to create issue: {str(e)}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute Jira skill with various operations"""
        action = kwargs.get("action", "list_projects")
        
        if action == "connect":
            return self.connect(
                kwargs.get("server"),
                kwargs.get("email"),
                kwargs.get("api_token")
            )
        elif action == "list_projects":
            return self.list_projects()
        elif action == "list_issues":
            return self.list_issues(
                kwargs.get("project_key"),
                kwargs.get("issue_type", "Bug")
            )
        elif action == "create_issue":
            return self.create_issue(
                kwargs.get("project_key"),
                kwargs.get("summary"),
                kwargs.get("description"),
                kwargs.get("issue_type", "Bug")
            )
        else:
            raise ValueError(f"Unknown action: {action}")

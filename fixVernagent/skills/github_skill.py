"""
GitHub Integration Skill
"""

from typing import Dict, List, Any
from github import Github, GithubException
from agent import Skill


class GitHubSkill(Skill):
    """Skill for GitHub repository management and interaction"""
    
    def __init__(self, access_token: str = None):
        super().__init__(
            name="GitHub",
            description="Connect to GitHub, list repos, manage issues, and fetch code"
        )
        self.access_token = access_token
        self.client = None
        if access_token:
            self.client = Github(access_token)
    
    def connect(self, access_token: str) -> Dict[str, Any]:
        """Connect to GitHub with access token"""
        try:
            self.client = Github(access_token)
            self.access_token = access_token
            user = self.client.get_user()
            return {
                "status": "connected",
                "user": user.login,
                "name": user.name,
                "email": user.email
            }
        except GithubException as e:
            raise Exception(f"GitHub connection failed: {str(e)}")
    
    def list_repositories(self) -> Dict[str, Any]:
        """List all repositories for authenticated user"""
        if not self.client:
            raise Exception("Not connected to GitHub. Call connect() first.")
        
        try:
            user = self.client.get_user()
            repos = []
            for repo in user.get_repos():
                repos.append({
                    "name": repo.name,
                    "url": repo.html_url,
                    "description": repo.description,
                    "language": repo.language,
                    "stars": repo.stargazers_count
                })
            return {"repositories": repos, "total": len(repos)}
        except Exception as e:
            raise Exception(f"Failed to list repositories: {str(e)}")
    
    def get_issues(self, repo_name: str, state: str = "open") -> Dict[str, Any]:
        """Get issues from a specific repository"""
        if not self.client:
            raise Exception("Not connected to GitHub.")
        
        try:
            user = self.client.get_user()
            repo = user.get_repo(repo_name)
            issues = []
            for issue in repo.get_issues(state=state):
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body[:200] if issue.body else None,
                    "state": issue.state,
                    "labels": [l.name for l in issue.labels],
                    "created_at": str(issue.created_at)
                })
            return {"issues": issues, "total": len(issues)}
        except Exception as e:
            raise Exception(f"Failed to get issues: {str(e)}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute GitHub skill with various operations"""
        action = kwargs.get("action", "list_repos")
        
        if action == "connect":
            return self.connect(kwargs.get("token"))
        elif action == "list_repos":
            return self.list_repositories()
        elif action == "get_issues":
            return self.get_issues(
                kwargs.get("repo_name"),
                kwargs.get("state", "open")
            )
        else:
            raise ValueError(f"Unknown action: {action}")

"""
GitHub Integration Skill
Handles all GitHub operations: cloning, fetching repos, branch management, PRs
"""

import os
import json
from typing import Dict, List, Optional
from github import Github, GithubException
import logging

logger = logging.getLogger(__name__)


class GitHubSkill:
    """Skill to manage GitHub operations"""

    def __init__(self, token: str):
        """Initialize GitHub connection"""
        self.client = Github(token)
        self.user = self.client.get_user()
        logger.info(f"Connected to GitHub as {self.user.login}")

    def get_repository(self, repo_name: str, owner: Optional[str] = None) -> Dict:
        """Fetch repository details"""
        try:
            if owner is None:
                owner = self.user.login
            repo = self.client.get_user(owner).get_repo(repo_name)
            return {
                "success": True,
                "repo_url": repo.html_url,
                "clone_url": repo.clone_url,
                "description": repo.description,
                "default_branch": repo.default_branch,
            }
        except GithubException as e:
            logger.error(f"Failed to fetch repo: {e}")
            return {"success": False, "error": str(e)}

    def create_branch(self, repo_name: str, branch_name: str, owner: Optional[str] = None) -> Dict:
        """Create a new branch"""
        try:
            if owner is None:
                owner = self.user.login
            repo = self.client.get_user(owner).get_repo(repo_name)
            base_branch = repo.get_branch(repo.default_branch)
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base_branch.commit.sha,
            )
            return {"success": True, "branch": branch_name}
        except GithubException as e:
            logger.error(f"Failed to create branch: {e}")
            return {"success": False, "error": str(e)}

    def create_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
        owner: Optional[str] = None,
    ) -> Dict:
        """Create a pull request"""
        try:
            if owner is None:
                owner = self.user.login
            repo = self.client.get_user(owner).get_repo(repo_name)
            pr = repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch,
            )
            return {
                "success": True,
                "pr_url": pr.html_url,
                "pr_number": pr.number,
            }
        except GithubException as e:
            logger.error(f"Failed to create PR: {e}")
            return {"success": False, "error": str(e)}

    def get_repo_files(self, repo_name: str, path: str = "", owner: Optional[str] = None) -> Dict:
        """Get list of files in repository"""
        try:
            if owner is None:
                owner = self.user.login
            repo = self.client.get_user(owner).get_repo(repo_name)
            contents = repo.get_contents(path)
            files = []
            if isinstance(contents, list):
                for item in contents:
                    files.append(
                        {
                            "name": item.name,
                            "path": item.path,
                            "type": item.type,
                        }
                    )
            return {"success": True, "files": files}
        except GithubException as e:
            logger.error(f"Failed to get files: {e}")
            return {"success": False, "error": str(e)}

    def add_comment_to_pr(
        self,
        repo_name: str,
        pr_number: int,
        comment: str,
        owner: Optional[str] = None,
    ) -> Dict:
        """Add comment to pull request"""
        try:
            if owner is None:
                owner = self.user.login
            repo = self.client.get_user(owner).get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
            return {"success": True, "message": "Comment added"}
        except GithubException as e:
            logger.error(f"Failed to add comment: {e}")
            return {"success": False, "error": str(e)}

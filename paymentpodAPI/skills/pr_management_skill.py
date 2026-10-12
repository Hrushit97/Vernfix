"""
PR Management Skill
Handles pull request creation, management, and automation
"""

import os
import subprocess
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PRManagementSkill:
    """Skill to manage pull requests"""

    def __init__(self, repo_path: str, username: str, email: str):
        """Initialize PR management"""
        self.repo_path = repo_path
        self.username = username
        self.email = email
        self._configure_git()

    def _configure_git(self):
        """Configure git for commits"""
        try:
            subprocess.run(
                ['git', 'config', 'user.name', self.username],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            subprocess.run(
                ['git', 'config', 'user.email', self.email],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            logger.info("Git configured successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Git configuration failed: {e}")

    def create_feature_branch(self, branch_name: str) -> Dict:
        """Create a feature branch"""
        try:
            # Fetch latest
            subprocess.run(
                ['git', 'fetch', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )

            # Create and checkout branch
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )

            logger.info(f"Created branch {branch_name}")
            return {'success': True, 'branch': branch_name}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create branch: {e}")
            return {'success': False, 'error': str(e)}

    def commit_changes(self, files: List[str], message: str) -> Dict:
        """Commit changes to branch"""
        try:
            # Stage files
            for file in files:
                subprocess.run(
                    ['git', 'add', file],
                    cwd=self.repo_path,
                    capture_output=True,
                    check=True
                )

            # Commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )

            logger.info(f"Committed changes: {message}")
            return {'success': True, 'message': 'Changes committed'}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit: {e}")
            return {'success': False, 'error': str(e)}

    def push_branch(self, branch_name: str) -> Dict:
        """Push branch to remote"""
        try:
            subprocess.run(
                ['git', 'push', 'origin', branch_name],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )

            logger.info(f"Pushed branch {branch_name}")
            return {'success': True, 'branch': branch_name}
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push branch: {e}")
            return {'success': False, 'error': str(e)}

    def get_current_branch(self) -> str:
        """Get current branch name"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return 'main'

    def get_changed_files(self) -> List[str]:
        """Get list of changed files in current branch"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'origin/main...HEAD'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError:
            return []

    def create_pr_description(self, vulnerabilities: List[Dict]) -> str:
        """Generate PR description from vulnerabilities"""
        description = "## Security Vulnerability Fixes\n\n"
        description += "This PR fixes the following security vulnerabilities:\n\n"

        for vuln in vulnerabilities:
            description += f"- **{vuln['type']}** ({vuln['severity']})\n"
            description += f"  - File: `{vuln['file']}`\n"
            description += f"  - Line: {vuln['line']}\n"

        description += "\n## Changes\n"
        description += "- Applied security best practices\n"
        description += "- Used parameterized queries for database operations\n"
        description += "- Moved secrets to environment variables\n"
        description += "- Used safe deserialization methods\n"
        description += "- Fixed XSS vulnerabilities\n"

        return description

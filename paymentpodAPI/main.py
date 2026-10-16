"""
Main entry point for Vulnerability Orchestrator
"""

import os
import json
import logging
from dotenv import load_dotenv
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config() -> dict:
    """Load configuration from environment variables"""
    return {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo': os.getenv('GITHUB_REPO', 'paymentpodAPI'),
        'github_owner': os.getenv('GITHUB_OWNER'),
        'jira_url': os.getenv('JIRA_URL'),
        'jira_username': os.getenv('JIRA_USERNAME'),
        'jira_api_token': os.getenv('JIRA_API_TOKEN'),
        'jira_project_key': os.getenv('JIRA_PROJECT_KEY', 'PAYMENT'),
        'repo_path': os.getenv('REPO_PATH'),
        'analyze_path': os.getenv('ANALYZE_PATH'),
        'git_username': os.getenv('GIT_USERNAME', 'Security Bot'),
        'git_email': os.getenv('GIT_EMAIL', 'security-bot@example.com'),
        # Optional Sonar integration (all three needed to enable it)
        'sonar_url': os.getenv('SONAR_URL'),
        'sonar_token': os.getenv('SONAR_TOKEN'),
        'sonar_project_key': os.getenv('SONAR_PROJECT_KEY'),
    }


def validate_config(config: dict) -> bool:
    """Validate that all required configuration is present"""
    required_keys = [
        'github_token', 'github_repo', 'github_owner',
        'jira_url', 'jira_username', 'jira_api_token',
        'repo_path', 'analyze_path'
    ]
    
    for key in required_keys:
        if not config.get(key):
            logger.error(f"Missing required configuration: {key}")
            return False
    
    return True


def main():
    """Main entry point"""
    logger.info("Starting Vulnerability Orchestrator")
    
    # Load and validate configuration
    config = load_config()
    if not validate_config(config):
        logger.error("Configuration validation failed")
        return False
    
    # Initialize orchestrator
    orchestrator = VulnerabilityOrchestrator(config)
    
    # Execute workflow
    result = orchestrator.execute_workflow(
        repo_name=config['github_repo'],
        repo_owner=config['github_owner'],
        project_key=config['jira_project_key'],
        analyze_path=config['analyze_path']
    )
    
    # Log results
    if result['success']:
        logger.info("Workflow completed successfully!")
        logger.info(f"PR URL: {result.get('pr_url')}")
        logger.info(f"Vulnerabilities fixed: {result.get('vulnerabilities_fixed')}")
        logger.info(f"Jira issues created: {result.get('jira_issues')}")
        return True
    else:
        logger.error(f"Workflow failed: {result.get('error')}")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

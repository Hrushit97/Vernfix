"""
Example usage of VernfixAgent with all skills
"""

import json
import os
from dotenv import load_dotenv
from agent import AIAgent
from skills import GitHubSkill, JiraSkill, BugFixingSkill


def print_result(title: str, result: dict) -> None:
    """Pretty print execution results"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2))


def main():
    """Main example demonstrating all agent skills"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize agent
    agent = AIAgent(name="VernfixAgent", model="openai")
    print(f"✓ Agent '{agent.name}' initialized")
    
    # Add skills to agent
    github_skill = GitHubSkill()
    jira_skill = JiraSkill()
    bug_skill = BugFixingSkill()
    
    agent.add_skill(github_skill)
    agent.add_skill(jira_skill)
    agent.add_skill(bug_skill)
    
    # Display available skills
    print_result("Available Skills", {"skills": agent.list_skills()})
    
    # Example 1: Bug Analysis (doesn't require credentials)
    print("\n" + "="*60)
    print("  Example 1: Analyzing Code for Bugs")
    print("="*60)
    
    buggy_code = """
def process_data(items=[]):
    try:
        for item in items:
            print(item)
    except:
        print("Error occurred")
    
    if data == None:
        return None
"""
    
    result = agent.execute_skill("BugFixer", action="analyze", code=buggy_code)
    print_result("Bug Analysis Results", result)
    
    # Example 2: Bug Fix Suggestion
    result = agent.execute_skill(
        "BugFixer",
        action="suggest_fix",
        bug_type="none_comparison",
        code_line="if data == None:"
    )
    print_result("Suggested Fix", result)
    
    # Example 3: GitHub Integration (requires token)
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        print("\n" + "="*60)
        print("  Example 2: GitHub Integration")
        print("="*60)
        
        result = agent.execute_skill("GitHub", action="connect", token=github_token)
        print_result("GitHub Connection", result)
        
        result = agent.execute_skill("GitHub", action="list_repos")
        print_result("GitHub Repositories", result)
    else:
        print("\n⚠ GitHub token not found. Set GITHUB_TOKEN in .env to test.")
    
    # Example 4: Jira Integration (requires credentials)
    jira_server = os.getenv("JIRA_SERVER")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")
    
    if all([jira_server, jira_email, jira_token]):
        print("\n" + "="*60)
        print("  Example 3: Jira Integration")
        print("="*60)
        
        result = agent.execute_skill(
            "Jira",
            action="connect",
            server=jira_server,
            email=jira_email,
            api_token=jira_token
        )
        print_result("Jira Connection", result)
        
        result = agent.execute_skill("Jira", action="list_projects")
        print_result("Jira Projects", result)
    else:
        print("\n⚠ Jira credentials not found. Set JIRA_* vars in .env to test.")
    
    # Display overall agent status
    print_result("Agent Status", agent.get_agent_status())


if __name__ == "__main__":
    main()

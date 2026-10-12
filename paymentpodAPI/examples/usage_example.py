"""
Example usage of the Vulnerability Orchestrator
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Load configuration
load_dotenv()

def example_basic_usage():
    """Basic usage example"""
    config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo': os.getenv('GITHUB_REPO'),
        'github_owner': os.getenv('GITHUB_OWNER'),
        'jira_url': os.getenv('JIRA_URL'),
        'jira_username': os.getenv('JIRA_USERNAME'),
        'jira_api_token': os.getenv('JIRA_API_TOKEN'),
        'jira_project_key': os.getenv('JIRA_PROJECT_KEY'),
        'repo_path': os.getenv('REPO_PATH'),
        'analyze_path': os.getenv('ANALYZE_PATH'),
        'git_username': os.getenv('GIT_USERNAME'),
        'git_email': os.getenv('GIT_EMAIL'),
    }
    
    # Initialize orchestrator
    orchestrator = VulnerabilityOrchestrator(config)
    
    # Run workflow
    result = orchestrator.execute_workflow(
        repo_name=config['github_repo'],
        repo_owner=config['github_owner'],
        project_key=config['jira_project_key'],
        analyze_path=config['analyze_path']
    )
    
    # Print results
    print("=" * 50)
    print("Workflow Results")
    print("=" * 50)
    print(f"Success: {result['success']}")
    
    if result['success']:
        print(f"\nPull Request: {result['pr_url']}")
        print(f"PR Number: {result['pr_number']}")
        print(f"Vulnerabilities Fixed: {result['vulnerabilities_fixed']}")
        print(f"Jira Issues Created: {len(result['jira_issues'])}")
        for issue in result['jira_issues']:
            print(f"  - {issue}")
    else:
        print(f"Error: {result['error']}")


def example_analysis_only():
    """Example: Only analyze code without fixing"""
    from skills.code_analysis_skill import CodeAnalysisSkill
    
    skill = CodeAnalysisSkill()
    analyze_path = os.getenv('ANALYZE_PATH')
    
    # Scan directory
    results = skill.scan_directory(analyze_path)
    
    print("=" * 50)
    print("Code Analysis Results")
    print("=" * 50)
    print(f"Total Files Scanned: {results['total_files']}")
    print(f"Total Vulnerabilities: {results['total_vulnerabilities']}")
    print("\nVulnerabilities:")
    
    for vuln in results['vulnerabilities']:
        print(f"\n  Type: {vuln['type']}")
        print(f"  File: {vuln['file']}")
        print(f"  Line: {vuln['line']}")
        print(f"  Severity: {vuln['severity']}")


def example_manual_fix():
    """Example: Manually fix specific vulnerabilities"""
    from skills.vulnerability_fixer_skill import VulnerabilityFixerSkill
    
    fixer = VulnerabilityFixerSkill()
    
    # Define vulnerability
    vuln = {
        'type': 'Hardcoded Secret',
        'line': 5,
        'file': '/path/to/file.py'
    }
    
    # Fix it
    result = fixer.fix_vulnerability(vuln['file'], vuln)
    
    print("=" * 50)
    print("Vulnerability Fix Result")
    print("=" * 50)
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Fix Applied: {result['fix']}")
    else:
        print(f"Error: {result['error']}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_type = sys.argv[1]
        
        if example_type == 'full':
            example_basic_usage()
        elif example_type == 'analysis':
            example_analysis_only()
        elif example_type == 'fix':
            example_manual_fix()
        else:
            print("Usage: python usage_example.py [full|analysis|fix]")
    else:
        print("Running basic usage example...")
        print("For full workflow: python usage_example.py full")
        print("For analysis only: python usage_example.py analysis")
        print("For manual fix: python usage_example.py fix")

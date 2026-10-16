"""
Unit tests for Vulnerability Orchestrator
Tests the orchestrator's workflow management and coordination
"""

import unittest
import sys
import os
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator


class TestVulnerabilityOrchestrator(unittest.TestCase):
    """Test VulnerabilityOrchestrator functionality"""

    def setUp(self):
        """Setup test fixtures"""
        self.config = {
            'github_token': 'test_token',
            'jira_url': 'https://test.atlassian.net',
            'jira_username': 'test@test.com',
            'jira_api_token': 'test_jira_token',
            'repo_path': '/tmp/test_repo',
            'git_username': 'testuser',
            'git_email': 'test@example.com',
            'github_repo': 'TestRepo',
            'github_owner': 'TestOwner'
        }

    def test_config_validation_missing_key(self):
        """Test that missing config raises ValueError"""
        bad_config = {'github_token': 'test'}
        with self.assertRaises(ValueError):
            VulnerabilityOrchestrator(bad_config)

    def test_config_validation_all_present(self):
        """Test that valid config doesn't raise"""
        # This will fail at initialization due to mocked skills,
        # but we're testing the validation passed
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill'):
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)
                            self.assertIsNotNone(orchestrator)

    def test_jira_priority_mapping(self):
        """Test CRITICAL severity maps to Highest priority"""
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill'):
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)

                            self.assertEqual(
                                orchestrator._get_jira_priority('CRITICAL'),
                                'Highest'
                            )
                            self.assertEqual(
                                orchestrator._get_jira_priority('HIGH'),
                                'High'
                            )
                            self.assertEqual(
                                orchestrator._get_jira_priority('MEDIUM'),
                                'Medium'
                            )
                            self.assertEqual(
                                orchestrator._get_jira_priority('LOW'),
                                'Low'
                            )
                            # Test default for unknown severity
                            self.assertEqual(
                                orchestrator._get_jira_priority('UNKNOWN'),
                                'Medium'
                            )

    def test_get_workflow_status(self):
        """Test workflow status retrieval"""
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill'):
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)
                            status = orchestrator.get_workflow_status()

                            self.assertEqual(status['status'], 'initialized')
                            self.assertTrue(all(status['skills_ready'].values()))
                            self.assertIn('config', status)

    def test_workflow_error_formatting(self):
        """Test error response formatting"""
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill'):
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)
                            error_result = orchestrator._workflow_error('Test error')

                            self.assertFalse(error_result['success'])
                            self.assertEqual(error_result['error'], 'Test error')
                            self.assertEqual(error_result['vulnerabilities_found'], 0)

    def test_sync_jira_to_github(self):
        """Test Jira to GitHub synchronization"""
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill') as mock_jira:
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)

                            # Mock the jira_skill.get_issues_by_labels
                            orchestrator.jira_skill.get_issues_by_labels = Mock(return_value={
                                'success': True,
                                'count': 2,
                                'issues': [
                                    {'key': 'PAYMENT-123', 'summary': 'SQL Injection'},
                                    {'key': 'PAYMENT-124', 'summary': 'XSS Vulnerability'}
                                ]
                            })

                            result = orchestrator.sync_jira_to_github(
                                'Vernfix', 'Hrushit97', 'PAYMENT'
                            )

                            self.assertTrue(result['success'])
                            self.assertEqual(result['synced_count'], 2)

    def test_get_existing_security_issues(self):
        """Test retrieving existing security issues"""
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'):
            with patch('orchestrator.vulnerability_orchestrator.JiraSkill'):
                with patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'):
                    with patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'):
                        with patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
                            orchestrator = VulnerabilityOrchestrator(self.config)

                            # Mock the jira_skill.get_issues_by_labels
                            orchestrator.jira_skill.get_issues_by_labels = Mock(return_value={
                                'success': True,
                                'count': 1,
                                'issues': [
                                    {'key': 'PAYMENT-123', 'summary': 'Security Issue'}
                                ]
                            })

                            result = orchestrator.get_existing_security_issues('PAYMENT')

                            self.assertTrue(result['success'])
                            self.assertEqual(result['count'], 1)
                            self.assertEqual(len(result['issues']), 1)

    def _make_orchestrator(self):
        with patch('orchestrator.vulnerability_orchestrator.GitHubSkill'), \
             patch('orchestrator.vulnerability_orchestrator.JiraSkill'), \
             patch('orchestrator.vulnerability_orchestrator.CodeAnalysisSkill'), \
             patch('orchestrator.vulnerability_orchestrator.VulnerabilityFixerSkill'), \
             patch('orchestrator.vulnerability_orchestrator.PRManagementSkill'):
            orch = VulnerabilityOrchestrator(self.config)
        orch.fixer_skill.fix_vulnerability = Mock(return_value={'success': True})
        return orch

    def test_fix_requires_human_approval(self):
        """Only approved vulnerabilities are fixed; rejected ones are skipped"""
        orch = self._make_orchestrator()
        vulns = [{'type': 'A', 'file': 'a.py'}, {'type': 'B', 'file': 'b.py'}]
        answers = iter(['yes', 'no'])
        fixed, failed = orch._step_fix_vulnerabilities(
            vulns, True, lambda v, i, n: next(answers))
        self.assertEqual(fixed, [vulns[0]])
        self.assertEqual(failed, [])
        self.assertEqual(orch.workflow_status['skipped_fixes'], [vulns[1]])
        orch.fixer_skill.fix_vulnerability.assert_called_once()

    def test_sonar_findings_merged_without_duplicates(self):
        """Sonar findings are added; same file+line as local findings is skipped"""
        orch = self._make_orchestrator()
        orch.sonar_skill = Mock()
        orch.sonar_skill.get_all_findings.return_value = {
            'success': True, 'count': 2, 'vulnerabilities': [
                {'file': 'a.py', 'line': 1, 'type': 'Sonar x'},
                {'file': 'c.py', 'line': 9, 'type': 'Sonar y'}]}
        local = [{'file': 'a.py', 'line': 1, 'type': 'SQL Injection'}]
        merged = orch._merge_sonar_findings(local)
        self.assertEqual([v['file'] for v in merged], ['a.py', 'c.py'])

    def test_sonar_failure_falls_back_to_local(self):
        orch = self._make_orchestrator()
        orch.sonar_skill = Mock()
        orch.sonar_skill.get_all_findings.return_value = {'success': False, 'error': 'down'}
        local = [{'file': 'a.py', 'line': 1}]
        self.assertEqual(orch._merge_sonar_findings(local), local)

    def test_fix_quit_and_all(self):
        """'quit' skips the rest; 'all' approves the rest without asking again"""
        orch = self._make_orchestrator()
        vulns = [{'type': 'A', 'file': 'a'}, {'type': 'B', 'file': 'b'}]
        fixed, _ = orch._step_fix_vulnerabilities(vulns, True, lambda v, i, n: 'quit')
        self.assertEqual(fixed, [])
        calls = []
        def cb(v, i, n):
            calls.append(i)
            return 'all'
        fixed, _ = orch._step_fix_vulnerabilities(vulns, True, cb)
        self.assertEqual(len(fixed), 2)
        self.assertEqual(calls, [1])



if __name__ == '__main__':
    unittest.main()

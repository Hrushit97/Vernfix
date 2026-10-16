"""Tests for the MCP server handlers (no network, no credentials)."""

import asyncio
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock

from mcp_server import tool_handlers as th
from mcp_server import code_handlers as ch
from mcp_server import resource_handlers as rh
from mcp_server.server import create_server, Services


class JiraGitHubTests(unittest.TestCase):
    def setUp(self):
        self.svc = MagicMock()

    def test_write_tools_need_confirm(self):
        for result in (
            th.create_jira_issue(self.svc, "PAY", "x"),
            th.link_pr_to_issue(self.svc, "PAY-1", "https://github.com/a/b/pull/1"),
            th.create_github_pr(self.svc, "repo", "t", "feature/x"),
        ):
            self.assertFalse(result['success'])
            self.assertIn('confirm', result['error'])
        self.svc.jira.create_issue.assert_not_called()
        self.svc.github.create_pull_request.assert_not_called()

    def test_confirmed_calls_reach_skills(self):
        th.create_jira_issue(self.svc, "PAY", "x", confirm=True)
        self.svc.jira.create_issue.assert_called_once()
        th.create_github_pr(self.svc, "repo", "t", "feature/x", confirm=True)
        self.svc.github.create_pull_request.assert_called_once()

    def test_input_validation(self):
        self.assertFalse(th.get_jira_issue(self.svc, "bad")['success'])
        self.assertFalse(th.search_jira_issues(self.svc, "pay; DROP")['success'])
        self.assertFalse(th.create_github_pr(self.svc, "r", "t", "../x", confirm=True)['success'])
        self.assertFalse(th.link_pr_to_issue(
            self.svc, "PAY-1", "http://evil.example/x", confirm=True)['success'])

    def test_skill_exception_gives_generic_error(self):
        self.svc.jira.get_issue.side_effect = RuntimeError("secret detail")
        result = th.get_jira_issue(self.svc, "PAY-1")
        self.assertFalse(result['success'])
        self.assertNotIn('secret detail', result['error'])


class SonarTests(unittest.TestCase):
    def test_passes_through_and_validates(self):
        svc = MagicMock()
        svc.sonar.get_quality_gate_status.return_value = {'success': True, 'passed': True}
        self.assertTrue(th.get_sonar_quality_gate(svc, None, "42")['passed'])
        svc.sonar.get_quality_gate_status.assert_called_with(None, "42")
        self.assertFalse(th.get_sonar_findings(svc, "bad branch!")['success'])


class CodeToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        with open(os.path.join(self.tmp, 'a.py'), 'w') as f:
            f.write('import yaml\nx = yaml.load(f)\n')
        os.environ['REPO_PATH'] = self.tmp
        self.svc = Services()

    def tearDown(self):
        os.environ.pop('REPO_PATH', None)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_analyze_then_list(self):
        self.assertFalse(ch.get_vulnerabilities(self.svc)['success'])  # before analysis
        res = ch.analyze_code(self.svc, ".", "python")
        self.assertEqual(res['total_vulnerabilities'], 1)
        listed = ch.get_vulnerabilities(self.svc, "critical", 10)
        self.assertEqual(listed['returned'], 1)
        self.assertEqual(ch.get_vulnerabilities(self.svc, "low")['returned'], 0)
        self.assertFalse(ch.get_vulnerabilities(self.svc, "all", 0)['success'])

    def test_javascript_filter_excludes_python(self):
        res = ch.analyze_code(self.svc, ".", "javascript")
        self.assertEqual(res['total_vulnerabilities'], 0)

    def test_path_traversal_blocked(self):
        self.assertFalse(ch.analyze_code(self.svc, "..")['success'])
        self.assertFalse(ch.fix_vulnerability(
            self.svc, "../x.py", 1, "Eval Usage", True)['success'])

    def test_fix_requires_confirm_and_modifies_file(self):
        path = os.path.join(self.tmp, 'a.py')
        self.assertFalse(ch.fix_vulnerability(
            self.svc, "a.py", 2, "Insecure Deserialization")['success'])
        self.assertIn('yaml.load(', open(path).read())
        res = ch.fix_vulnerability(self.svc, "a.py", 2, "Insecure Deserialization", True)
        self.assertTrue(res['success'])
        self.assertIn('yaml.safe_load(', open(path).read())
        status = ch.get_workflow_status(self.svc)
        self.assertEqual(status['fixes_applied'], 1)

    def test_unknown_vuln_type_rejected(self):
        self.assertFalse(ch.fix_vulnerability(self.svc, "a.py", 1, "Nope", True)['success'])


class ServerTests(unittest.TestCase):
    def test_registers_all_tools_and_resources(self):
        server = create_server(Services())

        async def listing():
            return await server.list_tools(), await server.list_resources()
        tools, resources = asyncio.run(listing())
        expected = sum(len(v) for v in rh.TOOLS.values())
        self.assertEqual(len(tools), expected)
        self.assertEqual(len(resources), 5)

    def test_config_resource_has_no_values(self):
        os.environ['GITHUB_TOKEN'] = 'super-secret-value'
        try:
            self.assertNotIn('super-secret-value', str(rh.get_config_info()))
        finally:
            os.environ.pop('GITHUB_TOKEN', None)


if __name__ == '__main__':
    unittest.main()

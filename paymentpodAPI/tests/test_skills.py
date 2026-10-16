"""
Unit tests for vulnerability fixing skills
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from skills.code_analysis_skill import CodeAnalysisSkill
from skills.vulnerability_fixer_skill import VulnerabilityFixerSkill


class TestCodeAnalysisSkill(unittest.TestCase):
    """Test code analysis functionality"""

    def setUp(self):
        """Setup test fixtures"""
        self.skill = CodeAnalysisSkill()
        self.temp_dir = tempfile.mkdtemp()

    def test_analyze_python_sql_injection(self):
        """Test detection of SQL injection vulnerability"""
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('execute("SELECT * FROM users WHERE id = %s")')
        
        vulns = self.skill.analyze_python(test_file)
        self.assertTrue(any(v['type'] == 'SQL Injection' for v in vulns))

    def test_analyze_python_hardcoded_secret(self):
        """Test detection of hardcoded secrets"""
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('password = "secretpassword123"')
        
        vulns = self.skill.analyze_python(test_file)
        self.assertTrue(any(v['type'] == 'Hardcoded Secret' for v in vulns))

    def test_scan_directory(self):
        """Test directory scanning"""
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('password = "secret"')
        
        result = self.skill.scan_directory(self.temp_dir)
        self.assertGreater(result['total_vulnerabilities'], 0)


class TestVulnerabilityFixerSkill(unittest.TestCase):
    """Test vulnerability fixing functionality"""

    def setUp(self):
        """Setup test fixtures"""
        self.skill = VulnerabilityFixerSkill()
        self.temp_dir = tempfile.mkdtemp()

    def test_fix_hardcoded_secret(self):
        """Test fixing hardcoded secrets"""
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('password = "secretpassword123"')
        
        vuln = {
            'type': 'Hardcoded Secret',
            'line': 1,
            'file': test_file
        }
        
        result = self.skill.fix_vulnerability(test_file, vuln)
        self.assertTrue(result['success'])
        
        with open(test_file, 'r') as f:
            content = f.read()
        self.assertIn('os.getenv', content)

    def test_fix_insecure_deserialization(self):
        """Test fixing insecure deserialization"""
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('import pickle\ndata = pickle.load(f)')
        
        vuln = {
            'type': 'Insecure Deserialization',
            'line': 2,
            'file': test_file
        }
        
        result = self.skill.fix_vulnerability(test_file, vuln)
        self.assertTrue(result['success'])


class TestSonarSkill(unittest.TestCase):
    """Test Sonar findings retrieval with mocked HTTP"""

    def setUp(self):
        from skills.sonar_skill import SonarSkill
        self.skill = SonarSkill('https://sonar.test', 'tok', 'proj', repo_path='/repo')

    def test_get_all_findings_normalised(self):
        def fake_get(path, params):
            if path == '/api/issues/search':
                return {'issues': [{'key': 'I1', 'component': 'proj:src/a.py', 'line': 3,
                                    'rule': 'python:S2077', 'message': 'SQL', 'severity': 'BLOCKER'}],
                        'paging': {'total': 1}}
            return {'hotspots': [{'key': 'H1', 'component': 'proj:src/b.py', 'line': 7,
                                  'ruleKey': 'python:S4426', 'message': 'Crypto',
                                  'vulnerabilityProbability': 'HIGH'}],
                    'paging': {'total': 1}}
        self.skill._get = fake_get
        result = self.skill.get_all_findings()
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 2)
        self.assertEqual(result['vulnerabilities'][0]['severity'], 'CRITICAL')
        self.assertEqual(result['vulnerabilities'][1]['sonar_kind'], 'hotspot')
        self.assertTrue(result['vulnerabilities'][0]['file'].endswith('a.py'))

    def test_pagination(self):
        pages = {1: {'issues': [{}] * 500, 'paging': {'total': 501}},
                 2: {'issues': [{}], 'paging': {'total': 501}}}
        self.skill._get = lambda path, params: pages[params['p']]
        self.assertEqual(len(self.skill._paginate('/x', {}, 'issues')), 501)

    def test_failure_returns_error(self):
        def boom(path, params):
            raise RuntimeError('401')
        self.skill._get = boom
        result = self.skill.get_all_findings()
        self.assertFalse(result['success'])


if __name__ == '__main__':
    unittest.main()

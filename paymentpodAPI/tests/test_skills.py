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


if __name__ == '__main__':
    unittest.main()

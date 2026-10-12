"""
Code Analysis Skill
Performs static analysis to detect security vulnerabilities
"""

import os
import re
import json
from typing import Dict, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Vulnerability severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CodeAnalysisSkill:
    """Skill to analyze code for vulnerabilities"""

    def __init__(self):
        """Initialize code analyzer"""
        self.vulnerabilities = []

    def analyze_python(self, file_path: str) -> List[Dict]:
        """Analyze Python files for vulnerabilities"""
        vulns = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for SQL injection patterns
            sql_patterns = [
                (r'execute\s*\(\s*["\'].*%s', 'SQL Injection'),
                (r'query\s*\(\s*["\'].*%', 'SQL Injection'),
            ]

            for pattern, vuln_type in sql_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulns.append(self._create_vuln(
                        file_path, line_num, vuln_type,
                        SeverityLevel.CRITICAL, match.group()
                    ))

            # Check for hardcoded secrets
            secret_patterns = [
                (r'(password\s*=\s*["\'][^"\']+["\'])', 'Hardcoded Secret'),
                (r'(api_key\s*=\s*["\'][^"\']+["\'])', 'Hardcoded API Key'),
                (r'(secret\s*=\s*["\'][^"\']+["\'])', 'Hardcoded Secret'),
            ]

            for pattern, vuln_type in secret_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    vulns.append(self._create_vuln(
                        file_path, line_num, vuln_type,
                        SeverityLevel.HIGH, match.group()
                    ))

            # Check for insecure deserialization
            if re.search(r'pickle\.load\s*\(|yaml\.load\s*\(', content):
                vulns.append(self._create_vuln(
                    file_path, 1, 'Insecure Deserialization',
                    SeverityLevel.CRITICAL, 'pickle/yaml.load usage'
                ))

            logger.info(f"Found {len(vulns)} vulnerabilities in {file_path}")
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")

        return vulns

    def analyze_javascript(self, file_path: str) -> List[Dict]:
        """Analyze JavaScript files for vulnerabilities"""
        vulns = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for eval usage
            if re.search(r'\beval\s*\(', content):
                vulns.append(self._create_vuln(
                    file_path, 1, 'Eval Usage',
                    SeverityLevel.CRITICAL, 'eval() detected'
                ))

            # Check for innerHTML assignments
            if re.search(r'\.innerHTML\s*=', content):
                vulns.append(self._create_vuln(
                    file_path, 1, 'XSS Vulnerability',
                    SeverityLevel.HIGH, 'innerHTML assignment'
                ))

            logger.info(f"Found {len(vulns)} vulnerabilities in {file_path}")
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")

        return vulns

    def scan_directory(self, directory: str) -> Dict:
        """Scan entire directory for vulnerabilities"""
        all_vulns = []
        file_count = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.py'):
                    all_vulns.extend(self.analyze_python(file_path))
                    file_count += 1
                elif file.endswith('.js') or file.endswith('.jsx'):
                    all_vulns.extend(self.analyze_javascript(file_path))
                    file_count += 1

        return {
            "total_files": file_count,
            "total_vulnerabilities": len(all_vulns),
            "vulnerabilities": all_vulns,
        }

    def _create_vuln(self, file_path: str, line_num: int, 
                     vuln_type: str, severity: SeverityLevel, code: str) -> Dict:
        """Create vulnerability report"""
        return {
            "file": file_path,
            "line": line_num,
            "type": vuln_type,
            "severity": severity.value,
            "code": code,
        }

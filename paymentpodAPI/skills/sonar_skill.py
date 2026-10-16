"""
Sonar Skill
Reads vulnerabilities and security hotspots from SonarQube / SonarCloud
via the Sonar Web API (the same data the Sonar MCP server exposes).
"""

import os
import logging
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

SONAR_SEVERITY_MAP = {
    'BLOCKER': 'CRITICAL', 'CRITICAL': 'CRITICAL',
    'MAJOR': 'HIGH', 'MINOR': 'MEDIUM', 'INFO': 'LOW',
}
HOTSPOT_SEVERITY_MAP = {'HIGH': 'HIGH', 'MEDIUM': 'MEDIUM', 'LOW': 'LOW'}
PAGE_SIZE = 500          # Sonar maximum per page
MAX_ISSUES = 10000       # Sonar search hard limit


class SonarSkill:
    """Skill to fetch all Sonar security findings for a project"""

    def __init__(self, sonar_url: str, sonar_token: str, project_key: str,
                 repo_path: Optional[str] = None, timeout: int = 30):
        """
        Args:
            sonar_url: e.g. https://sonarcloud.io or your SonarQube URL
            sonar_token: Sonar user token (read from env/secret store, never hardcode)
            project_key: Sonar project key
            repo_path: Local repo root, used to build absolute file paths
        """
        self.base_url = sonar_url.rstrip('/')
        self.project_key = project_key
        self.repo_path = repo_path
        self.timeout = timeout
        self.session = requests.Session()
        # Sonar token auth: token as username, empty password
        self.session.auth = (sonar_token, '')

    def _get(self, path: str, params: Dict) -> Dict:
        response = self.session.get(
            f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _paginate(self, path: str, params: Dict, items_key: str) -> List[Dict]:
        items, page = [], 1
        while True:
            data = self._get(path, {**params, 'p': page, 'ps': PAGE_SIZE})
            batch = data.get(items_key, [])
            items.extend(batch)
            total = data.get('paging', {}).get('total', len(items))
            if not batch or len(items) >= total or len(items) >= MAX_ISSUES:
                return items
            page += 1

    def _to_path(self, component: str) -> str:
        """Convert 'projectKey:src/app.py' into a local file path"""
        rel = component.split(':', 1)[-1]
        return os.path.join(self.repo_path, rel) if self.repo_path else rel

    def get_vulnerabilities(self, branch: Optional[str] = None,
                            pull_request: Optional[str] = None) -> Dict:
        """Get open VULNERABILITY issues"""
        params = {'componentKeys': self.project_key,
                  'types': 'VULNERABILITY', 'resolved': 'false'}
        if branch:
            params['branch'] = branch
        if pull_request:
            params['pullRequest'] = pull_request
        issues = self._paginate('/api/issues/search', params, 'issues')
        return {'success': True, 'count': len(issues), 'vulnerabilities': [
            self._normalise(i['component'], i.get('line', 1),
                            i.get('rule', 'sonar'), i.get('message', ''),
                            SONAR_SEVERITY_MAP.get(i.get('severity'), 'MEDIUM'),
                            i['key'], 'issue')
            for i in issues]}

    def get_security_hotspots(self, branch: Optional[str] = None,
                              pull_request: Optional[str] = None) -> Dict:
        """Get security hotspots still TO_REVIEW"""
        params = {'projectKey': self.project_key, 'status': 'TO_REVIEW'}
        if branch:
            params['branch'] = branch
        if pull_request:
            params['pullRequest'] = pull_request
        hotspots = self._paginate('/api/hotspots/search', params, 'hotspots')
        return {'success': True, 'count': len(hotspots), 'vulnerabilities': [
            self._normalise(h['component'], h.get('line', 1),
                            h.get('ruleKey', 'sonar-hotspot'), h.get('message', ''),
                            HOTSPOT_SEVERITY_MAP.get(
                                h.get('vulnerabilityProbability'), 'MEDIUM'),
                            h['key'], 'hotspot')
            for h in hotspots]}

    def get_quality_gate_status(self, branch: Optional[str] = None,
                                pull_request: Optional[str] = None) -> Dict:
        """Get quality gate result ('OK' or 'ERROR')"""
        params = {'projectKey': self.project_key}
        if branch:
            params['branch'] = branch
        if pull_request:
            params['pullRequest'] = pull_request
        data = self._get('/api/qualitygates/project_status', params)
        status = data.get('projectStatus', {}).get('status', 'NONE')
        return {'success': True, 'status': status, 'passed': status == 'OK'}

    def get_all_findings(self, branch: Optional[str] = None,
                         pull_request: Optional[str] = None) -> Dict:
        """Vulnerabilities + hotspots in the orchestrator's vulnerability format"""
        try:
            vulns = self.get_vulnerabilities(branch, pull_request)['vulnerabilities']
            hotspots = self.get_security_hotspots(branch, pull_request)['vulnerabilities']
            findings = vulns + hotspots
            return {'success': True, 'count': len(findings), 'vulnerabilities': findings}
        except Exception as e:
            logger.error(f"Sonar fetch failed: {e}")
            return {'success': False, 'error': str(e), 'count': 0, 'vulnerabilities': []}

    def _normalise(self, component: str, line: int, rule: str, message: str,
                   severity: str, key: str, kind: str) -> Dict:
        return {
            'file': self._to_path(component),
            'line': line,
            'type': f"Sonar {rule}",
            'severity': severity,
            'code': message,
            'source': 'sonar',
            'sonar_key': key,
            'sonar_kind': kind,
        }

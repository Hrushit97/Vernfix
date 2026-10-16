"""
MCP handlers for code analysis, fixing and session status (blueprint tools
analyze_code, get_vulnerabilities, fix_vulnerability, get_workflow_status).

`services` needs: .analyzer, .fixer, .repo_root, .last_analysis, .fix_log.
All file paths must stay inside services.repo_root. fix_vulnerability edits
files, so it needs confirm=True.
"""

import os
from typing import Dict, Optional

from mcp_server.tool_handlers import _error, _need_confirm, _safe

FILE_TYPES = {'python': ('.py',), 'javascript': ('.js', '.jsx'),
              'all': ('.py', '.js', '.jsx')}
FIXABLE_TYPES = {'SQL Injection', 'Hardcoded Secret', 'Hardcoded API Key',
                 'Insecure Deserialization', 'Eval Usage', 'XSS Vulnerability'}
SEVERITIES = ('critical', 'high', 'medium', 'low')
MAX_LIMIT = 500


def resolve_in_root(services, path: str) -> Optional[str]:
    """Absolute real path if `path` is inside the repo root, else None"""
    if not isinstance(path, str) or not path or '\x00' in path:
        return None
    root = os.path.realpath(services.repo_root)
    full = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
    try:
        return full if os.path.commonpath([root, full]) == root else None
    except ValueError:  # different drive on Windows
        return None


def _counts(vulns) -> Dict:
    counts = {s: 0 for s in SEVERITIES}
    for v in vulns:
        sev = str(v.get('severity', '')).lower()
        if sev in counts:
            counts[sev] += 1
    return counts


@_safe
def analyze_code(services, path: str = ".", file_type: str = "all") -> Dict:
    if file_type not in FILE_TYPES:
        return _error(f"file_type must be one of {sorted(FILE_TYPES)}")
    full = resolve_in_root(services, path)
    if not full or not os.path.isdir(full):
        return _error("path must be a directory inside the repository root")
    result = services.analyzer.scan_directory(full)
    exts = FILE_TYPES[file_type]
    vulns = [v for v in result.get('vulnerabilities', [])
             if str(v.get('file', '')).endswith(exts)]
    services.last_analysis = {'path': full, 'file_type': file_type,
                              'total_files': result.get('total_files', 0),
                              'vulnerabilities': vulns}
    return {'success': True, 'total_files': result.get('total_files', 0),
            'total_vulnerabilities': len(vulns), 'by_severity': _counts(vulns)}


@_safe
def get_vulnerabilities(services, filter: str = "all", limit: int = 50) -> Dict:
    if filter != 'all' and filter not in SEVERITIES:
        return _error(f"filter must be 'all' or one of {list(SEVERITIES)}")
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= MAX_LIMIT:
        return _error(f"limit must be an integer from 1 to {MAX_LIMIT}")
    if not services.last_analysis:
        return _error("No analysis yet: call analyze_code first")
    vulns = services.last_analysis['vulnerabilities']
    if filter != 'all':
        vulns = [v for v in vulns if str(v.get('severity', '')).lower() == filter]
    return {'success': True, 'total_matching': len(vulns), 'returned': min(len(vulns), limit),
            'vulnerabilities': vulns[:limit]}


@_safe
def fix_vulnerability(services, file: str, line: int, vuln_type: str,
                      confirm: bool = False) -> Dict:
    err = _need_confirm(confirm, 'modify a file')
    if err:
        return err
    if vuln_type not in FIXABLE_TYPES:
        return _error(f"vuln_type must be one of {sorted(FIXABLE_TYPES)}")
    if not isinstance(line, int) or isinstance(line, bool) or line < 1:
        return _error("line must be a positive integer")
    full = resolve_in_root(services, file)
    if not full or not os.path.isfile(full) or not full.endswith(FILE_TYPES['all']):
        return _error("file must be an existing .py/.js/.jsx file inside the repository root")
    result = services.fixer.fix_vulnerability(full, {'type': vuln_type, 'line': line})
    services.fix_log.append({'file': full, 'line': line, 'type': vuln_type,
                             'success': bool(result.get('success'))})
    return result


@_safe
def get_workflow_status(services) -> Dict:
    last = services.last_analysis
    return {'success': True,
            'analysis': None if not last else {
                'path': last['path'], 'total_files': last['total_files'],
                'total_vulnerabilities': len(last['vulnerabilities']),
                'by_severity': _counts(last['vulnerabilities'])},
            'fixes_applied': sum(1 for f in services.fix_log if f['success']),
            'fixes_failed': sum(1 for f in services.fix_log if not f['success']),
            'fix_log': services.fix_log[-20:]}

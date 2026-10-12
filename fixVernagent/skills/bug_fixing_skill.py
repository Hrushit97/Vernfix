"""
Bug Fixing Skill for Code Analysis and Repair
"""

import re
import ast
from typing import Dict, List, Any
from agent import Skill


class BugFixingSkill(Skill):
    """Skill for analyzing and fixing bugs in code"""
    
    def __init__(self):
        super().__init__(
            name="BugFixer",
            description="Analyze code for bugs and generate fixes"
        )
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code for potential bugs"""
        bugs = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            bugs.append({
                "type": "syntax_error",
                "line": e.lineno,
                "message": e.msg,
                "severity": "critical"
            })
            return {"bugs": bugs, "code_valid": False}
        
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for common bug patterns
            if self._check_bare_except(line):
                bugs.append({
                    "type": "bare_except",
                    "line": i,
                    "message": "Bare 'except:' clause is too broad",
                    "severity": "high"
                })
            
            if self._check_none_comparison(line):
                bugs.append({
                    "type": "none_comparison",
                    "line": i,
                    "message": "Use 'is None' instead of '== None'",
                    "severity": "medium"
                })
            
            if self._check_mutable_default(line):
                bugs.append({
                    "type": "mutable_default",
                    "line": i,
                    "message": "Using mutable object as default argument",
                    "severity": "high"
                })
        
        return {"bugs": bugs, "code_valid": True, "total_bugs": len(bugs)}
    
    def _check_bare_except(self, line: str) -> bool:
        """Check for bare except clause"""
        return bool(re.search(r'except\s*:', line))
    
    def _check_none_comparison(self, line: str) -> bool:
        """Check for None comparison with =="""
        return bool(re.search(r'(==\s*None|None\s*==)', line))
    
    def _check_mutable_default(self, line: str) -> bool:
        """Check for mutable default arguments"""
        return bool(re.search(r'def\s+\w+\([^)]*=\s*(\[|{)', line))
    
    def generate_fix(self, bug_type: str, code_line: str) -> Dict[str, str]:
        """Generate a fix for identified bug"""
        fixes = {
            "bare_except": {
                "before": "except:",
                "after": "except Exception as e:",
                "explanation": "Catch specific exceptions to avoid masking bugs"
            },
            "none_comparison": {
                "before": code_line.strip(),
                "after": code_line.replace("== None", "is None").replace("None ==", "is"),
                "explanation": "Use 'is' for singleton comparison with None"
            },
            "mutable_default": {
                "before": code_line.strip(),
                "after": "Use None as default, initialize inside function",
                "explanation": "Mutable defaults are shared across function calls"
            }
        }
        return fixes.get(bug_type, {"explanation": "Unknown bug type"})
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute bug fixing skill"""
        action = kwargs.get("action", "analyze")
        code = kwargs.get("code", "")
        
        if action == "analyze":
            return self.analyze_code(code)
        elif action == "suggest_fix":
            bug_type = kwargs.get("bug_type")
            code_line = kwargs.get("code_line", "")
            return self.generate_fix(bug_type, code_line)
        else:
            raise ValueError(f"Unknown action: {action}")

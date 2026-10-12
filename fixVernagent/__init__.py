"""
VernfixAgent - Python AI Agent with Multiple Skills
"""

from .agent import AIAgent, Skill, SkillStatus
from .skills import GitHubSkill, JiraSkill, BugFixingSkill

__version__ = "1.0.0"
__author__ = "VernfixAgent Team"

__all__ = [
    'AIAgent',
    'Skill',
    'SkillStatus',
    'GitHubSkill',
    'JiraSkill',
    'BugFixingSkill'
]

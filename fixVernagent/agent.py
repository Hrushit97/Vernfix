"""
Core AI Agent Framework with Skill Management
"""

import json
from typing import Dict, List, Any, Callable
from abc import ABC, abstractmethod
from enum import Enum


class SkillStatus(Enum):
    """Skill execution status"""
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NOT_EXECUTED = "not_executed"


class Skill(ABC):
    """Base class for all agent skills"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = SkillStatus.NOT_EXECUTED
        self.result = None
        self.error = None
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with given parameters"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current skill status"""
        return {
            "name": self.name,
            "status": self.status.value,
            "result": self.result,
            "error": self.error
        }


class AIAgent:
    """Main AI Agent with multiple skills"""
    
    def __init__(self, name: str = "VernfixAgent", model: str = "openai"):
        self.name = name
        self.model = model
        self.skills: Dict[str, Skill] = {}
        self.execution_history: List[Dict] = []
    
    def add_skill(self, skill: Skill) -> None:
        """Register a new skill"""
        self.skills[skill.name] = skill
        print(f"✓ Skill '{skill.name}' registered")
    
    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific skill"""
        if skill_name not in self.skills:
            return {
                "status": SkillStatus.FAILED.value,
                "error": f"Skill '{skill_name}' not found"
            }
        
        skill = self.skills[skill_name]
        skill.status = SkillStatus.IN_PROGRESS
        
        try:
            result = skill.execute(**kwargs)
            skill.status = SkillStatus.SUCCESS
            skill.result = result
            execution_record = {
                "skill": skill_name,
                "status": SkillStatus.SUCCESS.value,
                "result": result
            }
        except Exception as e:
            skill.status = SkillStatus.FAILED
            skill.error = str(e)
            execution_record = {
                "skill": skill_name,
                "status": SkillStatus.FAILED.value,
                "error": str(e)
            }
        
        self.execution_history.append(execution_record)
        return skill.get_status()
    
    def list_skills(self) -> List[Dict[str, str]]:
        """List all available skills"""
        return [
            {"name": skill.name, "description": skill.description}
            for skill in self.skills.values()
        ]
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get overall agent status"""
        return {
            "agent_name": self.name,
            "model": self.model,
            "total_skills": len(self.skills),
            "skills": self.list_skills(),
            "execution_history": self.execution_history
        }

"""
Unit tests for VernfixAgent
"""

import unittest
from agent import AIAgent, Skill, SkillStatus
from skills import BugFixingSkill


class TestSkillBase(unittest.TestCase):
    """Test base Skill class"""
    
    def test_skill_initialization(self):
        """Test skill can be initialized"""
        skill = BugFixingSkill()
        self.assertEqual(skill.name, "BugFixer")
        self.assertIsNotNone(skill.description)
        self.assertEqual(skill.status, SkillStatus.NOT_EXECUTED)


class TestAIAgent(unittest.TestCase):
    """Test AIAgent class"""
    
    def setUp(self):
        """Set up test agent"""
        self.agent = AIAgent(name="TestAgent", model="openai")
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.model, "openai")
        self.assertEqual(len(self.agent.skills), 0)
    
    def test_add_skill(self):
        """Test adding a skill"""
        skill = BugFixingSkill()
        self.agent.add_skill(skill)
        self.assertIn("BugFixer", self.agent.skills)
        self.assertEqual(len(self.agent.skills), 1)
    
    def test_list_skills(self):
        """Test listing skills"""
        skill = BugFixingSkill()
        self.agent.add_skill(skill)
        skills = self.agent.list_skills()
        self.assertEqual(len(skills), 1)
        self.assertEqual(skills[0]["name"], "BugFixer")
    
    def test_execute_nonexistent_skill(self):
        """Test executing non-existent skill"""
        result = self.agent.execute_skill("NonExistent")
        self.assertEqual(result["status"], "failed")
        self.assertIn("not found", result["error"])


class TestBugFixingSkill(unittest.TestCase):
    """Test BugFixingSkill"""
    
    def setUp(self):
        """Set up test skill"""
        self.skill = BugFixingSkill()
    
    def test_analyze_valid_code(self):
        """Test analyzing valid code"""
        code = "x = 1\nprint(x)"
        result = self.skill.execute(action="analyze", code=code)
        self.assertTrue(result["code_valid"])
    
    def test_detect_syntax_error(self):
        """Test detecting syntax errors"""
        code = "def foo(\n    pass"
        result = self.skill.execute(action="analyze", code=code)
        self.assertFalse(result["code_valid"])
        self.assertGreater(len(result["bugs"]), 0)
    
    def test_detect_bare_except(self):
        """Test detecting bare except"""
        code = """
try:
    x = 1
except:
    pass
"""
        result = self.skill.execute(action="analyze", code=code)
        self.assertTrue(result["code_valid"])
        bugs = [b for b in result["bugs"] if b["type"] == "bare_except"]
        self.assertGreater(len(bugs), 0)
    
    def test_detect_none_comparison(self):
        """Test detecting None comparison"""
        code = "if x == None:\n    pass"
        result = self.skill.execute(action="analyze", code=code)
        bugs = [b for b in result["bugs"] if b["type"] == "none_comparison"]
        self.assertGreater(len(bugs), 0)
    
    def test_suggest_fix(self):
        """Test generating fix suggestions"""
        result = self.skill.execute(
            action="suggest_fix",
            bug_type="none_comparison",
            code_line="if x == None:"
        )
        self.assertIn("explanation", result)


class TestAgentStatus(unittest.TestCase):
    """Test agent status tracking"""
    
    def setUp(self):
        """Set up test"""
        self.agent = AIAgent()
        self.agent.add_skill(BugFixingSkill())
    
    def test_get_agent_status(self):
        """Test getting agent status"""
        status = self.agent.get_agent_status()
        self.assertEqual(status["total_skills"], 1)
        self.assertIsNotNone(status["agent_name"])
        self.assertIsNotNone(status["skills"])
    
    def test_execution_history(self):
        """Test execution history tracking"""
        code = "x = 1"
        self.agent.execute_skill("BugFixer", action="analyze", code=code)
        status = self.agent.get_agent_status()
        self.assertGreater(len(status["execution_history"]), 0)


if __name__ == "__main__":
    unittest.main()

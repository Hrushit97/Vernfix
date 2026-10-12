"""
Unit tests for Jira Skill
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from skills.jira_skill import JiraSkill


class TestJiraSkillInitialization(unittest.TestCase):
    """Test Jira Skill initialization"""
    
    def test_skill_initialization_without_credentials(self):
        """Test initializing without credentials"""
        skill = JiraSkill()
        self.assertEqual(skill.name, "Jira")
        self.assertIsNone(skill.client)
        self.assertIsNone(skill.server)
        self.assertIsNone(skill.email)
        self.assertIsNone(skill.api_token)
    
    def test_skill_initialization_with_credentials(self):
        """Test initializing with credentials"""
        with patch('skills.jira_skill.JIRA'):
            skill = JiraSkill(
                server="https://test.atlassian.net",
                email="test@test.com",
                api_token="token123"
            )
            self.assertEqual(skill.server, "https://test.atlassian.net")
            self.assertEqual(skill.email, "test@test.com")
            self.assertEqual(skill.api_token, "token123")


class TestJiraSkillConnect(unittest.TestCase):
    """Test Jira connection methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.skill = JiraSkill()
    
    @patch('skills.jira_skill.JIRA')
    def test_connect_success(self, mock_jira):
        """Test successful connection"""
        mock_client = MagicMock()
        mock_client.myself.return_value = {
            "displayName": "Test User",
            "emailAddress": "test@example.com"
        }
        mock_jira.return_value = mock_client
        
        result = self.skill.connect(
            "https://test.atlassian.net",
            "test@example.com",
            "token123"
        )
        
        self.assertEqual(result["status"], "connected")
        self.assertEqual(result["user"], "Test User")
        self.assertEqual(result["email"], "test@example.com")
        self.assertIsNotNone(self.skill.client)
    
    @patch('skills.jira_skill.JIRA')
    def test_connect_failure(self, mock_jira):
        """Test connection failure"""
        mock_jira.side_effect = Exception("Invalid credentials")
        
        with self.assertRaises(Exception) as context:
            self.skill.connect(
                "https://test.atlassian.net",
                "test@example.com",
                "invalid_token"
            )
        
        self.assertIn("Jira connection failed", str(context.exception))


class TestJiraSkillProjects(unittest.TestCase):
    """Test Jira project listing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.skill = JiraSkill()
        self.mock_client = MagicMock()
        self.skill.client = self.mock_client
    
    def test_list_projects_success(self):
        """Test successful project listing"""
        mock_project1 = Mock(key="PROJ1", name="Project 1", projectTypeKey="software")
        mock_project2 = Mock(key="PROJ2", name="Project 2", projectTypeKey="business")
        self.mock_client.projects.return_value = [mock_project1, mock_project2]
        
        result = self.skill.list_projects()
        
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["projects"]), 2)
        self.assertEqual(result["projects"][0]["key"], "PROJ1")
        self.assertEqual(result["projects"][1]["key"], "PROJ2")
    
    def test_list_projects_not_connected(self):
        """Test list projects without connection"""
        skill = JiraSkill()
        
        with self.assertRaises(Exception) as context:
            skill.list_projects()
        
        self.assertIn("Not connected to Jira", str(context.exception))
    
    def test_list_projects_api_error(self):
        """Test list projects with API error"""
        self.mock_client.projects.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception) as context:
            self.skill.list_projects()
        
        self.assertIn("Failed to list projects", str(context.exception))


class TestJiraSkillIssues(unittest.TestCase):
    """Test Jira issue operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.skill = JiraSkill()
        self.mock_client = MagicMock()
        self.skill.client = self.mock_client
    
    def test_list_issues_success(self):
        """Test successful issue listing"""
        mock_issue1 = Mock(
            key="PROJ-1",
            fields=Mock(
                summary="Bug 1",
                status=Mock(name="Open"),
                priority=Mock(name="High"),
                assignee=Mock(displayName="Dev 1"),
                created="2024-01-01"
            )
        )
        self.mock_client.search_issues.return_value = [mock_issue1]
        
        result = self.skill.list_issues("PROJ", "Bug")
        
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["issues"][0]["key"], "PROJ-1")
        self.assertEqual(result["issues"][0]["summary"], "Bug 1")
        self.assertEqual(result["issues"][0]["status"], "Open")
    
    def test_list_issues_not_connected(self):
        """Test list issues without connection"""
        skill = JiraSkill()
        
        with self.assertRaises(Exception):
            skill.list_issues("PROJ")
    
    def test_list_issues_no_assignee(self):
        """Test listing issues with unassigned issue"""
        mock_issue = Mock(
            key="PROJ-2",
            fields=Mock(
                summary="Unassigned Bug",
                status=Mock(name="Open"),
                priority=None,
                assignee=None,
                created="2024-01-02"
            )
        )
        self.mock_client.search_issues.return_value = [mock_issue]
        
        result = self.skill.list_issues("PROJ", "Bug")
        
        self.assertIsNone(result["issues"][0]["assignee"])
        self.assertIsNone(result["issues"][0]["priority"])
    
    def test_create_issue_success(self):
        """Test successful issue creation"""
        mock_created_issue = Mock(key="PROJ-100")
        self.mock_client.create_issue.return_value = mock_created_issue
        
        result = self.skill.create_issue(
            "PROJ",
            "New Bug",
            "Bug description",
            "Bug"
        )
        
        self.assertEqual(result["status"], "created")
        self.assertEqual(result["issue_key"], "PROJ-100")
    
    def test_create_issue_not_connected(self):
        """Test create issue without connection"""
        skill = JiraSkill()
        
        with self.assertRaises(Exception):
            skill.create_issue("PROJ", "Summary", "Description")
    
    def test_create_issue_api_error(self):
        """Test create issue with API error"""
        self.mock_client.create_issue.side_effect = Exception("Creation failed")
        
        with self.assertRaises(Exception) as context:
            self.skill.create_issue("PROJ", "Summary", "Description")
        
        self.assertIn("Failed to create issue", str(context.exception))


class TestJiraSkillExecute(unittest.TestCase):
    """Test Jira skill execute method"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.skill = JiraSkill()
        self.mock_client = MagicMock()
        self.skill.client = self.mock_client
    
    @patch('skills.jira_skill.JIRA')
    def test_execute_connect(self, mock_jira):
        """Test execute with connect action"""
        mock_client = MagicMock()
        mock_client.myself.return_value = {
            "displayName": "User",
            "emailAddress": "user@test.com"
        }
        mock_jira.return_value = mock_client
        
        result = self.skill.execute(
            action="connect",
            server="https://test.atlassian.net",
            email="user@test.com",
            api_token="token"
        )
        
        self.assertEqual(result["status"], "connected")
    
    def test_execute_list_projects(self):
        """Test execute with list_projects action"""
        mock_project = Mock(key="PROJ", name="Project", projectTypeKey="software")
        self.mock_client.projects.return_value = [mock_project]
        
        result = self.skill.execute(action="list_projects")
        
        self.assertEqual(result["total"], 1)
    
    def test_execute_list_issues(self):
        """Test execute with list_issues action"""
        mock_issue = Mock(
            key="PROJ-1",
            fields=Mock(
                summary="Issue",
                status=Mock(name="Open"),
                priority=Mock(name="High"),
                assignee=Mock(displayName="User"),
                created="2024-01-01"
            )
        )
        self.mock_client.search_issues.return_value = [mock_issue]
        
        result = self.skill.execute(
            action="list_issues",
            project_key="PROJ"
        )
        
        self.assertEqual(result["total"], 1)
    
    def test_execute_create_issue(self):
        """Test execute with create_issue action"""
        mock_issue = Mock(key="PROJ-50")
        self.mock_client.create_issue.return_value = mock_issue
        
        result = self.skill.execute(
            action="create_issue",
            project_key="PROJ",
            summary="New Issue",
            description="Description"
        )
        
        self.assertEqual(result["status"], "created")
    
    def test_execute_invalid_action(self):
        """Test execute with invalid action"""
        with self.assertRaises(ValueError) as context:
            self.skill.execute(action="invalid_action")
        
        self.assertIn("Unknown action", str(context.exception))


class TestJiraSkillEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.skill = JiraSkill()
        self.mock_client = MagicMock()
        self.skill.client = self.mock_client
    
    def test_list_empty_projects(self):
        """Test listing when no projects exist"""
        self.mock_client.projects.return_value = []
        
        result = self.skill.list_projects()
        
        self.assertEqual(result["total"], 0)
        self.assertEqual(len(result["projects"]), 0)
    
    def test_list_empty_issues(self):
        """Test listing when no issues exist"""
        self.mock_client.search_issues.return_value = []
        
        result = self.skill.list_issues("PROJ", "Bug")
        
        self.assertEqual(result["total"], 0)
        self.assertEqual(len(result["issues"]), 0)
    
    def test_create_issue_with_custom_type(self):
        """Test creating issue with custom type"""
        mock_issue = Mock(key="PROJ-1")
        self.mock_client.create_issue.return_value = mock_issue
        
        result = self.skill.create_issue(
            "PROJ",
            "Summary",
            "Description",
            "Task"
        )
        
        self.assertEqual(result["issue_key"], "PROJ-1")


if __name__ == "__main__":
    unittest.main()

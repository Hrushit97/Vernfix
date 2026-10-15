# MCP Implementation - Detailed Blueprint

## 🎯 Complete Implementation Plan

---

## 📁 Directory Structure

```
paymentpodAPI/
├── mcp/                          # NEW: MCP implementation
│   ├── __init__.py
│   ├── mcp_server.py            # MCP server instance
│   ├── mcp_tools.py             # Tool definitions
│   ├── mcp_resources.py         # Resource handlers
│   ├── tool_handlers.py         # Tool logic
│   └── resource_handlers.py     # Resource logic
├── orchestrator/
│   └── vulnerability_orchestrator.py
├── skills/
│   ├── code_analysis_skill.py
│   ├── github_skill.py
│   ├── jira_skill.py
│   ├── vulnerability_fixer_skill.py
│   └── pr_management_skill.py
└── main.py
```

---

## 🔧 Implementation Details

### 1. MCP Server (`mcp/mcp_server.py`)

**Responsibilities:**
- Initialize MCP server
- Register tools
- Register resources
- Handle protocol messages
- Manage orchestrator instance

**Key Functions:**
```python
def create_server() -> Server:
    """Create and configure MCP server"""
    
def register_tools(server: Server):
    """Register all available tools"""
    
def register_resources(server: Server):
    """Register all available resources"""
    
async def run_server():
    """Run MCP server"""
```

---

### 2. Tools Definition (`mcp/mcp_tools.py`)

**Tools to Implement:**

#### Tool 1: analyze_code

```python
{
    "name": "analyze_code",
    "description": "Analyze code for vulnerabilities",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Directory to analyze"},
            "file_type": {"type": "string", "enum": ["python", "javascript", "all"]}
        },
        "required": ["path"]
    }
}
```

#### Tool 2: get_vulnerabilities
```python
{
    "name": "get_vulnerabilities",
    "description": "Get list of detected vulnerabilities",
    "input_schema": {
        "type": "object",
        "properties": {
            "filter": {"type": "string", "enum": ["all", "critical", "high", "medium", "low"]},
            "limit": {"type": "integer", "default": 50}
        }
    }
}
```

#### Tool 3: fix_vulnerability
```python
{
    "name": "fix_vulnerability",
    "description": "Apply automatic fix to vulnerability",
    "input_schema": {
        "type": "object",
        "properties": {
            "file": {"type": "string"},
            "line": {"type": "integer"},
            "vuln_type": {"type": "string"}
        },
        "required": ["file", "line", "vuln_type"]
    }
}
```

#### Tool 4: create_github_pr
```python
{
    "name": "create_github_pr",
    "description": "Create pull request with fixes",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "branch": {"type": "string"}
        },
        "required": ["title"]
    }
}
```

#### Tool 5: create_jira_issue
```python
{
    "name": "create_jira_issue",
    "description": "Create Jira ticket for vulnerability",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "description": {"type": "string"},
            "priority": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]}
        },
        "required": ["summary"]
    }
}
```

---

### 3. Resources Definition (`mcp/mcp_resources.py`)

**Resources to Implement:**

#### Resource 1: codebase://overview
```
Returns project structure and statistics
{
    "project": "Vulnerability Orchestrator",
    "version": "1.0.0",
    "skills": ["CodeAnalysis", "GitHub", "Jira", "Fixer", "PRManagement"],
    "test_coverage": "46%",
    "total_files": N
}
```

#### Resource 2: codebase://skills
```
Lists all available skills with descriptions
{
    "skills": [
        {"name": "CodeAnalysisSkill", "methods": [...]},
        {"name": "GitHubSkill", "methods": [...]},
        ...
    ]
}
```

#### Resource 3: codebase://vulnerabilities
```
Current vulnerability status
{
    "total_found": N,
    "critical": N,
    "high": N,
    "medium": N,
    "low": N
}
```

#### Resource 4: codebase://config
```
Configuration requirements
{
    "required_env_vars": [...],
    "setup_instructions": "...",
    "api_keys_needed": [...]
}
```

---

## 📊 Tool → Orchestrator Mapping

| MCP Tool | Calls | Returns |
|----------|-------|---------|
| analyze_code | CodeAnalysisSkill.scan_directory() | vulnerabilities list |
| fix_vulnerability | VulnerabilityFixerSkill.fix() | fix result |
| create_github_pr | GitHubSkill.create_pull_request() | PR URL |
| create_jira_issue | JiraSkill.create_issue() | issue key |
| get_workflow_status | Orchestrator.get_status() | workflow status |

---

## 🔄 Execution Flow

```
Claude Request
    ↓
MCP Server receives request
    ↓
Validate input schema
    ↓
Route to tool handler
    ↓
Tool handler calls Orchestrator
    ↓
Orchestrator calls appropriate Skill
    ↓
Skill executes (GitHub API, Jira API, file I/O)
    ↓
Result returned to handler
    ↓
Format as MCP response
    ↓
Send to Claude
```

---

## 🚀 Implementation Priority

1. **Phase 1 (High)** - Core Server
   - MCP server setup
   - Tool registration
   - Basic handlers

2. **Phase 2 (High)** - Critical Tools
   - analyze_code
   - get_vulnerabilities
   - fix_vulnerability

3. **Phase 3 (Medium)** - Integration Tools
   - create_github_pr
   - create_jira_issue
   - link_pr_to_issue

4. **Phase 4 (Low)** - Resources
   - Codebase overview
   - Skills catalog
   - Status endpoints

---

## 📝 Configuration

**MCP Server Config** (in setup.py):
```python
entry_points={
    'console_scripts': [
        'vulnerability-orchestrator=main:main',
        'mcp-server=mcp.mcp_server:run_server',  # NEW
    ],
}
```

---

## 🔐 Security

**Input Validation:**
- Validate file paths (no traversal)
- Validate vulnerability types
- Validate branch names
- Rate limit tool calls

**Error Handling:**
- Catch all exceptions
- Log security events
- Return safe error messages

---

## 📚 Documentation

**What to Document:**
- Tool usage examples
- Resource descriptions
- Error codes
- Rate limits
- Security policies

---

## ✅ Testing Strategy

1. Unit test each tool
2. Integration test with orchestrator
3. Test with Claude desktop/API
4. Security testing (input validation)
5. Load testing (concurrent calls)

---

## 🎯 Success Criteria

✅ All tools callable from Claude
✅ Resources accessible
✅ Full error handling
✅ Security validated
✅ Documented
✅ Unit tests passing
✅ Integration tests passing

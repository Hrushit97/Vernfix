# MCP Implementation - Detailed Blueprint

> **Status (2026-10-19):** Implemented in `mcp_server/`. ✅ = done, ⚠️ = partly done, ❌ = not done. Changes from this plan are noted under each section.

## 🎯 Complete Implementation Plan

---

## 📁 Directory Structure

```
paymentpodAPI/
├── mcp_server/                  # MCP server (named mcp_server so it does not clash with the mcp package)
│   ├── __init__.py
│   ├── server.py                # Server, tool and resource registration, stdio entry point
│   ├── tool_handlers.py         # Jira, GitHub and Sonar tool logic
│   ├── code_handlers.py         # analyze_code, fix_vulnerability and status tools
│   ├── resource_handlers.py     # Resource data (no secret values)
│   ├── MCP_JIRA.md
│   ├── MCP_GITHUB.md
│   └── MCP_SONAR.md
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

### 1. MCP Server (`mcp_server/server.py`) ✅

**Responsibilities:**
- Initialize MCP server
- Register tools
- Register resources
- Handle protocol messages
- Manage the Jira, GitHub, Sonar and code services (created on first use from environment variables)

> **Change:** the server does not use `VulnerabilityOrchestrator`. Tool calls go straight to the skills.

**Key Functions:**
```python
def create_server(services=None) -> MCPServer:
    """Create the MCP server and register tools and resources"""
    
# Tools and resources are registered inside create_server() with @server.tool() and @server.resource()
    

    
def run_server() -> None:
    """Entry point: load .env, then run over stdio"""
```

---

### 2. Tools (`mcp_server/tool_handlers.py`, `mcp_server/code_handlers.py`) ✅

**Status:** The five planned tools are implemented, with the changes noted under each. The server exposes 16 tools in total (see the table at the end of this section). The input schemas are generated from the Python type hints by the `mcp` package.

#### Tool 1: analyze_code ✅

- **Args:** `path` (default `"."`), `file_type` (`python`, `javascript`, `all`)
- **Rule:** `path` must be a directory inside the repo root
- **Change:** `path` is optional, not required. The result is kept for `get_vulnerabilities`.

#### Tool 2: get_vulnerabilities ✅

- **Args:** `filter` (`all`, `critical`, `high`, `medium`, `low`), `limit` (1 to 500, default 50)
- **Rule:** reads the last `analyze_code` result; returns an error if there is none

#### Tool 3: fix_vulnerability ✅

- **Args:** `file`, `line`, `vuln_type`, `confirm` (must be `true`)
- **Rule:** `vuln_type` must be one of the six types the fixer supports. `file` must be an existing `.py`, `.js` or `.jsx` file inside the repo root.
- **Calls:** `VulnerabilityFixerSkill.fix_vulnerability(file, {type, line})`
- **Change:** `confirm` was added. The plan did not have it.

#### Tool 4: create_github_pr ✅

- **Args:** `repo_name`, `title` (1 to 256 characters), `head_branch`, `body`, `base_branch` (default `main`), `owner`, `confirm` (must be `true`)
- **Calls:** `GitHubSkill.create_pull_request`
- **Change:** the plan's `description` is now `body`, and `branch` is now `head_branch`. `repo_name` is required and `confirm` was added.

#### Tool 5: create_jira_issue ✅

- **Args:** `project_key`, `summary` (1 to 255 characters), `description`, `priority` (`Lowest`, `Low`, `Medium`, `High`, `Highest`, `Critical`; default `High`), `issue_type` (default `Bug`), `labels`, `confirm` (must be `true`)
- **Calls:** `JiraSkill.create_issue`
- **Change:** `project_key` is required. The priority list is longer than the plan's four values.

#### All Tools Exposed by the Server ✅

| Group | Tool | Write? | Skill method |
|-------|------|--------|--------------|
| Jira | `create_jira_issue` | Yes (`confirm`) | `JiraSkill.create_issue` |
| Jira | `search_jira_issues` | No | `JiraSkill.search_issues` |
| Jira | `find_duplicate_jira_issues` | No | `JiraSkill.find_duplicate_issues` |
| Jira | `get_existing_security_issues` | No | `JiraSkill.get_issues_by_labels` |
| Jira | `get_jira_issue` | No | `JiraSkill.get_issue` |
| Jira | `link_pr_to_issue` | Yes (`confirm`) | `JiraSkill.link_issue_to_pr` |
| GitHub | `get_github_repository` | No | `GitHubSkill.get_repository` |
| GitHub | `create_github_pr` | Yes (`confirm`) | `GitHubSkill.create_pull_request` |
| Sonar | `get_sonar_vulnerabilities` | No | `SonarSkill.get_vulnerabilities` |
| Sonar | `get_sonar_hotspots` | No | `SonarSkill.get_security_hotspots` |
| Sonar | `get_sonar_quality_gate` | No | `SonarSkill.get_quality_gate_status` |
| Sonar | `get_sonar_findings` | No | `SonarSkill.get_all_findings` |
| Code | `analyze_code` | No | `CodeAnalysisSkill.scan_directory` |
| Code | `get_vulnerabilities` | No | none (reads the saved result) |
| Code | `fix_vulnerability` | Yes (`confirm`) | `VulnerabilityFixerSkill.fix_vulnerability` |
| Code | `get_workflow_status` | No | none (reads session state) |

The Sonar tools are not in the original plan. Their reference is `mcp_server/MCP_SONAR.md`.

---

### 3. Resources (`mcp_server/server.py`, `mcp_server/resource_handlers.py`) ✅

**Status:** The plan had 4 resources. The server has 5. None of them returns secret values.

#### Resource 1: codebase://overview ✅
Returns the project name, version, skill names, tool count, and the number of `.py`, `.js` and `.jsx` files under the repo root.
**Change:** there is no test coverage figure. The plan's `"46%"` was not calculated.

#### Resource 2: codebase://skills ✅
Lists each skill and its method names, including `SonarSkill`. `PRManagementSkill` is listed as text ("local git: branch, commit, push").

#### Resource 3: codebase://vulnerabilities ✅
Counts from the last `analyze_code` run: `analyzed`, `total_found`, `critical`, `high`, `medium`, `low`.

#### Resource 4: codebase://config ✅
Lists the required and optional environment variable names, with `true` or `false` for whether each is set.
**Change:** there is no `api_keys_needed` list. `setup_instructions` is a single sentence. Values are never returned.

#### Resource 5: codebase://tools ✅ (added)
Lists the tool names by group, and the four tools that need `confirm=true`.

---

## 📊 Tool → Orchestrator Mapping

| Tool | Calls | Returns |
|------|-------|---------|
| analyze_code | CodeAnalysisSkill.scan_directory() | counts and vulnerability list |
| fix_vulnerability | VulnerabilityFixerSkill.fix_vulnerability() | fix result |
| create_github_pr | GitHubSkill.create_pull_request() | skill result (includes PR URL) |
| create_jira_issue | JiraSkill.create_issue() | skill result (includes issue key) |
| get_workflow_status | none (reads session state in `services`) | last analysis and fix log |

**Change:** `Orchestrator.get_status()` does not exist. The server reads its session state directly and does not use `VulnerabilityOrchestrator`.

---

## 🔄 Execution Flow

```
Claude Request
    ↓
MCP Server receives request
    ↓
Validate input (the MCP SDK checks types; handlers check values)
    ↓
Route to tool handler
    ↓
Tool handler calls the skill directly (the orchestrator is not used)
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

1. ✅ **Phase 1 (High)** - Core Server
   - MCP server setup
   - Tool registration
   - Basic handlers

2. ✅ **Phase 2 (High)** - Critical Tools
   - analyze_code
   - get_vulnerabilities
   - fix_vulnerability

3. ✅ **Phase 3 (Medium)** - Integration Tools
   - create_github_pr
   - create_jira_issue
   - link_pr_to_issue

4. ✅ **Phase 4 (Low)** - Resources
   - Codebase overview
   - Skills catalog
   - Status endpoints (`codebase://vulnerabilities`, `get_workflow_status`)

**Added beyond the plan:** the four Sonar tools (see `mcp_server/MCP_SONAR.md`).

---

## 📝 Configuration

**MCP Server Config** (in setup.py): ✅ Implemented. `mcp>=2.3.0,<3` is in `install_requires`, and `python_requires` is `>=3.10`.
```python
entry_points={
    'console_scripts': [
        'vulnerability-orchestrator=main:main',
        'mcp-server=mcp_server.server:run_server',  # Implemented
    ],
}
```

---

## 🔐 Security

**Input Validation:**
- ✅ Validate file paths (no traversal): paths must resolve inside the repo root (`REPO_PATH`, or the working directory). Null bytes are rejected.
- ✅ Validate vulnerability types: `fix_vulnerability` accepts only the six types the fixer supports
- ✅ Validate branch names and Jira, GitHub and Sonar identifiers with regex checks
- ❌ Rate limit tool calls: not implemented

**Error Handling:**
- ✅ Catch all exceptions: the `_safe` wrapper returns a generic error
- ⚠️ Log security events: errors are logged to stderr. There is no separate security event log.
- ✅ Return safe error messages
- ✅ Write tools need `confirm=true` (added; not in the original plan)

---

## 📚 Documentation

**What to Document:** ⚠️ Mostly done. The three `.md` files in `mcp_server/` and the MCP section of `ARCHITECTURE.md` cover most of these.
- ✅ Tool usage examples
- ✅ Resource descriptions
- ⚠️ Error codes: there are no error codes. Errors are returned as `{"success": false, "error": "..."}`.
- ❌ Rate limits: not applicable, since rate limiting is not implemented
- ✅ Security policies (input checks and `confirm=true` gates)

---

## ✅ Testing Strategy

1. ⚠️ Unit test each tool: partly done. `tests/test_mcp_server.py` has 12 tests for write gates, input checks, path traversal, Sonar, code tools and server registration. Not every tool has its own test.
2. ❌ Integration test with orchestrator: not done. The MCP server does not call the orchestrator.
3. ❌ Test with Claude Desktop/API: not done. No MCP client has been run against the server.
4. ⚠️ Security testing (input validation): covered by the unit tests. There is no separate security test pass.
5. ❌ Load testing (concurrent calls): not done

---

## 🎯 Success Criteria

⚠️ All tools registered; not yet called from Claude
⚠️ Resources registered; not yet read from an MCP client
✅ Full error handling
⚠️ Security validated (unit tests only; rate limiting missing)
✅ Documented
✅ Unit tests passing (12 MCP tests; 31 in the full suite)
❌ Integration tests passing (none written)

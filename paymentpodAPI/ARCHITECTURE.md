# Vulnerability Orchestrator - Architecture Documentation

## System Overview

The Vulnerability Orchestrator is a modular, skill-based security automation system designed to detect, fix, and track security vulnerabilities in the Payment Pod API.

Key properties:
- **Hybrid detection**: built-in regex analysis plus optional SonarQube/SonarCloud findings.
- **Jira de-duplication**: existing Jira tickets are reused instead of creating duplicates.
- **Human-in-the-loop**: each fix needs human approval before it is applied (on by default).
- **MCP server**: the Jira and GitHub skills are also exposed as tools to AI clients (see "MCP Server" below).

## Component Architecture

### 1. Skills Layer
Each skill is an independent, reusable component with a specific responsibility:

```
┌──────────────────────────────────────────────────────────────┐
│               Vulnerability Orchestrator (Main)               │
└───────┬────────┬─────────┬─────────┬─────────┬───────────────┘
        │        │         │         │         │         │ (optional)
        ▼        ▼         ▼         ▼         ▼         ▼
    ┌───────┐┌───────┐┌─────────┐┌───────┐┌────────┐┌───────┐
    │GitHub ││ Jira  ││Analysis ││Fixer  ││PR Mgmt ││ Sonar │
    │Skill  ││ Skill ││Skill    ││Skill  ││Skill   ││ Skill │
    └───────┘└───────┘└─────────┘└───────┘└────────┘└───────┘
```

| Skill | File | Responsibility |
|-------|------|----------------|
| GitHubSkill | `skills/github_skill.py` | Repo info, pull requests, comments |
| JiraSkill | `skills/jira_skill.py` | Issues, duplicate search, linking |
| CodeAnalysisSkill | `skills/code_analysis_skill.py` | Regex-based scan of `.py` / `.js` / `.jsx` |
| VulnerabilityFixerSkill | `skills/vulnerability_fixer_skill.py` | Automatic patches for the 6 built-in types |
| PRManagementSkill | `skills/pr_management_skill.py` | Local git: branch, commit, push |
| SonarSkill (optional) | `skills/sonar_skill.py` | Sonar vulnerabilities, security hotspots, quality gate via the Sonar Web API |

### 2. Workflow Pipeline

The orchestrator runs 9 steps (`execute_workflow`):

| Step | Action | Skill |
|------|--------|-------|
| 1 | Get repository info | GitHub |
| 2 | Analyze code; merge Sonar findings if enabled | Analysis, Sonar |
| 3 | Create Jira issues (reuse existing ones) | Jira |
| 4 | Create feature branch | PR Mgmt |
| 5 | Fix vulnerabilities (**human approval**) | Fixer |
| 6 | Commit changes | PR Mgmt |
| 7 | Push branch | PR Mgmt |
| 8 | Create pull request | GitHub |
| 9 | Link PR to Jira issues | Jira |

**Sonar merge (Step 2)**: Sonar findings are added to the regex findings. A Sonar finding at the same file and line as a regex finding is skipped. If Sonar is unreachable, the workflow logs a warning and continues with regex findings only.

**Human approval (Step 5)**: controlled by `require_approval` (default `True`) and an optional `approval_callback(vuln, idx, total)`.
- Answers: `yes`, `no`, `all` (approve the rest), `quit` (skip the rest).
- Default is a console prompt. With no keyboard input (e.g. CI) the answer is `no`, so nothing is changed.
- Skipped fixes are stored in `workflow_status['skipped_fixes']`; only approved fixes are committed.
- Set `require_approval=False` for fully automatic runs.

### 3. Data Flow

```
Repo Code → Analysis Skill ─┐
                            ├→ Merged Vulnerabilities
Sonar Server → Sonar Skill ─┘            │
                                         ├→ Jira Skill → Issues (duplicates reused)
                                         ▼
                              Human Approval Gate
                                         ▼
                         Fixer Skill → Fixed Code
                                         ▼
                         PR Mgmt Skill → Commit + Push
                                         ▼
                         GitHub Skill → PR → Link to Jira
```

## Security Patterns Detected

1. **SQL Injection**: String concatenation in queries
2. **Hardcoded Credentials**: Plaintext secrets in code
3. **Insecure Deserialization**: pickle.load, yaml.load
4. **Code Injection**: eval() usage
5. **XSS Vulnerabilities**: innerHTML assignments

## Fix Strategies

1. **SQL**: Convert to parameterized queries
2. **Secrets**: Move to environment variables
3. **Serialization**: Use safe alternatives (json, yaml.safe_load)
4. **Injection**: Use safer evaluation methods
5. **XSS**: Replace innerHTML with textContent

Findings from Sonar are reported as `Sonar <rule>`. The fixer does not know these types, so the automatic fix fails and they appear in `failed_fixes`. They still get a Jira ticket and appear in the approval prompt; the patch must be written by a person.

## Integration Points

### GitHub
- Repository access
- Branch management
- PR creation and management
- Code comments

### Jira
- Issue tracking
- Status transitions
- Linking
- Priority management
- Duplicate detection (search by file + vulnerability type)

### SonarQube / SonarCloud (optional)
- Open vulnerability issues (`/api/issues/search`, paged 500 at a time)
- Security hotspots to review (`/api/hotspots/search`)
- Quality gate status (`/api/qualitygates/project_status`); available but not yet called by the workflow
- Branch and pull-request filters
- Token authentication; the Sonar MCP server exposes the same data, but the orchestrator calls the Web API directly

## MCP Server (Jira, GitHub and Sonar)

`mcp_server/` lets an MCP client (for example Claude Desktop) call the Jira, GitHub and Sonar skills as tools. Per-system details: `mcp_server/MCP_JIRA.md`, `mcp_server/MCP_GITHUB.md`, `mcp_server/MCP_SONAR.md`. It uses `mcp` 2.x (`mcp.server.mcpserver.MCPServer`; the old `FastMCP` import no longer exists). The folder is named `mcp_server` so it does not shadow the installed `mcp` package.

| File | Role |
|------|------|
| `server.py` | Creates the server, registers tools and resources, builds the skills from environment variables on first use, runs over stdio |
| `tool_handlers.py` | Plain functions that validate input and call the skills; testable without the MCP SDK |
| `resource_handlers.py` | Data for the two resources |

**Tools**
- Jira: `create_jira_issue`, `search_jira_issues`, `find_duplicate_jira_issues`, `get_existing_security_issues`, `get_jira_issue`, `link_pr_to_issue`
- GitHub: `get_github_repository`, `create_github_pr`
- Sonar (all read-only, optional `branch` / `pull_request`): `get_sonar_vulnerabilities`, `get_sonar_hotspots`, `get_sonar_quality_gate`, `get_sonar_findings`

**Resources**: `codebase://config` (which environment variables are set, never their values) and `codebase://tools` (tool list).

**Safety rules**
- Write tools (`create_jira_issue`, `link_pr_to_issue`, `create_github_pr`) refuse to run unless `confirm=true`, so a human must approve first.
- Project keys, issue keys, repository names and branch names are checked against patterns; PR links must start with `https://github.com/`.
- Errors returned to the client are generic; details go to the server log (stderr).

Run with `python -m mcp_server.server`. It uses the same Jira and GitHub environment variables as the orchestrator. The MCP server does not yet expose analysis, fixing or workflow status.

## Extension Points

### Adding New Vulnerability Types
1. Add detection pattern in `CodeAnalysisSkill`
2. Implement fix logic in `VulnerabilityFixerSkill`
3. Update `_create_vuln()` and fix methods

### Adding New Languages
1. Create `analyze_<lang>()` method in `CodeAnalysisSkill`
2. Add corresponding fix methods in `VulnerabilityFixerSkill`

## Configuration

Environment-based configuration via `.env` file (read in `main.py`):
- Integration credentials (`GITHUB_TOKEN`, `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`)
- Repository paths (`REPO_PATH`, `ANALYZE_PATH`)
- Optional Sonar: `SONAR_URL`, `SONAR_TOKEN`, `SONAR_PROJECT_KEY` (all three required to enable it)
- Workflow flags passed to `execute_workflow`: `skip_jira`, `skip_pr`, `require_approval`, `approval_callback`

Never commit tokens; keep them in environment variables or a secret store.

## Error Handling

- Graceful degradation on API failures
- Comprehensive logging
- Failed fixes are recorded and skipped; the orchestrator does not roll back file changes
- Detailed error reporting

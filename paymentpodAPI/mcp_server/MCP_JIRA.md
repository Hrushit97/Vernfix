# MCP Tools: Jira

Implemented in `mcp_server/tool_handlers.py`, backed by `skills/jira_skill.py`.

## Setup
Set these environment variables (never commit them): `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`.

## Tools

| Tool | Writes? | Arguments | Result |
|------|---------|-----------|--------|
| `create_jira_issue` | **Yes, needs `confirm=true`** | `project_key`, `summary` (1-255 chars), `description`, `priority` (Lowest, Low, Medium, High, Highest, Critical), `issue_type` (default Bug), `labels`, `confirm` | `issue_key`, `issue_url` |
| `search_jira_issues` | No | `project_key`, `keyword`, `status` | matching issues |
| `find_duplicate_jira_issues` | No | `project_key`, `file_path`, `vuln_type` | existing issues for that file and type |
| `get_existing_security_issues` | No | `project_key`, `labels` (default `security`) | issues with those labels |
| `get_jira_issue` | No | `issue_key`, e.g. `PAYMENT-123` | issue details |
| `link_pr_to_issue` | **Yes, needs `confirm=true`** | `issue_key`, `pr_url` (must start with `https://github.com/`), `confirm` | adds the PR link as a comment |

## Input checks
- Project key: capital letters, digits, underscore (e.g. `PAYMENT`).
- Issue key: `PROJECT-number`.
- A write call without `confirm=true` returns an error and does nothing.

## Recommended order
1. `find_duplicate_jira_issues` (or `search_jira_issues`) to avoid a duplicate ticket.
2. Ask a human to approve.
3. `create_jira_issue` with `confirm=true`.
4. After the PR exists, `link_pr_to_issue` with `confirm=true`.

## Errors
Failures return `{"success": false, "error": "..."}`. Unexpected errors give a generic message; details are in the server log (stderr).

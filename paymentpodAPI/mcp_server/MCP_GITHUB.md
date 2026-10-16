# MCP Tools: GitHub

Implemented in `mcp_server/tool_handlers.py`, backed by `skills/github_skill.py`.

## Setup
Set `GITHUB_TOKEN` in your environment (never commit it). Optional: `GITHUB_OWNER`, `GITHUB_REPO`.

## Tools

| Tool | Writes? | Arguments | Result |
|------|---------|-----------|--------|
| `get_github_repository` | No | `repo_name`, `owner` (optional, defaults to the token's user) | repository details |
| `create_github_pr` | **Yes, needs `confirm=true`** | `repo_name`, `title` (1-256 chars), `head_branch`, `body`, `base_branch` (default `main`), `owner`, `confirm` | `pr_url`, `pr_number` |

## Input checks
- Repository and owner names: letters, digits, `.`, `_`, `-`.
- Branch names: no leading `/`, no `..`, no `//`, no trailing `/` or `.`.
- A write call without `confirm=true` returns an error and does nothing.

## Notes
- `create_github_pr` only opens the PR. The branch must already be pushed; the MCP server does not commit or push.
- Pass the returned `pr_url` to `link_pr_to_issue` (see `MCP_JIRA.md`).

## Errors
Failures return `{"success": false, "error": "..."}`. Unexpected errors give a generic message; details are in the server log (stderr).

# MCP Tools: SonarQube / SonarCloud

Implemented in `mcp_server/tool_handlers.py`, backed by `skills/sonar_skill.py` (Sonar Web API). All four tools are **read-only**. They read results; they do not start a scan. Scans are run by the Sonar scanner, usually in CI.

## Setup
Set these environment variables (never commit the token):
- `SONAR_URL`: `https://sonarcloud.io` or your SonarQube URL
- `SONAR_TOKEN`: a Sonar user token
- `SONAR_PROJECT_KEY`
- `REPO_PATH` (optional): turns Sonar file names into local paths

## Tools
All take optional `branch` and `pull_request`.

| Tool | Result |
|------|--------|
| `get_sonar_vulnerabilities` | open `VULNERABILITY` issues |
| `get_sonar_hotspots` | security hotspots still `TO_REVIEW` |
| `get_sonar_quality_gate` | `status` (`OK` or `ERROR`) and `passed` |
| `get_sonar_findings` | vulnerabilities and hotspots together, in the orchestrator's format |

Each finding has `file`, `line`, `type` (`Sonar <rule>`), `severity`, `code` (the Sonar message), `source`, `sonar_key` and `sonar_kind` (`issue` or `hotspot`).

Severity mapping: BLOCKER and CRITICAL become CRITICAL, MAJOR becomes HIGH, MINOR becomes MEDIUM, INFO becomes LOW. Hotspot probability HIGH, MEDIUM and LOW map to the same names.

## Input checks
`branch` and `pull_request` accept only letters, digits, `.`, `_`, `/`, `-`.

## Typical use with the other tools
1. `get_sonar_findings` to list everything.
2. For each finding, `find_duplicate_jira_issues` (see `MCP_JIRA.md`) before creating a ticket.
3. After a fix PR is opened, `get_sonar_quality_gate` with `pull_request` to see whether it passes.

## Limits
- Sonar findings have no automatic fix; a person writes the patch.
- Results are capped at 10,000 items (Sonar's search limit).
- Errors from Sonar (bad token, wrong URL) return a generic error; details are in the server log (stderr).

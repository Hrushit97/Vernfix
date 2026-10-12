# Vulnerability Orchestrator - Architecture Documentation

## System Overview

The Vulnerability Orchestrator is a modular, skill-based security automation system designed to detect, fix, and track security vulnerabilities in the Payment Pod API.

## Component Architecture

### 1. Skills Layer
Each skill is an independent, reusable component with a specific responsibility:

```
┌─────────────────────────────────────────────────────┐
│          Vulnerability Orchestrator (Main)           │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────────┬──────────────┬──────────────┐
        │          │              │              │              │
        ▼          ▼              ▼              ▼              ▼
    ┌────────┐ ┌────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ GitHub │ │ Jira   │   │ Analysis│   │ Fixer   │   │ PR Mgmt │
    │ Skill  │ │ Skill  │   │ Skill   │   │ Skill   │   │ Skill   │
    └────────┘ └────────┘   └─────────┘   └─────────┘   └─────────┘
```

### 2. Workflow Pipeline

**Stage 1: Analysis**
- Repository information retrieval
- Code scanning
- Vulnerability identification
- Severity classification

**Stage 2: Tracking**
- Jira issue creation
- Priority assignment
- Labeling and categorization

**Stage 3: Remediation**
- Feature branch creation
- Automatic code fixes
- Change staging

**Stage 4: Integration**
- Commit and push
- PR creation
- Jira linking

### 3. Data Flow

```
Repo Code → Analysis Skill → Vulnerabilities → Fixer Skill → Fixed Code
                ↓
          Jira Skill → Issues
                ↓
          PR Skill → GitHub PR
                ↓
          GitHub Skill → Link PR to Jira
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

## Extension Points

### Adding New Vulnerability Types
1. Add detection pattern in `CodeAnalysisSkill`
2. Implement fix logic in `VulnerabilityFixerSkill`
3. Update `_create_vuln()` and fix methods

### Adding New Languages
1. Create `analyze_<lang>()` method in `CodeAnalysisSkill`
2. Add corresponding fix methods in `VulnerabilityFixerSkill`

## Configuration

Environment-based configuration via `.env` file:
- Integration credentials
- Repository paths
- Feature flags
- Logging level

## Error Handling

- Graceful degradation on API failures
- Comprehensive logging
- Transaction rollback on critical errors
- Detailed error reporting

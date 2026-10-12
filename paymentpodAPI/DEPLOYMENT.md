# Deployment Guide

## Development Setup

### Local Development

1. **Clone repository**
```bash
git clone https://github.com/your-org/paymentpodAPI.git
cd paymentpodAPI
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run tests**
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## GitHub/Jira Setup

### Generate GitHub Personal Access Token

1. Go to Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`
4. Copy token to `.env`

### Generate Jira API Token

1. Go to Atlassian account settings
2. Security → API tokens
3. Create new API token
4. Copy token to `.env`

## Running in Production

### Option 1: Direct Execution

```bash
python main.py
```

### Option 2: Scheduled via Cron (Linux/Mac)

```bash
# Add to crontab
0 2 * * * cd /path/to/paymentpodAPI && python main.py
```

### Option 3: Windows Task Scheduler

1. Create task with script:
```batch
@echo off
cd C:\path\to\paymentpodAPI
python main.py
```

2. Schedule to run at desired time

### Option 4: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t vulnerability-orchestrator .
docker run --env-file .env vulnerability-orchestrator
```

## Monitoring & Logging

### Log Output

Logs are printed to console with timestamps.

To save to file:
```bash
python main.py >> logs/workflow.log 2>&1
```

### Error Notifications

Modify `main.py` to send alerts on failure:
```python
if not success:
    send_email("security-team@company.com", "Workflow failed")
```

## Security Best Practices

1. **Never commit credentials** - Use `.env` file (git-ignored)
2. **Rotate tokens regularly** - Monthly recommended
3. **Use minimum permissions** - Only required scopes
4. **Audit logs** - Review successful/failed runs
5. **Test in staging** - Before production deployment

## Troubleshooting

### Issue: "Failed to connect to GitHub"
- Check token is valid
- Verify internet connectivity
- Check repository access

### Issue: "Jira issue creation failed"
- Verify project key is correct
- Check Jira credentials
- Verify user has permission

### Issue: "Git commit failed"
- Check local repository state
- Verify git is configured
- Check file permissions

## Backup & Recovery

### Backup Configuration

```bash
cp .env .env.backup
cp config/config.example.json config/config.backup.json
```

### Recovery

```bash
cp .env.backup .env
```

## Performance Tuning

For large repositories:
- Exclude large files in analysis
- Run analysis in parallel batches
- Increase timeout for API calls

## Support

For issues:
1. Check logs for error messages
2. Review ARCHITECTURE.md
3. Check SKILLS_REFERENCE.md
4. Submit issue with logs attached

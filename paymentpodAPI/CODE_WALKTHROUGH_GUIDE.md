# Code Walk-Through Guide: Line-by-Line Explanation

## 🎯 Complete Flow Explanation with Line Numbers

### **STEP 1: User Calls the Method (main.py)**

```python
# Line 1: Import orchestrator
from orchestrator.vulnerability_orchestrator import VulnerabilityOrchestrator

# Line 5: Configuration
config = {
    'jira_url': 'https://domain.atlassian.net',
    'jira_username': 'email@example.com',
    'jira_api_token': 'YOUR_TOKEN',
    # ... other config
}

# Line 15: Create instance
orchestrator = VulnerabilityOrchestrator(config)

# Line 20: Call the method (THIS IS WHERE OUR FLOW STARTS)
result = orchestrator.get_existing_security_issues('PAYMENT')

# Line 25: Handle response
if result['success']:
    print(f"Found {result['count']} issues")
    for issue in result['issues']:
        print(f"{issue['key']}: {issue['summary']}")
```

**What Happens Here:**
- Line 20: Calls orchestrator's method
- FLOW → Goes to Step 2 in orchestrator/vulnerability_orchestrator.py

---

### **STEP 2: Orchestrator Method (orchestrator/vulnerability_orchestrator.py)**

```python
# Lines 494-530
def get_existing_security_issues(self, project_key: str) -> Dict:
    """Get all existing security-related Jira issues"""
    
    try:
        # Line 500: Log that we're starting
        logger.info(f"Fetching existing security issues for project {project_key}")
        # Output: "2026-10-15 12:50:50 INFO Fetching existing security issues for PAYMENT"
        
        # Line 505: Call JiraSkill method
        result = self.jira_skill.get_issues_by_labels(
            project_key,
            ['security', 'automated-fix']
        )
        # FLOW → Goes to Step 3 in skills/jira_skill.py
        # Returns Dict: {'success': True, 'count': N, 'issues': [...]}
        
        # Line 510: Check if successful
        if result.get('success'):
            # Line 512: Log success
            logger.info(f"Found {result['count']} existing security issues")
            # Output: "Found 2 existing security issues"
            
            # Line 514: Return to user
            return result  ← GOES BACK TO STEP 1
            
        else:
            # Line 517: Log error
            logger.warning(f"Failed to fetch: {result.get('error')}")
            
            # Line 520: Return error to user
            return {
                'success': False,
                'error': result.get('error'),
                'issues': []
            }
    
    except Exception as e:
        # Line 526: Catch any exceptions
        logger.error(f"Error getting issues: {e}")
        
        # Line 528: Return error
        return {
            'success': False,
            'error': str(e),
            'issues': []
        }
```

**What Happens Here:**
- Line 505-507: Calls JiraSkill method with:
  - `project_key` = 'PAYMENT'
  - `labels` = ['security', 'automated-fix']
- FLOW → Goes to Step 3

---

### **STEP 3: JiraSkill Method (skills/jira_skill.py)**

```python
# Lines 173-200
def get_issues_by_labels(self, project_key: str, labels: List[str]) -> Dict:
    """Get issues by labels"""
    
    try:
        # Line 178: Build JQL query string
        label_query = " OR ".join([f'labels in ({label})' for label in labels])
        # Result: "labels in (security) OR labels in (automated-fix)"
        
        # Line 179: Build full JQL
        jql = f"project = {project_key} AND ({label_query})"
        # Result: "project = PAYMENT AND (labels in (security) OR labels in (automated-fix))"
        
        # Line 180: Log the query
        logger.info(f"Searching with JQL: {jql}")
        
        # Line 183: Call Jira library (THIS MAKES HTTP REQUEST)
        issues = self.jira.search_issues(jql, maxResults=100)
        # FLOW → Goes to Step 4 (Jira Library)
        # Returns: List of Jira Issue objects
        
        # Line 185: Loop through results
        issues_list = []
        for issue in issues:
            # Line 187-191: Extract fields from each issue
            issues_list.append({
                'key': issue.key,           # e.g., 'PAYMENT-123'
                'summary': issue.fields.summary,  # e.g., '[CRITICAL] Fix SQL...'
                'status': str(issue.fields.status),    # e.g., 'Open'
                'labels': issue.fields.labels,  # e.g., ['security', 'automated-fix']
            })
        
        # Line 194: Return success response to Orchestrator
        return {
            'success': True,
            'count': len(issues_list),  # e.g., 2
            'issues': issues_list       # e.g., [{'key': 'PAYMENT-123', ...}, ...]
        }
        
    except Exception as e:
        # Line 199: Catch any exceptions
        logger.error(f"Failed to get issues: {e}")
        
        # Line 200: Return error
        return {'success': False, 'error': str(e), 'issues': []}
```

**What Happens Here:**
- Line 178-179: Builds JQL query string
- Line 183: Makes HTTP request to Jira API
- FLOW → Goes to Step 4

---

### **STEP 4: Jira Library HTTP Call**

```python
# Inside jira library (self.jira.search_issues):

# Step 4a: Build HTTP Request
Request Type: POST
URL: https://domain.atlassian.net/rest/api/2/search
Headers:
  - Authorization: Basic base64(email@example.com:api_token)
  - Content-Type: application/json

Body (JSON):
{
  "jql": "project = PAYMENT AND (labels in (security) OR labels in (automated-fix))",
  "maxResults": 100
}

# Step 4b: Send to Jira API
Over HTTP/HTTPS

# Step 4c: Jira API Validates Credentials
Checks: Is this user authorized?

# Step 4d: Query Jira Database
Searches: Find all issues matching JQL

# Step 4e: Build Response
If found 2 issues:
{
  "issues": [
    {
      "key": "PAYMENT-123",
      "fields": {
        "summary": "[CRITICAL] Fix SQL Injection in app.py",
        "status": { "name": "Open" },
        "labels": ["security", "automated-fix"]
      }
    },
    {
      "key": "PAYMENT-124",
      "fields": {
        "summary": "[HIGH] Fix XSS Vulnerability in form.js",
        "status": { "name": "In Progress" },
        "labels": ["security", "automated-fix"]
      }
    }
  ]
}

# Step 4f: Send Response Back
Over HTTPS to Jira Library
```

---

### **STEP 5: Data Returns to JiraSkill**

```python
# Line 183 (in skills/jira_skill.py) gets the response:
issues = self.jira.search_issues(...)

# 'issues' is now a list of Jira Issue objects
# issues[0].key = 'PAYMENT-123'
# issues[0].fields.summary = '[CRITICAL] Fix SQL Injection in app.py'

# Lines 185-192: Convert to Python dict
issues_list = [
    {
        'key': 'PAYMENT-123',
        'summary': '[CRITICAL] Fix SQL Injection in app.py',
        'status': 'Open',
        'labels': ['security', 'automated-fix']
    },
    {
        'key': 'PAYMENT-124',
        'summary': '[HIGH] Fix XSS Vulnerability in form.js',
        'status': 'In Progress',
        'labels': ['security', 'automated-fix']
    }
]

# Line 194: Return to orchestrator
return {
    'success': True,
    'count': 2,
    'issues': issues_list
}
```

---

### **STEP 6: Data Returns to Orchestrator**

```python
# Line 510 (in orchestrator/vulnerability_orchestrator.py):
result = self.jira_skill.get_issues_by_labels(...)

# 'result' is now:
{
    'success': True,
    'count': 2,
    'issues': [
        {'key': 'PAYMENT-123', ...},
        {'key': 'PAYMENT-124', ...}
    ]
}

# Line 512: Check if success
if result.get('success'):  # True
    logger.info(f"Found {result['count']} existing security issues")
    # Output: "Found 2 existing security issues"

# Line 514: Return to user
return result
```

---

### **STEP 7: Data Returns to User Code**

```python
# Line 20 (in main.py):
result = orchestrator.get_existing_security_issues('PAYMENT')

# 'result' is now the dict:
{
    'success': True,
    'count': 2,
    'issues': [
        {
            'key': 'PAYMENT-123',
            'summary': '[CRITICAL] Fix SQL Injection in app.py',
            'status': 'Open',
            'labels': ['security', 'automated-fix']
        },
        {
            'key': 'PAYMENT-124',
            'summary': '[HIGH] Fix XSS Vulnerability in form.js',
            'status': 'In Progress',
            'labels': ['security', 'automated-fix']
        }
    ]
}

# Lines 22-26: Use the data
if result['success']:
    print(f"Found {result['count']} issues")  # Output: "Found 2 issues"
    for issue in result['issues']:
        print(f"{issue['key']}: {issue['summary']}")
        # Output: "PAYMENT-123: [CRITICAL] Fix SQL Injection in app.py"
        # Output: "PAYMENT-124: [HIGH] Fix XSS Vulnerability in form.js"
```

---

## 📊 Data Type Transformations

```
Input:
  project_key: str = 'PAYMENT'

↓ In Orchestrator:
  labels: List[str] = ['security', 'automated-fix']

↓ In JiraSkill:
  jql: str = "project = PAYMENT AND (labels in ...)"
  issues: List[JiraIssueObject]

↓ Processed in JiraSkill:
  issues_list: List[Dict[str, Any]]

↓ In Orchestrator:
  result: Dict[str, Any] = {'success': True, 'count': int, 'issues': List[Dict]}

↓ To User:
  result: Dict[str, Any]
```

---

## 🔍 Key Points

1. **Only ONE HTTP request** - Made at line 183 in jira_skill.py
2. **Authentication** - Automatic via Jira library with credentials from config
3. **JQL Query** - Built dynamically based on labels
4. **Data Conversion** - Jira objects → Python dicts → Back to user
5. **Error Handling** - Try-catch at each level
6. **Logging** - Tracked at orchestrator and skill levels
7. **Response Format** - Consistent dict structure throughout

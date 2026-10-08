# 🔒 Quick Security Checklist

## Before Production Deployment

- [ ] **H2 Console Disabled**
  - [ ] application-prod.yaml: `h2.console.enabled: false`
  
- [ ] **Authentication Added**
  - [ ] Spring Security dependency added
  - [ ] SecurityConfig class created
  - [ ] All endpoints protected
  
- [ ] **Input Validation**
  - [ ] @Valid annotation on @RequestBody
  - [ ] @NotNull on required fields
  - [ ] @DecimalMin on prices
  - [ ] @Min/@Max on quantities
  
- [ ] **Database Security**
  - [ ] ddl-auto set to 'validate'
  - [ ] DB credentials in environment variables
  - [ ] Strong password configured
  
- [ ] **HTTPS/SSL**
  - [ ] SSL certificate configured
  - [ ] server.ssl properties set
  - [ ] HTTP redirect to HTTPS enabled
  
- [ ] **Configuration Hardening**
  - [ ] SQL logging disabled (show-sql: false)
  - [ ] Debug mode disabled
  - [ ] Environment-specific configs (dev/prod)
  
- [ ] **API Security**
  - [ ] CORS configured
  - [ ] Rate limiting implemented
  - [ ] Global exception handler added
  - [ ] Error messages don't expose internals
  
- [ ] **Logging & Auditing**
  - [ ] Audit logs configured
  - [ ] No sensitive data in logs
  - [ ] Log rotation enabled
  
- [ ] **Dependencies**
  - [ ] Run: `mvn org.owasp:dependency-check-maven:check`
  - [ ] No vulnerable dependencies
  - [ ] All versions up-to-date
  
- [ ] **Testing**
  - [ ] Security tests written
  - [ ] Penetration testing planned
  - [ ] OWASP Top 10 review done

---

## One-Liner Fixes

### Disable H2 Console
```yaml
h2:
  console:
    enabled: false
```

### Add Validation
```java
import jakarta.validation.constraints.*;
@NotBlank private String name;
@DecimalMin("0.01") private Double price;
```

### Run Vulnerability Check
```bash
mvn org.owasp:dependency-check-maven:check
```

### Check for Default Credentials
```bash
grep -r "password:" . --include="*.yaml" --include="*.yml"
grep -r "username: sa" . --include="*.yaml" --include="*.yml"
```

### Verify ddl-auto Setting
```bash
grep "ddl-auto" src/main/resources/application*.yaml
# Should be: ddl-auto: validate (for prod)
```

---

## Environment Variables to Set

```bash
export DB_USER=your_db_user
export DB_PASSWORD=your_secure_password
export ALLOWED_ORIGINS=https://yourdomain.com
export SSL_KEYSTORE_PATH=/path/to/keystore.p12
export SSL_KEYSTORE_PASSWORD=your_keystore_password
```

---

## Testing Commands

### Test H2 Access
```bash
curl http://localhost:8080/h2-console
# Should return 404 or 403 in production
```

### Test Authentication
```bash
curl http://localhost:8080/api/products/1
# Should return 401 Unauthorized
```

### Test Validation
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"","price":-100}'
# Should return 400 Bad Request
```

### Run Security Scan
```bash
mvn verify
mvn org.owasp:dependency-check-maven:check
mvn spotbugs:check
```

---

## Critical Files to Review

- [ ] pom.xml - Dependencies for vulnerabilities
- [ ] application.yaml - No exposed credentials
- [ ] application-prod.yaml - Production hardened
- [ ] ProductController.java - Input validation
- [ ] Product.java - Entity constraints
- [ ] SecurityConfig.java - Authentication rules
- [ ] CorsConfig.java - CORS restrictions
- [ ] GlobalExceptionHandler.java - Error handling

---

## Quick Security Audit

Run this to find potential issues:

```bash
# Find passwords/credentials in config
grep -r "password" src/main/resources/

# Find default usernames
grep -r "sa\|admin\|root" src/main/resources/

# Find enabled H2 console
grep -r "enabled: true" src/main/resources/ | grep h2

# Find auto-DDL
grep -r "ddl-auto: update" src/main/resources/

# Find SQL logging enabled
grep -r "show-sql: true" src/main/resources/
```

---

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Spring Security: https://spring.io/projects/spring-security
- CWE Top 25: https://cwe.mitre.org/top25/

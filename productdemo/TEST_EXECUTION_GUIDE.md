# 🚀 Test Execution Guide

## Quick Start

### Run All Tests
```bash
mvn clean test
```

**Expected Output:**
```
Tests run: 69, Failures: 0, Errors: 0, Skipped: 0
Total time: ~15-20 seconds
```

---

## Test Execution by Layer

### 1. Run Entity Tests Only
```bash
mvn test -Dtest=ProductEntityTest
```
**11 tests** - Tests entity getters/setters and constructors
**Duration**: ~1-2 seconds

### 2. Run Repository Tests Only
```bash
mvn test -Dtest=ProductRepositoryTest
```
**14 tests** - Tests database operations (save, find, update, delete)
**Duration**: ~3-5 seconds
**Note**: Creates temporary in-memory H2 database

### 3. Run Service Tests Only
```bash
mvn test -Dtest=ProductServiceTest
```
**11 tests** - Tests business logic with mocks
**Duration**: ~2-3 seconds

### 4. Run Controller Unit Tests Only
```bash
mvn test -Dtest=ProductControllerUnitTest
```
**11 tests** - Tests REST controller with mocks
**Duration**: ~2-3 seconds

### 5. Run Controller Integration Tests Only
```bash
mvn test -Dtest=ProductControllerIntegrationTest
```
**11 tests** - End-to-end API testing
**Duration**: ~3-5 seconds
**Note**: Starts full Spring Boot application

### 6. Run Edge Case Tests Only
```bash
mvn test -Dtest=EdgeCaseTest
```
**11 tests** - Tests boundary conditions
**Duration**: ~3-5 seconds

---

## Test Execution Patterns

### Run Multiple Test Classes
```bash
mvn test -Dtest=ProductEntityTest,ProductRepositoryTest
```

### Run Tests Matching Pattern
```bash
mvn test -Dtest=*Repository*
```

### Run Specific Test Method
```bash
mvn test -Dtest=ProductEntityTest#testSetGetId
```

### Run Tests Excluding Pattern
```bash
mvn test -Dtest=!*EdgeCase*
```

---

## Detailed Execution with Output

### Show Test Names During Execution
```bash
mvn test -X
```

### Fail Fast (Stop on First Failure)
```bash
mvn test -DfailIfNoTests=false
```

### Run in Parallel (Faster Execution)
```bash
mvn test -DreuseForks=false -DargLine=-Xmx1024m
```

---

## Test Coverage Analysis

### Generate Coverage Report
```bash
mvn clean test jacoco:report
```

**Report Location**: `target/site/jacoco/index.html`

### View Coverage Summary
```bash
mvn jacoco:report
```

### Coverage Thresholds Check
```bash
mvn jacoco:check
```

---

## Maven Profile-Based Execution

### Run with Test Profile
```bash
mvn test -Ptest
```

### Skip Tests (for builds)
```bash
mvn clean package -DskipTests
```

### Run Integration Tests Only
```bash
mvn verify -DskipUnitTests
```

---

## Troubleshooting

### Tests Not Found
```bash
mvn test -Dtest=ProductRepositoryTest -v
```
**Check**: Test file location and class name match

### Port Already in Use
```bash
# For integration tests that start full app
lsof -i :8080
kill -9 <PID>
```

### Database Lock Issues
```bash
# H2 in-memory database should clean up automatically
# If issues persist, restart Maven/IDE
```

### Timeout Issues
```bash
mvn test -DtimeoutInMinutes=5
```

---

## Continuous Integration (CI/CD)

### Jenkins/GitLab CI Command
```bash
mvn clean test jacoco:report
```

### GitHub Actions Workflow
```yaml
- name: Run Tests
  run: mvn clean test

- name: Generate Coverage Report
  run: mvn jacoco:report
```

### Docker Test Execution
```bash
docker run -v $(pwd):/app -w /app maven:3.9 mvn clean test
```

---

## Performance Metrics

### Test Execution Summary
```bash
mvn test -Dtest=* | grep -E "Tests run|Time"
```

### Individual Test Timings
Use `@DisplayName` tests with timestamps in output.

---

## Test Data Cleanup

### Automatic Cleanup
- `@BeforeEach` methods handle cleanup
- `@DataJpaTest` auto-rolls back transactions
- H2 in-memory database resets after each test

### Manual Cleanup (if needed)
```bash
rm -rf target/h2*
```

---

## Expected Test Results

### Passing Tests Output
```
Tests run: 69
Success ✅
Failures: 0
Errors: 0
Skipped: 0
Duration: ~15-20s
```

### Test Class Breakdown
```
ProductEntityTest: 11/11 ✅
ProductRepositoryTest: 14/14 ✅
ProductServiceTest: 11/11 ✅
ProductControllerUnitTest: 11/11 ✅
ProductControllerIntegrationTest: 11/11 ✅
EdgeCaseTest: 11/11 ✅
───────────────────────
Total: 69/69 ✅
```

---

## IDE Test Execution

### IntelliJ IDEA
- Right-click test class → Run 'ClassName'
- Right-click test method → Run 'methodName'
- Ctrl+Shift+F10 (Windows) or Cmd+Shift+R (Mac)

### Eclipse
- Right-click test class → Run As → JUnit Test
- Alt+Shift+X, T

### VS Code
- Install "Test Explorer UI" extension
- Click test in explorer panel

---

## Notes

- All tests use `@DisplayName` for clarity
- Tests are designed to be independent (order doesn't matter)
- H2 database automatically cleans between tests
- Integration tests start full Spring Boot application (slower)
- Edge case tests verify boundary conditions and unusual inputs

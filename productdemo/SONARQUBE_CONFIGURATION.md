# SonarQube Configuration Details

## JaCoCo Plugin Configuration

### What is JaCoCo?
JaCoCo (Java Code Coverage) measures which lines/branches of code are executed during tests.

### Configuration in pom.xml
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.10</version>
  <executions>
    <!-- prepare-agent: Instruments code before tests -->
    <!-- report: Generates coverage report after tests -->
    <!-- check: Enforces minimum coverage rules -->
  </executions>
</plugin>
```

## SonarQube Plugin Configuration

### Properties in pom.xml
```xml
<sonar.projectKey>Vernfix_productdemo</sonar.projectKey>
<sonar.organization>vernfix</sonar.organization>
<sonar.host.url>https://sonarcloud.io</sonar.host.url>
<sonar.coverage.jacoco.xmlReportPaths>...</sonar.coverage.jacoco.xmlReportPaths>
```

## Maven Commands

### Run All Tests with Coverage
```bash
mvn clean test
```

### Generate Coverage Report Only
```bash
mvn org.jacoco:jacoco-maven-plugin:report
```

### Run SonarQube Analysis
```bash
mvn sonar:sonar \
  -Dsonar.login=YOUR_TOKEN
```

### Complete Pipeline
```bash
mvn clean \
  org.jacoco:jacoco-maven-plugin:prepare-agent \
  test \
  org.jacoco:jacoco-maven-plugin:report \
  sonar:sonar
```

## Coverage Thresholds

Minimum coverage requirements enforced:
- **Line Coverage**: 50% minimum
- **Branch Coverage**: Configurable
- **Exclusions**: Test classes excluded

## Troubleshooting

### Issue: "SONAR_TOKEN not set"
Solution: Add token to GitHub Secrets

### Issue: Coverage report not generated
Solution: Ensure JaCoCo plugin executes:
```bash
mvn clean test jacoco:report
```

### Issue: SonarCloud not showing results
Solution: Wait 1-2 minutes after workflow completes

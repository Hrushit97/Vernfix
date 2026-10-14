# Local Security Scanner Script for Banking Payment API
# Run all 5 security scanning tools
# Usage: .\RUN_LOCAL_SCANNER.ps1

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Banking Payment API - Local Security Scanner" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi"
Set-Location $projectPath

Write-Host "Project Path: $projectPath" -ForegroundColor Yellow
Write-Host ""

# Check if Maven is installed
Write-Host "[1/6] Checking Maven installation..." -ForegroundColor Green
$mvnTest = Invoke-Expression "mvn -version 2>&1" | Select-Object -First 1
if ($mvnTest -like "*Apache Maven*") {
    Write-Host "✓ Maven found" -ForegroundColor Green
} else {
    Write-Host "✗ Maven not found. Please install Maven." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/6] Building project..." -ForegroundColor Green
mvn clean install -DskipTests
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Build failed" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Build successful" -ForegroundColor Green

Write-Host ""
Write-Host "[3/6] Running SpotBugs (Bug Detection)..." -ForegroundColor Green
mvn spotbugs:check
Write-Host "✓ SpotBugs report: target/spotbugsXml.xml" -ForegroundColor Green

Write-Host ""
Write-Host "[4/6] Running Checkstyle (Code Standards)..." -ForegroundColor Green
mvn checkstyle:check
Write-Host "✓ Checkstyle report: target/checkstyle-result.xml" -ForegroundColor Green

Write-Host ""
Write-Host "[5/6] Running JaCoCo (Code Coverage)..." -ForegroundColor Green
mvn clean test jacoco:report
Write-Host "✓ Coverage report: target/site/jacoco/index.html" -ForegroundColor Green

Write-Host ""
Write-Host "[6/6] Running OWASP Dependency Check (CVE Detection)..." -ForegroundColor Green
mvn org.owasp:dependency-check-maven:check
Write-Host "✓ Dependency Check report: target/dependency-check-report.html" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "All scans completed successfully!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 REPORTS GENERATED:" -ForegroundColor Yellow
Write-Host "  1. Code Coverage:       target/site/jacoco/index.html" -ForegroundColor White
Write-Host "  2. Dependency Check:    target/dependency-check-report.html" -ForegroundColor White
Write-Host "  3. SpotBugs:            target/spotbugsXml.xml" -ForegroundColor White
Write-Host "  4. Checkstyle:          target/checkstyle-result.xml" -ForegroundColor White
Write-Host ""
Write-Host "📈 OPEN COVERAGE REPORT? (y/n)" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq "y" -or $response -eq "yes") {
    Start-Process "target/site/jacoco/index.html"
}

Write-Host ""
Write-Host "Next: Review reports and fix identified issues" -ForegroundColor Cyan

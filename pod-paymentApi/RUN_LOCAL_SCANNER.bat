@echo off
REM Local Security Scanner for Banking Payment API
REM Run all 5 scanning tools
REM Usage: RUN_LOCAL_SCANNER.bat

setlocal enabledelayedexpansion

echo.
echo =====================================================
echo Banking Payment API - Local Security Scanner
echo =====================================================
echo.

cd /d c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

REM Check if Maven is installed
echo [1/6] Checking Maven installation...
mvn -version >nul 2>&1
if errorlevel 1 (
    echo Maven not found. Please install Maven.
    pause
    exit /b 1
)
echo Maven found - OK

REM Step 1: Build project
echo.
echo [2/6] Building project...
call mvn clean install -DskipTests
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)
echo Build successful - OK

REM Step 2: SpotBugs
echo.
echo [3/6] Running SpotBugs (Bug Detection)...
call mvn spotbugs:check
echo SpotBugs completed - Check target/spotbugsXml.xml

REM Step 3: Checkstyle
echo.
echo [4/6] Running Checkstyle (Code Standards)...
call mvn checkstyle:check
echo Checkstyle completed - Check target/checkstyle-result.xml

REM Step 4: JaCoCo
echo.
echo [5/6] Running JaCoCo (Code Coverage)...
call mvn clean test jacoco:report
echo Coverage report created - Check target/site/jacoco/index.html

REM Step 5: OWASP Dependency Check
echo.
echo [6/6] Running OWASP Dependency Check (CVE Detection)...
call mvn org.owasp:dependency-check-maven:check
echo Dependency Check completed - Check target/dependency-check-report.html

echo.
echo =====================================================
echo All scans completed successfully!
echo =====================================================
echo.
echo REPORTS GENERATED:
echo   1. Code Coverage:       target/site/jacoco/index.html
echo   2. Dependency Check:    target/dependency-check-report.html
echo   3. SpotBugs:            target/spotbugsXml.xml
echo   4. Checkstyle:          target/checkstyle-result.xml
echo.
echo Next: Review reports and fix identified issues
echo.
pause

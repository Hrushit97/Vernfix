# Fixing Maven Dependency Resolution Issues

## Problem

The IDE is showing:
- `AccessDeniedException` on Maven repository files
- "Missing artifact" errors for Spring Boot and other dependencies

## Root Cause

Maven local repository cache has permission issues or is corrupted.

## Solution

### Option 1: Clean Maven Cache (Recommended)

**For Windows PowerShell:**
```powershell
# Delete the corrupted Maven cache
Remove-Item -Path $env:USERPROFILE\.m2\repository -Recurse -Force

# OR if you want to keep other caches
Remove-Item -Path "$env:USERPROFILE\.m2\repository\org\springframework" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.m2\repository\io\jsonwebtoken" -Recurse -Force
```

### Option 2: Disable Offline Mode (If Enabled)

In VS Code / IDE:
1. Check Maven settings
2. Ensure offline mode is **disabled**
3. Restart the IDE

### Option 3: Force Maven to Redownload Dependencies

```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# Force update snapshots and redownload everything
mvn clean install -U --no-offline

# Or clear entire cache and rebuild
mvn clean
del /s /q %USERPROFILE%\.m2\repository
mvn install
```

### Option 4: Configure Maven Settings

Create or edit `.m2/settings.xml`:

```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0">
  <mirrors>
    <mirror>
      <id>central</id>
      <name>Central Repository</name>
      <url>https://repo.maven.apache.org/maven2</url>
      <mirrorOf>*</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

## Steps to Resolve

### Step 1: Clean Everything
```bash
# Open PowerShell and run:
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# Stop any running Maven/Java processes
Get-Process | where {$_.Name -like "*java*" -or $_.Name -like "*mvn*"} | Stop-Process -Force

# Clear Maven cache
Remove-Item -Path $env:USERPROFILE\.m2\repository -Recurse -Force
```

### Step 2: Rebuild Project
```bash
# Navigate to project
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi

# Clean and reinstall with forced update
mvn clean install -U -DskipTests
```

### Step 3: Refresh IDE
1. Close VS Code completely
2. Delete `.vscode` folder in project (if exists)
3. Reopen VS Code
4. Let Maven reimport project

### Step 4: Verify
```bash
# Should show no errors
mvn clean verify

# Build and run
mvn clean install
mvn spring-boot:run
```

## If Issues Persist

### Check Maven Installation
```bash
# Verify Maven is installed
mvn -version

# Should show Maven version and Java version 17+
```

### Check File Permissions
```bash
# Check if .m2 folder has proper permissions
icacls $env:USERPROFILE\.m2 /grant:r "%USERDOMAIN%\%USERNAME%":(OI)(CI)F
```

### Disable IDE Cache
1. VS Code: Extensions → Maven for Java → Settings
2. Uncheck "Maven: Offline"
3. Set "Maven: Update project on pom.xml changes" to true

### Manual Dependency Download

If automatic download fails, download manually from:
- https://repo1.maven.org/maven2/

Download these key files:
- org/springframework/boot/spring-boot-starter-web/3.1.5/
- io/jsonwebtoken/jjwt-api/0.12.3/
- org/projectlombok/lombok/1.18.30/

Place them in: `%USERPROFILE%\.m2\repository\`

## Expected Output After Fix

When you run `mvn clean install`, you should see:
```
[INFO] BUILD SUCCESS
[INFO] Total time: X.XXs
[INFO] Finished at: YYYY-MM-DDTHH:MM:SS+XX:XX
```

## Post-Fix Verification

Run test build:
```bash
mvn clean install -DskipTests
```

If successful, the project is ready for use!

## Reference

- Maven Official Docs: https://maven.apache.org/
- Maven Repository: https://mvnrepository.com/
- Spring Boot Docs: https://spring.io/projects/spring-boot

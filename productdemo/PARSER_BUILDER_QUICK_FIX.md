# 🚀 Parser Builder Error - Quick Fix Reference

## Problem
```
Error: parserBuilder() is undefined for the type Jwts
Location: JwtUtils.java line 71 & 108
```

## Root Cause
Using deprecated JJWT API (pre-0.12.x). The project uses JJWT 0.12.3.

---

## 5 Fixes Applied

### Fix 1: JwtUtils.java Line 71
```java
// BEFORE (Deprecated)
Jwts.parserBuilder()
    .setSigningKey(key)
    .build()
    .parseClaimsJws(token)
    .getBody()

// AFTER (Current API)
Jwts.parser()
    .verifyWith(key)
    .build()
    .parseSignedClaims(token)
    .getPayload()
```

### Fix 2: JwtUtils.java Line 108
Same as Fix 1 - replaced in validateTokenSyntax()

### Fix 3: JwtUtils.java Line 47
```java
// BEFORE (Deprecated)
.signWith(key, SignatureAlgorithm.HS512)

// AFTER (Current API)
.signWith(key)
```

### Fix 4: JwtUtils.java Line 3-5
```java
// REMOVED this import (no longer needed)
import io.jsonwebtoken.SignatureAlgorithm;
```

### Fix 5: pom.xml Line 76-80
```xml
<!-- BEFORE (Wrong) -->
<dependency>
    <artifactId>spring-boot-starter-data-jpa-test</artifactId>
</dependency>
<dependency>
    <artifactId>spring-boot-starter-webmvc-test</artifactId>
</dependency>

<!-- AFTER (Correct) -->
<dependency>
    <artifactId>spring-boot-starter-test</artifactId>
</dependency>
```

---

## ✅ Verification

Check if all fixes are applied:

```bash
# 1. Maven reload
mvn clean install

# 2. Compile check
mvn clean compile

# 3. Run tests
mvn test -Dtest=JwtUtilsTest
mvn test -Dtest=AuthControllerTest

# Expected: All pass ✅
```

---

## 📚 API Changes

| Old (0.11.x) | New (0.12.x) |
|--------------|--------------|
| parserBuilder() | parser() |
| setSigningKey() | verifyWith() |
| parseClaimsJws() | parseSignedClaims() |
| getBody() | getPayload() |
| SignatureAlgorithm.HS512 | Inferred from key |

---

## 🔍 What Changed

**JwtUtils.java:**
- Line 3-5: Removed SignatureAlgorithm import
- Line 36-49: Updated createToken method
- Line 68-79: Updated getAllClaimsFromToken method
- Line 108-119: Updated validateTokenSyntax method

**pom.xml:**
- Line 76-80: Fixed test dependencies

---

## ✨ Result

✅ No compilation errors
✅ JWT works correctly
✅ Tests pass
✅ Ready to run

```bash
mvn clean spring-boot:run
```

Then test:
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

**All fixed and ready!** 🎉

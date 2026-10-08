# 🔐 Security Implementation - Product API

## Overview

Comprehensive security has been added to the Product API with authentication, authorization, input validation, and error handling.

---

## Security Features Implemented

### ✅ 1. Spring Security Integration
- **HTTP Basic Authentication**: Requests must include credentials
- **Role-Based Access Control (RBAC)**: Different permissions for ADMIN and USER roles
- **Password Encryption**: BCrypt password encoder

### ✅ 2. Two Default Users
```
Admin User:
  Username: admin
  Password: admin123
  Role: ADMIN, USER

Regular User:
  Username: user
  Password: user123
  Role: USER
```

### ✅ 3. Input Validation
Product entity fields are validated:
- **name**: Required, 2-100 characters
- **price**: Required, must be > 0.01
- **quantity**: Required, cannot be negative

### ✅ 4. API Endpoint Protection

| Endpoint | Method | Required Role | Description |
|----------|--------|---------------|-------------|
| `/api/products` | POST | ADMIN | Create product (ADMIN only) |
| `/api/products/{id}` | GET | USER/ADMIN | Get product (requires authentication) |

### ✅ 5. CORS Configuration
- Allowed origins: `localhost:3000`, `localhost:8080`, `127.0.0.1:3000`
- Allowed methods: GET, POST, PUT, DELETE
- Credentials allowed for secure requests

### ✅ 6. Global Exception Handler
- Validation error responses (400 Bad Request)
- Access denied responses (403 Forbidden)
- Generic error handling (500 Internal Server Error)

---

## Files Created/Modified

### New Files:
1. `src/main/java/com/product/productdemo/config/SecurityConfig.java`
2. `src/main/java/com/product/productdemo/config/CorsConfig.java`
3. `src/main/java/com/product/productdemo/exception/GlobalExceptionHandler.java`
4. `src/main/java/com/product/productdemo/exception/ErrorResponse.java`

### Modified Files:
1. `pom.xml` - Added Spring Security and Validation dependencies
2. `src/main/java/com/product/productdemo/entity/Product.java` - Added validation
3. `src/main/java/com/product/productdemo/controller/ProductController.java` - Added @Valid, @PreAuthorize
4. `src/main/java/com/product/productdemo/ProductdemoApplication.java` - Added @EnableMethodSecurity
5. `src/main/resources/application.yaml` - Security and logging configuration

---

## How to Test Security

### 1. Create Product (ADMIN ONLY)
```bash
# With valid credentials (admin/admin123)
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"name": "Laptop", "price": 999.99, "quantity": 5}'

# With user credentials (will fail - 403 Forbidden)
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u user:user123 \
  -d '{"name": "Laptop", "price": 999.99, "quantity": 5}'

# Without credentials (will fail - 401 Unauthorized)
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "quantity": 5}'
```

### 2. Get Product (USER/ADMIN)
```bash
# With credentials
curl -X GET http://localhost:8080/api/products/1 \
  -u user:user123

# Without credentials (will fail)
curl -X GET http://localhost:8080/api/products/1
```

### 3. Test Validation
```bash
# Invalid price (negative)
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"name": "Item", "price": -50, "quantity": 10}'
# Response: 400 Bad Request with validation errors

# Missing required field
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"name": "Item", "quantity": 10}'
# Response: 400 Bad Request
```

---

## Security Configuration Details

### SecurityConfig.java
- **HTTP Basic Auth**: Username/password in Authorization header
- **CSRF Disabled**: For REST API (stateless)
- **Authorization Rules**:
  - `/api/**` endpoints require authentication
  - `/h2-console/**` allowed for development

### CorsConfig.java
- Restricts cross-origin requests
- Allows specific origins only
- Prevents unauthorized cross-origin access

### Input Validation
- @NotBlank: Ensures field is not empty
- @Size: Validates string length
- @NotNull: Requires field presence
- @DecimalMin: Validates minimum price value
- @Min: Validates minimum quantity

### Error Handling
- Returns proper HTTP status codes
- Includes error details in response
- Sensitive information not exposed

---

## Dependencies Added

```xml
<!-- Spring Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<!-- Validation -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

---

## Production Recommendations

⚠️ **Important for Production:**

1. **Use External User Database**
   - Replace InMemoryUserDetailsManager with database-backed authentication
   - Use LDAP or OAuth2 if needed

2. **Use HTTPS/SSL**
   - Enable SSL in application.yaml
   - Use valid certificates

3. **Disable H2 Console**
   - Remove H2 console access in production

4. **Configure CORS Origins**
   - Update allowed origins for your domain
   - Never use `*` (allow all)

5. **Database Credentials**
   - Use environment variables
   - Never hardcode passwords

6. **Logging**
   - Don't log sensitive information
   - Implement proper audit logging

---

## Testing

All existing tests pass with security enabled. Test users have appropriate roles for test execution.

Run tests:
```bash
mvn clean test
```

---

**Status**: ✅ Security fully implemented and ready for use

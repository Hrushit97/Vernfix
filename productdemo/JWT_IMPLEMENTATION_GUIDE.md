# 🔐 JWT Authentication Implementation Guide

## Overview
Complete JWT (JSON Web Token) authentication system integrated with the Product API. All product endpoints now require valid JWT tokens.

---

## 🚀 Quick Start

### 1. **Get JWT Token (Login)**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9...",
  "tokenType": "Bearer",
  "username": "admin",
  "roles": ["ROLE_ADMIN", "ROLE_USER"]
}
```

### 2. **Use Token for Protected Endpoints**
```bash
curl -X GET http://localhost:8080/api/products/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

### 3. **Validate Token**
```bash
curl -X POST http://localhost:8080/api/auth/validate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

---

## 👥 Default Users

| Username | Password | Role | Access |
|----------|----------|------|--------|
| **admin** | admin123 | ADMIN, USER | Create, Read Products |
| **user** | user123 | USER | Read Only |

---

## 📋 API Endpoints

### Authentication Endpoints (No Token Required)

**1. Login - Get JWT Token**
- **URL**: `POST /api/auth/login`
- **Body**: `{"username":"admin","password":"admin123"}`
- **Response**: JWT Token with 24-hour expiration

**2. Validate Token**
- **URL**: `POST /api/auth/validate`
- **Header**: `Authorization: Bearer <token>`
- **Response**: `true` or `false`

### Product Endpoints (JWT Token Required)

**3. Create Product (ADMIN Only)**
- **URL**: `POST /api/products`
- **Header**: `Authorization: Bearer <token>`
- **Body**: `{"name":"Laptop","price":999.99,"quantity":5}`

**4. Get Product**
- **URL**: `GET /api/products/{id}`
- **Header**: `Authorization: Bearer <token>`

---

## 🔧 JWT Configuration

**File**: `application.yaml`

```yaml
jwt:
  secret: mySecretKeyForJWTAuthenticationProductDemoApplicationWithMoreThan256Bits
  expiration: 86400000  # 24 hours in milliseconds
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `JwtUtils.java` | Token generation and validation |
| `JwtAuthenticationFilter.java` | Extract and validate tokens |
| `AuthController.java` | Login and token endpoints |
| `LoginRequest.java` | DTO for login request |
| `JwtAuthenticationResponse.java` | DTO for token response |

---

## ✨ Key Features

✅ **JWT Token-based Authentication**
✅ **24-hour Token Expiration**
✅ **Role-Based Access Control**
✅ **BCrypt Password Encryption**
✅ **Stateless Session Management**
✅ **Token Validation Endpoint**

---

## 🧪 Testing with Postman/cURL

1. Login to get token
2. Copy token from response
3. Add to Authorization header: `Bearer <token>`
4. Call protected endpoints

Token expires after 24 hours. Get a new one when needed.

---

**Next**: See `JWT_USAGE_EXAMPLES.md` for detailed examples.

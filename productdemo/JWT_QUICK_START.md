# 🚀 JWT Quick Start Guide

## 1️⃣ Start the Application
```bash
mvn clean spring-boot:run
```
App runs on: `http://localhost:8080`

---

## 2️⃣ Login and Get Token

**Command:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Save the token from response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzUxMiJ9...",
  "tokenType": "Bearer",
  "username": "admin",
  "roles": ["ROLE_ADMIN", "ROLE_USER"]
}
```

---

## 3️⃣ Create Product (Admin Only)

**Replace TOKEN with your JWT token:**
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 5
  }'
```

---

## 4️⃣ Get Product

```bash
curl -X GET http://localhost:8080/api/products/1 \
  -H "Authorization: Bearer TOKEN"
```

---

## 5️⃣ Validate Token

```bash
curl -X POST http://localhost:8080/api/auth/validate \
  -H "Authorization: Bearer TOKEN"
```

Response: `true` or `false`

---

## 👥 Default Credentials

| User | Password | Role |
|------|----------|------|
| admin | admin123 | ADMIN, USER |
| user | user123 | USER (read-only) |

---

## 📱 Using Postman

1. **Login Request:**
   - POST: `http://localhost:8080/api/auth/login`
   - Body: `{"username":"admin","password":"admin123"}`
   - Copy `accessToken` value

2. **Get Token in Environment:**
   - Go to Tests tab in login response
   - Add: `pm.environment.set("jwt_token", pm.response.json().accessToken);`

3. **Use Token in Headers:**
   - In any protected request
   - Header: `Authorization: Bearer {{jwt_token}}`

---

## ⏱️ Token Expiration

- **Validity**: 24 hours
- **Expired?** Login again to get new token
- **Check expiration**: Decode token at `jwt.io`

---

## 🔄 Common Workflow

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | grep -o '"accessToken":"[^"]*' | cut -d'"' -f4)

# 2. Create product
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"Mouse","price":29.99,"quantity":50}'

# 3. Get product
curl -X GET http://localhost:8080/api/products/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

## ❌ Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid credentials | Check username/password |
| 401 Missing token | No Authorization header | Add: `Authorization: Bearer TOKEN` |
| 403 Forbidden | User lacks permission | Use admin account |
| Token expired | 24-hour limit exceeded | Login again |

---

## 📚 More Help

- `JWT_IMPLEMENTATION_GUIDE.md` - Detailed setup
- `JWT_USAGE_EXAMPLES.md` - Code examples
- `JWT_SECURITY_CHECKLIST.md` - Security details

---

**Ready?** Start the app and follow steps 1-4 above! 🎉

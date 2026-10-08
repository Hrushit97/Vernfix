# 🚀 API Usage Guide - Secure Product API

## Authentication

All API endpoints require HTTP Basic Authentication.

### Default Credentials

```
Admin User:
  Username: admin
  Password: admin123

Regular User:
  Username: user
  Password: user123
```

---

## API Endpoints

### 1. Create Product
**Endpoint**: `POST /api/products`  
**Required Role**: ADMIN  
**Authentication**: Required (admin/admin123)

**Request**:
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 5
  }'
```

**Success Response (201 Created)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "price": 999.99,
  "quantity": 5
}
```

**Error Response (400 Bad Request)**:
```json
{
  "status": 400,
  "message": "Validation failed",
  "timestamp": "2026-10-08T10:30:00",
  "errors": {
    "name": "Product name is required",
    "price": "Price must be greater than 0"
  }
}
```

---

### 2. Get Product
**Endpoint**: `GET /api/products/{id}`  
**Required Role**: USER or ADMIN  
**Authentication**: Required (any valid user)

**Request**:
```bash
curl -X GET http://localhost:8080/api/products/1 \
  -u user:user123
```

**Success Response (200 OK)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "price": 999.99,
  "quantity": 5
}
```

**Not Found Response (404)**:
```json
No content
```

---

## Error Responses

### 401 Unauthorized
Missing or invalid credentials
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Item", "price": 100, "quantity": 5}'
```

Response: 401 Unauthorized

### 403 Forbidden
User role doesn't have permission
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u user:user123 \
  -d '{"name": "Item", "price": 100, "quantity": 5}'
```

Response:
```json
{
  "status": 403,
  "message": "Access denied",
  "timestamp": "2026-10-08T10:30:00"
}
```

### 400 Bad Request
Validation errors
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"name": "Item", "price": -50, "quantity": 5}'
```

Response: Shows validation errors for each field

---

## Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| name | 2-100 characters, required | "Laptop" |
| price | > 0.01, required | 999.99 |
| quantity | >= 0, required | 5 |

---

## Using with Postman

### Setup Authentication
1. Open Postman
2. Go to Authorization tab
3. Select "Basic Auth"
4. Enter username and password
5. Click Send

### Example Request
```
POST http://localhost:8080/api/products
Headers:
  Content-Type: application/json

Body:
{
  "name": "Keyboard",
  "price": 79.99,
  "quantity": 20
}
```

---

## Using with JavaScript

```javascript
// Create product
fetch('http://localhost:8080/api/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + btoa('admin:admin123')
  },
  body: JSON.stringify({
    name: 'Laptop',
    price: 999.99,
    quantity: 5
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Get product
fetch('http://localhost:8080/api/products/1', {
  headers: {
    'Authorization': 'Basic ' + btoa('user:user123')
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Using with Python

```python
import requests
from requests.auth import HTTPBasicAuth

# Create product
response = requests.post(
    'http://localhost:8080/api/products',
    json={
        'name': 'Laptop',
        'price': 999.99,
        'quantity': 5
    },
    auth=HTTPBasicAuth('admin', 'admin123')
)
print(response.json())

# Get product
response = requests.get(
    'http://localhost:8080/api/products/1',
    auth=HTTPBasicAuth('user', 'user123')
)
print(response.json())
```

---

## Common Issues

### Issue: 401 Unauthorized
**Cause**: Missing or incorrect credentials  
**Solution**: Check username/password format

### Issue: 403 Forbidden
**Cause**: User role doesn't have permission  
**Solution**: Use admin account for POST, any user for GET

### Issue: 400 Bad Request
**Cause**: Validation failed  
**Solution**: Check field values match validation rules

---

**Status**: ✅ API fully secured and documented

# JWT Usage Examples

## 📌 Complete Workflow Examples

### Example 1: Using cURL Commands

#### Step 1: Login and Get Token
```bash
RESPONSE=$(curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

echo $RESPONSE
```

Expected Response:
```json
{
  "accessToken": "eyJhbGciOiJIUzUxMiJ9...",
  "tokenType": "Bearer",
  "username": "admin",
  "roles": ["ROLE_ADMIN", "ROLE_USER"]
}
```

#### Step 2: Extract Token
```bash
TOKEN=$(echo $RESPONSE | grep -o '"accessToken":"[^"]*' | cut -d'"' -f4)
echo $TOKEN
```

#### Step 3: Create Product (Admin Only)
```bash
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Laptop",
    "price": 1299.99,
    "quantity": 10
  }'
```

#### Step 4: Get Product
```bash
curl -X GET http://localhost:8080/api/products/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Example 2: Postman Collection

**Environment Variables:**
```json
{
  "baseUrl": "http://localhost:8080",
  "token": "{{accessToken}}"
}
```

**Login Request:**
- Method: POST
- URL: `{{baseUrl}}/api/auth/login`
- Body (raw JSON):
```json
{
  "username": "admin",
  "password": "admin123"
}
```
- Tests Script:
```javascript
var jsonData = pm.response.json();
pm.environment.set("accessToken", jsonData.accessToken);
```

**Create Product Request:**
- Method: POST
- URL: `{{baseUrl}}/api/products`
- Headers: `Authorization: Bearer {{token}}`
- Body:
```json
{
  "name": "Mouse",
  "price": 29.99,
  "quantity": 50
}
```

---

### Example 3: Node.js Client

```javascript
const axios = require('axios');

async function createProduct() {
  try {
    // Login
    const loginRes = await axios.post(
      'http://localhost:8080/api/auth/login',
      { username: 'admin', password: 'admin123' }
    );
    
    const token = loginRes.data.accessToken;
    
    // Create Product
    const productRes = await axios.post(
      'http://localhost:8080/api/products',
      { name: 'Keyboard', price: 79.99, quantity: 20 },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    console.log('Product created:', productRes.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
}

createProduct();
```

---

### Example 4: Token Validation

**Check if token is valid:**
```bash
curl -X POST http://localhost:8080/api/auth/validate \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response: `true` or `false`

---

## 🚫 Error Responses

| Status | Error | Solution |
|--------|-------|----------|
| 401 | Invalid credentials | Check username/password |
| 401 | Missing token | Add Authorization header |
| 401 | Expired token | Get new token (login again) |
| 403 | Insufficient permissions | Use ADMIN account |
| 400 | Invalid JSON | Check request body |

---

## 💾 Token Storage

**Best Practices:**
- ✅ Store in secure httpOnly cookie
- ✅ Store in localStorage for SPAs
- ❌ Never expose in console logs
- ❌ Never commit to git

---

**See JWT_IMPLEMENTATION_GUIDE.md for more details.**

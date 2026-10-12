# Banking Payment API - Testing Guide

## Prerequisites

1. **Java 17+** installed
2. **Maven 3.6+** installed
3. **Postman** (optional, for API testing)
4. **cURL** or any HTTP client

## Building the Project

### Step 1: Navigate to project directory
```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
```

### Step 2: Build the project
```bash
mvn clean install
```

### Step 3: Run the application
```bash
mvn spring-boot:run
```

Or run the JAR file:
```bash
java -jar target/payment-api-1.0.0.jar
```

The application will start on `http://localhost:8080`

## Testing with cURL

### 1. Login to get JWT Token

**User1 Login:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "username": "user1",
  "role": "USER",
  "accountNumber": "ACC001"
}
```

Copy the `token` value.

### 2. Create Payment

Replace `{TOKEN}` with the token from login response:

```bash
curl -X POST http://localhost:8080/api/payments/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{
    "fromAccount": "ACC001",
    "toAccount": "ACC002",
    "amount": 250.75,
    "description": "Payment for services"
  }'
```

**Response:**
```json
{
  "id": 1,
  "transactionId": "550e8400-e29b-41d4-a716-446655440000",
  "fromAccount": "ACC001",
  "toAccount": "ACC002",
  "amount": 250.75,
  "status": "COMPLETED",
  "description": "Payment for services",
  "createdAt": "2024-01-15T10:30:00",
  "updatedAt": "2024-01-15T10:30:00"
}
```

Save the `transactionId` and `id`.

### 3. Retrieve Payment by ID

```bash
curl -X GET http://localhost:8080/api/payments/1 \
  -H "Authorization: Bearer {TOKEN}"
```

### 4. Retrieve Payment by Transaction ID

```bash
curl -X GET "http://localhost:8080/api/payments/transaction/{TRANSACTION_ID}" \
  -H "Authorization: Bearer {TOKEN}"
```

## Testing with Postman

1. Import the `Banking_Payment_API.postman_collection.json` file into Postman
2. Set the `{{token}}` variable with the JWT token from login
3. Set the `{{transactionId}}` variable with the transaction ID from create payment
4. Execute requests in order

## H2 Console Access

Access the H2 database console at:
```
http://localhost:8080/h2-console
```

- **JDBC URL**: jdbc:h2:mem:testdb
- **User Name**: sa
- **Password**: (leave empty)

## SQL Queries for H2 Console

### View all payments
```sql
SELECT * FROM payments;
```

### View all users
```sql
SELECT * FROM users;
```

### Count payments by account
```sql
SELECT from_account, COUNT(*) as count FROM payments GROUP BY from_account;
```

## Test Scenarios

### Scenario 1: Valid Payment Creation
1. Login with user1 credentials
2. Create payment from ACC001 to ACC002 with amount 100
3. Expected: HTTP 201 CREATED with payment details

### Scenario 2: Invalid Payment (Zero Amount)
1. Login with user1 credentials
2. Create payment with amount 0
3. Expected: HTTP 400 BAD_REQUEST with error message

### Scenario 3: Same Account Payment
1. Login with user1 credentials
2. Create payment from ACC001 to ACC001
3. Expected: HTTP 400 BAD_REQUEST with error

### Scenario 4: Unauthorized Access
1. Don't provide Authorization header
2. Try to create payment
3. Expected: HTTP 401 UNAUTHORIZED

### Scenario 5: Non-existent Payment
1. Login with user1 credentials
2. Get payment by non-existent ID (999)
3. Expected: HTTP 404 NOT_FOUND

## Test Users

| Username | Password | Account | Role |
|----------|----------|---------|------|
| user1 | password123 | ACC001 | USER |
| user2 | password456 | ACC002 | USER |
| admin | admin123 | ADMIN001 | ADMIN |

## Error Responses

All error responses follow this format:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "status": 400,
  "error": "Invalid Payment",
  "message": "Amount must be greater than zero",
  "path": "/api/payments/create"
}
```

## Troubleshooting

### Port 8080 already in use
```bash
# Find process using port 8080
netstat -ano | findstr :8080

# Kill process (replace PID)
taskkill /PID {PID} /F
```

### H2 Console not accessible
- Ensure the application has started successfully
- Check that Spring Boot is running on port 8080
- Verify CORS is enabled in SecurityConfig

### JWT Token expired
- Login again to get a new token
- Default expiration: 24 hours

## Running Unit Tests

```bash
mvn test
```

## Building Docker Image (Optional)

Create a `Dockerfile`:
```dockerfile
FROM openjdk:17-slim
COPY target/payment-api-1.0.0.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```

Build and run:
```bash
docker build -t banking-payment-api .
docker run -p 8080:8080 banking-payment-api
```

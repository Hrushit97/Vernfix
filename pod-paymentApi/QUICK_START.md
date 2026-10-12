# Banking Payment API - Quick Start Guide

## 5-Minute Setup

### Step 1: Build the Application (2 minutes)
```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
mvn clean install
```

### Step 2: Run the Application (30 seconds)
```bash
mvn spring-boot:run
```

Wait for the message: **"Application started successfully"**

### Step 3: Test with Login (1 minute)

Open any terminal and run:
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password123"}'
```

You'll get a response with a JWT token. Copy the `token` value.

### Step 4: Create a Payment (1 minute)

Replace `YOUR_TOKEN_HERE` with the token from Step 3:
```bash
curl -X POST http://localhost:8080/api/payments/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "fromAccount":"ACC001",
    "toAccount":"ACC002",
    "amount":100.50,
    "description":"Test payment"
  }'
```

### Step 5: Retrieve Payment (30 seconds)

```bash
curl -X GET http://localhost:8080/api/payments/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Done! ✓

Your Banking Payment API is running with:
- ✓ H2 In-Memory Database
- ✓ JWT Authentication
- ✓ Payment Management
- ✓ Exception Handling

## Key Features at a Glance

| Feature | Status |
|---------|--------|
| User Authentication | ✓ JWT-based |
| Create Payments | ✓ With validation |
| Retrieve Payments | ✓ By ID or Transaction ID |
| Data Persistence | ✓ H2 Database |
| Security | ✓ BCrypt + JWT |
| Exception Handling | ✓ Global error handler |

## Test Credentials

- **User 1**: `user1` / `password123`
- **User 2**: `user2` / `password456`
- **Admin**: `admin` / `admin123`

## Access H2 Console

After starting the app, visit:
```
http://localhost:8080/h2-console
```

- URL: `jdbc:h2:mem:testdb`
- User: `sa`
- Password: (leave empty)

## Endpoints Summary

### Authentication
- **Login**: `POST /api/auth/login`

### Payments
- **Create**: `POST /api/payments/create`
- **Get by ID**: `GET /api/payments/{id}`
- **Get by Transaction**: `GET /api/payments/transaction/{transactionId}`

## Documentation

- **Full Setup**: See `README.md`
- **Testing Guide**: See `API_TESTING_GUIDE.md`
- **Architecture**: See `PROJECT_STRUCTURE.md`
- **Postman**: Import `Banking_Payment_API.postman_collection.json`

## Troubleshooting

### Port 8080 already in use?
```bash
# Kill the process
netstat -ano | findstr :8080
taskkill /PID {PID} /F
```

### Build fails?
```bash
# Clear cache and rebuild
mvn clean install -U
```

### JWT expired?
Simply login again to get a new token.

## Next Steps

1. ✓ Test all endpoints
2. ✓ Check the database via H2 console
3. ✓ Review error handling by sending invalid requests
4. ✓ Read full documentation for advanced features
5. ✓ Extend with additional endpoints as needed

## Questions?

- Check `README.md` for detailed documentation
- Review `API_TESTING_GUIDE.md` for testing examples
- See `PROJECT_STRUCTURE.md` for architecture details

# Banking Payment API - Complete Setup Instructions

## Environment Setup

### Prerequisites
- **Java 17 or higher** - Download from [Oracle JDK](https://www.oracle.com/java/technologies/downloads/)
- **Maven 3.6 or higher** - Download from [Apache Maven](https://maven.apache.org/download.cgi)
- **Git** (optional) - For version control

### Verify Installation
```bash
java -version
mvn -version
```

## Project Setup

### 1. Navigate to Project Directory
```bash
cd c:\Users\Aparajita\Documents\project\Vernfix\pod-paymentApi
```

### 2. Clean Build
```bash
mvn clean
```

### 3. Install Dependencies
```bash
mvn install
```

### 4. Build Project
```bash
mvn clean install
```

This will:
- Download all dependencies
- Compile source code
- Run unit tests
- Create JAR file in `target/` directory

## Running the Application

### Option 1: Using Maven
```bash
mvn spring-boot:run
```

### Option 2: Using JAR File
```bash
java -jar target/payment-api-1.0.0.jar
```

### Verify Startup
Wait for message: `Started PaymentApiApplication`

Access application: `http://localhost:8080`

## First Test

### Step 1: Get JWT Token
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "password123"
  }'
```

Save the `token` value from response.

### Step 2: Create Payment
```bash
curl -X POST http://localhost:8080/api/payments/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {YOUR_TOKEN_HERE}" \
  -d '{
    "fromAccount": "ACC001",
    "toAccount": "ACC002",
    "amount": 150.00,
    "description": "Test payment"
  }'
```

### Step 3: Retrieve Payment
```bash
curl -X GET http://localhost:8080/api/payments/1 \
  -H "Authorization: Bearer {YOUR_TOKEN_HERE}"
```

## Using Postman

1. Open Postman
2. Click "Import"
3. Select `Banking_Payment_API.postman_collection.json`
4. Execute requests in order:
   - Login first (save token in {{token}} variable)
   - Create payment
   - Retrieve payment

## H2 Console Access

1. Start the application
2. Open browser: `http://localhost:8080/h2-console`
3. Login with:
   - JDBC URL: `jdbc:h2:mem:testdb`
   - User Name: `sa`
   - Password: (leave empty)
4. Click "Connect"

### Useful Queries
```sql
-- View all payments
SELECT * FROM PAYMENTS;

-- View all users
SELECT * FROM USERS;

-- Count payments by account
SELECT FROM_ACCOUNT, COUNT(*) FROM PAYMENTS GROUP BY FROM_ACCOUNT;

-- View recent transactions
SELECT * FROM PAYMENTS ORDER BY CREATED_AT DESC LIMIT 10;
```

## Available Test Credentials

| Username | Password | Account | Role | Purpose |
|----------|----------|---------|------|---------|
| user1 | password123 | ACC001 | USER | Testing sender |
| user2 | password456 | ACC002 | USER | Testing receiver |
| admin | admin123 | ADMIN001 | ADMIN | Admin access |

## Complete API Reference

### Authentication

**POST /api/auth/login**
- Request: `{ username, password }`
- Response: `{ token, username, role, accountNumber }`
- Status: 200 OK / 401 UNAUTHORIZED

### Payment Endpoints

**POST /api/payments/create**
- Auth: Required (JWT)
- Request: `{ fromAccount, toAccount, amount, description }`
- Response: Full payment details with transactionId
- Status: 201 CREATED / 400 BAD_REQUEST / 401 UNAUTHORIZED

**GET /api/payments/{id}**
- Auth: Required (JWT)
- Response: Payment details
- Status: 200 OK / 404 NOT_FOUND / 401 UNAUTHORIZED

**GET /api/payments/transaction/{transactionId}**
- Auth: Required (JWT)
- Response: Payment details
- Status: 200 OK / 404 NOT_FOUND / 401 UNAUTHORIZED

## Directory Structure

```
pod-paymentApi/
├── src/main/java/com/banking/
│   ├── PaymentApiApplication.java
│   ├── controller/          (AuthController, PaymentController)
│   ├── service/             (AuthService, PaymentService)
│   ├── repository/          (PaymentRepository, UserRepository)
│   ├── model/               (Payment, User)
│   ├── dto/                 (Request/Response objects)
│   ├── exception/           (Custom exceptions + handler)
│   ├── security/            (JWT utilities and filter)
│   └── config/              (Security, Data initialization)
├── src/main/resources/
│   └── application.properties
├── src/test/java/
│   └── com/banking/service/PaymentServiceTest.java
├── pom.xml
├── README.md
├── QUICK_START.md
├── API_TESTING_GUIDE.md
├── PROJECT_STRUCTURE.md
├── IMPLEMENTATION_SUMMARY.md
├── SETUP_INSTRUCTIONS.md
└── Banking_Payment_API.postman_collection.json
```

## Troubleshooting

### Issue: Port 8080 already in use

**Solution:**
```bash
# Find process
netstat -ano | findstr :8080

# Kill process (replace PID)
taskkill /PID {PID} /F
```

### Issue: Maven command not found

**Solution:**
- Ensure Maven is installed and in PATH
- Download from: https://maven.apache.org/download.cgi
- Add to Windows PATH environment variable

### Issue: Java version too old

**Solution:**
- Download Java 17+: https://www.oracle.com/java/technologies/downloads/
- Set JAVA_HOME environment variable
- Restart terminal

### Issue: Build fails with dependency errors

**Solution:**
```bash
# Clear Maven cache
mvn clean install -U

# Force update snapshots
mvn clean install -U -Dmaven.repo.local=.m2
```

### Issue: H2 console not accessible

**Solution:**
- Verify application started successfully
- Check port 8080 is accessible
- Clear browser cache and try again
- Try incognito/private browser window

## Performance Tips

1. **First Build**: Takes longer due to dependency downloads
2. **Subsequent Builds**: Much faster (dependencies cached)
3. **Test Run**: Use `mvn spring-boot:run` for development
4. **Production**: Use `java -jar` for better startup time

## Documentation Files

| File | Purpose |
|------|---------|
| README.md | Overview and features |
| QUICK_START.md | 5-minute setup |
| API_TESTING_GUIDE.md | Detailed testing with examples |
| PROJECT_STRUCTURE.md | Architecture and design |
| IMPLEMENTATION_SUMMARY.md | Completed components |
| SETUP_INSTRUCTIONS.md | This file |

## Next Steps

1. ✓ Ensure Java and Maven are installed
2. ✓ Build the project: `mvn clean install`
3. ✓ Run the application: `mvn spring-boot:run`
4. ✓ Test endpoints using Postman or cURL
5. ✓ Check H2 console for database
6. ✓ Review documentation files for details

## Support & Reference

- Spring Boot Docs: https://spring.io/projects/spring-boot
- JWT Docs: https://github.com/jwtk/jjwt
- H2 Database: http://h2database.com
- Maven Guide: https://maven.apache.org/guides/

---

**Ready to build and deploy your Banking Payment API!**

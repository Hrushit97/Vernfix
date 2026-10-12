# Banking Payment API - Project Structure

## Directory Layout

```
pod-paymentApi/
├── src/
│   ├── main/
│   │   ├── java/com/banking/
│   │   │   ├── PaymentApiApplication.java          # Main Spring Boot application
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java              # Authentication endpoints
│   │   │   │   └── PaymentController.java           # Payment CRUD endpoints
│   │   │   ├── service/
│   │   │   │   ├── AuthService.java                 # Authentication logic
│   │   │   │   └── PaymentService.java              # Payment business logic
│   │   │   ├── repository/
│   │   │   │   ├── PaymentRepository.java           # Payment data access
│   │   │   │   └── UserRepository.java              # User data access
│   │   │   ├── model/
│   │   │   │   ├── Payment.java                     # Payment entity
│   │   │   │   └── User.java                        # User entity
│   │   │   ├── dto/
│   │   │   │   ├── PaymentRequest.java              # Payment creation request
│   │   │   │   ├── PaymentResponse.java             # Payment response
│   │   │   │   ├── AuthRequest.java                 # Login request
│   │   │   │   └── AuthResponse.java                # Login response
│   │   │   ├── exception/
│   │   │   │   ├── ResourceNotFoundException.java   # 404 exceptions
│   │   │   │   ├── InvalidPaymentException.java     # Validation exceptions
│   │   │   │   ├── UnauthorizedException.java       # Auth exceptions
│   │   │   │   └── GlobalExceptionHandler.java      # Centralized exception handling
│   │   │   ├── security/
│   │   │   │   ├── JwtUtil.java                     # JWT token generation/validation
│   │   │   │   └── JwtFilter.java                   # JWT authentication filter
│   │   │   └── config/
│   │   │       ├── SecurityConfig.java              # Spring Security configuration
│   │   │       └── DataInitializer.java             # Test data initialization
│   │   └── resources/
│   │       └── application.properties                # Application configuration
│   └── test/
│       └── java/com/banking/service/
│           └── PaymentServiceTest.java              # Unit tests
├── pom.xml                                           # Maven configuration
├── README.md                                         # Project overview
├── API_TESTING_GUIDE.md                              # Testing guide
├── PROJECT_STRUCTURE.md                              # This file
└── Banking_Payment_API.postman_collection.json       # Postman test collection
```

## Component Details

### Models

**Payment.java**
- Entity for payment transactions
- Fields: id, transactionId, fromAccount, toAccount, amount, status, description, timestamps
- Payment Status: PENDING, COMPLETED, FAILED, CANCELLED
- Auto-generated transactionId (UUID)
- Automatic timestamp management

**User.java**
- Entity for system users
- Fields: id, username, password, email, role, enabled, accountNumber
- Supports different roles (USER, ADMIN)

### DTOs (Data Transfer Objects)

**PaymentRequest**
- fromAccount, toAccount, amount, description
- Used for creating payments

**PaymentResponse**
- Complete payment details with timestamps
- Converted from Payment entity

**AuthRequest**
- username, password
- Used for login

**AuthResponse**
- JWT token, username, role, accountNumber
- Returned after successful authentication

### Services

**AuthService**
- Authenticates users
- Generates JWT tokens
- Validates credentials

**PaymentService**
- Creates payments with validation
- Retrieves payments by ID or transactionId
- Validates: amount > 0, valid accounts, no self-transfer

### Repositories

**PaymentRepository**
- JPA operations for Payment entity
- Custom queries: findByTransactionId, findByFromAccount, findByToAccount

**UserRepository**
- JPA operations for User entity
- Custom queries: findByUsername, findByEmail, findByAccountNumber

### Controllers

**AuthController**
- POST /api/auth/login - User authentication

**PaymentController**
- POST /api/payments/create - Create payment
- GET /api/payments/{id} - Retrieve by ID
- GET /api/payments/transaction/{transactionId} - Retrieve by transaction ID

### Security

**JwtUtil**
- Generates JWT tokens with claims (role, accountNumber)
- Validates tokens
- Extracts claims from tokens
- Uses HMAC-SHA256 signing

**JwtFilter**
- OncePerRequestFilter implementation
- Validates JWT in Authorization header
- Sets authentication context

**SecurityConfig**
- Configures Spring Security
- Enables JWT-based stateless authentication
- BCrypt password encoding
- CORS support

### Exception Handling

**GlobalExceptionHandler**
- ResourceNotFoundException (404)
- InvalidPaymentException (400)
- UnauthorizedException (401)
- General Exception (500)
- Consistent error response format with timestamp, status, message

### Configuration

**application.properties**
- H2 database: jdbc:h2:mem:testdb
- JWT secret and expiration
- JPA DDL: create-drop
- H2 console enabled

**DataInitializer**
- CommandLineRunner implementation
- Creates 3 test users on startup
- user1, user2, and admin accounts

## Dependencies

### Core
- spring-boot-starter-web
- spring-boot-starter-data-jpa
- spring-boot-starter-security

### Database
- h2 (embedded in-memory database)

### Security
- jjwt-api, jjwt-impl, jjwt-jackson (0.12.3)

### Utilities
- lombok (annotation processing)

### Testing
- spring-boot-starter-test
- junit-jupiter
- mockito

## Build and Deployment

### Build
```bash
mvn clean install
```

### Run
```bash
mvn spring-boot:run
```

### Package
```bash
mvn package
```

### Docker
```bash
docker build -t banking-payment-api .
docker run -p 8080:8080 banking-payment-api
```

## API Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/auth/login | No | User authentication |
| POST | /api/payments/create | Yes | Create payment |
| GET | /api/payments/{id} | Yes | Get payment by ID |
| GET | /api/payments/transaction/{txnId} | Yes | Get payment by transaction ID |

## Configuration Files

### pom.xml
- Maven project configuration
- Spring Boot parent version 3.1.5
- All dependencies and plugins

### application.properties
- H2 connection string
- JWT secret and expiration
- JPA and Hibernate settings
- H2 console configuration
- Logging levels

## Testing

### Unit Tests
- PaymentServiceTest: Test payment creation and retrieval logic
- Uses Mockito for mocking repository
- Tests success and error scenarios

### Integration Tests
- Can be added using @SpringBootTest
- Test full request/response cycle
- Database integration

### Manual Testing
- Use Postman collection: Banking_Payment_API.postman_collection.json
- Use cURL commands from API_TESTING_GUIDE.md
- Access H2 console for database inspection

## Error Responses Format

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "status": 400,
  "error": "Error Type",
  "message": "Error message",
  "path": "/api/endpoint"
}
```

## Security Features

1. JWT-based authentication
2. BCrypt password hashing
3. Stateless session management
4. CORS enabled
5. Authorization header validation
6. Custom exception handling
7. Role-based access control (USER, ADMIN)

## Performance Considerations

1. H2 in-memory database for fast testing
2. Stateless JWT authentication
3. JPA query methods optimized
4. Transaction management enabled
5. Connection pooling available

## Future Enhancements

1. Payment status workflow (PENDING → COMPLETED → SETTLED)
2. Transaction history and audit logs
3. Rate limiting and throttling
4. Pagination for list endpoints
5. Advanced search and filtering
6. Payment scheduling
7. Notification system
8. Multi-currency support

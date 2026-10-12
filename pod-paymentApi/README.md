# Banking Payment API

A comprehensive Spring Boot REST API for banking payment processing with JWT authentication, H2 database, and exception handling.

## Features

- **Payment Management**: Create and retrieve payment transactions
- **JWT Authentication**: Secure endpoints with JWT bearer tokens
- **H2 Database**: In-memory database for development and testing
- **Exception Handling**: Global exception handler for consistent error responses
- **Request Validation**: Comprehensive validation for payment amounts and accounts

## Project Structure

```
src/main/java/com/banking/
├── controller/         # REST controllers
├── service/           # Business logic
├── repository/        # Database access layer
├── model/             # Entity classes
├── dto/               # Data transfer objects
├── exception/         # Custom exceptions
├── security/          # JWT utilities
└── config/            # Security and data initialization
```

## Quick Start

### Build
```bash
mvn clean install
```

### Run
```bash
mvn spring-boot:run
```

The API will be available at `http://localhost:8080`

## API Endpoints

### Authentication

**Login**
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "user1",
  "password": "password123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "user1",
  "role": "USER",
  "accountNumber": "ACC001"
}
```

### Payment Endpoints

**Create Payment**
```
POST /api/payments/create
Authorization: Bearer {token}
Content-Type: application/json

{
  "fromAccount": "ACC001",
  "toAccount": "ACC002",
  "amount": 100.00,
  "description": "Payment for services"
}

Response:
{
  "id": 1,
  "transactionId": "uuid-string",
  "fromAccount": "ACC001",
  "toAccount": "ACC002",
  "amount": 100.00,
  "status": "COMPLETED",
  "description": "Payment for services",
  "createdAt": "2024-01-15T10:30:00",
  "updatedAt": "2024-01-15T10:30:00"
}
```

**Retrieve Payment by ID**
```
GET /api/payments/{id}
Authorization: Bearer {token}

Response: Payment object (as above)
```

**Retrieve Payment by Transaction ID**
```
GET /api/payments/transaction/{transactionId}
Authorization: Bearer {token}

Response: Payment object (as above)
```

## Test Credentials

- **User 1**: username=`user1`, password=`password123`
- **User 2**: username=`user2`, password=`password456`
- **Admin**: username=`admin`, password=`admin123`

## H2 Database Console

Access the H2 console at: `http://localhost:8080/h2-console`

- URL: `jdbc:h2:mem:testdb`
- Username: `sa`
- Password: (leave empty)

## Technology Stack

- **Spring Boot 3.1.5**
- **Spring Data JPA**
- **Spring Security**
- **H2 Database**
- **JWT (jjwt 0.12.3)**
- **Lombok**
- **Java 17**

## Exception Handling

The API includes global exception handling for:
- `ResourceNotFoundException` - 404
- `InvalidPaymentException` - 400
- `UnauthorizedException` - 401
- General exceptions - 500

All error responses include timestamp, status code, error message, and request path.

## Security

- JWT-based authentication
- BCrypt password encoding
- Stateless session management
- CORS enabled for development

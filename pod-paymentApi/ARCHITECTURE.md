# Banking Payment API - Architecture

## Layered Architecture

The application follows a **4-Layer Architecture Pattern**:

```
┌─────────────────────────────────┐
│     REST Controller Layer        │
│  (HTTP Request/Response)         │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     Service Layer               │
│  (Business Logic)               │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     Repository Layer            │
│  (Data Access - JPA)            │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     Database Layer              │
│  (H2 In-Memory)                 │
└─────────────────────────────────┘
```

## Component Structure

### Layer 1: Controllers (REST Endpoints)
- **AuthController**: Handle authentication requests
- **PaymentController**: Handle payment operations

### Layer 2: Services (Business Logic)
- **AuthService**: User authentication and JWT generation
- **PaymentService**: Payment validation and processing

### Layer 3: Repositories (Data Access)
- **UserRepository**: JPA interface for User entity
- **PaymentRepository**: JPA interface for Payment entity

### Layer 4: Database
- **H2 Database**: In-memory relational database
- **Tables**: USERS, PAYMENTS

## Exception Handling Flow

```
Request → Controller → Service → Repository → Database
  ↓         ↓            ↓           ↓           ↓
  └─────────────────────────────────────────────┘
                        ↓
              GlobalExceptionHandler
                        ↓
            JSON Error Response (HTTP Status)
```

## Security Components

1. **JwtUtil**: Token generation and validation
2. **JwtFilter**: Request-level JWT validation
3. **SecurityConfig**: Spring Security configuration
4. **BCryptPasswordEncoder**: Password hashing

## Data Models

### User Entity
- Stores user credentials and account information
- Passwords encrypted with BCrypt
- Supports role-based access (USER, ADMIN)

### Payment Entity
- Stores transaction details
- Unique transaction ID (UUID)
- Status tracking (PENDING, COMPLETED, FAILED, CANCELLED)
- Automatic timestamp management

## Request/Response Flow

### Login Request
```
Client → POST /api/auth/login → AuthController
         → AuthService → UserRepository
         → JwtUtil → AuthResponse (with token)
```

### Payment Request
```
Client → (JWT Token) → JwtFilter (validate)
         → POST /api/payments/create → PaymentController
         → PaymentService (validate) → PaymentRepository
         → PaymentResponse
```

## Error Handling

All errors return consistent format:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "status": 400,
  "error": "Error Type",
  "message": "Detailed message",
  "path": "/api/endpoint"
}
```

HTTP Status Codes:
- 200: OK
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (auth error)
- 404: Not Found
- 500: Internal Server Error



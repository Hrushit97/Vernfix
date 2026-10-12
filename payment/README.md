# Payment API

A simple Express.js-based payment API with create and get endpoints.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

The API will run on `http://localhost:3000`

## API Endpoints

### 1. Create Payment
**POST** `/payments`

Create a new payment transaction.

**Request Body:**
```json
{
  "amount": 100.50,
  "currency": "USD",
  "description": "Order #12345"
}
```

**Response (201 Created):**
```json
{
  "message": "Payment created successfully",
  "payment": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "amount": 100.50,
    "currency": "USD",
    "description": "Order #12345",
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00.000Z"
  }
}
```

### 2. Get Payment
**GET** `/payments/:id`

Retrieve payment details by ID.

**Response (200 OK):**
```json
{
  "message": "Payment retrieved successfully",
  "payment": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "amount": 100.50,
    "currency": "USD",
    "description": "Order #12345",
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00.000Z"
  }
}
```

**Response (404 Not Found):**
```json
{
  "error": "Payment not found"
}
```

### 3. Health Check (Bonus)
**GET** `/health`

Check if the API is running.

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

## Example Usage

### Create a payment:
```bash
curl -X POST http://localhost:3000/payments \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "currency": "USD",
    "description": "Test payment"
  }'
```

### Get a payment:
```bash
curl http://localhost:3000/payments/123e4567-e89b-12d3-a456-426614174000
```

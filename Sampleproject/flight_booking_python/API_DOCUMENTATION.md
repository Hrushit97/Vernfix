# Flight Booking System - API Documentation

## MCP Tools Reference

### Flight Search Tools

#### search_flights
Search for available flights between two cities.

**Input:**
```json
{
  "origin": "New York",
  "destination": "Los Angeles"
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": "flight-uuid",
      "airline": "United Airlines",
      "route": "New York → Los Angeles",
      "departure": "2024-01-15 08:00",
      "arrival": "2024-01-15 11:30",
      "price": "$250",
      "available_seats": 50,
      "status": "Available"
    }
  ],
  "count": 1
}
```

#### list_available_flights
Get all available flights in the system.

**Input:** None (no parameters)

**Response:**
```json
{
  "status": "success",
  "data": [...],
  "count": 5
}
```

---

### Booking Tools

#### book_flight
Create a new flight booking.

**Input:**
```json
{
  "flight_id": "flight-uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "555-0101"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "booking_id": "booking-uuid",
    "passenger_name": "John Doe",
    "passenger_email": "john@example.com",
    "flight_id": "flight-uuid",
    "airline": "United Airlines",
    "route": "New York → Los Angeles",
    "departure_time": "2024-01-15 08:00",
    "arrival_time": "2024-01-15 11:30",
    "seat_number": "Unassigned",
    "total_price": "$250",
    "status": "Confirmed",
    "booking_date": "2024-01-10T10:30:00.000000"
  },
  "booking_id": "booking-uuid"
}
```

#### cancel_booking
Cancel an existing booking.

**Input:**
```json
{
  "booking_id": "booking-uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "booking_id": "booking-uuid",
    "status": "Cancelled",
    ...
  }
}
```

#### get_booking_details
Retrieve details of a specific booking.

**Input:**
```json
{
  "booking_id": "booking-uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "data": { ... }
}
```

#### get_my_bookings
Get all bookings for a passenger.

**Input:**
```json
{
  "passenger_id": "passenger-uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "data": [...],
  "count": 3
}
```

#### assign_seat
Assign a seat to a booking.

**Input:**
```json
{
  "booking_id": "booking-uuid",
  "seat_number": "12A"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "booking_id": "booking-uuid",
    "seat_number": "12A",
    ...
  }
}
```

---

### Statistics Tools

#### get_flight_stats
Get system-wide flight statistics.

**Input:** None

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_flights": 5,
    "available_flights": 3,
    "booked_flights": 2
  }
}
```

#### get_booking_stats
Get system-wide booking statistics.

**Input:** None

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_bookings": 10,
    "confirmed_bookings": 8,
    "cancelled_bookings": 2,
    "total_revenue": 2050
  }
}
```

---

## Error Responses

All endpoints follow this error format:

```json
{
  "status": "error",
  "message": "Description of the error"
}
```

### Common Errors
- "Flight not found" - Invalid flight ID
- "Booking not found" - Invalid booking ID
- "No seats available on this flight" - Flight is full
- "Unknown tool" - Invalid tool name

---

## Agent Interaction Examples

### Example 1: Search and Book
```
User: "I want to fly from New York to Los Angeles next week. Can you find me the cheapest flight?"
Agent: Uses search_flights → lists options → asks for confirmation → uses book_flight
```

### Example 2: Manage Booking
```
User: "Cancel my booking for flight ABC123"
Agent: Uses cancel_booking → confirms cancellation
```

### Example 3: Get Information
```
User: "What are my bookings?"
Agent: Uses get_my_bookings → displays all passenger bookings
```

### Example 4: Seat Assignment
```
User: "Can I change my seat to 5C?"
Agent: Uses assign_seat → confirms seat change
```

---

## Integration Guide

### Using the Agent in Code

```python
from agent.booking_agent import FlightBookingAgent
from services.flight_service import FlightService
from services.booking_service import BookingService

# Initialize
flight_service = FlightService()
booking_service = BookingService()
agent = FlightBookingAgent(flight_service, booking_service)

# Chat with agent
response = agent.chat("Book a flight from NYC to LAX")
print(response)
```

### Using Tools Directly

```python
from tools.mcp_tools import FlightBookingMCPTools

tools = FlightBookingMCPTools(flight_service, booking_service)

# Call tool directly
result = tools.search_flights("New York", "Los Angeles")
print(result)
```

---

## Response Status Codes

- `success` - Operation completed successfully
- `error` - Operation failed

All responses include a status field and either data or message field.

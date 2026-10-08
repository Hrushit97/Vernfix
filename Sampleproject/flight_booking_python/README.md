# Flight Ticket Booking System - Python Edition

A comprehensive Python application for managing flight bookings and ticket reservations with AI agent capabilities powered by Claude and MCP tools.

## Features

- ✈️ **Flight Management**: Add, search, and manage flights
- 🎫 **Booking System**: Create and manage flight bookings
- 👤 **Passenger Management**: Store passenger information
- 🤖 **AI Agent**: Claude-powered intelligent booking assistant
- 🔧 **MCP Tools**: Model Context Protocol tools for flight operations
- 📊 **Statistics**: Track bookings and revenue
- 🌤️ **Weather Integration**: Real-time weather checking and risk assessment
- ✅ **Status Monitoring**: Flight and booking status tracking
- 🤖 **Multi-Agent Workflow**: LangGraph-based coordinated agent system
- 🧪 **Unit Tests**: Comprehensive pytest coverage

## Project Structure

```
flight_booking_python/
├── models/
│   ├── flight.py        # Flight model
│   ├── passenger.py     # Passenger model
│   ├── booking.py       # Booking model
│   └── __init__.py
├── services/
│   ├── flight_service.py      # Flight operations
│   ├── booking_service.py     # Booking operations
│   ├── weather_service.py     # Weather checking & risk assessment
│   ├── status_service.py      # Flight & booking status monitoring
│   └── __init__.py
├── tools/
│   ├── mcp_tools.py     # MCP tool definitions
│   └── __init__.py
├── agent/
│   ├── booking_agent.py        # AI Agent using Claude
│   ├── multiagent_workflow.py  # LangGraph multi-agent system
│   └── __init__.py
├── tests/
│   ├── test_flight.py
│   ├── test_booking_service.py
│   ├── test_weather_service.py
│   ├── test_status_service.py
│   └── __init__.py
├── main.py                     # Main application
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── MULTIAGENT_GUIDE.md        # Multi-agent workflow documentation
└── API_DOCUMENTATION.md       # API reference
```

## Installation

### 1. Navigate to project directory
```bash
cd flight_booking_python
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

### Run the application

```bash
python main.py
```

This will:
1. Initialize sample flights
2. Run a demo of direct API usage
3. Run a demo of AI agent interactions
4. Start an interactive chat with the AI agent

### Run tests

```bash
pytest tests/ -v
```

### Run specific test file

```bash
pytest tests/test_flight.py -v
```

## MCP Tools Available

### Flight Operations
- **search_flights** - Search flights by origin and destination
- **list_available_flights** - List all available flights
- **get_flight_stats** - Get flight system statistics

### Booking Operations
- **book_flight** - Book a flight for a passenger
- **cancel_booking** - Cancel an existing booking
- **get_booking_details** - Get details of a specific booking
- **get_my_bookings** - Get all bookings for a passenger
- **assign_seat** - Assign a seat to a booking
- **get_booking_stats** - Get booking statistics

## API Overview

### Flight Model
```python
flight = Flight(airline, origin, destination, departure_time, arrival_time, price, available_seats)
flight.is_available()           # Check availability
flight.book_seat()              # Book a seat
flight.cancel_seat()            # Cancel a seat
flight.get_flight_info()        # Get flight details
```

### Passenger Model
```python
passenger = Passenger(first_name, last_name, email, phone)
passenger.get_full_name()       # Get full name
passenger.set_passport_number(number)  # Add passport
passenger.get_passenger_info()  # Get details
```

### Booking Model
```python
booking = Booking(passenger, flight)
booking.set_seat_number(seat)   # Assign seat
booking.cancel()                 # Cancel booking
booking.get_booking_details()   # Get details
```

### Services
```python
flight_service = FlightService()
flight_service.add_flight(flight)
flight_service.search_flights(origin, destination)
flight_service.list_available_flights()

booking_service = BookingService()
booking_service.create_booking(passenger, flight)
booking_service.cancel_booking(booking_id)
booking_service.get_booking_stats()
```

## AI Agent Usage

### Interactive Chat
```python
from agent.booking_agent import FlightBookingAgent

agent = FlightBookingAgent(flight_service, booking_service)
response = agent.chat("Find flights from New York to Los Angeles")
```

### Example Interactions

**Search flights:**
```
User: "Find flights from New York to Los Angeles"
Agent: Searches and displays available flights with prices and seat information
```

**Book a flight:**
```
User: "Book a flight for me. Name: John Doe, Email: john@example.com, Phone: 555-0101, Flight: United to LAX"
Agent: Creates booking and provides confirmation with booking ID
```

**Check bookings:**
```
User: "What are my bookings?"
Agent: Retrieves and displays all passenger bookings
```

**Get statistics:**
```
User: "How many flights are available?"
Agent: Retrieves and displays flight and booking statistics
```

## Example Usage

```python
from models.flight import Flight
from models.passenger import Passenger
from services.flight_service import FlightService
from services.booking_service import BookingService

# Initialize services
flight_service = FlightService()
booking_service = BookingService()

# Create and add flight
flight = Flight("United Airlines", "NYC", "LAX", 
                "2024-01-15 08:00", "2024-01-15 11:30", 250)
flight_service.add_flight(flight)

# Create passenger and booking
passenger = Passenger("John", "Doe", "john@example.com", "555-0101")
booking = booking_service.create_booking(passenger, flight)
booking.set_seat_number("12A")

# Display booking details
print(booking.get_booking_details())
```

## Multi-Agent Workflow (LangGraph)

The system includes a sophisticated multi-agent workflow orchestrated by LangGraph:

### Agent Workflow Chain

```
User Request
    ↓
Flight Search Agent (Find available flights)
    ↓
Weather Check Agent (Analyze weather conditions)
    ↓
Booking Agent (Process booking)
    ↓
Status Check Agent (Monitor flight status)
    ↓
Recommendation Agent (Generate recommendations)
    ↓
Response
```

### Agent Responsibilities

- **Flight Search Agent**: Searches for available flights
- **Weather Check Agent**: Analyzes weather conditions and risk levels
- **Booking Agent**: Creates booking when flights are available
- **Status Check Agent**: Monitors real-time flight status
- **Recommendation Agent**: Consolidates all information and provides recommendations

For detailed information, see [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md)

## Technologies Used

- **Python 3.8+** - Programming language
- **FastAPI/Uvicorn** - Web framework (optional for API)
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM (optional for database)
- **Anthropic Claude** - AI model for agent
- **LangGraph** - Multi-agent orchestration framework
- **LangChain** - LLM framework
- **MCP** - Model Context Protocol for tool integration
- **Pytest** - Testing framework
- **Requests** - HTTP client library

## Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` - Your Anthropic API key

### API Model
Default: `claude-3-5-sonnet-20241022`
Can be changed in `agent/booking_agent.py`

## Testing

The project includes comprehensive tests:

### Test Coverage
- **test_flight.py** - Flight model tests
- **test_booking_service.py** - Booking service tests

### Run All Tests
```bash
pytest tests/ -v --cov=.
```

## Error Handling

All services include error handling:
- Invalid flight bookings
- Booking not found
- Full flights
- Invalid passenger data

## License

ISC

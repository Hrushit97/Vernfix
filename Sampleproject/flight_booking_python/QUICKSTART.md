# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY="sk-..."
```

### 3. Run the Application
```bash
python main.py
```

---

## What You'll See

The application will:
1. **Initialize 5 sample flights** (NYC↔LAX, NYC→Miami, etc.)
2. **Run direct API demo** - Shows booking without AI agent
3. **Run AI agent demo** - Shows Claude interacting with flights
4. **Start interactive chat** - You can talk to the agent

---

## Try These Commands

### In Interactive Mode

**Search flights:**
```
Find flights from New York to Los Angeles
```

**Book a flight:**
```
Book a flight for me. I'm John Smith, email john@example.com, phone 555-1234, and I want the United Airlines flight to Los Angeles
```

**Check bookings:**
```
Show me all available flights and booking statistics
```

**Manage seat:**
```
Assign me seat 12A on my booking
```

**Get info:**
```
How many flights are currently available?
```

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_flight.py -v

# With coverage
pytest tests/ --cov=. -v
```

---

## Project Structure

```
flight_booking_python/
├── models/          # Data models (Flight, Passenger, Booking)
├── services/        # Business logic (FlightService, BookingService)
├── tools/           # MCP tools for Claude
├── agent/           # AI agent (FlightBookingAgent)
├── tests/           # Unit tests
├── main.py          # Entry point
└── requirements.txt # Dependencies
```

---

## Key Files to Explore

- **main.py** - Application entry point and demos
- **agent/booking_agent.py** - Claude AI integration
- **tools/mcp_tools.py** - Available operations
- **services/** - Business logic implementation
- **models/** - Data structures

---

## API Methods

### Services (Direct Usage)

```python
# Flight operations
flight_service.search_flights("NYC", "LAX")
flight_service.list_available_flights()
flight_service.add_flight(flight)

# Booking operations
booking_service.create_booking(passenger, flight)
booking_service.cancel_booking(booking_id)
booking_service.get_booking_stats()
```

### Agent (AI-Powered)

```python
agent = FlightBookingAgent(flight_service, booking_service)
response = agent.chat("Find me a flight to Paris")
```

---

## Common Tasks

### Add a New Flight
```python
from models.flight import Flight
from services.flight_service import FlightService

flight_service = FlightService()
flight = Flight(
    airline="United Airlines",
    origin="NYC",
    destination="LAX",
    departure_time="2024-01-15 08:00",
    arrival_time="2024-01-15 11:30",
    price=250,
    available_seats=100
)
flight_service.add_flight(flight)
```

### Create a Booking
```python
from models.passenger import Passenger

passenger = Passenger("John", "Doe", "john@example.com", "555-0101")
booking = booking_service.create_booking(passenger, flight)
booking.set_seat_number("12A")
```

### Query Bookings
```python
bookings = booking_service.get_bookings_by_passenger(passenger.id)
stats = booking_service.get_booking_stats()
```

---

## Environment Variables

Create `.env` file (copy from `.env.example`):

```
ANTHROPIC_API_KEY=your-key-here
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

---

## Troubleshooting

**ImportError when running main.py?**
- Make sure you're in the project directory
- Check that all files are in the correct structure

**API key error?**
- Set ANTHROPIC_API_KEY environment variable
- Or update the agent to use your key

**Tests failing?**
- Ensure pytest is installed: `pip install pytest`
- Run from project root: `pytest tests/`

---

## Next Steps

1. ✅ Run `python main.py` to see it work
2. ✅ Try the interactive chat mode
3. ✅ Run tests: `pytest tests/ -v`
4. ✅ Explore the code structure
5. ✅ Read API_DOCUMENTATION.md for detailed info

---

## Need Help?

- Check README.md for detailed documentation
- See API_DOCUMENTATION.md for all available tools
- Review example code in main.py
- Look at tests/ for usage examples

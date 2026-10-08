# Documentation Index

Complete guide to all documentation for the Flight Booking System with Multi-Agent Capabilities.

## 📚 Documentation Files

### Getting Started
1. **[README.md](README.md)** - Main project documentation
   - Project overview
   - Features list
   - Installation instructions
   - Basic usage examples
   - Technology stack

2. **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
   - 5-minute setup
   - Running the application
   - Interactive mode guide
   - Common commands
   - Troubleshooting

### Multi-Agent System
3. **[MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md)** - Complete multi-agent documentation
   - Architecture overview
   - Agent responsibilities
   - Workflow execution details
   - State management
   - Service descriptions
   - Integration guide
   - Custom extensions

4. **[MULTIAGENT_ENHANCEMENTS.md](MULTIAGENT_ENHANCEMENTS.md)** - Enhancement summary
   - Components added
   - New services overview
   - Test coverage
   - Updated files
   - Usage examples
   - Benefits and future enhancements

### Architecture & Design
5. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture diagrams
   - High-level architecture
   - Multi-agent workflow diagram
   - Service dependencies
   - Data flow visualization
   - Component interaction map
   - State transitions
   - Database schema
   - Technology stack layers

### API Reference
6. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API reference
   - MCP tools documentation
   - Tool definitions
   - Input/output schemas
   - Error responses
   - Agent interaction examples
   - Integration guide
   - Response status codes

## 🗂️ File Organization

```
flight_booking_python/
│
├── 📖 Documentation/
│   ├── README.md                      # Main readme
│   ├── QUICKSTART.md                  # Quick start guide
│   ├── MULTIAGENT_GUIDE.md           # Multi-agent documentation
│   ├── MULTIAGENT_ENHANCEMENTS.md    # Enhancement summary
│   ├── ARCHITECTURE.md                # System architecture
│   ├── API_DOCUMENTATION.md          # API reference
│   ├── DOCUMENTATION_INDEX.md        # This file
│   └── .env.example                  # Example env config
│
├── 🏗️ Core Application/
│   ├── main.py                        # Entry point
│   ├── examples_multiagent.py        # Multi-agent examples
│   ├── requirements.txt               # Dependencies
│   └── pytest.ini                    # Pytest config
│
├── 📦 Models/
│   ├── flight.py                      # Flight model
│   ├── passenger.py                   # Passenger model
│   ├── booking.py                     # Booking model
│   └── __init__.py
│
├── 🔧 Services/
│   ├── flight_service.py             # Flight operations
│   ├── booking_service.py            # Booking operations
│   ├── weather_service.py            # Weather checking
│   ├── status_service.py             # Status monitoring
│   └── __init__.py
│
├── 🤖 Agents/
│   ├── booking_agent.py              # Single AI agent
│   ├── multiagent_workflow.py        # Multi-agent system
│   └── __init__.py
│
├── 🔨 Tools/
│   ├── mcp_tools.py                  # MCP tool definitions
│   └── __init__.py
│
└── ✅ Tests/
    ├── test_flight.py
    ├── test_booking_service.py
    ├── test_weather_service.py
    ├── test_status_service.py
    └── __init__.py
```

## 🚀 How to Navigate

### For New Users
1. Start with [README.md](README.md) for overview
2. Follow [QUICKSTART.md](QUICKSTART.md) for setup
3. Check examples in `main.py` and `examples_multiagent.py`

### For Developers
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Study [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) for workflow details
3. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for available tools
4. Explore code in `agent/`, `services/`, `models/`

### For Integration
1. Check [MULTIAGENT_ENHANCEMENTS.md](MULTIAGENT_ENHANCEMENTS.md) for what's new
2. Reference [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for tool usage
3. Look at [examples_multiagent.py](examples_multiagent.py) for integration patterns

## 📋 Quick Reference

### Key Classes
- **Flight** - Represents a flight
- **Passenger** - Represents a passenger
- **Booking** - Represents a booking
- **FlightService** - Flight management
- **BookingService** - Booking management
- **WeatherService** - Weather checking
- **StatusService** - Status monitoring
- **FlightBookingAgent** - Single-agent Claude interface
- **MultiAgentWorkflow** - LangGraph multi-agent orchestration

### Key Files to Modify
- `main.py` - Main application logic
- `agent/multiagent_workflow.py` - Add new agents
- `services/` - Add new services
- `requirements.txt` - Update dependencies

## 🔍 Topics by Use Case

### Booking Flights
- See: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) → book_flight tool
- Example: [examples_multiagent.py](examples_multiagent.py) → example_1_basic_workflow

### Checking Weather
- See: [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) → WeatherService section
- Example: [examples_multiagent.py](examples_multiagent.py) → example_2_weather_risk_assessment

### Monitoring Status
- See: [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) → StatusService section
- Example: [examples_multiagent.py](examples_multiagent.py) → example_3_flight_status_tracking

### Running Workflows
- See: [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) → Usage Examples
- Example: [examples_multiagent.py](examples_multiagent.py)

### Adding New Agents
- See: [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) → Custom Workflow Extension
- Code: `agent/multiagent_workflow.py`

### Understanding Architecture
- See: [ARCHITECTURE.md](ARCHITECTURE.md)
- Diagrams showing all system components and interactions

## 📞 Service Overview

| Service | Purpose | Location |
|---------|---------|----------|
| FlightService | Flight CRUD & search | `services/flight_service.py` |
| BookingService | Booking management | `services/booking_service.py` |
| WeatherService | Weather data & risk | `services/weather_service.py` |
| StatusService | Flight/booking status | `services/status_service.py` |

## 🤖 Agent Overview

| Agent | Purpose | Type |
|-------|---------|------|
| FlightBookingAgent | Claude AI with MCP | Single-agent |
| MultiAgentWorkflow | LangGraph orchestration | Multi-agent |

## 🧪 Testing

All test files documented in tests/:
- `test_flight.py` - Flight model tests
- `test_booking_service.py` - Booking tests
- `test_weather_service.py` - Weather service tests
- `test_status_service.py` - Status service tests

Run: `pytest tests/ -v`

## 🔗 External Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📝 Notes

- All paths are relative to project root (`flight_booking_python/`)
- Ensure dependencies installed: `pip install -r requirements.txt`
- Set API key: `export ANTHROPIC_API_KEY="your-key"`
- Run application: `python main.py`
- Run examples: `python examples_multiagent.py`
- Run tests: `pytest tests/ -v`

## ✅ Checklist for Getting Started

- [ ] Read README.md
- [ ] Follow QUICKSTART.md setup
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set ANTHROPIC_API_KEY environment variable
- [ ] Run main.py: `python main.py`
- [ ] Check out examples: `python examples_multiagent.py`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Review ARCHITECTURE.md for system design
- [ ] Study MULTIAGENT_GUIDE.md for workflow details

---

**Last Updated:** 2024
**Version:** 1.0 with Multi-Agent Support

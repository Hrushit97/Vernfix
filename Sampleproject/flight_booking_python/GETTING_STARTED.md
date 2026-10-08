# Getting Started with Multi-Agent Flight Booking System

## 5-Minute Quick Start

### Step 1: Install Dependencies (2 min)
```bash
cd flight_booking_python
pip install -r requirements.txt
```

### Step 2: Set API Key (1 min)
```bash
export ANTHROPIC_API_KEY="sk-your-key-here"
```

### Step 3: Run the Application (2 min)
```bash
python main.py
```

You'll see:
1. ✈️ Sample flights initialized
2. 📋 Direct API usage demo
3. 🤖 Multi-agent workflow demo
4. 💬 Interactive chat mode

---

## System Overview

```
Your Request
    ↓
[Multi-Agent Workflow]
    ├─ Flight Search Agent 🔍
    ├─ Weather Check Agent 🌤️
    ├─ Booking Agent 🎫
    ├─ Status Check Agent 📊
    └─ Recommendation Agent 💡
    ↓
Recommendations + Results
```

---

## Key Features

### 🎫 Flight Booking
- Search available flights
- Create bookings
- Manage passenger info
- Track bookings

### 🌤️ Weather Integration
- Real-time weather
- Risk assessment
- Safety alerts
- Recommendations

### 📊 Status Monitoring
- Flight status tracking
- Gate information
- Boarding updates
- Seat confirmation

### 🤖 AI Agents
- Claude-powered single agent
- LangGraph multi-agent system
- Intelligent recommendations

---

## What's in the Box

```
flight_booking_python/
├── 🎯 Quick Start
│   ├── main.py              ← Run this first!
│   ├── examples_multiagent.py
│   └── QUICKSTART.md
│
├── 📚 Documentation
│   ├── README.md
│   ├── MULTIAGENT_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── API_DOCUMENTATION.md
│
├── 💼 Application Code
│   ├── models/              (Flight, Passenger, Booking)
│   ├── services/            (Flight, Booking, Weather, Status)
│   ├── agent/               (AI Agents)
│   └── tools/               (MCP Tools)
│
└── ✅ Tests
    └── tests/               (Comprehensive test suite)
```

---

## Common Tasks

### View Available Flights
```python
flights = flight_service.list_available_flights()
for flight in flights:
    print(f"{flight['airline']} - {flight['route']} - {flight['price']}")
```

### Check Weather for Route
```python
weather = weather_service.check_flight_weather("New York", "Los Angeles")
if weather["safe_to_fly"]:
    print("✅ Safe to fly!")
else:
    print(f"⚠️ {weather['recommendation']}")
```

### Check Flight Status
```python
status = status_service.check_flight_status("FL-001")
print(f"Flight Status: {status['status']}")
print(f"Gate: {status['gate']}")
```

### Run Multi-Agent Workflow
```python
workflow = MultiAgentWorkflow(fs, bs, ws, ss)
result = workflow.run_workflow(
    user_request="Book NYC to LAX",
    origin="New York",
    destination="Los Angeles"
)
print(workflow.format_workflow_result(result))
```

---

## Interactive Mode

After running `python main.py`, you can chat with the AI agent:

```
You: Find flights from New York to Los Angeles

Agent: I'll search for available flights from New York to Los Angeles...
[Uses Flight Search Agent] ✓
[Uses Weather Check Agent] ✓
[Uses Status Check Agent] ✓

Agent: I found 3 available flights. Weather conditions are good.
Here are the options:
1. United Airlines - $250 - 50 seats
2. Delta Airlines - $180 - 40 seats
3. American Airlines - $200 - 60 seats

Would you like to book one?
```

---

## File Guide

### Must-Read Files
1. **README.md** - Project overview
2. **QUICKSTART.md** - Fast setup guide
3. **MULTIAGENT_GUIDE.md** - Workflow details

### For Developers
1. **ARCHITECTURE.md** - System design
2. **API_DOCUMENTATION.md** - API reference
3. **examples_multiagent.py** - Code examples

### For Learning
1. **IMPLEMENTATION_SUMMARY.md** - What was added
2. **MULTIAGENT_ENHANCEMENTS.md** - All changes
3. **DOCUMENTATION_INDEX.md** - All docs index

---

## Running Examples

### Basic Example
```bash
python main.py
```

### Multi-Agent Examples
```bash
python examples_multiagent.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_weather_service.py -v
```

---

## Project Structure at a Glance

```
📦 flight_booking_python/
 ├── 📄 main.py                 Main application (START HERE)
 ├── 📄 examples_multiagent.py   Examples
 ├── 📂 models/                  Data models
 ├── 📂 services/                Business logic
 │   ├── flight_service.py
 │   ├── booking_service.py
 │   ├── weather_service.py      NEW ✨
 │   └── status_service.py       NEW ✨
 ├── 📂 agent/                   AI Agents
 │   ├── booking_agent.py
 │   └── multiagent_workflow.py  NEW ✨ (LangGraph)
 ├── 📂 tools/                   MCP Tools
 ├── 📂 tests/                   Test Suite
 ├── 📄 requirements.txt         Dependencies
 └── 📚 Documentation            See files below
```

---

## Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| README.md | Overview | First time |
| QUICKSTART.md | Fast setup | Need quick start |
| MULTIAGENT_GUIDE.md | Workflow details | Want to understand agents |
| ARCHITECTURE.md | System design | Want to modify system |
| API_DOCUMENTATION.md | API reference | Building integrations |
| examples_multiagent.py | Code examples | Need examples |
| IMPLEMENTATION_SUMMARY.md | What's new | Want to see changes |
| MULTIAGENT_ENHANCEMENTS.md | All changes | Need detailed changes |

---

## Troubleshooting

### Import Error
```
Error: ModuleNotFoundError: No module named 'langgraph'
Solution: pip install -r requirements.txt
```

### API Key Error
```
Error: API key not found
Solution: export ANTHROPIC_API_KEY="your-key-here"
```

### Port Already in Use
```
Error: Address already in use
Solution: Kill existing process or change port
```

### Test Failures
```
Solution: Make sure all dependencies installed
Run: pip install -r requirements.txt
Then: pytest tests/ -v
```

---

## Next Steps

1. ✅ Run `python main.py`
2. ✅ Check the output and demos
3. ✅ Try interactive mode
4. ✅ Read MULTIAGENT_GUIDE.md
5. ✅ Run `python examples_multiagent.py`
6. ✅ Run `pytest tests/ -v`
7. ✅ Explore the code
8. ✅ Build your own features!

---

## Key Concepts

### Agents
Different AI agents handling specific tasks:
- 🔍 Flight Search Agent
- 🌤️ Weather Check Agent
- 🎫 Booking Agent
- 📊 Status Check Agent
- 💡 Recommendation Agent

### Workflow
LangGraph orchestrates agents in sequence with conditional branches.

### State
TypedDict manages data flow between agents.

### Services
Handle business logic and data operations.

### Models
Represent domain entities (Flight, Passenger, Booking).

---

## System Capabilities

| Capability | Status |
|-----------|--------|
| Flight booking | ✅ Complete |
| Weather checking | ✅ Complete |
| Status monitoring | ✅ Complete |
| Multi-agent workflow | ✅ Complete |
| AI agent integration | ✅ Complete |
| API documentation | ✅ Complete |
| Test coverage | ✅ Complete |
| Example code | ✅ Complete |

---

## Support & Resources

- **Docs**: See DOCUMENTATION_INDEX.md
- **Examples**: Check examples_multiagent.py
- **Tests**: Review test files for usage
- **Code**: All well-commented

---

**Ready to start? Run: `python main.py`**

---

## Quick Links

- 📖 Full Documentation: [README.md](README.md)
- 🚀 Quick Setup: [QUICKSTART.md](QUICKSTART.md)
- 🤖 Multi-Agent Guide: [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md)
- 🏗️ Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- 📚 All Docs: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

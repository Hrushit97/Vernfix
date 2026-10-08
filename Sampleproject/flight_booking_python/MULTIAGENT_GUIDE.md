# Multi-Agent Workflow Guide - LangGraph Integration

## Overview

This system implements a sophisticated multi-agent workflow using LangGraph to manage flight bookings with real-time weather and status checking capabilities.

## Architecture

### Agent Types

The system includes 5 specialized agents working in a coordinated workflow:

```
User Request
    ↓
[Flight Search Agent] → [Weather Check Agent] → [Booking Agent]
                                                     ↓
                                            [Status Check Agent]
                                                     ↓
                                            [Recommendation Agent]
                                                     ↓
                                                  Response
```

### Agents Breakdown

#### 1. **Flight Search Agent** 🔍
- **Responsibility**: Search for available flights
- **Input**: Origin, Destination, Date
- **Output**: List of available flights with details
- **Decision**: Determines if flights exist for the route

#### 2. **Weather Check Agent** 🌤️
- **Responsibility**: Analyze weather conditions
- **Input**: Origin and Destination cities
- **Output**: Weather data, risk assessment, safety recommendation
- **Risk Levels**: Low, Moderate, High, Critical
- **Decision**: Warns if conditions are unsafe

#### 3. **Booking Agent** 🎫
- **Responsibility**: Process flight bookings
- **Input**: Selected flight and passenger details
- **Output**: Booking confirmation with ID
- **Decision**: Prepares booking if flights are available

#### 4. **Status Check Agent** 📊
- **Responsibility**: Monitor flight status
- **Input**: Flight ID
- **Output**: Current flight status, gate info, delays
- **Decision**: Provides real-time flight information

#### 5. **Recommendation Agent** 💡
- **Responsibility**: Generate recommendations
- **Input**: Data from all agents
- **Output**: Consolidated recommendations
- **Decision**: Summarizes findings and advice

## Workflow Execution

### State Management

The workflow uses a TypedDict `FlightBookingState` to maintain state:

```python
{
    "user_request": str,           # User's booking request
    "origin": str,                 # Flight origin
    "destination": str,            # Flight destination
    "departure_date": str,         # Departure date
    "flight_info": dict,           # Flight search results
    "weather_info": dict,          # Weather analysis
    "flight_status": dict,         # Flight status info
    "booking_info": dict,          # Booking details
    "recommendations": list,       # Agent recommendations
    "messages": list              # Agent activity log
}
```

### State Transitions

```
flight_search_agent
        ↓ (always)
weather_check_agent
        ↓ (always)
booking_agent
        ↓ (conditional)
   if booking created → status_check_agent
   else → recommendation_agent
        ↓ (always)
recommendation_agent
        ↓
       END
```

## Usage Examples

### Basic Workflow Execution

```python
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from agent.multiagent_workflow import MultiAgentWorkflow

# Initialize services
flight_service = FlightService()
booking_service = BookingService()
weather_service = WeatherService()
status_service = StatusService()

# Create workflow
workflow = MultiAgentWorkflow(
    flight_service,
    booking_service,
    weather_service,
    status_service
)

# Run workflow
result = workflow.run_workflow(
    user_request="Book a flight from NYC to LAX",
    origin="New York",
    destination="Los Angeles",
    departure_date="2024-01-15"
)

# Display results
print(workflow.format_workflow_result(result))
```

### Handling Results

```python
result = workflow.run_workflow("NYC to LAX", "New York", "Los Angeles")

# Access flight information
flights = result["flight_info"]["flights"]

# Access weather data
origin_weather = result["weather_info"]["origin"]
destination_weather = result["weather_info"]["destination"]

# View recommendations
for rec in result["recommendations"]:
    print(rec)

# Track agent activities
for msg in result["agent_messages"]:
    print(f"{msg['agent']}: {msg['result']}")
```

## Services Overview

### WeatherService

Provides weather information and flight safety assessment:

```python
weather_service = WeatherService()

# Check weather for both cities
weather = weather_service.check_flight_weather("NYC", "LAX")

# Get risk assessment
risk_status = weather["risk_status"]  # Low, Moderate, High, Critical

# Check if safe to fly
safe = weather["safe_to_fly"]  # boolean

# Get weather alert (if severe)
alert = weather_service.get_weather_alert("NYC", "LAX")
```

### StatusService

Monitors flight and booking statuses:

```python
status_service = StatusService()

# Check flight status
flight_status = status_service.check_flight_status("flight-id")
print(flight_status["status"])  # On Time, Delayed, Cancelled, etc.
print(flight_status["gate"])    # Gate information

# Check booking status
booking_status = status_service.check_booking_status("booking-id", "flight-id")
print(booking_status["flight_status"])
print(booking_status["seat_confirmed"])
```

## Weather Risk Assessment

### Risk Levels

| Level | Score | Condition | Impact |
|-------|-------|-----------|--------|
| Low | 0-1 | Sunny, Clear | No concerns |
| Moderate | 2-3 | Cloudy, Partly Cloudy, Rainy | Minor delays possible |
| High | 4-5 | Windy, Stormy, Snowy | Consider rescheduling |
| Critical | 6+ | Severe Storms | Flight not recommended |

### Weather Conditions

- ✅ Sunny, Clear: Best flying conditions
- 🟨 Cloudy, Partly Cloudy, Foggy: Normal with caution
- ⚠️ Rainy, Windy: Adverse conditions
- ❌ Snowy, Stormy: Dangerous conditions

## Flight Status Types

- **On Time**: Flight departing on schedule
- **Delayed**: Flight delayed (includes delay duration)
- **Cancelled**: Flight cancelled
- **Boarding**: Currently boarding passengers
- **Departed**: Flight has departed
- **In Flight**: Flight is in the air
- **Landed**: Flight has arrived

## Integration with Existing System

The multi-agent workflow integrates seamlessly with existing services:

```python
# Uses existing services
flight_service.search_flights(origin, destination)
booking_service.create_booking(passenger, flight)

# Adds new capabilities
weather_service.check_flight_weather(origin, destination)
status_service.check_flight_status(flight_id)

# Coordinates through LangGraph
workflow.run_workflow(request, origin, destination)
```

## Custom Workflow Extension

To add new agents, extend the workflow:

```python
class CustomMultiAgentWorkflow(MultiAgentWorkflow):
    def _build_workflow(self):
        workflow = super()._build_workflow()
        
        # Add custom agent node
        workflow.add_node("price_analysis_agent", self.price_analysis_agent)
        
        # Add to workflow path
        workflow.add_edge("booking_agent", "price_analysis_agent")
        workflow.add_edge("price_analysis_agent", "status_check_agent")
        
        return workflow.compile()
    
    def price_analysis_agent(self, state):
        # Custom agent logic
        return state
```

## Error Handling

The workflow includes comprehensive error handling:

```python
try:
    result = workflow.run_workflow("NYC", "LAX", "London")
except KeyError:
    print("Invalid city name")
except Exception as e:
    print(f"Workflow error: {str(e)}")
```

## Performance Considerations

- **Parallel Execution**: Agents execute sequentially but can be modified for parallel processing
- **State Size**: Efficiently manages workflow state
- **Caching**: Weather and status data can be cached
- **Scalability**: LangGraph allows easy addition of new agents

## Configuration

Environment variables for multi-agent system:

```
# Weather Service
WEATHER_CACHE_TTL=3600
WEATHER_UPDATE_INTERVAL=300

# Status Service
STATUS_REFRESH_INTERVAL=60
STATUS_CACHE_SIZE=1000

# Workflow
MAX_WORKFLOW_TIMEOUT=30
AGENT_EXECUTION_TIMEOUT=10
```

## Testing Multi-Agent Workflows

```python
import pytest
from agent.multiagent_workflow import MultiAgentWorkflow

def test_workflow_execution():
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    result = workflow.run_workflow("test", "NYC", "LAX")
    
    assert result["flight_info"]["found"]
    assert result["weather_info"]["safe_to_fly"]
    assert len(result["recommendations"]) > 0
```

## Debugging Workflows

Enable verbose logging:

```python
workflow = MultiAgentWorkflow(fs, bs, ws, ss)
result = workflow.run_workflow("test", "NYC", "LAX")

# View agent messages for debugging
for msg in result["agent_messages"]:
    print(f"[{msg['agent']}] {msg['result']}")
```

## Next Steps

1. Run the demo: `python main.py`
2. Explore agent interactions
3. Customize agents for your needs
4. Add more service integrations
5. Implement parallel agent execution

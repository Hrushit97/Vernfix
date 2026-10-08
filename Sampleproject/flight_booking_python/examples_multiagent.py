"""
Examples of using the multi-agent workflow system.
This demonstrates how to use LangGraph with multiple specialized agents.
"""

from models.flight import Flight
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from agent.multiagent_workflow import MultiAgentWorkflow


def setup_services():
    """Initialize all services"""
    flight_service = FlightService()
    booking_service = BookingService()
    weather_service = WeatherService()
    status_service = StatusService()
    
    # Add sample flights
    flights = [
        Flight("United Airlines", "New York", "Los Angeles",
               "2024-01-15 08:00", "2024-01-15 11:30", 250, 50),
        Flight("Delta Airlines", "New York", "Miami",
               "2024-01-15 10:00", "2024-01-15 13:45", 180, 40),
        Flight("American Airlines", "Los Angeles", "Chicago",
               "2024-01-15 14:00", "2024-01-15 19:00", 200, 60),
        Flight("Southwest Airlines", "Miami", "Denver",
               "2024-01-15 16:30", "2024-01-15 19:00", 160, 80),
        Flight("United Airlines", "Chicago", "San Francisco",
               "2024-01-16 07:00", "2024-01-16 10:00", 220, 45),
    ]
    
    for flight in flights:
        flight_service.add_flight(flight)
    
    return flight_service, booking_service, weather_service, status_service


def example_1_basic_workflow():
    """Example 1: Basic workflow execution"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Multi-Agent Workflow")
    print("="*70)
    
    fs, bs, ws, ss = setup_services()
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    
    result = workflow.run_workflow(
        user_request="Book a flight from NYC to Los Angeles",
        origin="New York",
        destination="Los Angeles"
    )
    
    print(workflow.format_workflow_result(result))


def example_2_weather_risk_assessment():
    """Example 2: Workflow with weather risk assessment"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Weather Risk Assessment in Workflow")
    print("="*70)
    
    fs, bs, ws, ss = setup_services()
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    
    # Routes with different weather conditions
    routes = [
        ("New York", "Los Angeles", "NYC to LAX (Sunny route)"),
        ("New York", "Miami", "NYC to Miami (Tropical route)"),
        ("Chicago", "Denver", "Chicago to Denver (Mountain route)"),
    ]
    
    for origin, destination, description in routes:
        print(f"\n📍 Testing: {description}")
        result = workflow.run_workflow(
            user_request=f"Check {description}",
            origin=origin,
            destination=destination
        )
        
        weather = result.get("weather_info", {})
        if weather:
            print(f"   Risk Status: {weather.get('risk_status')}")
            print(f"   Safe to Fly: {'✅ Yes' if weather.get('safe_to_fly') else '❌ No'}")
            print(f"   Recommendation: {weather.get('recommendation')}")


def example_3_flight_status_tracking():
    """Example 3: Flight status tracking"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Flight Status Tracking")
    print("="*70)
    
    fs, bs, ws, ss = setup_services()
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    
    # Simulate different flight statuses
    statuses = ["On Time", "Delayed", "Boarding"]
    for status in statuses:
        flight_id = f"FL-{status.upper().replace(' ', '')}"
        ss.update_flight_status(flight_id, status)
    
    result = workflow.run_workflow(
        user_request="Check flight status",
        origin="New York",
        destination="Los Angeles"
    )
    
    print(workflow.format_workflow_result(result))
    
    if result.get("flight_status"):
        print(f"\n✈️  Flight Status Details:")
        print(f"   Status: {result['flight_status']['status']}")
        print(f"   Gate: {result['flight_status']['gate']}")
        print(f"   Terminal: {result['flight_status']['terminal']}")


def example_4_comprehensive_analysis():
    """Example 4: Comprehensive multi-agent analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Comprehensive Multi-Agent Analysis")
    print("="*70)
    
    fs, bs, ws, ss = setup_services()
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    
    # Run analysis for multiple routes
    routes = [
        ("New York", "Los Angeles"),
        ("Miami", "Denver"),
        ("Chicago", "San Francisco"),
    ]
    
    summary = {}
    for origin, destination in routes:
        result = workflow.run_workflow(
            user_request=f"Analyze {origin} to {destination}",
            origin=origin,
            destination=destination
        )
        
        summary[f"{origin} → {destination}"] = {
            "flights_found": result["flight_info"].get("count", 0),
            "weather_safe": result["weather_info"].get("safe_to_fly", False),
            "risk_level": result["weather_info"].get("risk_status", "Unknown"),
            "recommendations": len(result.get("recommendations", []))
        }
    
    print("\n📊 Route Summary:")
    for route, data in summary.items():
        print(f"\n  {route}:")
        print(f"    Flights Found: {data['flights_found']}")
        print(f"    Weather Safe: {'✅' if data['weather_safe'] else '❌'}")
        print(f"    Risk Level: {data['risk_level']}")
        print(f"    Recommendations: {data['recommendations']}")


def example_5_agent_collaboration():
    """Example 5: Agent collaboration showcase"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Agent Collaboration Showcase")
    print("="*70)
    
    fs, bs, ws, ss = setup_services()
    workflow = MultiAgentWorkflow(fs, bs, ws, ss)
    
    result = workflow.run_workflow(
        user_request="Complete flight booking with all checks",
        origin="New York",
        destination="Los Angeles"
    )
    
    print("\n🤖 Agent Collaboration Steps:")
    for i, msg in enumerate(result.get("agent_messages", []), 1):
        print(f"\n  Step {i}: {msg['agent']}")
        print(f"  └─ {msg['result']}")
    
    print("\n💡 Final Recommendations:")
    for i, rec in enumerate(result.get("recommendations", []), 1):
        print(f"  {i}. {rec}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("MULTI-AGENT WORKFLOW EXAMPLES")
    print("Demonstrating LangGraph-based agent orchestration")
    print("="*70)
    
    example_1_basic_workflow()
    example_2_weather_risk_assessment()
    example_3_flight_status_tracking()
    example_4_comprehensive_analysis()
    example_5_agent_collaboration()
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

from models.flight import Flight
from models.passenger import Passenger
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from agent.booking_agent import FlightBookingAgent
from agent.multiagent_workflow import MultiAgentWorkflow
from agent.langgraph_multinode_workflow import LangGraphMultiNodeWorkflow
from agent.langchain_agent import LangChainFlightAgent


def initialize_sample_flights(flight_service: FlightService):
    """Initialize sample flights"""
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
    print("✈️  Sample flights initialized!\n")


def demo_direct_usage(flight_service: FlightService, booking_service: BookingService):
    """Demo direct usage without agent"""
    print("=" * 50)
    print("DIRECT USAGE DEMO")
    print("=" * 50 + "\n")
    
    print("📋 Available Flights:")
    flights = flight_service.list_available_flights()
    for i, flight in enumerate(flights[:3], 1):
        print(f"{i}. {flight['airline']} | {flight['route']} | {flight['departure']} | Seats: {flight['available_seats']}")
    print()
    
    # Book a flight
    print("🎫 Creating Booking...")
    passenger = Passenger("John", "Doe", "john@example.com", "555-0101")
    flight = flight_service.get_all_flights()[0]
    booking = booking_service.create_booking(passenger, flight)
    booking.set_seat_number("12A")
    print("✅ Booking Confirmed!")
    print(f"   Booking ID: {booking.id}")
    print(f"   Passenger: {booking.passenger.get_full_name()}")
    print(f"   Flight: {booking.flight.airline} ({booking.flight.origin} → {booking.flight.destination})")
    print(f"   Seat: {booking.seat_number}")
    print()


def demo_agent_usage(flight_service: FlightService, booking_service: BookingService):
    """Demo agent usage with Claude AI"""
    print("=" * 50)
    print("AI AGENT DEMO")
    print("=" * 50 + "\n")
    
    agent = FlightBookingAgent(flight_service, booking_service)
    
    # Example 1: Search flights
    print("🤖 Agent: 'Find flights from New York to Los Angeles'")
    response = agent.chat("Find flights from New York to Los Angeles")
    print(f"Response:\n{response}\n")
    
    # Example 2: Get stats
    print("🤖 Agent: 'What are the current booking statistics?'")
    response = agent.chat("What are the current booking statistics?")
    print(f"Response:\n{response}\n")
    
    # Example 3: Book a flight
    print("🤖 Agent: 'Book a flight for me. My name is Jane Smith, email is jane@example.com, phone is 555-0102, and I want the first flight from New York to Miami'")
    response = agent.chat(
        "Book a flight for me. My name is Jane Smith, email is jane@example.com, phone is 555-0102, and I want the first flight from New York to Miami"
    )
    print(f"Response:\n{response}\n")


def demo_multiagent_workflow(flight_service: FlightService,
                              booking_service: BookingService):
    """Demo multi-agent workflow with LangGraph"""
    print("=" * 60)
    print("MULTI-AGENT WORKFLOW DEMO (LangGraph)")
    print("=" * 60 + "\n")

    # Initialize additional services
    weather_service = WeatherService()
    status_service = StatusService()

    # Create workflow
    workflow = MultiAgentWorkflow(
        flight_service,
        booking_service,
        weather_service,
        status_service
    )

    # Example 1: Search with weather check
    print("Example 1: Flight Search with Weather Analysis")
    result = workflow.run_workflow(
        user_request="Check flights and weather conditions",
        origin="New York",
        destination="Los Angeles"
    )
    print(workflow.format_workflow_result(result))

    # Example 2: Different route
    print("\nExample 2: Miami to Denver with Status Check")
    result = workflow.run_workflow(
        user_request="Check Miami to Denver flights",
        origin="Miami",
        destination="Denver"
    )
    print(workflow.format_workflow_result(result))


def demo_langgraph_multinode(flight_service: FlightService,
                              booking_service: BookingService):
    """Demo advanced LangGraph multi-node workflow"""
    print("\n" + "=" * 70)
    print("ADVANCED LANGGRAPH MULTI-NODE WORKFLOW DEMO")
    print("=" * 70 + "\n")

    weather_service = WeatherService()
    status_service = StatusService()

    workflow = LangGraphMultiNodeWorkflow(
        flight_service, booking_service, weather_service, status_service
    )

    # Run workflow
    result = workflow.run_workflow(
        user_request="Complete flight booking with weather analysis",
        origin="New York",
        destination="Los Angeles"
    )

    print(workflow.format_result(result))


def demo_langchain_agent(flight_service: FlightService,
                         booking_service: BookingService):
    """Demo advanced LangChain agent with MCP tools"""
    print("\n" + "=" * 70)
    print("ADVANCED LANGCHAIN AGENT WITH MCP TOOLS DEMO")
    print("=" * 70 + "\n")

    weather_service = WeatherService()
    status_service = StatusService()

    agent = LangChainFlightAgent(
        flight_service, booking_service, weather_service, status_service
    )

    # Example interactions
    queries = [
        "Find flights from New York to Los Angeles with weather check",
        "What are the safety risks for Miami to Denver flights?",
        "Book a flight for John Doe (john@example.com, 555-0101) to LAX"
    ]

    for query in queries[:2]:  # Limit to avoid API overload
        print(f"\n🤖 Query: {query}")
        response = agent.chat(query)
        print(f"Response: {response}\n")


def main():
    """Main application"""
    print("\n" + "=" * 60)
    print("FLIGHT TICKET BOOKING SYSTEM - PYTHON")
    print("WITH LANGCHAIN & LANGGRAPH MULTI-NODE WORKFLOW")
    print("=" * 60 + "\n")

    # Initialize services
    flight_service = FlightService()
    booking_service = BookingService()

    # Initialize sample data
    initialize_sample_flights(flight_service)

    # Run all demos
    demo_direct_usage(flight_service, booking_service)
    demo_langgraph_multinode(flight_service, booking_service)
    demo_multiagent_workflow(flight_service, booking_service)
    demo_langchain_agent(flight_service, booking_service)
    demo_agent_usage(flight_service, booking_service)
    
    print("=" * 60)
    print("Interactive Mode - Chat with the Agent")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    agent = FlightBookingAgent(flight_service, booking_service)
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")


if __name__ == "__main__":
    main()

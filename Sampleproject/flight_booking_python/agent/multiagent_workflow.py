from typing import Any, Dict, TypedDict
from langgraph.graph import StateGraph, END
from anthropic import Anthropic
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService


class FlightBookingState(TypedDict):
    """State for flight booking workflow"""
    user_request: str
    origin: str
    destination: str
    departure_date: str
    flight_info: Dict[str, Any]
    weather_info: Dict[str, Any]
    flight_status: Dict[str, Any]
    booking_info: Dict[str, Any]
    recommendations: list
    messages: list


class MultiAgentWorkflow:
    """Multi-agent workflow using LangGraph for flight booking system"""
    
    def __init__(self, flight_service: FlightService, 
                 booking_service: BookingService,
                 weather_service: WeatherService,
                 status_service: StatusService):
        self.flight_service = flight_service
        self.booking_service = booking_service
        self.weather_service = weather_service
        self.status_service = status_service
        self.client = Anthropic()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(FlightBookingState)
        
        # Add nodes
        workflow.add_node("flight_search_agent", self.flight_search_agent)
        workflow.add_node("weather_check_agent", self.weather_check_agent)
        workflow.add_node("booking_agent", self.booking_agent)
        workflow.add_node("status_check_agent", self.status_check_agent)
        workflow.add_node("recommendation_agent", self.recommendation_agent)
        
        # Add edges
        workflow.add_edge("flight_search_agent", "weather_check_agent")
        workflow.add_edge("weather_check_agent", "booking_agent")
        workflow.add_conditional_edges(
            "booking_agent",
            self._should_check_status,
            {
                True: "status_check_agent",
                False: "recommendation_agent"
            }
        )
        workflow.add_edge("status_check_agent", "recommendation_agent")
        workflow.add_edge("recommendation_agent", END)
        
        # Set entry point
        workflow.set_entry_point("flight_search_agent")
        
        return workflow.compile()
    
    def _should_check_status(self, state: FlightBookingState) -> bool:
        """Decide if we should check flight status"""
        return "booking_info" in state and state["booking_info"]
    
    def flight_search_agent(self, state: FlightBookingState) -> FlightBookingState:
        """Agent responsible for searching flights"""
        print("🔍 Flight Search Agent: Searching for flights...")
        
        flights = self.flight_service.search_flights(state["origin"], state["destination"])
        
        if flights:
            state["flight_info"] = {
                "found": True,
                "count": len(flights),
                "flights": [f.get_flight_info() for f in flights[:3]]
            }
        else:
            state["flight_info"] = {"found": False, "count": 0}
        
        state["messages"].append({
            "agent": "Flight Search Agent",
            "result": f"Found {len(flights)} flights from {state['origin']} to {state['destination']}"
        })
        
        return state
    
    def weather_check_agent(self, state: FlightBookingState) -> FlightBookingState:
        """Agent responsible for checking weather conditions"""
        print("🌤️  Weather Check Agent: Checking weather conditions...")
        
        weather = self.weather_service.check_flight_weather(state["origin"], state["destination"])
        
        state["weather_info"] = {
            "origin": weather["origin_weather"],
            "destination": weather["destination_weather"],
            "risk_status": weather["risk_status"],
            "recommendation": weather["recommendation"],
            "safe_to_fly": weather["safe_to_fly"]
        }
        
        state["messages"].append({
            "agent": "Weather Check Agent",
            "result": f"Weather Status: {weather['risk_status']} - {weather['recommendation']}"
        })
        
        return state
    
    def booking_agent(self, state: FlightBookingState) -> FlightBookingState:
        """Agent responsible for managing bookings"""
        print("🎫 Booking Agent: Processing booking...")
        
        if state["flight_info"].get("found"):
            # Simulate booking creation
            state["booking_info"] = {
                "status": "PENDING",
                "booking_id": "BK-12345",
                "flight_id": state["flight_info"]["flights"][0]["id"] if state["flight_info"]["flights"] else None,
                "message": "Booking ready - awaiting confirmation"
            }
            
            state["messages"].append({
                "agent": "Booking Agent",
                "result": "Booking prepared and ready for confirmation"
            })
        else:
            state["booking_info"] = None
        
        return state
    
    def status_check_agent(self, state: FlightBookingState) -> FlightBookingState:
        """Agent responsible for checking flight status"""
        print("📊 Status Check Agent: Checking flight status...")
        
        if state["booking_info"] and state["booking_info"]["flight_id"]:
            flight_status = self.status_service.check_flight_status(
                state["booking_info"]["flight_id"]
            )
            
            state["flight_status"] = flight_status
            
            state["messages"].append({
                "agent": "Status Check Agent",
                "result": f"Flight Status: {flight_status['status']} at Gate {flight_status['gate']}"
            })
        
        return state
    
    def recommendation_agent(self, state: FlightBookingState) -> FlightBookingState:
        """Agent responsible for providing recommendations"""
        print("💡 Recommendation Agent: Generating recommendations...")
        
        recommendations = []
        
        # Flight availability recommendation
        if state["flight_info"].get("found"):
            recommendations.append("✅ Flights are available for your route")
        else:
            recommendations.append("❌ No flights found - consider alternative dates")
        
        # Weather recommendation
        if state["weather_info"]["safe_to_fly"]:
            recommendations.append(f"✅ Weather conditions are {state['weather_info']['risk_status'].lower()}")
        else:
            recommendations.append(f"⚠️  {state['weather_info']['recommendation']}")
        
        # Status recommendation
        if state.get("flight_status"):
            status = state["flight_status"]["status"]
            if "Delayed" in status:
                recommendations.append(f"⚠️  Flight is delayed by {state['flight_status'].get('delay_minutes', 0)} minutes")
            else:
                recommendations.append(f"✅ Flight status: {status}")
        
        state["recommendations"] = recommendations
        
        state["messages"].append({
            "agent": "Recommendation Agent",
            "result": "Recommendations generated successfully"
        })
        
        return state
    
    def run_workflow(self, user_request: str, origin: str, 
                     destination: str, departure_date: str = None) -> Dict:
        """Run the complete workflow"""
        print(f"\n🚀 Starting Multi-Agent Workflow for: {user_request}\n")
        
        initial_state: FlightBookingState = {
            "user_request": user_request,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date or "2024-01-15",
            "flight_info": {},
            "weather_info": {},
            "flight_status": {},
            "booking_info": {},
            "recommendations": [],
            "messages": []
        }
        
        # Execute the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "user_request": final_state["user_request"],
            "origin": final_state["origin"],
            "destination": final_state["destination"],
            "flight_info": final_state.get("flight_info"),
            "weather_info": final_state.get("weather_info"),
            "flight_status": final_state.get("flight_status"),
            "recommendations": final_state.get("recommendations", []),
            "agent_messages": final_state.get("messages", [])
        }
    
    def format_workflow_result(self, result: Dict) -> str:
        """Format workflow result for display"""
        output = []
        output.append("\n" + "="*60)
        output.append("MULTI-AGENT WORKFLOW RESULTS")
        output.append("="*60)
        
        output.append(f"\n📍 Route: {result['origin']} → {result['destination']}")
        
        if result.get("flight_info", {}).get("found"):
            output.append(f"✈️  Flights Found: {result['flight_info']['count']}")
        else:
            output.append("✈️  No flights found")
        
        output.append("\n🌤️  Weather Information:")
        if result.get("weather_info"):
            origin_weather = result["weather_info"].get("origin", {})
            dest_weather = result["weather_info"].get("destination", {})
            output.append(f"  Origin: {origin_weather.get('condition')} ({origin_weather.get('temp')}°F)")
            output.append(f"  Destination: {dest_weather.get('condition')} ({dest_weather.get('temp')}°F)")
        
        output.append("\n💡 Recommendations:")
        for rec in result.get("recommendations", []):
            output.append(f"  {rec}")
        
        output.append("\n📋 Agent Activities:")
        for msg in result.get("agent_messages", []):
            output.append(f"  [{msg['agent']}] {msg['result']}")
        
        output.append("\n" + "="*60)
        
        return "\n".join(output)

"""
Advanced LangGraph multi-node workflow with LangChain integration
Implements a sophisticated flight booking system with weather detection and multi-agent tools
"""

from typing import Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from anthropic import Anthropic
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from tools.enhanced_mcp_tools import EnhancedMCPTools


class AgentState(TypedDict):
    """Advanced state for multi-node workflow"""
    messages: Annotated[list[BaseMessage], add_messages]
    user_request: str
    origin: str
    destination: str
    departure_date: str
    flight_data: dict
    weather_data: dict
    status_data: dict
    booking_data: dict
    tool_calls: list
    recommendations: list
    current_node: str
    error_state: str | None
    decision_checkpoint: str


class LangGraphMultiNodeWorkflow:
    """
    Advanced LangGraph workflow with multiple specialized nodes.
    Each node handles a specific aspect of flight booking with weather integration.
    """
    
    def __init__(self, flight_service: FlightService,
                 booking_service: BookingService,
                 weather_service: WeatherService,
                 status_service: StatusService):
        self.flight_service = flight_service
        self.booking_service = booking_service
        self.weather_service = weather_service
        self.status_service = status_service
        self.mcp_tools = EnhancedMCPTools(
            flight_service, booking_service, weather_service, status_service
        )
        self.client = Anthropic()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow with multiple nodes"""
        workflow = StateGraph(AgentState)
        
        # Add all nodes
        workflow.add_node("input_validator", self.input_validator_node)
        workflow.add_node("flight_search", self.flight_search_node)
        workflow.add_node("weather_analyzer", self.weather_analyzer_node)
        workflow.add_node("risk_assessor", self.risk_assessor_node)
        workflow.add_node("booking_processor", self.booking_processor_node)
        workflow.add_node("status_monitor", self.status_monitor_node)
        workflow.add_node("recommendation_generator", self.recommendation_generator_node)
        workflow.add_node("error_handler", self.error_handler_node)
        workflow.add_node("final_output", self.final_output_node)
        
        # Define edges for sequential and conditional routing
        workflow.add_edge("input_validator", "flight_search")
        workflow.add_edge("flight_search", "weather_analyzer")
        workflow.add_edge("weather_analyzer", "risk_assessor")
        
        # Conditional edge based on risk assessment
        workflow.add_conditional_edges(
            "risk_assessor",
            self._route_on_risk,
            {
                "safe": "booking_processor",
                "warning": "recommendation_generator",
                "critical": "error_handler"
            }
        )
        
        workflow.add_edge("booking_processor", "status_monitor")
        workflow.add_edge("status_monitor", "recommendation_generator")
        workflow.add_edge("recommendation_generator", "final_output")
        workflow.add_edge("error_handler", "final_output")
        workflow.add_edge("final_output", END)
        
        # Set entry point
        workflow.set_entry_point("input_validator")
        
        return workflow.compile()
    
    def _route_on_risk(self, state: AgentState) -> str:
        """Route based on weather risk assessment"""
        if not state.get("weather_data"):
            return "booking_processor"
        
        risk_status = state["weather_data"].get("risk_status", "Low")
        
        if risk_status == "Critical":
            return "error_handler"
        elif risk_status in ["High", "Moderate"]:
            return "recommendation_generator"
        return "booking_processor"
    
    def input_validator_node(self, state: AgentState) -> AgentState:
        """Validate and normalize input"""
        print("🔍 Input Validator Node: Validating request...")
        
        if not state.get("origin") or not state.get("destination"):
            state["error_state"] = "Missing origin or destination"
        
        state["current_node"] = "input_validator"
        state["messages"].append(HumanMessage(
            content=f"Validating request: {state['origin']} to {state['destination']}"
        ))
        
        return state
    
    def flight_search_node(self, state: AgentState) -> AgentState:
        """Search for available flights"""
        print("✈️  Flight Search Node: Searching flights...")
        
        try:
            flights = self.flight_service.search_flights(
                state["origin"], 
                state["destination"]
            )
            
            state["flight_data"] = {
                "count": len(flights),
                "flights": [f.get_flight_info() for f in flights[:5]],
                "found": len(flights) > 0
            }
            
            state["current_node"] = "flight_search"
            state["messages"].append(AIMessage(
                content=f"Found {len(flights)} flights from {state['origin']} to {state['destination']}"
            ))
        except Exception as e:
            state["error_state"] = f"Flight search error: {str(e)}"
        
        return state
    
    def weather_analyzer_node(self, state: AgentState) -> AgentState:
        """Analyze weather conditions"""
        print("🌤️  Weather Analyzer Node: Checking weather...")
        
        try:
            weather = self.weather_service.check_flight_weather(
                state["origin"],
                state["destination"]
            )
            
            state["weather_data"] = {
                "origin_weather": weather["origin_weather"],
                "destination_weather": weather["destination_weather"],
                "risk_status": weather["risk_status"],
                "safe_to_fly": weather["safe_to_fly"],
                "recommendation": weather["recommendation"]
            }
            
            state["current_node"] = "weather_analyzer"
            state["messages"].append(AIMessage(
                content=f"Weather analysis: {weather['risk_status']} risk - {weather['recommendation']}"
            ))
        except Exception as e:
            state["error_state"] = f"Weather analysis error: {str(e)}"
        
        return state
    
    def risk_assessor_node(self, state: AgentState) -> AgentState:
        """Assess overall risk and safety"""
        print("⚠️  Risk Assessor Node: Assessing risk...")
        
        risk_assessment = {
            "flight_available": state["flight_data"].get("found", False),
            "weather_safe": state["weather_data"].get("safe_to_fly", False),
            "overall_risk": "high" if not state["weather_data"].get("safe_to_fly") else "low"
        }
        
        state["decision_checkpoint"] = "risk_assessed"
        state["current_node"] = "risk_assessor"
        
        return state
    
    def booking_processor_node(self, state: AgentState) -> AgentState:
        """Process booking if conditions are met"""
        print("🎫 Booking Processor Node: Processing booking...")
        
        if state["flight_data"].get("found") and state["weather_data"].get("safe_to_fly"):
            state["booking_data"] = {
                "status": "confirmed",
                "booking_id": f"BK-{id(state)}",
                "message": "Booking confirmed"
            }
        else:
            state["booking_data"] = {
                "status": "pending",
                "message": "Booking conditions not met"
            }
        
        state["current_node"] = "booking_processor"
        
        return state
    
    def status_monitor_node(self, state: AgentState) -> AgentState:
        """Monitor flight status"""
        print("📊 Status Monitor Node: Checking status...")
        
        if state["booking_data"].get("status") == "confirmed":
            flight_id = state["flight_data"]["flights"][0]["id"] if state["flight_data"]["flights"] else None
            
            if flight_id:
                status = self.status_service.check_flight_status(flight_id)
                state["status_data"] = status
        
        state["current_node"] = "status_monitor"
        
        return state
    
    def recommendation_generator_node(self, state: AgentState) -> AgentState:
        """Generate consolidated recommendations"""
        print("💡 Recommendation Generator Node: Generating recommendations...")
        
        recommendations = []
        
        if state["flight_data"].get("found"):
            recommendations.append("✅ Flights are available")
        else:
            recommendations.append("❌ No flights found")
        
        if state["weather_data"].get("safe_to_fly"):
            recommendations.append("✅ Weather conditions are safe")
        else:
            recommendations.append(f"⚠️  {state['weather_data'].get('recommendation')}")
        
        state["recommendations"] = recommendations
        state["current_node"] = "recommendation_generator"
        
        return state
    
    def error_handler_node(self, state: AgentState) -> AgentState:
        """Handle errors and critical situations"""
        print("❌ Error Handler Node: Handling error...")
        
        state["current_node"] = "error_handler"
        
        if state.get("error_state"):
            state["messages"].append(AIMessage(content=f"Error: {state['error_state']}"))
        
        state["recommendations"] = ["⚠️  Critical conditions detected. Please try again later."]
        
        return state
    
    def final_output_node(self, state: AgentState) -> AgentState:
        """Prepare final output"""
        print("📋 Final Output Node: Preparing output...")
        
        state["current_node"] = "final_output"
        
        return state
    
    def run_workflow(self, user_request: str, origin: str,
                    destination: str, departure_date: str = None) -> dict:
        """Execute the complete workflow"""
        print(f"\n{'='*70}")
        print(f"🚀 Starting Advanced LangGraph Multi-Node Workflow")
        print(f"{'='*70}\n")
        
        initial_state: AgentState = {
            "messages": [HumanMessage(content=user_request)],
            "user_request": user_request,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date or "2024-01-15",
            "flight_data": {},
            "weather_data": {},
            "status_data": {},
            "booking_data": {},
            "tool_calls": [],
            "recommendations": [],
            "current_node": "start",
            "error_state": None,
            "decision_checkpoint": None
        }
        
        # Execute workflow
        final_state = self.graph.invoke(initial_state)
        
        return {
            "user_request": final_state["user_request"],
            "origin": final_state["origin"],
            "destination": final_state["destination"],
            "flight_data": final_state.get("flight_data"),
            "weather_data": final_state.get("weather_data"),
            "status_data": final_state.get("status_data"),
            "booking_data": final_state.get("booking_data"),
            "recommendations": final_state.get("recommendations", []),
            "messages": [str(m) for m in final_state.get("messages", [])],
            "execution_path": final_state.get("current_node")
        }
    
    def format_result(self, result: dict) -> str:
        """Format workflow result for display"""
        output = []
        output.append("\n" + "="*70)
        output.append("ADVANCED LANGGRAPH MULTI-NODE WORKFLOW RESULTS")
        output.append("="*70)
        
        output.append(f"\n📍 Route: {result['origin']} → {result['destination']}")
        
        if result.get("flight_data", {}).get("found"):
            output.append(f"✈️  Flights Found: {result['flight_data']['count']}")
        
        if result.get("weather_data"):
            output.append(f"\n🌤️  Weather: {result['weather_data'].get('risk_status')}")
        
        output.append("\n💡 Recommendations:")
        for rec in result.get("recommendations", []):
            output.append(f"  {rec}")
        
        output.append("\n" + "="*70 + "\n")
        
        return "\n".join(output)

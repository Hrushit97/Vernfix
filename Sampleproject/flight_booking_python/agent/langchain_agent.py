"""
Advanced LangChain Agent with Tool Integration
Uses Claude model with MCP tools for flight booking operations
"""

import json
from typing import Any, Dict
from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from anthropic import Anthropic
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from tools.enhanced_mcp_tools import EnhancedMCPTools


class LangChainFlightAgent:
    """Advanced LangChain agent for flight booking with tool integration"""
    
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
        self.conversation_history = []
        self.agent_executor = self._setup_agent()
    
    def _setup_agent(self) -> AgentExecutor:
        """Setup LangChain agent with tools"""
        
        # Create LangChain tools
        tools = [
            Tool(
                name="search_flights",
                func=lambda origin, destination: self.mcp_tools.search_flights(origin, destination),
                description="Search for flights between origin and destination cities"
            ),
            Tool(
                name="check_weather",
                func=lambda origin, destination: self.mcp_tools.check_weather(origin, destination),
                description="Check weather conditions at origin and destination"
            ),
            Tool(
                name="assess_risk",
                func=lambda origin, destination: self.mcp_tools.assess_risk(origin, destination),
                description="Assess flight safety risk based on weather conditions"
            ),
            Tool(
                name="book_flight",
                func=lambda flight_id, first_name, last_name, email, phone: 
                    self.mcp_tools.book_flight(flight_id, first_name, last_name, email, phone),
                description="Book a flight for a passenger"
            ),
            Tool(
                name="check_status",
                func=lambda flight_id: self.mcp_tools.check_status(flight_id),
                description="Check real-time flight status"
            ),
            Tool(
                name="get_recommendations",
                func=lambda origin, destination: self.mcp_tools.get_recommendations(origin, destination),
                description="Get AI recommendations for flight selection"
            ),
            Tool(
                name="compare_flights",
                func=lambda flight_ids, compare_by: self.mcp_tools.compare_flights(flight_ids, compare_by),
                description="Compare flights by price, duration, or amenities"
            ),
            Tool(
                name="calculate_cost",
                func=lambda flight_id, num_passengers: 
                    self.mcp_tools.calculate_total_cost(flight_id, num_passengers),
                description="Calculate total flight cost including taxes and fees"
            ),
        ]
        
        # Create LangChain model
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
            max_tokens=2048
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an advanced flight booking assistant powered by LangChain and Claude.
                You have access to comprehensive MCP tools for flight searching, weather checking,
                risk assessment, and booking operations.
                
                Always consider:
                1. Flight availability
                2. Weather conditions at both origin and destination
                3. Safety risk assessment
                4. Cost calculations
                5. Real-time flight status
                
                Provide recommendations based on all available data."""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        
        # Create executor
        executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=10,
            early_stopping_method="force"
        )
        
        return executor
    
    def chat(self, user_message: str) -> str:
        """Send message to agent and get response"""
        try:
            response = self.agent_executor.invoke({
                "input": user_message,
                "chat_history": self.conversation_history
            })
            
            assistant_response = response.get("output", "No response generated")
            
            # Update conversation history
            self.conversation_history.append(("user", user_message))
            self.conversation_history.append(("assistant", assistant_response))
            
            return assistant_response
        
        except Exception as e:
            error_message = f"Agent error: {str(e)}"
            self.conversation_history.append(("user", user_message))
            self.conversation_history.append(("assistant", error_message))
            return error_message
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def process_tool_call(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Process individual tool calls"""
        try:
            tool_map = {
                "search_flights": self.mcp_tools.search_flights,
                "check_weather": self.mcp_tools.check_weather,
                "assess_risk": self.mcp_tools.assess_risk,
                "book_flight": self.mcp_tools.book_flight,
                "check_status": self.mcp_tools.check_status,
                "get_recommendations": self.mcp_tools.get_recommendations,
                "compare_flights": self.mcp_tools.compare_flights,
                "calculate_cost": self.mcp_tools.calculate_total_cost,
            }
            
            tool_func = tool_map.get(tool_name)
            if not tool_func:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})
            
            result = tool_func(**tool_input)
            return json.dumps(result)
        
        except Exception as e:
            return json.dumps({"error": str(e)})

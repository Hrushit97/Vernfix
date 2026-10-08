import json
from typing import Any, Dict, List
from anthropic import Anthropic
from services.flight_service import FlightService
from services.booking_service import BookingService
from tools.mcp_tools import FlightBookingMCPTools


class FlightBookingAgent:
    """AI Agent for Flight Booking using Claude and MCP Tools"""
    
    def __init__(self, flight_service: FlightService, booking_service: BookingService):
        self.client = Anthropic()
        self.flight_service = flight_service
        self.booking_service = booking_service
        self.mcp_tools = FlightBookingMCPTools(flight_service, booking_service)
        self.conversation_history = []
        self.tools_definitions = self._build_tools_definitions()
    
    def _build_tools_definitions(self) -> List[Dict[str, Any]]:
        """Build tool definitions for Claude"""
        return [
            {
                "name": "search_flights",
                "description": "Search for flights by origin and destination cities",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "origin": {"type": "string", "description": "Origin city"},
                        "destination": {"type": "string", "description": "Destination city"}
                    },
                    "required": ["origin", "destination"]
                }
            },
            {
                "name": "list_available_flights",
                "description": "List all currently available flights",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "book_flight",
                "description": "Book a flight for a passenger",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "flight_id": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"}
                    },
                    "required": ["flight_id", "first_name", "last_name", "email", "phone"]
                }
            },
            {
                "name": "cancel_booking",
                "description": "Cancel an existing booking",
                "input_schema": {
                    "type": "object",
                    "properties": {"booking_id": {"type": "string"}},
                    "required": ["booking_id"]
                }
            },
            {
                "name": "get_booking_details",
                "description": "Get details of a specific booking",
                "input_schema": {
                    "type": "object",
                    "properties": {"booking_id": {"type": "string"}},
                    "required": ["booking_id"]
                }
            },
            {
                "name": "get_my_bookings",
                "description": "Get all bookings for a passenger",
                "input_schema": {
                    "type": "object",
                    "properties": {"passenger_id": {"type": "string"}},
                    "required": ["passenger_id"]
                }
            },
            {
                "name": "assign_seat",
                "description": "Assign a seat to a booking",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "booking_id": {"type": "string"},
                        "seat_number": {"type": "string"}
                    },
                    "required": ["booking_id", "seat_number"]
                }
            },
            {
                "name": "get_flight_stats",
                "description": "Get flight statistics",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_booking_stats",
                "description": "Get booking statistics",
                "input_schema": {"type": "object", "properties": {}}
            }
        ]
    
    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool and return result"""
        tool_map = {
            "search_flights": self.mcp_tools.search_flights,
            "list_available_flights": self.mcp_tools.list_available_flights,
            "book_flight": self.mcp_tools.book_flight,
            "cancel_booking": self.mcp_tools.cancel_booking,
            "get_booking_details": self.mcp_tools.get_booking_details,
            "get_my_bookings": self.mcp_tools.get_my_bookings,
            "assign_seat": self.mcp_tools.assign_seat,
            "get_flight_stats": self.mcp_tools.get_flight_stats,
            "get_booking_stats": self.mcp_tools.get_booking_stats,
        }
        
        tool_func = tool_map.get(tool_name)
        if not tool_func:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
        
        try:
            result = tool_func(**tool_input)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def chat(self, user_message: str) -> str:
        """Send a message to the agent and get response"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        while True:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                tools=self.tools_definitions,
                messages=self.conversation_history
            )
            
            if response.stop_reason == "tool_use":
                assistant_message = {"role": "assistant", "content": response.content}
                self.conversation_history.append(assistant_message)
                
                tool_results = []
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_result = self._execute_tool(
                            content_block.name,
                            content_block.input
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": tool_result
                        })
                
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                response_text = ""
                for content_block in response.content:
                    if hasattr(content_block, 'text'):
                        response_text += content_block.text
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                return response_text

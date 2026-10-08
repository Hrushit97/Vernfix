"""
Enhanced MCP (Model Context Protocol) Tools for Flight Booking
Comprehensive tool definitions for multi-agent systems
"""

import json
from typing import Any, Dict, List, Optional
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from models.passenger import Passenger


class EnhancedMCPTools:
    """Enhanced MCP tool suite for flight booking operations"""
    
    def __init__(self, flight_service: FlightService, 
                 booking_service: BookingService,
                 weather_service: WeatherService,
                 status_service: StatusService):
        self.flight_service = flight_service
        self.booking_service = booking_service
        self.weather_service = weather_service
        self.status_service = status_service
    
    def get_tools_definitions(self) -> List[Dict[str, Any]]:
        """Get all MCP tool definitions for Claude"""
        return [
            self._tool_search_flights(),
            self._tool_check_weather(),
            self._tool_assess_risk(),
            self._tool_book_flight(),
            self._tool_check_status(),
            self._tool_get_recommendations(),
            self._tool_compare_flights(),
            self._tool_calculate_total_cost(),
            self._tool_get_flight_details(),
            self._tool_validate_booking(),
        ]
    
    def _tool_search_flights(self) -> Dict[str, Any]:
        """Search flights tool definition"""
        return {
            "name": "search_flights",
            "description": "Search for available flights between two cities",
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin city"},
                    "destination": {"type": "string", "description": "Destination city"},
                    "date": {"type": "string", "description": "Departure date (optional)"}
                },
                "required": ["origin", "destination"]
            }
        }
    
    def _tool_check_weather(self) -> Dict[str, Any]:
        """Weather checking tool definition"""
        return {
            "name": "check_weather",
            "description": "Check weather conditions at origin and destination",
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"}
                },
                "required": ["origin", "destination"]
            }
        }
    
    def _tool_assess_risk(self) -> Dict[str, Any]:
        """Risk assessment tool definition"""
        return {
            "name": "assess_risk",
            "description": "Assess flight safety risk based on weather and conditions",
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "include_weather": {"type": "boolean", "default": True}
                },
                "required": ["origin", "destination"]
            }
        }
    
    def _tool_book_flight(self) -> Dict[str, Any]:
        """Flight booking tool definition"""
        return {
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
        }
    
    def _tool_check_status(self) -> Dict[str, Any]:
        """Flight status checking tool definition"""
        return {
            "name": "check_status",
            "description": "Check real-time flight status",
            "input_schema": {
                "type": "object",
                "properties": {
                    "flight_id": {"type": "string"}
                },
                "required": ["flight_id"]
            }
        }
    
    def _tool_get_recommendations(self) -> Dict[str, Any]:
        """Get recommendations tool definition"""
        return {
            "name": "get_recommendations",
            "description": "Get AI recommendations for flight selection",
            "input_schema": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                    "preferences": {"type": "string"}
                },
                "required": ["origin", "destination"]
            }
        }
    
    def _tool_compare_flights(self) -> Dict[str, Any]:
        """Compare flights tool definition"""
        return {
            "name": "compare_flights",
            "description": "Compare multiple flights by price, duration, or amenities",
            "input_schema": {
                "type": "object",
                "properties": {
                    "flight_ids": {"type": "array", "items": {"type": "string"}},
                    "compare_by": {"type": "string", "enum": ["price", "duration", "amenities"]}
                },
                "required": ["flight_ids", "compare_by"]
            }
        }
    
    def _tool_calculate_total_cost(self) -> Dict[str, Any]:
        """Calculate total cost tool definition"""
        return {
            "name": "calculate_total_cost",
            "description": "Calculate total cost including fees, taxes, insurance",
            "input_schema": {
                "type": "object",
                "properties": {
                    "flight_id": {"type": "string"},
                    "num_passengers": {"type": "integer"},
                    "add_insurance": {"type": "boolean"},
                    "seat_upgrades": {"type": "boolean"}
                },
                "required": ["flight_id", "num_passengers"]
            }
        }
    
    def _tool_get_flight_details(self) -> Dict[str, Any]:
        """Get detailed flight information tool definition"""
        return {
            "name": "get_flight_details",
            "description": "Get comprehensive flight details",
            "input_schema": {
                "type": "object",
                "properties": {
                    "flight_id": {"type": "string"}
                },
                "required": ["flight_id"]
            }
        }
    
    def _tool_validate_booking(self) -> Dict[str, Any]:
        """Validate booking tool definition"""
        return {
            "name": "validate_booking",
            "description": "Validate booking before final confirmation",
            "input_schema": {
                "type": "object",
                "properties": {
                    "booking_id": {"type": "string"},
                    "check_payment": {"type": "boolean"}
                },
                "required": ["booking_id"]
            }
        }
    
    # Tool execution methods
    
    def search_flights(self, origin: str, destination: str, date: str = None) -> Dict:
        """Execute search flights tool"""
        try:
            flights = self.flight_service.search_flights(origin, destination)
            return {
                "status": "success",
                "count": len(flights),
                "flights": [f.get_flight_info() for f in flights[:5]]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_weather(self, origin: str, destination: str) -> Dict:
        """Execute weather checking tool"""
        try:
            weather = self.weather_service.check_flight_weather(origin, destination)
            return {
                "status": "success",
                "origin_weather": weather["origin_weather"],
                "destination_weather": weather["destination_weather"],
                "risk_status": weather["risk_status"],
                "safe_to_fly": weather["safe_to_fly"]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def assess_risk(self, origin: str, destination: str, include_weather: bool = True) -> Dict:
        """Execute risk assessment tool"""
        try:
            if include_weather:
                weather = self.weather_service.check_flight_weather(origin, destination)
                risk_score = 0 if weather["safe_to_fly"] else 10
                return {
                    "status": "success",
                    "risk_level": weather["risk_status"],
                    "safe": weather["safe_to_fly"],
                    "recommendation": weather["recommendation"]
                }
            return {"status": "success", "risk_level": "Low", "safe": True}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def book_flight(self, flight_id: str, first_name: str, last_name: str,
                   email: str, phone: str) -> Dict:
        """Execute flight booking tool"""
        try:
            flight = self.flight_service.get_flight_by_id(flight_id)
            if not flight:
                return {"status": "error", "message": "Flight not found"}
            
            passenger = Passenger(first_name, last_name, email, phone)
            booking = self.booking_service.create_booking(passenger, flight)
            
            return {
                "status": "success",
                "booking_id": booking.id,
                "details": booking.get_booking_details()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_status(self, flight_id: str) -> Dict:
        """Execute status checking tool"""
        try:
            status = self.status_service.check_flight_status(flight_id)
            return {"status": "success", "data": status}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_recommendations(self, origin: str, destination: str, 
                           preferences: str = None) -> Dict:
        """Execute recommendations tool"""
        try:
            flights = self.flight_service.search_flights(origin, destination)
            weather = self.weather_service.check_flight_weather(origin, destination)
            
            recommendations = []
            if weather["safe_to_fly"]:
                recommendations.append("✅ Weather conditions are favorable")
            else:
                recommendations.append(f"⚠️  {weather['recommendation']}")
            
            return {
                "status": "success",
                "recommendations": recommendations,
                "best_options": [f.get_flight_info() for f in flights[:3]]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def compare_flights(self, flight_ids: List[str], compare_by: str) -> Dict:
        """Execute flight comparison tool"""
        try:
            flights = [self.flight_service.get_flight_by_id(fid) for fid in flight_ids]
            flights = [f for f in flights if f]
            
            if compare_by == "price":
                flights.sort(key=lambda f: f.price)
            
            return {
                "status": "success",
                "comparison": [f.get_flight_info() for f in flights]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def calculate_total_cost(self, flight_id: str, num_passengers: int,
                            add_insurance: bool = False,
                            seat_upgrades: bool = False) -> Dict:
        """Execute cost calculation tool"""
        try:
            flight = self.flight_service.get_flight_by_id(flight_id)
            if not flight:
                return {"status": "error", "message": "Flight not found"}
            
            base_cost = flight.price * num_passengers
            taxes = base_cost * 0.12
            insurance = (base_cost * 0.05) if add_insurance else 0
            upgrades = (base_cost * 0.10) if seat_upgrades else 0
            
            total = base_cost + taxes + insurance + upgrades
            
            return {
                "status": "success",
                "breakdown": {
                    "base_fare": base_cost,
                    "taxes": taxes,
                    "insurance": insurance,
                    "upgrades": upgrades,
                    "total": total
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_flight_details(self, flight_id: str) -> Dict:
        """Execute get flight details tool"""
        try:
            flight = self.flight_service.get_flight_by_id(flight_id)
            if not flight:
                return {"status": "error", "message": "Flight not found"}
            
            return {
                "status": "success",
                "details": flight.to_dict()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def validate_booking(self, booking_id: str, check_payment: bool = False) -> Dict:
        """Execute booking validation tool"""
        try:
            booking = self.booking_service.get_booking_by_id(booking_id)
            if not booking:
                return {"status": "error", "message": "Booking not found"}
            
            return {
                "status": "success",
                "valid": True,
                "booking": booking.get_booking_details()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

import json
from typing import Any, Dict
from services.flight_service import FlightService
from services.booking_service import BookingService
from models.flight import Flight
from models.passenger import Passenger


class FlightBookingMCPTools:
    """MCP Tools for Flight Booking System"""
    
    def __init__(self, flight_service: FlightService, booking_service: BookingService):
        self.flight_service = flight_service
        self.booking_service = booking_service
    
    def get_tools(self) -> list:
        """Get all available tools"""
        return [
            self._create_tool_definition("search_flights", self.search_flights),
            self._create_tool_definition("list_available_flights", self.list_available_flights),
            self._create_tool_definition("book_flight", self.book_flight),
            self._create_tool_definition("cancel_booking", self.cancel_booking),
            self._create_tool_definition("get_booking_details", self.get_booking_details),
            self._create_tool_definition("get_my_bookings", self.get_my_bookings),
            self._create_tool_definition("get_flight_stats", self.get_flight_stats),
            self._create_tool_definition("get_booking_stats", self.get_booking_stats),
            self._create_tool_definition("assign_seat", self.assign_seat),
        ]
    
    def _create_tool_definition(self, name: str, func) -> Dict[str, Any]:
        """Create tool definition"""
        return {
            "name": name,
            "description": func.__doc__ or "Tool description",
            "function": func
        }
    
    def search_flights(self, origin: str, destination: str) -> Dict[str, Any]:
        """Search flights by origin and destination"""
        try:
            flights = self.flight_service.search_flights(origin, destination)
            return {
                "status": "success",
                "data": [f.get_flight_info() for f in flights],
                "count": len(flights)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def list_available_flights(self) -> Dict[str, Any]:
        """List all available flights"""
        try:
            flights = self.flight_service.list_available_flights()
            return {
                "status": "success",
                "data": flights,
                "count": len(flights)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def book_flight(self, flight_id: str, first_name: str, last_name: str,
                   email: str, phone: str) -> Dict[str, Any]:
        """Book a flight for a passenger"""
        try:
            flight = self.flight_service.get_flight_by_id(flight_id)
            if not flight:
                return {"status": "error", "message": "Flight not found"}
            
            passenger = Passenger(first_name, last_name, email, phone)
            booking = self.booking_service.create_booking(passenger, flight)
            
            return {
                "status": "success",
                "data": booking.get_booking_details(),
                "booking_id": booking.id
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """Cancel a booking"""
        try:
            booking = self.booking_service.cancel_booking(booking_id)
            return {
                "status": "success",
                "data": booking.get_booking_details()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_booking_details(self, booking_id: str) -> Dict[str, Any]:
        """Get booking details"""
        try:
            booking = self.booking_service.get_booking_by_id(booking_id)
            if not booking:
                return {"status": "error", "message": "Booking not found"}
            
            return {
                "status": "success",
                "data": booking.get_booking_details()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_my_bookings(self, passenger_id: str) -> Dict[str, Any]:
        """Get bookings for a passenger"""
        try:
            bookings = self.booking_service.get_bookings_by_passenger(passenger_id)
            return {
                "status": "success",
                "data": [b.get_booking_details() for b in bookings],
                "count": len(bookings)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_flight_stats(self) -> Dict[str, Any]:
        """Get flight statistics"""
        try:
            stats = self.flight_service.get_flight_stats()
            return {"status": "success", "data": stats}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_booking_stats(self) -> Dict[str, Any]:
        """Get booking statistics"""
        try:
            stats = self.booking_service.get_booking_stats()
            return {"status": "success", "data": stats}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def assign_seat(self, booking_id: str, seat_number: str) -> Dict[str, Any]:
        """Assign a seat to a booking"""
        try:
            booking = self.booking_service.assign_seat(booking_id, seat_number)
            return {
                "status": "success",
                "data": booking.get_booking_details()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

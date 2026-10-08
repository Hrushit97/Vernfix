from typing import List, Optional
from models.flight import Flight


class FlightService:
    """Service for managing flights"""
    
    def __init__(self):
        self.flights: List[Flight] = []
    
    def add_flight(self, flight: Flight) -> Flight:
        """Add a new flight"""
        self.flights.append(flight)
        return flight
    
    def get_all_flights(self) -> List[Flight]:
        """Get all flights"""
        return self.flights
    
    def get_flight_by_id(self, flight_id: str) -> Optional[Flight]:
        """Get flight by ID"""
        for flight in self.flights:
            if flight.id == flight_id:
                return flight
        return None
    
    def search_flights(self, origin: str, destination: str) -> List[Flight]:
        """Search flights by origin and destination"""
        return [
            f for f in self.flights
            if f.origin.lower() == origin.lower() and
               f.destination.lower() == destination.lower() and
               f.is_available()
        ]
    
    def search_by_route_and_date(self, origin: str, destination: str, 
                                 departure_date: str) -> List[Flight]:
        """Search flights by route and date"""
        return [
            f for f in self.flights
            if f.origin.lower() == origin.lower() and
               f.destination.lower() == destination.lower() and
               f.departure_time.startswith(departure_date) and
               f.is_available()
        ]
    
    def list_available_flights(self) -> List[dict]:
        """Get list of available flights"""
        return [f.get_flight_info() for f in self.flights if f.is_available()]
    
    def get_flight_stats(self) -> dict:
        """Get flight statistics"""
        available = sum(1 for f in self.flights if f.is_available())
        booked = len(self.flights) - available
        return {
            "total_flights": len(self.flights),
            "available_flights": available,
            "booked_flights": booked
        }
    
    def delete_flight(self, flight_id: str) -> bool:
        """Delete a flight"""
        self.flights = [f for f in self.flights if f.id != flight_id]
        return True

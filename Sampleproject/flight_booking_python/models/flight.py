from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Flight:
    """Flight model for flight ticket booking system"""
    
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: float
    available_seats: int = 100
    id: str = field(default_factory=lambda: str(uuid4()))
    total_seats: int = field(default=100, init=False)
    
    def __post_init__(self):
        self.total_seats = self.available_seats
    
    def is_available(self) -> bool:
        """Check if flight has available seats"""
        return self.available_seats > 0
    
    def book_seat(self) -> bool:
        """Book a seat on the flight"""
        if self.available_seats > 0:
            self.available_seats -= 1
            return True
        return False
    
    def cancel_seat(self) -> bool:
        """Cancel a seat booking"""
        if self.available_seats < self.total_seats:
            self.available_seats += 1
            return True
        return False
    
    def get_flight_info(self) -> dict:
        """Get flight information"""
        return {
            "id": self.id,
            "airline": self.airline,
            "route": f"{self.origin} → {self.destination}",
            "departure": self.departure_time,
            "arrival": self.arrival_time,
            "price": f"${self.price}",
            "available_seats": self.available_seats,
            "status": "Available" if self.is_available() else "Full"
        }
    
    def to_dict(self) -> dict:
        """Convert flight to dictionary"""
        return {
            "id": self.id,
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price,
            "available_seats": self.available_seats,
            "total_seats": self.total_seats
        }

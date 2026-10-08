from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .passenger import Passenger
    from .flight import Flight


@dataclass
class Booking:
    """Booking model for flight ticket booking system"""
    
    passenger: 'Passenger'
    flight: 'Flight'
    id: str = field(default_factory=lambda: str(uuid4()))
    booking_date: datetime = field(default_factory=datetime.now)
    seat_number: str = None
    status: str = "Confirmed"
    total_price: float = field(init=False)
    
    def __post_init__(self):
        self.total_price = self.flight.price
    
    def set_seat_number(self, seat_number: str) -> None:
        """Set seat number for booking"""
        self.seat_number = seat_number
    
    def cancel(self) -> None:
        """Cancel the booking"""
        self.status = "Cancelled"
    
    def get_booking_details(self) -> dict:
        """Get booking details"""
        return {
            "booking_id": self.id,
            "passenger_name": self.passenger.get_full_name(),
            "passenger_email": self.passenger.email,
            "flight_id": self.flight.id,
            "airline": self.flight.airline,
            "route": f"{self.flight.origin} → {self.flight.destination}",
            "departure_time": self.flight.departure_time,
            "arrival_time": self.flight.arrival_time,
            "seat_number": self.seat_number or "Unassigned",
            "total_price": f"${self.total_price}",
            "status": self.status,
            "booking_date": self.booking_date.isoformat()
        }
    
    def to_dict(self) -> dict:
        """Convert booking to dictionary"""
        return {
            "id": self.id,
            "passenger_id": self.passenger.id,
            "flight_id": self.flight.id,
            "seat_number": self.seat_number,
            "status": self.status,
            "total_price": self.total_price,
            "booking_date": self.booking_date.isoformat()
        }

from typing import List, Optional
from models.booking import Booking
from models.passenger import Passenger
from models.flight import Flight


class BookingService:
    """Service for managing bookings"""
    
    def __init__(self):
        self.bookings: List[Booking] = []
    
    def create_booking(self, passenger: Passenger, flight: Flight) -> Booking:
        """Create a new booking"""
        if not flight.book_seat():
            raise Exception("No seats available on this flight")
        
        booking = Booking(passenger, flight)
        self.bookings.append(booking)
        return booking
    
    def get_all_bookings(self) -> List[Booking]:
        """Get all bookings"""
        return self.bookings
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Booking]:
        """Get booking by ID"""
        for booking in self.bookings:
            if booking.id == booking_id:
                return booking
        return None
    
    def get_bookings_by_passenger(self, passenger_id: str) -> List[Booking]:
        """Get bookings for a passenger"""
        return [b for b in self.bookings if b.passenger.id == passenger_id]
    
    def cancel_booking(self, booking_id: str) -> Booking:
        """Cancel a booking"""
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise Exception("Booking not found")
        
        booking.cancel()
        booking.flight.cancel_seat()
        return booking
    
    def assign_seat(self, booking_id: str, seat_number: str) -> Booking:
        """Assign a seat to booking"""
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise Exception("Booking not found")
        
        booking.set_seat_number(seat_number)
        return booking
    
    def get_booking_stats(self) -> dict:
        """Get booking statistics"""
        confirmed = sum(1 for b in self.bookings if b.status == "Confirmed")
        cancelled = sum(1 for b in self.bookings if b.status == "Cancelled")
        revenue = sum(b.total_price for b in self.bookings if b.status == "Confirmed")
        
        return {
            "total_bookings": len(self.bookings),
            "confirmed_bookings": confirmed,
            "cancelled_bookings": cancelled,
            "total_revenue": revenue
        }

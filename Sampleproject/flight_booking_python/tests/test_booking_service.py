import pytest
from models.flight import Flight
from models.passenger import Passenger
from services.booking_service import BookingService


def test_create_booking():
    """Test creating a booking"""
    booking_service = BookingService()
    passenger = Passenger("John", "Doe", "john@example.com", "555-0101")
    flight = Flight("United", "NYC", "LAX", "2024-01-15 08:00", "2024-01-15 11:30", 250, 100)
    
    booking = booking_service.create_booking(passenger, flight)
    assert booking.id
    assert booking.status == "Confirmed"
    assert flight.available_seats == 99


def test_cannot_book_full_flight():
    """Test cannot book when flight is full"""
    booking_service = BookingService()
    passenger = Passenger("Jane", "Smith", "jane@example.com", "555-0102")
    flight = Flight("Delta", "NYC", "MIA", "2024-01-15 10:00", "2024-01-15 13:45", 180, 0)
    
    with pytest.raises(Exception):
        booking_service.create_booking(passenger, flight)


def test_get_all_bookings():
    """Test getting all bookings"""
    booking_service = BookingService()
    passenger1 = Passenger("John", "Doe", "john@example.com", "555-0101")
    flight1 = Flight("United", "NYC", "LAX", "2024-01-15 08:00", "2024-01-15 11:30", 250, 100)
    passenger2 = Passenger("Jane", "Smith", "jane@example.com", "555-0102")
    flight2 = Flight("Delta", "NYC", "MIA", "2024-01-15 10:00", "2024-01-15 13:45", 180, 100)
    
    booking_service.create_booking(passenger1, flight1)
    booking_service.create_booking(passenger2, flight2)
    bookings = booking_service.get_all_bookings()
    
    assert len(bookings) == 2


def test_cancel_booking():
    """Test cancelling a booking"""
    booking_service = BookingService()
    passenger = Passenger("Bob", "Johnson", "bob@example.com", "555-0103")
    flight = Flight("American", "LAX", "CHI", "2024-01-15 14:00", "2024-01-15 19:00", 200, 100)
    booking = booking_service.create_booking(passenger, flight)
    
    booking_service.cancel_booking(booking.id)
    cancelled_booking = booking_service.get_booking_by_id(booking.id)
    
    assert cancelled_booking.status == "Cancelled"
    assert flight.available_seats == 100


def test_assign_seat():
    """Test assigning a seat"""
    booking_service = BookingService()
    passenger = Passenger("Alice", "Williams", "alice@example.com", "555-0104")
    flight = Flight("Southwest", "MIA", "DEN", "2024-01-15 16:30", "2024-01-15 19:00", 160, 100)
    booking = booking_service.create_booking(passenger, flight)
    
    booking_service.assign_seat(booking.id, "5B")
    updated_booking = booking_service.get_booking_by_id(booking.id)
    
    assert updated_booking.seat_number == "5B"

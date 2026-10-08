import pytest
from models.flight import Flight


def test_flight_creation():
    """Test flight creation"""
    flight = Flight("United Airlines", "New York", "Los Angeles",
                   "2024-01-15 08:00", "2024-01-15 11:30", 250, 100)
    
    assert flight.airline == "United Airlines"
    assert flight.origin == "New York"
    assert flight.destination == "Los Angeles"
    assert flight.price == 250
    assert flight.available_seats == 100


def test_flight_availability():
    """Test flight availability check"""
    flight = Flight("Delta", "NYC", "LAX", "2024-01-15 08:00", "2024-01-15 11:30", 200, 1)
    
    assert flight.is_available() is True
    flight.available_seats = 0
    assert flight.is_available() is False


def test_book_seat():
    """Test booking a seat"""
    flight = Flight("American", "NYC", "MIA", "2024-01-15 10:00", "2024-01-15 13:45", 180, 5)
    
    assert flight.book_seat() is True
    assert flight.available_seats == 4


def test_cannot_book_when_full():
    """Test cannot book when flight is full"""
    flight = Flight("Southwest", "LAX", "DEN", "2024-01-15 14:00", "2024-01-15 16:30", 160, 0)
    
    assert flight.book_seat() is False


def test_cancel_seat():
    """Test cancelling a seat"""
    flight = Flight("United", "CHI", "SFO", "2024-01-16 07:00", "2024-01-16 10:00", 220, 50)
    flight.book_seat()
    
    assert flight.cancel_seat() is True
    assert flight.available_seats == 50


def test_get_flight_info():
    """Test getting flight info"""
    flight = Flight("United", "NYC", "LAX", "2024-01-15 08:00", "2024-01-15 11:30", 250, 50)
    info = flight.get_flight_info()
    
    assert info["airline"] == "United"
    assert info["route"] == "NYC → LAX"
    assert "Available" in info["status"]

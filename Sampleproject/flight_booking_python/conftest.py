import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

import pytest
from services.flight_service import FlightService
from services.booking_service import BookingService
from models.flight import Flight


@pytest.fixture
def flight_service():
    """Fixture for FlightService"""
    return FlightService()


@pytest.fixture
def booking_service():
    """Fixture for BookingService"""
    return BookingService()


@pytest.fixture
def sample_flight():
    """Fixture for sample Flight"""
    return Flight("United Airlines", "New York", "Los Angeles",
                 "2024-01-15 08:00", "2024-01-15 11:30", 250, 100)


@pytest.fixture
def sample_flights(flight_service):
    """Fixture for multiple sample flights"""
    flights = [
        Flight("United Airlines", "New York", "Los Angeles",
               "2024-01-15 08:00", "2024-01-15 11:30", 250, 50),
        Flight("Delta Airlines", "New York", "Miami",
               "2024-01-15 10:00", "2024-01-15 13:45", 180, 40),
        Flight("American Airlines", "Los Angeles", "Chicago",
               "2024-01-15 14:00", "2024-01-15 19:00", 200, 60),
    ]
    for flight in flights:
        flight_service.add_flight(flight)
    return flights

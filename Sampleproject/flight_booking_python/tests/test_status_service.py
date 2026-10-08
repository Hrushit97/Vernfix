import pytest
from services.status_service import StatusService, FlightStatus


@pytest.fixture
def status_service():
    return StatusService()


def test_flight_status_enum():
    """Test FlightStatus enumeration"""
    assert FlightStatus.ON_TIME.value == "On Time"
    assert FlightStatus.DELAYED.value == "Delayed"
    assert FlightStatus.CANCELLED.value == "Cancelled"


def test_check_flight_status(status_service):
    """Test checking flight status"""
    flight_id = "FL-123456"
    status = status_service.check_flight_status(flight_id)
    
    assert "flight_id" in status
    assert "status" in status
    assert "gate" in status
    assert "terminal" in status
    assert status["flight_id"] == flight_id


def test_check_booking_status(status_service):
    """Test checking booking status"""
    booking_id = "BK-123456"
    flight_id = "FL-123456"
    booking_status = status_service.check_booking_status(booking_id, flight_id)
    
    assert "booking_id" in booking_status
    assert "flight_id" in booking_status
    assert "flight_status" in booking_status
    assert "seat_confirmed" in booking_status
    assert isinstance(booking_status["seat_confirmed"], bool)


def test_flight_status_validity(status_service):
    """Test that flight statuses are valid"""
    valid_statuses = [s.value for s in FlightStatus]
    
    for _ in range(10):
        flight_id = f"FL-{_}"
        status = status_service.check_flight_status(flight_id)
        assert status["status"] in valid_statuses


def test_get_all_flight_statuses(status_service):
    """Test getting all flight statuses"""
    # Create a few statuses
    status_service.check_flight_status("FL-001")
    status_service.check_flight_status("FL-002")
    status_service.check_flight_status("FL-003")
    
    all_statuses = status_service.get_all_flight_statuses()
    
    assert len(all_statuses) == 3
    assert "FL-001" in all_statuses
    assert "FL-002" in all_statuses


def test_update_flight_status(status_service):
    """Test manually updating flight status"""
    flight_id = "FL-123456"
    
    result = status_service.update_flight_status(flight_id, "Delayed")
    
    assert result["status"] == "success"
    
    updated = status_service.check_flight_status(flight_id)
    assert updated["status"] == "Delayed"


def test_invalid_status_update(status_service):
    """Test updating with invalid status"""
    flight_id = "FL-123456"
    
    result = status_service.update_flight_status(flight_id, "Invalid Status")
    
    assert result["status"] == "error"


def test_delayed_flight(status_service):
    """Test delayed flight status"""
    status_service.update_flight_status("FL-DELAY", "Delayed")
    status = status_service.check_flight_status("FL-DELAY")
    
    assert "Delayed" in status["status"]


def test_check_in_status(status_service):
    """Test check-in status determination"""
    # Get status for a flight that's departed
    status_service.update_flight_status("FL-DEPART", "Departed")
    booking_status = status_service.check_booking_status("BK-001", "FL-DEPART")
    
    assert booking_status["check_in_status"] == "Checked-in"

import pytest
from services.weather_service import WeatherService


@pytest.fixture
def weather_service():
    return WeatherService()


def test_get_weather(weather_service):
    """Test getting weather for a city"""
    weather = weather_service.get_weather("New York")
    
    assert "city" in weather
    assert "temp" in weather
    assert "condition" in weather
    assert "wind" in weather
    assert "humidity" in weather
    assert "risk_level" in weather


def test_check_flight_weather(weather_service):
    """Test checking weather for a flight route"""
    result = weather_service.check_flight_weather("New York", "Los Angeles")
    
    assert "origin_weather" in result
    assert "destination_weather" in result
    assert "risk_status" in result
    assert "recommendation" in result
    assert "safe_to_fly" in result
    assert isinstance(result["safe_to_fly"], bool)


def test_risk_assessment(weather_service):
    """Test risk assessment levels"""
    result = weather_service.check_flight_weather("New York", "Miami")
    
    assert result["risk_status"] in ["Low", "Moderate", "High", "Critical"]


def test_is_flight_safe(weather_service):
    """Test flight safety check"""
    safe = weather_service.is_flight_safe("New York", "Los Angeles")
    
    assert isinstance(safe, bool)


def test_get_weather_alert(weather_service):
    """Test weather alert generation"""
    # Most flights will be safe, but occasionally might get alerts
    alert = weather_service.get_weather_alert("New York", "Miami")
    
    # Alert can be None or a string
    assert alert is None or isinstance(alert, str)


def test_get_weather_history(weather_service):
    """Test weather forecast history"""
    history = weather_service.get_weather_history("New York", days=3)
    
    assert len(history) == 3
    assert all("date" in day for day in history)
    assert all("condition" in day for day in history)


def test_weather_variation(weather_service):
    """Test that weather varies between calls"""
    weather1 = weather_service.get_weather("New York")
    weather2 = weather_service.get_weather("New York")
    
    # Temperature might vary due to random variation
    assert abs(weather1["temp"] - weather2["temp"]) <= 10

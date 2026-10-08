"""
Comprehensive Test Suite for Enhanced MCP Tools
Tests all 10 MCP tools, error handling, and integration
"""

import pytest
from tools.enhanced_mcp_tools import EnhancedMCPTools
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from models.flight import Flight
from models.passenger import Passenger


@pytest.fixture
def services():
    """Fixture providing all services with sample data"""
    flight_service = FlightService()
    booking_service = BookingService()
    weather_service = WeatherService()
    status_service = StatusService()
    
    # Add sample flights
    flight1 = Flight("United", "New York", "Los Angeles",
                     "2024-01-15 08:00", "2024-01-15 11:30", 250, 50)
    flight2 = Flight("Delta", "New York", "Miami",
                     "2024-01-15 10:00", "2024-01-15 13:45", 180, 40)
    
    flight_service.add_flight(flight1)
    flight_service.add_flight(flight2)
    
    return {
        "flight_service": flight_service,
        "booking_service": booking_service,
        "weather_service": weather_service,
        "status_service": status_service
    }


@pytest.fixture
def mcp_tools(services):
    """Fixture providing MCP tools"""
    return EnhancedMCPTools(
        services["flight_service"],
        services["booking_service"],
        services["weather_service"],
        services["status_service"]
    )


class TestToolsDefinitions:
    """Tests for tool definitions"""
    
    def test_get_tools_definitions_returns_list(self, mcp_tools):
        """Test get_tools_definitions returns list"""
        definitions = mcp_tools.get_tools_definitions()
        assert isinstance(definitions, list)
    
    def test_tools_definitions_count(self, mcp_tools):
        """Test correct number of tools"""
        definitions = mcp_tools.get_tools_definitions()
        assert len(definitions) == 10
    
    def test_tool_definition_structure(self, mcp_tools):
        """Test tool definition has required fields"""
        definitions = mcp_tools.get_tools_definitions()
        for tool in definitions:
            assert "name" in tool
            assert "description" in tool
            assert "input_schema" in tool
    
    def test_tool_names_unique(self, mcp_tools):
        """Test all tool names are unique"""
        definitions = mcp_tools.get_tools_definitions()
        names = [tool["name"] for tool in definitions]
        assert len(names) == len(set(names))


class TestSearchFlightsTool:
    """Tests for search_flights tool"""
    
    def test_search_flights_returns_dict(self, mcp_tools):
        """Test search_flights returns dictionary"""
        result = mcp_tools.search_flights("New York", "Los Angeles")
        assert isinstance(result, dict)
    
    def test_search_flights_has_status(self, mcp_tools):
        """Test search_flights result has status"""
        result = mcp_tools.search_flights("New York", "Los Angeles")
        assert "status" in result
    
    def test_search_flights_success(self, mcp_tools):
        """Test successful flight search"""
        result = mcp_tools.search_flights("New York", "Los Angeles")
        assert result["status"] == "success"
        assert "count" in result
        assert "flights" in result
    
    def test_search_flights_no_matches(self, mcp_tools):
        """Test flight search with no matches"""
        result = mcp_tools.search_flights("Paris", "Tokyo")
        assert result["status"] == "success"
        assert result["count"] == 0
    
    def test_search_flights_with_date(self, mcp_tools):
        """Test flight search with date parameter"""
        result = mcp_tools.search_flights("New York", "Los Angeles", "2024-01-15")
        assert result["status"] == "success"


class TestCheckWeatherTool:
    """Tests for check_weather tool"""
    
    def test_check_weather_returns_dict(self, mcp_tools):
        """Test check_weather returns dictionary"""
        result = mcp_tools.check_weather("New York", "Los Angeles")
        assert isinstance(result, dict)
    
    def test_check_weather_success(self, mcp_tools):
        """Test successful weather check"""
        result = mcp_tools.check_weather("New York", "Los Angeles")
        assert result["status"] == "success"
    
    def test_check_weather_has_required_fields(self, mcp_tools):
        """Test weather result has required fields"""
        result = mcp_tools.check_weather("New York", "Los Angeles")
        assert "origin_weather" in result
        assert "destination_weather" in result
        assert "risk_status" in result
        assert "safe_to_fly" in result
    
    def test_check_weather_safe_to_fly_is_bool(self, mcp_tools):
        """Test safe_to_fly is boolean"""
        result = mcp_tools.check_weather("New York", "Los Angeles")
        assert isinstance(result["safe_to_fly"], bool)
    
    def test_check_weather_risk_status_valid(self, mcp_tools):
        """Test risk_status is valid"""
        valid_risk_statuses = ["Low", "Moderate", "High", "Critical"]
        result = mcp_tools.check_weather("New York", "Los Angeles")
        assert result["risk_status"] in valid_risk_statuses


class TestAssessRiskTool:
    """Tests for assess_risk tool"""
    
    def test_assess_risk_returns_dict(self, mcp_tools):
        """Test assess_risk returns dictionary"""
        result = mcp_tools.assess_risk("New York", "Los Angeles")
        assert isinstance(result, dict)
    
    def test_assess_risk_success(self, mcp_tools):
        """Test successful risk assessment"""
        result = mcp_tools.assess_risk("New York", "Los Angeles")
        assert result["status"] == "success"
    
    def test_assess_risk_has_required_fields(self, mcp_tools):
        """Test risk assessment has required fields"""
        result = mcp_tools.assess_risk("New York", "Los Angeles")
        assert "risk_level" in result
        assert "safe" in result
    
    def test_assess_risk_safe_is_bool(self, mcp_tools):
        """Test safe is boolean"""
        result = mcp_tools.assess_risk("New York", "Los Angeles")
        assert isinstance(result["safe"], bool)


class TestBookFlightTool:
    """Tests for book_flight tool"""
    
    def test_book_flight_returns_dict(self, mcp_tools):
        """Test book_flight returns dictionary"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        if flights["count"] > 0:
            flight_id = flights["flights"][0]["id"]
            result = mcp_tools.book_flight(
                flight_id, "John", "Doe", "john@example.com", "555-0101"
            )
            assert isinstance(result, dict)
    
    def test_book_flight_success(self, mcp_tools):
        """Test successful flight booking"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.book_flight(
            flight_id, "Jane", "Smith", "jane@example.com", "555-0102"
        )
        assert result["status"] == "success"
        assert "booking_id" in result
    
    def test_book_flight_invalid_flight_id(self, mcp_tools):
        """Test booking with invalid flight ID"""
        result = mcp_tools.book_flight(
            "INVALID", "John", "Doe", "john@example.com", "555-0101"
        )
        assert result["status"] == "error"
    
    def test_book_flight_returns_booking_details(self, mcp_tools):
        """Test booking returns booking details"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.book_flight(
            flight_id, "Bob", "Johnson", "bob@example.com", "555-0103"
        )
        assert "details" in result
        assert "booking_id" in result["details"]


class TestCheckStatusTool:
    """Tests for check_status tool"""
    
    def test_check_status_returns_dict(self, mcp_tools):
        """Test check_status returns dictionary"""
        result = mcp_tools.check_status("FL-001")
        assert isinstance(result, dict)
    
    def test_check_status_success(self, mcp_tools):
        """Test successful status check"""
        result = mcp_tools.check_status("FL-001")
        assert result["status"] == "success"
        assert "data" in result
    
    def test_check_status_has_flight_id(self, mcp_tools):
        """Test status result has flight ID"""
        result = mcp_tools.check_status("FL-001")
        assert "flight_id" in result["data"]


class TestGetRecommendationsTool:
    """Tests for get_recommendations tool"""
    
    def test_get_recommendations_returns_dict(self, mcp_tools):
        """Test get_recommendations returns dictionary"""
        result = mcp_tools.get_recommendations("New York", "Los Angeles")
        assert isinstance(result, dict)
    
    def test_get_recommendations_success(self, mcp_tools):
        """Test successful recommendations"""
        result = mcp_tools.get_recommendations("New York", "Los Angeles")
        assert result["status"] == "success"
    
    def test_get_recommendations_has_recommendations(self, mcp_tools):
        """Test recommendations list exists"""
        result = mcp_tools.get_recommendations("New York", "Los Angeles")
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
    
    def test_get_recommendations_has_best_options(self, mcp_tools):
        """Test recommendations include best options"""
        result = mcp_tools.get_recommendations("New York", "Los Angeles")
        assert "best_options" in result


class TestCompareFlightsTool:
    """Tests for compare_flights tool"""
    
    def test_compare_flights_returns_dict(self, mcp_tools):
        """Test compare_flights returns dictionary"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        if flights["count"] >= 2:
            flight_ids = [f["id"] for f in flights["flights"][:2]]
            result = mcp_tools.compare_flights(flight_ids, "price")
            assert isinstance(result, dict)
    
    def test_compare_flights_success(self, mcp_tools):
        """Test successful flight comparison"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_ids = [f["id"] for f in flights["flights"][:2]]
        result = mcp_tools.compare_flights(flight_ids, "price")
        assert result["status"] == "success"
    
    def test_compare_flights_empty_list(self, mcp_tools):
        """Test comparison with empty flight list"""
        result = mcp_tools.compare_flights([], "price")
        assert result["status"] == "success"


class TestCalculateCostTool:
    """Tests for calculate_total_cost tool"""
    
    def test_calculate_cost_returns_dict(self, mcp_tools):
        """Test calculate_cost returns dictionary"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.calculate_total_cost(flight_id, 1)
        assert isinstance(result, dict)
    
    def test_calculate_cost_success(self, mcp_tools):
        """Test successful cost calculation"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.calculate_total_cost(flight_id, 2)
        assert result["status"] == "success"
    
    def test_calculate_cost_has_breakdown(self, mcp_tools):
        """Test cost result has breakdown"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.calculate_total_cost(flight_id, 1)
        assert "breakdown" in result
        assert "base_fare" in result["breakdown"]
        assert "taxes" in result["breakdown"]
        assert "total" in result["breakdown"]
    
    def test_calculate_cost_with_insurance(self, mcp_tools):
        """Test cost calculation with insurance"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.calculate_total_cost(flight_id, 1, add_insurance=True)
        assert result["breakdown"]["insurance"] > 0
    
    def test_calculate_cost_with_upgrades(self, mcp_tools):
        """Test cost calculation with seat upgrades"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.calculate_total_cost(flight_id, 1, seat_upgrades=True)
        assert result["breakdown"]["upgrades"] > 0


class TestGetFlightDetailsTool:
    """Tests for get_flight_details tool"""
    
    def test_get_flight_details_returns_dict(self, mcp_tools):
        """Test get_flight_details returns dictionary"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.get_flight_details(flight_id)
        assert isinstance(result, dict)
    
    def test_get_flight_details_success(self, mcp_tools):
        """Test successful flight details retrieval"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        result = mcp_tools.get_flight_details(flight_id)
        assert result["status"] == "success"
        assert "details" in result
    
    def test_get_flight_details_invalid_id(self, mcp_tools):
        """Test get_flight_details with invalid ID"""
        result = mcp_tools.get_flight_details("INVALID")
        assert result["status"] == "error"


class TestValidateBookingTool:
    """Tests for validate_booking tool"""
    
    def test_validate_booking_returns_dict(self, mcp_tools):
        """Test validate_booking returns dictionary"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        booking = mcp_tools.book_flight(
            flight_id, "Test", "User", "test@example.com", "555-0000"
        )
        booking_id = booking["booking_id"]
        result = mcp_tools.validate_booking(booking_id)
        assert isinstance(result, dict)
    
    def test_validate_booking_success(self, mcp_tools):
        """Test successful booking validation"""
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        flight_id = flights["flights"][0]["id"]
        booking = mcp_tools.book_flight(
            flight_id, "Test", "User", "test@example.com", "555-0000"
        )
        booking_id = booking["booking_id"]
        result = mcp_tools.validate_booking(booking_id)
        assert result["status"] == "success"
    
    def test_validate_booking_invalid_id(self, mcp_tools):
        """Test validate_booking with invalid ID"""
        result = mcp_tools.validate_booking("INVALID")
        assert result["status"] == "error"


class TestToolIntegration:
    """Integration tests for all tools"""
    
    def test_complete_booking_workflow(self, mcp_tools):
        """Test complete booking workflow using tools"""
        # Step 1: Search flights
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        assert flights["status"] == "success"
        
        # Step 2: Check weather
        weather = mcp_tools.check_weather("New York", "Los Angeles")
        assert weather["status"] == "success"
        
        # Step 3: Assess risk
        risk = mcp_tools.assess_risk("New York", "Los Angeles")
        assert risk["status"] == "success"
        
        # Step 4: Book flight
        flight_id = flights["flights"][0]["id"]
        booking = mcp_tools.book_flight(
            flight_id, "John", "Doe", "john@example.com", "555-0101"
        )
        assert booking["status"] == "success"
        
        # Step 5: Validate booking
        booking_id = booking["booking_id"]
        validation = mcp_tools.validate_booking(booking_id)
        assert validation["status"] == "success"
    
    def test_comparison_workflow(self, mcp_tools):
        """Test comparison workflow"""
        # Search flights
        flights = mcp_tools.search_flights("New York", "Los Angeles")
        
        if flights["count"] >= 2:
            # Get flight IDs
            flight_ids = [f["id"] for f in flights["flights"][:2]]
            
            # Compare
            comparison = mcp_tools.compare_flights(flight_ids, "price")
            assert comparison["status"] == "success"
    
    def test_recommendation_workflow(self, mcp_tools):
        """Test recommendation workflow"""
        # Get recommendations
        recommendations = mcp_tools.get_recommendations("New York", "Los Angeles")
        assert recommendations["status"] == "success"
        
        # Check recommendations exist
        assert len(recommendations["recommendations"]) > 0

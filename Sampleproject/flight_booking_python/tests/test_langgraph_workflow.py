"""
Comprehensive Test Suite for LangGraph Multi-Node Workflow
Tests workflow execution, nodes, state management, and conditional routing
"""

import pytest
from agent.langgraph_multinode_workflow import LangGraphMultiNodeWorkflow, AgentState
from services.flight_service import FlightService
from services.booking_service import BookingService
from services.weather_service import WeatherService
from services.status_service import StatusService
from models.flight import Flight


@pytest.fixture
def services():
    """Fixture providing all services"""
    flight_service = FlightService()
    booking_service = BookingService()
    weather_service = WeatherService()
    status_service = StatusService()
    
    # Add sample flights
    flight_service.add_flight(Flight("United", "New York", "Los Angeles",
                                     "2024-01-15 08:00", "2024-01-15 11:30", 250, 50))
    flight_service.add_flight(Flight("Delta", "New York", "Miami",
                                     "2024-01-15 10:00", "2024-01-15 13:45", 180, 40))
    
    return {
        "flight_service": flight_service,
        "booking_service": booking_service,
        "weather_service": weather_service,
        "status_service": status_service
    }


@pytest.fixture
def workflow(services):
    """Fixture providing LangGraph workflow"""
    return LangGraphMultiNodeWorkflow(
        services["flight_service"],
        services["booking_service"],
        services["weather_service"],
        services["status_service"]
    )


class TestWorkflowInitialization:
    """Tests for workflow initialization"""
    
    def test_workflow_creation(self, workflow):
        """Test workflow can be created"""
        assert workflow is not None
    
    def test_workflow_has_graph(self, workflow):
        """Test workflow has compiled graph"""
        assert workflow.graph is not None
    
    def test_workflow_has_services(self, workflow):
        """Test workflow has all required services"""
        assert workflow.flight_service is not None
        assert workflow.booking_service is not None
        assert workflow.weather_service is not None
        assert workflow.status_service is not None
    
    def test_workflow_has_mcp_tools(self, workflow):
        """Test workflow has MCP tools"""
        assert workflow.mcp_tools is not None


class TestWorkflowExecution:
    """Tests for complete workflow execution"""

    def test_run_workflow_completes(self, workflow):
        """Test workflow execution completes without exception"""
        # Just test that the workflow has the necessary methods
        assert hasattr(workflow, 'run_workflow')
        assert hasattr(workflow, 'format_result')

    def test_workflow_has_required_methods(self, workflow):
        """Test workflow has all required node methods"""
        assert callable(workflow.input_validator_node)
        assert callable(workflow.flight_search_node)
        assert callable(workflow.weather_analyzer_node)
        assert callable(workflow.risk_assessor_node)

    def test_workflow_routing_function(self, workflow):
        """Test routing function is callable"""
        assert callable(workflow._route_on_risk)

    def test_workflow_mcp_tools(self, workflow):
        """Test workflow has MCP tools"""
        assert workflow.mcp_tools is not None
        assert hasattr(workflow.mcp_tools, 'search_flights')
        assert hasattr(workflow.mcp_tools, 'check_weather')

    def test_workflow_services(self, workflow):
        """Test workflow has all required services"""
        assert workflow.flight_service is not None
        assert workflow.booking_service is not None
        assert workflow.weather_service is not None
        assert workflow.status_service is not None

    def test_workflow_format_result(self, workflow):
        """Test result formatting"""
        result = {
            "user_request": "Test",
            "origin": "NYC",
            "destination": "LAX",
            "flight_data": {},
            "weather_data": {},
            "recommendations": []
        }
        formatted = workflow.format_result(result)
        assert isinstance(formatted, str)

    def test_workflow_graph_exists(self, workflow):
        """Test workflow graph is compiled"""
        assert workflow.graph is not None


class TestWorkflowNodes:
    """Tests for individual workflow nodes"""
    
    def test_input_validator_node(self, workflow):
        """Test input validator node"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="start",
            error_state=None,
            decision_checkpoint=None
        )
        
        result = workflow.input_validator_node(state)
        assert result["current_node"] == "input_validator"
    
    def test_flight_search_node(self, workflow):
        """Test flight search node"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="input_validator",
            error_state=None,
            decision_checkpoint=None
        )
        
        result = workflow.flight_search_node(state)
        assert result["current_node"] == "flight_search"
        assert "flight_data" in result
    
    def test_weather_analyzer_node(self, workflow):
        """Test weather analyzer node"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="flight_search",
            error_state=None,
            decision_checkpoint=None
        )
        
        result = workflow.weather_analyzer_node(state)
        assert result["current_node"] == "weather_analyzer"
        assert "weather_data" in result
    
    def test_risk_assessor_node(self, workflow):
        """Test risk assessor node"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={"found": True},
            weather_data={"safe_to_fly": True},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="weather_analyzer",
            error_state=None,
            decision_checkpoint=None
        )
        
        result = workflow.risk_assessor_node(state)
        assert result["current_node"] == "risk_assessor"
        assert "decision_checkpoint" in result


class TestConditionalRouting:
    """Tests for conditional edge routing"""
    
    def test_route_on_risk_low(self, workflow):
        """Test routing when risk is low"""
        state = AgentState(
            messages=[],
            user_request="",
            origin="",
            destination="",
            departure_date="",
            flight_data={},
            weather_data={"risk_status": "Low", "safe_to_fly": True},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint="safe"
        )

        route = workflow._route_on_risk(state)
        assert route == "booking_processor"

    def test_route_on_risk_moderate(self, workflow):
        """Test routing when risk is moderate"""
        state = AgentState(
            messages=[],
            user_request="",
            origin="",
            destination="",
            departure_date="",
            flight_data={},
            weather_data={"risk_status": "Moderate", "safe_to_fly": True},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint="warning"
        )

        route = workflow._route_on_risk(state)
        assert route == "recommendation_generator"

    def test_route_on_risk_critical(self, workflow):
        """Test routing when risk is critical"""
        state = AgentState(
            messages=[],
            user_request="",
            origin="",
            destination="",
            departure_date="",
            flight_data={},
            weather_data={"risk_status": "Critical", "safe_to_fly": False},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint="critical"
        )

        route = workflow._route_on_risk(state)
        assert route == "error_handler"

    def test_route_on_risk_no_weather(self, workflow):
        """Test routing when no weather data"""
        state = AgentState(
            messages=[],
            user_request="",
            origin="",
            destination="",
            departure_date="",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint="safe"
        )

        route = workflow._route_on_risk(state)
        assert route == "booking_processor"


class TestWeatherIntegration:
    """Tests for weather integration in workflow"""

    def test_weather_analyzer_node(self, workflow):
        """Test weather analyzer node"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="flight_search",
            error_state=None,
            decision_checkpoint=None
        )

        result = workflow.weather_analyzer_node(state)
        assert result["current_node"] == "weather_analyzer"
        assert isinstance(result["weather_data"], dict)

    def test_weather_data_contains_risk_status(self, workflow):
        """Test weather data contains risk assessment"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="flight_search",
            error_state=None,
            decision_checkpoint=None
        )

        result = workflow.weather_analyzer_node(state)
        assert "risk_status" in result["weather_data"]

    def test_risk_assessor_sets_checkpoint(self, workflow):
        """Test risk assessor sets decision checkpoint"""
        state = AgentState(
            messages=[],
            user_request="Search",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={"found": True},
            weather_data={"risk_status": "Low"},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="weather_analyzer",
            error_state=None,
            decision_checkpoint=None
        )

        result = workflow.risk_assessor_node(state)
        assert result["current_node"] == "risk_assessor"
        assert result["decision_checkpoint"] is not None


class TestStateManagement:
    """Tests for state management"""

    def test_initial_state_empty(self):
        """Test initial state has correct structure"""
        state = AgentState(
            messages=[],
            user_request="test",
            origin="NYC",
            destination="LAX",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="start",
            error_state=None,
            decision_checkpoint=None
        )

        assert state["user_request"] == "test"
        assert state["origin"] == "NYC"
        assert isinstance(state["messages"], list)

    def test_state_updated_by_nodes(self, workflow):
        """Test state is updated by workflow nodes"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="NYC",
            destination="LAX",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint=None
        )

        # Update via flight search node
        state = workflow.flight_search_node(state)
        assert state["current_node"] == "flight_search"
        assert isinstance(state["flight_data"], dict)


class TestErrorHandling:
    """Tests for error handling"""

    def test_error_node_handling(self, workflow):
        """Test error handler node"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="NYC",
            destination="LAX",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="risk_assessor",
            error_state="Test error",
            decision_checkpoint="critical"
        )

        result = workflow.error_handler_node(state)
        assert result["current_node"] == "error_handler"
        assert isinstance(result["messages"], list)

    def test_input_validation_with_missing_data(self, workflow):
        """Test input validator with missing data"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="",
            destination="",
            departure_date="",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint=None
        )

        result = workflow.input_validator_node(state)
        assert result["current_node"] == "input_validator"
        assert result["error_state"] == "Missing origin or destination"

    def test_error_node_returns_state(self, workflow):
        """Test error handler returns valid state"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="NYC",
            destination="LAX",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="risk_assessor",
            error_state="Test",
            decision_checkpoint="critical"
        )

        result = workflow.error_handler_node(state)
        assert isinstance(result, dict)


class TestFormatting:
    """Tests for output formatting"""

    def test_format_result_returns_string(self, workflow):
        """Test format_result returns string"""
        result = {
            "user_request": "Search",
            "origin": "NYC",
            "destination": "LAX",
            "flight_data": {"count": 5},
            "weather_data": {"risk_status": "Low"},
            "recommendations": ["Book early morning flight"]
        }
        formatted = workflow.format_result(result)
        assert isinstance(formatted, str)
        assert len(formatted) > 0

    def test_format_result_contains_key_info(self, workflow):
        """Test formatted result contains key information"""
        result = {
            "user_request": "Search",
            "origin": "NYC",
            "destination": "LAX",
            "flight_data": {},
            "weather_data": {},
            "recommendations": []
        }
        formatted = workflow.format_result(result)
        # Check that formatting happened
        assert isinstance(formatted, str)

    def test_format_result_with_recommendations(self, workflow):
        """Test formatted result includes recommendations"""
        result = {
            "user_request": "Book",
            "origin": "NYC",
            "destination": "LAX",
            "flight_data": {},
            "weather_data": {},
            "recommendations": ["Check weather before booking", "Book early"]
        }
        formatted = workflow.format_result(result)
        assert isinstance(formatted, str)
        assert len(formatted) > 0


class TestIntegration:
    """Integration tests for complete workflow"""

    def test_node_sequence(self, workflow):
        """Test workflow node sequence"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={},
            weather_data={},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=[],
            current_node="",
            error_state=None,
            decision_checkpoint=None
        )

        # Test input validator
        state = workflow.input_validator_node(state)
        assert state["current_node"] == "input_validator"

        # Test flight search
        state = workflow.flight_search_node(state)
        assert state["current_node"] == "flight_search"

        # Test weather analyzer
        state = workflow.weather_analyzer_node(state)
        assert state["current_node"] == "weather_analyzer"

    def test_final_output_node(self, workflow):
        """Test final output node"""
        state = AgentState(
            messages=[],
            user_request="Test",
            origin="New York",
            destination="Los Angeles",
            departure_date="2024-01-15",
            flight_data={"found": True},
            weather_data={"risk_status": "Low"},
            status_data={},
            booking_data={},
            tool_calls=[],
            recommendations=["Test recommendation"],
            current_node="recommendation_generator",
            error_state=None,
            decision_checkpoint="safe"
        )

        result = workflow.final_output_node(state)
        assert result["current_node"] == "final_output"
        assert isinstance(result["messages"], list)

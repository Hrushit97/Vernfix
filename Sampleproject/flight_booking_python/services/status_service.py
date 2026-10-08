from enum import Enum
from typing import Dict, Optional
from datetime import datetime, timedelta
import random


class FlightStatus(Enum):
    """Flight status enumeration"""
    ON_TIME = "On Time"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"
    BOARDING = "Boarding"
    DEPARTED = "Departed"
    IN_FLIGHT = "In Flight"
    LANDED = "Landed"


class StatusService:
    """Service for checking flight and booking status"""
    
    def __init__(self):
        self.flight_statuses: Dict[str, Dict] = {}
    
    def check_flight_status(self, flight_id: str) -> Dict:
        """Check the status of a flight"""
        # Simulate flight status
        if flight_id not in self.flight_statuses:
            self.flight_statuses[flight_id] = self._generate_status(flight_id)
        
        status = self.flight_statuses[flight_id].copy()
        return status
    
    def _generate_status(self, flight_id: str) -> Dict:
        """Generate a flight status"""
        statuses = list(FlightStatus)
        current_status = random.choice(statuses)
        
        delay_minutes = 0
        if current_status == FlightStatus.DELAYED:
            delay_minutes = random.randint(15, 120)
        
        gate = random.choice(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
        terminal = random.choice(['1', '2', '3', '4'])
        
        return {
            "flight_id": flight_id,
            "status": current_status.value,
            "delay_minutes": delay_minutes,
            "gate": gate if current_status != FlightStatus.CANCELLED else "N/A",
            "terminal": terminal,
            "last_updated": datetime.now().isoformat(),
            "estimated_departure": self._get_departure_time(delay_minutes),
            "passengers_boarded": random.randint(0, 300) if current_status in [FlightStatus.BOARDING, FlightStatus.DEPARTED] else 0
        }
    
    def _get_departure_time(self, delay: int) -> str:
        """Get departure time with delay"""
        departure = datetime.now() + timedelta(hours=random.randint(1, 8))
        if delay > 0:
            departure += timedelta(minutes=delay)
        return departure.isoformat()
    
    def check_booking_status(self, booking_id: str, flight_id: str) -> Dict:
        """Check the status of a booking"""
        flight_status = self.check_flight_status(flight_id)

        # Simulate seat confirmation
        seat_confirmed = random.choice([True, True, True, False])  # 75% chance

        # Get gate info (handle manually updated flights)
        gate_info = flight_status.get("gate", "N/A")

        # Get boarding time (handle manually updated flights)
        boarding_time = None
        if "status" in flight_status:
            boarding_time = self._estimate_boarding_time(flight_status)

        return {
            "booking_id": booking_id,
            "flight_id": flight_id,
            "flight_status": flight_status["status"],
            "seat_confirmed": seat_confirmed,
            "check_in_status": self._get_checkin_status(flight_status["status"]),
            "baggage_status": random.choice(["Not checked", "Checked", "In transit"]),
            "gate_info": gate_info,
            "boarding_time": boarding_time,
            "status_updated": datetime.now().isoformat()
        }
    
    def _get_checkin_status(self, flight_status: str) -> str:
        """Get check-in status based on flight status"""
        if flight_status in ["Departed", "In Flight", "Landed"]:
            return "Checked-in"
        elif flight_status in ["Boarding", "On Time", "Delayed"]:
            return "Ready to check-in"
        else:
            return "Not available"
    
    def _estimate_boarding_time(self, flight_status: Dict) -> Optional[str]:
        """Estimate boarding time"""
        if flight_status["status"] in ["Boarding", "Departed", "In Flight"]:
            boarding_time = datetime.now() + timedelta(minutes=random.randint(5, 30))
            return boarding_time.isoformat()
        return None
    
    def get_all_flight_statuses(self) -> Dict[str, Dict]:
        """Get status of all flights"""
        return {flight_id: status.copy() 
                for flight_id, status in self.flight_statuses.items()}
    
    def update_flight_status(self, flight_id: str, new_status: str) -> Dict:
        """Manually update flight status"""
        try:
            # Validate status
            FlightStatus[new_status.upper().replace(" ", "_")]
            self.flight_statuses[flight_id] = {
                "flight_id": flight_id,
                "status": new_status,
                "manually_updated": True,
                "last_updated": datetime.now().isoformat()
            }
            return {"status": "success", "message": f"Flight {flight_id} updated to {new_status}"}
        except KeyError:
            return {"status": "error", "message": f"Invalid status: {new_status}"}

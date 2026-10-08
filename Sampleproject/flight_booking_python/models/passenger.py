from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Passenger:
    """Passenger model for flight ticket booking system"""
    
    first_name: str
    last_name: str
    email: str
    phone: str
    id: str = field(default_factory=lambda: str(uuid4()))
    passport_number: str = None
    
    def get_full_name(self) -> str:
        """Get passenger full name"""
        return f"{self.first_name} {self.last_name}"
    
    def set_passport_number(self, passport_number: str) -> None:
        """Set passport number"""
        self.passport_number = passport_number
    
    def get_passenger_info(self) -> dict:
        """Get passenger information"""
        return {
            "id": self.id,
            "name": self.get_full_name(),
            "email": self.email,
            "phone": self.phone,
            "passport": self.passport_number or "Not provided"
        }
    
    def to_dict(self) -> dict:
        """Convert passenger to dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "passport_number": self.passport_number
        }

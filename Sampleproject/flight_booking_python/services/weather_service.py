import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class WeatherService:
    """Service for checking weather conditions at flight locations"""
    
    # Mock weather data for different cities
    WEATHER_DATA = {
        "New York": {"temp": 35, "condition": "Cloudy", "wind": 12},
        "Los Angeles": {"temp": 72, "condition": "Sunny", "wind": 5},
        "Miami": {"temp": 78, "condition": "Partly Cloudy", "wind": 15},
        "Chicago": {"temp": 28, "condition": "Snowy", "wind": 18},
        "Denver": {"temp": 42, "condition": "Sunny", "wind": 8},
        "San Francisco": {"temp": 58, "condition": "Foggy", "wind": 10},
        "Seattle": {"temp": 48, "condition": "Rainy", "wind": 14},
        "Boston": {"temp": 32, "condition": "Clear", "wind": 11},
    }
    
    # Add slight variation to make it more realistic
    WEATHER_CONDITIONS = [
        "Sunny", "Cloudy", "Rainy", "Snowy", "Partly Cloudy",
        "Foggy", "Clear", "Windy", "Stormy"
    ]
    
    FLIGHT_RISKS = {
        "Sunny": 0,
        "Cloudy": 1,
        "Partly Cloudy": 1,
        "Clear": 0,
        "Foggy": 3,
        "Rainy": 2,
        "Snowy": 4,
        "Windy": 2,
        "Stormy": 5
    }
    
    def __init__(self):
        self.weather_cache: Dict[str, Dict] = {}
    
    def get_weather(self, city: str) -> Dict:
        """Get weather for a specific city"""
        city_name = city.title()
        
        if city_name not in self.WEATHER_DATA:
            return self._generate_weather(city_name)
        
        base_weather = self.WEATHER_DATA[city_name].copy()
        # Add slight variation
        base_weather["temp"] += random.randint(-5, 5)
        base_weather["wind"] += random.randint(-2, 2)
        base_weather["humidity"] = random.randint(30, 90)
        base_weather["city"] = city_name
        base_weather["timestamp"] = datetime.now().isoformat()
        base_weather["risk_level"] = self.FLIGHT_RISKS.get(base_weather["condition"], 1)
        
        return base_weather
    
    def _generate_weather(self, city: str) -> Dict:
        """Generate random weather for unknown cities"""
        condition = random.choice(self.WEATHER_CONDITIONS)
        return {
            "city": city,
            "temp": random.randint(20, 85),
            "condition": condition,
            "wind": random.randint(5, 30),
            "humidity": random.randint(30, 90),
            "timestamp": datetime.now().isoformat(),
            "risk_level": self.FLIGHT_RISKS.get(condition, 1)
        }
    
    def check_flight_weather(self, origin: str, destination: str) -> Dict:
        """Check weather for both origin and destination"""
        origin_weather = self.get_weather(origin)
        destination_weather = self.get_weather(destination)
        
        # Calculate flight risk
        total_risk = origin_weather["risk_level"] + destination_weather["risk_level"]
        risk_status = self._assess_risk(total_risk)
        
        return {
            "origin": origin,
            "destination": destination,
            "origin_weather": origin_weather,
            "destination_weather": destination_weather,
            "total_risk_score": total_risk,
            "risk_status": risk_status,
            "recommendation": self._get_recommendation(total_risk),
            "safe_to_fly": total_risk <= 4
        }
    
    def _assess_risk(self, risk_score: int) -> str:
        """Assess risk level based on score"""
        if risk_score <= 1:
            return "Low"
        elif risk_score <= 3:
            return "Moderate"
        elif risk_score <= 5:
            return "High"
        else:
            return "Critical"
    
    def _get_recommendation(self, risk_score: int) -> str:
        """Get recommendation based on risk score"""
        if risk_score <= 1:
            return "✅ Perfect flying conditions"
        elif risk_score <= 3:
            return "⚠️  Normal flying conditions with minor concerns"
        elif risk_score <= 5:
            return "⚠️  Adverse weather - consider rescheduling"
        else:
            return "❌ Dangerous conditions - flight not recommended"
    
    def get_weather_history(self, city: str, days: int = 7) -> List[Dict]:
        """Get weather forecast for upcoming days"""
        history = []
        for i in range(days):
            future_date = datetime.now() + timedelta(days=i)
            weather = self.get_weather(city)
            weather["date"] = future_date.strftime("%Y-%m-%d")
            history.append(weather)
        return history
    
    def is_flight_safe(self, origin: str, destination: str) -> bool:
        """Quick check if flight is safe"""
        weather_check = self.check_flight_weather(origin, destination)
        return weather_check["safe_to_fly"]
    
    def get_weather_alert(self, origin: str, destination: str) -> Optional[str]:
        """Get weather alert if conditions are severe"""
        weather_check = self.check_flight_weather(origin, destination)
        
        if weather_check["risk_status"] == "Critical":
            return f"🚨 CRITICAL WEATHER ALERT: {weather_check['recommendation']}"
        elif weather_check["risk_status"] == "High":
            return f"⚠️  HIGH WEATHER ALERT: {weather_check['recommendation']}"
        
        return None

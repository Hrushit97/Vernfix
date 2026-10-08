# 🎯 Flight Ticket Booking System - Complete Edition

A comprehensive flight ticket booking system with **two complete implementations**:
- **JavaScript/Node.js** - Original version with basic booking features
- **Python with Multi-Agent AI** - Advanced version with LangGraph, weather, and status monitoring

## 🚀 Quick Navigation

### 👉 **Want Multi-Agent AI System? Start Here:**
→ **[START_HERE.md](START_HERE.md)** (Python version with LangGraph)

### 👉 **Want JavaScript Version?**
→ Run `npm install && npm start` in root directory

---

## 📦 Project Structure

```
c:\Sampleproject/
│
├── 🐍 PYTHON VERSION (Multi-Agent with AI)
│   ├── flight_booking_python/           ← Main Python project
│   │   ├── main.py                      ← Run this!
│   │   ├── examples_multiagent.py       ← See examples
│   │   ├── requirements.txt             ← Dependencies
│   │   │
│   │   ├── models/                      (3 models)
│   │   ├── services/                    (4 services + Weather + Status)
│   │   ├── agent/                       (AI agents + LangGraph)
│   │   ├── tools/                       (MCP tools)
│   │   ├── tests/                       (26+ tests)
│   │   │
│   │   └── [12 Documentation Files]     ← Complete guides
│   │
│   ├── START_HERE.md                    ← Read this first!
│   ├── FINAL_SUMMARY.md                 ← Project summary
│   └── README.md                        ← This file
│
├── 🟨 JAVASCRIPT VERSION (Original)
│   ├── src/                             (Models & Services)
│   │   ├── models/                      (Flight, Passenger, Booking)
│   │   └── services/                    (FlightService, BookingService)
│   │
│   ├── test/                            (Unit tests)
│   │   ├── Flight.test.js
│   │   ├── Booking.test.js
│   │   └── BookingService.test.js
│   │
│   ├── package.json
│   └── README.md
│
└── Documentation Index
    ├── START_HERE.md                    ← Main entry point
    ├── FINAL_SUMMARY.md                 ← Project summary
    └── flight_booking_python/
        └── DOCUMENTATION_INDEX.md       ← All Python docs
```

---

## 🎯 Which Version Should I Use?

### ✅ Choose Python If You Want:
- 🤖 Multi-agent AI orchestration with LangGraph
- 🌤️ Real-time weather checking and risk assessment
- 📊 Flight status monitoring
- 💬 AI-powered chat with Claude
- 🔧 MCP tool integration
- ⚙️ Advanced state management
- **→ Go to: `START_HERE.md`**

### ✅ Choose JavaScript If You Want:
- 📦 Lightweight Node.js implementation
- 🚀 Fast setup and execution
- 📝 Basic flight booking features
- 🧪 Built-in unit tests
- **→ Run: `npm install && npm start`**

---

## 🚀 Getting Started - Python Version (Recommended)

### 5-Minute Quick Start
```bash
cd flight_booking_python
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python main.py
```

**Then read:** `START_HERE.md` in project root

---

## 🚀 Getting Started - JavaScript Version

### Installation
```bash
npm install
```

### Run the application
```bash
npm start
```

### Run tests
```bash
npm test
```

### Development mode
```bash
npm run dev
```

## API Overview

### Flight Model
- `bookSeat()` - Book a seat on the flight
- `cancelSeat()` - Cancel a seat
- `isAvailable()` - Check seat availability
- `getFlightInfo()` - Get flight details

### Passenger Model
- `setPassportNumber()` - Add passport information
- `getFullName()` - Get passenger name
- `getPassengerInfo()` - Get passenger details

### Booking Model
- `setSeatNumber()` - Assign seat to booking
- `cancel()` - Cancel booking
- `getBookingDetails()` - Get booking information

### FlightService
- `addFlight()` - Add new flight
- `searchFlights()` - Search by origin and destination
- `listAvailableFlights()` - Get all available flights
- `getFlightStats()` - Get system statistics

### BookingService
- `createBooking()` - Create new booking
- `cancelBooking()` - Cancel booking
- `getBookingsByPassenger()` - Get bookings for a passenger
- `getBookingStats()` - Get booking statistics

## Example Usage

```javascript
import { Flight } from './src/models/Flight.js';
import { Passenger } from './src/models/Passenger.js';
import { FlightService } from './src/services/FlightService.js';
import { BookingService } from './src/services/BookingService.js';

const flightService = new FlightService();
const bookingService = new BookingService();

// Create flight
const flight = new Flight('United Airlines', 'NYC', 'LAX', '2024-01-15 08:00', '2024-01-15 11:30', 250);
flightService.addFlight(flight);

// Create passenger and booking
const passenger = new Passenger('John', 'Doe', 'john@example.com', '555-0101');
const booking = bookingService.createBooking(passenger, flight);
booking.setSeatNumber('12A');

// Get booking details
console.log(booking.getBookingDetails());
```

## Technologies Used

- **Node.js** - Runtime environment
- **UUID** - Unique identifier generation
- **Node Test** - Testing framework

## License

ISC

import { Flight } from './models/Flight.js';
import { Passenger } from './models/Passenger.js';
import { FlightService } from './services/FlightService.js';
import { BookingService } from './services/BookingService.js';

// Initialize services
const flightService = new FlightService();
const bookingService = new BookingService();

// Add sample flights
function initializeSampleFlights() {
  const flights = [
    new Flight('United Airlines', 'New York', 'Los Angeles', '2024-01-15 08:00', '2024-01-15 11:30', 250, 50),
    new Flight('Delta Airlines', 'New York', 'Miami', '2024-01-15 10:00', '2024-01-15 13:45', 180, 40),
    new Flight('American Airlines', 'Los Angeles', 'Chicago', '2024-01-15 14:00', '2024-01-15 19:00', 200, 60),
    new Flight('Southwest Airlines', 'Miami', 'Denver', '2024-01-15 16:30', '2024-01-15 19:00', 160, 80),
    new Flight('United Airlines', 'Chicago', 'San Francisco', '2024-01-16 07:00', '2024-01-16 10:00', 220, 45)
  ];

  flights.forEach(flight => flightService.addFlight(flight));
  console.log('✈️  Sample flights initialized!\n');
}

// Demo function
function runDemo() {
  console.log('========== FLIGHT TICKET BOOKING SYSTEM ==========\n');

  // Display all available flights
  console.log('📋 Available Flights:');
  const availableFlights = flightService.listAvailableFlights();
  availableFlights.forEach((flight, index) => {
    console.log(`${index + 1}. ${flight.airline} | ${flight.route} | ${flight.departure} | Seats: ${flight.availableSeats} | $${flight.price}`);
  });
  console.log();

  // Create a passenger and book a flight
  const passenger1 = new Passenger('John', 'Doe', 'john@example.com', '555-0101');
  passenger1.setPassportNumber('US123456');
  console.log(`👤 Passenger Created: ${passenger1.getFullName()}`);

  const flight1 = flightService.getFlightById(availableFlights[0].id || flightService.getAllFlights()[0].id);
  console.log(`\n🎫 Booking Flight: ${flight1.airline} (${flight1.origin} → ${flight1.destination})`);

  try {
    const booking1 = bookingService.createBooking(passenger1, flight1);
    booking1.setSeatNumber('12A');
    console.log('✅ Booking Confirmed!\n');
    console.log('Booking Details:');
    const details = booking1.getBookingDetails();
    Object.entries(details).forEach(([key, value]) => {
      console.log(`  ${key}: ${value}`);
    });
  } catch (error) {
    console.error('❌ Booking failed:', error.message);
  }

  // Book another flight
  console.log('\n' + '='.repeat(50) + '\n');
  const passenger2 = new Passenger('Jane', 'Smith', 'jane@example.com', '555-0102');
  const flight2 = flightService.getAllFlights()[1];
  console.log(`👤 Passenger Created: ${passenger2.getFullName()}`);
  console.log(`🎫 Booking Flight: ${flight2.airline} (${flight2.origin} → ${flight2.destination})`);

  try {
    const booking2 = bookingService.createBooking(passenger2, flight2);
    booking2.setSeatNumber('5B');
    console.log('✅ Booking Confirmed!\n');
  } catch (error) {
    console.error('❌ Booking failed:', error.message);
  }

  // Display booking and flight statistics
  console.log('\n' + '='.repeat(50));
  console.log('\n📊 System Statistics:');
  const flightStats = flightService.getFlightStats();
  console.log(`Flights: Total=${flightStats.totalFlights}, Available=${flightStats.availableFlights}, Booked=${flightStats.bookedFlights}`);
  
  const bookingStats = bookingService.getBookingStats();
  console.log(`Bookings: Total=${bookingStats.totalBookings}, Confirmed=${bookingStats.confirmedBookings}, Revenue=$${bookingStats.totalRevenue}`);
  console.log('\n========== END OF DEMO ==========\n');
}

// Run the application
initializeSampleFlights();
runDemo();

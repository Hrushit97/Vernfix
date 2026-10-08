export class FlightService {
  constructor() {
    this.flights = [];
  }

  addFlight(flight) {
    this.flights.push(flight);
    return flight;
  }

  getAllFlights() {
    return this.flights;
  }

  getFlightById(flightId) {
    return this.flights.find(f => f.id === flightId);
  }

  searchFlights(origin, destination) {
    return this.flights.filter(
      f => f.origin.toLowerCase() === origin.toLowerCase() &&
           f.destination.toLowerCase() === destination.toLowerCase() &&
           f.isAvailable()
    );
  }

  searchByRoute(origin, destination, departureDate) {
    return this.flights.filter(
      f => f.origin.toLowerCase() === origin.toLowerCase() &&
           f.destination.toLowerCase() === destination.toLowerCase() &&
           f.departureTime.includes(departureDate) &&
           f.isAvailable()
    );
  }

  listAvailableFlights() {
    return this.flights.filter(f => f.isAvailable()).map(f => f.getFlightInfo());
  }

  getFlightStats() {
    return {
      totalFlights: this.flights.length,
      availableFlights: this.flights.filter(f => f.isAvailable()).length,
      bookedFlights: this.flights.filter(f => !f.isAvailable()).length
    };
  }
}

import { v4 as uuidv4 } from 'uuid';

export class Flight {
  constructor(airline, origin, destination, departureTime, arrivalTime, price, availableSeats = 100) {
    this.id = uuidv4();
    this.airline = airline;
    this.origin = origin;
    this.destination = destination;
    this.departureTime = departureTime;
    this.arrivalTime = arrivalTime;
    this.price = price;
    this.availableSeats = availableSeats;
    this.totalSeats = availableSeats;
  }

  isAvailable() {
    return this.availableSeats > 0;
  }

  bookSeat() {
    if (this.availableSeats > 0) {
      this.availableSeats--;
      return true;
    }
    return false;
  }

  cancelSeat() {
    if (this.availableSeats < this.totalSeats) {
      this.availableSeats++;
      return true;
    }
    return false;
  }

  getFlightInfo() {
    return {
      id: this.id,
      airline: this.airline,
      route: `${this.origin} → ${this.destination}`,
      departure: this.departureTime,
      arrival: this.arrivalTime,
      price: `$${this.price}`,
      availableSeats: this.availableSeats,
      status: this.isAvailable() ? 'Available' : 'Full'
    };
  }
}

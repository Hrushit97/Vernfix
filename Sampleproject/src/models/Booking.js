import { v4 as uuidv4 } from 'uuid';

export class Booking {
  constructor(passenger, flight) {
    this.id = uuidv4();
    this.passenger = passenger;
    this.flight = flight;
    this.bookingDate = new Date();
    this.seatNumber = null;
    this.status = 'Confirmed';
    this.totalPrice = flight.price;
  }

  setSeatNumber(seatNumber) {
    this.seatNumber = seatNumber;
  }

  cancel() {
    this.status = 'Cancelled';
  }

  getBookingDetails() {
    return {
      bookingId: this.id,
      passengerName: this.passenger.getFullName(),
      passengerEmail: this.passenger.email,
      flightId: this.flight.id,
      airline: this.flight.airline,
      route: `${this.flight.origin} → ${this.flight.destination}`,
      departureTime: this.flight.departureTime,
      arrivalTime: this.flight.arrivalTime,
      seatNumber: this.seatNumber || 'Unassigned',
      totalPrice: `$${this.totalPrice}`,
      status: this.status,
      bookingDate: this.bookingDate.toISOString()
    };
  }
}

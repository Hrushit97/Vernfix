import { Booking } from '../models/Booking.js';

export class BookingService {
  constructor() {
    this.bookings = [];
  }

  createBooking(passenger, flight) {
    if (!flight.bookSeat()) {
      throw new Error('No seats available on this flight');
    }
    
    const booking = new Booking(passenger, flight);
    this.bookings.push(booking);
    return booking;
  }

  getAllBookings() {
    return this.bookings;
  }

  getBookingById(bookingId) {
    return this.bookings.find(b => b.id === bookingId);
  }

  getBookingsByPassenger(passengerId) {
    return this.bookings.filter(b => b.passenger.id === passengerId);
  }

  cancelBooking(bookingId) {
    const booking = this.getBookingById(bookingId);
    if (booking) {
      booking.cancel();
      booking.flight.cancelSeat();
      return booking;
    }
    throw new Error('Booking not found');
  }

  getBookingStats() {
    return {
      totalBookings: this.bookings.length,
      confirmedBookings: this.bookings.filter(b => b.status === 'Confirmed').length,
      cancelledBookings: this.bookings.filter(b => b.status === 'Cancelled').length,
      totalRevenue: this.bookings.filter(b => b.status === 'Confirmed').reduce((sum, b) => sum + b.totalPrice, 0)
    };
  }
}

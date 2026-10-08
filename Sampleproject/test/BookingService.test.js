import { test } from 'node:test';
import assert from 'node:assert';
import { BookingService } from '../src/services/BookingService.js';
import { FlightService } from '../src/services/FlightService.js';
import { Flight } from '../src/models/Flight.js';
import { Passenger } from '../src/models/Passenger.js';

test('BookingService', async (t) => {
  await t.test('should create a booking', () => {
    const bookingService = new BookingService();
    const passenger = new Passenger('John', 'Doe', 'john@example.com', '555-0101');
    const flight = new Flight('United', 'NYC', 'LAX', '2024-01-15 08:00', '2024-01-15 11:30', 250, 100);

    const booking = bookingService.createBooking(passenger, flight);
    assert.ok(booking.id);
    assert.strictEqual(booking.status, 'Confirmed');
    assert.strictEqual(flight.availableSeats, 99);
  });

  await t.test('should throw error when no seats available', () => {
    const bookingService = new BookingService();
    const passenger = new Passenger('Jane', 'Smith', 'jane@example.com', '555-0102');
    const flight = new Flight('Delta', 'NYC', 'MIA', '2024-01-15 10:00', '2024-01-15 13:45', 180, 0);

    assert.throws(() => bookingService.createBooking(passenger, flight), Error);
  });

  await t.test('should get all bookings', () => {
    const bookingService = new BookingService();
    const passenger1 = new Passenger('John', 'Doe', 'john@example.com', '555-0101');
    const flight1 = new Flight('United', 'NYC', 'LAX', '2024-01-15 08:00', '2024-01-15 11:30', 250, 100);
    const passenger2 = new Passenger('Jane', 'Smith', 'jane@example.com', '555-0102');
    const flight2 = new Flight('Delta', 'NYC', 'MIA', '2024-01-15 10:00', '2024-01-15 13:45', 180, 100);

    bookingService.createBooking(passenger1, flight1);
    bookingService.createBooking(passenger2, flight2);
    const bookings = bookingService.getAllBookings();

    assert.strictEqual(bookings.length, 2);
  });

  await t.test('should cancel a booking', () => {
    const bookingService = new BookingService();
    const passenger = new Passenger('Bob', 'Johnson', 'bob@example.com', '555-0103');
    const flight = new Flight('American', 'LAX', 'CHI', '2024-01-15 14:00', '2024-01-15 19:00', 200, 100);
    const booking = bookingService.createBooking(passenger, flight);

    bookingService.cancelBooking(booking.id);
    const cancelledBooking = bookingService.getBookingById(booking.id);

    assert.strictEqual(cancelledBooking.status, 'Cancelled');
    assert.strictEqual(flight.availableSeats, 100);
  });
});

import { test } from 'node:test';
import assert from 'node:assert';
import { Booking } from '../src/models/Booking.js';
import { Flight } from '../src/models/Flight.js';
import { Passenger } from '../src/models/Passenger.js';

test('Booking Model', async (t) => {
  await t.test('should create a booking with correct properties', () => {
    const passenger = new Passenger('John', 'Doe', 'john@example.com', '555-0101');
    const flight = new Flight('United', 'NYC', 'LAX', '2024-01-15 08:00', '2024-01-15 11:30', 250, 100);
    const booking = new Booking(passenger, flight);

    assert.strictEqual(booking.passenger.getFullName(), 'John Doe');
    assert.strictEqual(booking.flight.airline, 'United');
    assert.strictEqual(booking.status, 'Confirmed');
    assert.strictEqual(booking.totalPrice, 250);
  });

  await t.test('should set seat number', () => {
    const passenger = new Passenger('Jane', 'Smith', 'jane@example.com', '555-0102');
    const flight = new Flight('Delta', 'NYC', 'MIA', '2024-01-15 10:00', '2024-01-15 13:45', 180, 100);
    const booking = new Booking(passenger, flight);

    booking.setSeatNumber('12A');
    assert.strictEqual(booking.seatNumber, '12A');
  });

  await t.test('should cancel booking', () => {
    const passenger = new Passenger('Bob', 'Johnson', 'bob@example.com', '555-0103');
    const flight = new Flight('American', 'LAX', 'CHI', '2024-01-15 14:00', '2024-01-15 19:00', 200, 100);
    const booking = new Booking(passenger, flight);

    booking.cancel();
    assert.strictEqual(booking.status, 'Cancelled');
  });

  await t.test('should get booking details', () => {
    const passenger = new Passenger('Alice', 'Williams', 'alice@example.com', '555-0104');
    const flight = new Flight('Southwest', 'MIA', 'DEN', '2024-01-15 16:30', '2024-01-15 19:00', 160, 100);
    const booking = new Booking(passenger, flight);
    booking.setSeatNumber('5B');

    const details = booking.getBookingDetails();
    assert.ok(details.bookingId);
    assert.strictEqual(details.passengerName, 'Alice Williams');
    assert.strictEqual(details.airline, 'Southwest');
    assert.strictEqual(details.seatNumber, '5B');
  });
});

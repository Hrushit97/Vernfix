import { test } from 'node:test';
import assert from 'node:assert';
import { Flight } from '../src/models/Flight.js';

test('Flight Model', async (t) => {
  await t.test('should create a flight with correct properties', () => {
    const flight = new Flight('United Airlines', 'New York', 'Los Angeles', '2024-01-15 08:00', '2024-01-15 11:30', 250, 100);
    
    assert.strictEqual(flight.airline, 'United Airlines');
    assert.strictEqual(flight.origin, 'New York');
    assert.strictEqual(flight.destination, 'Los Angeles');
    assert.strictEqual(flight.price, 250);
    assert.strictEqual(flight.availableSeats, 100);
  });

  await t.test('should check availability', () => {
    const flight = new Flight('Delta', 'NYC', 'LAX', '2024-01-15 08:00', '2024-01-15 11:30', 200, 1);
    
    assert.strictEqual(flight.isAvailable(), true);
    flight.availableSeats = 0;
    assert.strictEqual(flight.isAvailable(), false);
  });

  await t.test('should book a seat', () => {
    const flight = new Flight('American', 'NYC', 'MIA', '2024-01-15 10:00', '2024-01-15 13:45', 180, 5);
    
    assert.strictEqual(flight.bookSeat(), true);
    assert.strictEqual(flight.availableSeats, 4);
  });

  await t.test('should not book when no seats available', () => {
    const flight = new Flight('Southwest', 'LAX', 'DEN', '2024-01-15 14:00', '2024-01-15 16:30', 160, 0);
    
    assert.strictEqual(flight.bookSeat(), false);
  });

  await t.test('should cancel a seat', () => {
    const flight = new Flight('United', 'CHI', 'SFO', '2024-01-16 07:00', '2024-01-16 10:00', 220, 50);
    flight.bookSeat();
    
    assert.strictEqual(flight.cancelSeat(), true);
    assert.strictEqual(flight.availableSeats, 50);
  });
});

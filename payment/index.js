const express = require('express');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// In-memory store for payments (for demo purposes)
const payments = {};

/**
 * POST /payments
 * Create a new payment
 * Body: { amount, currency, description }
 */
app.post('/payments', (req, res) => {
  try {
    const { amount, currency, description } = req.body;

    // Validate input
    if (!amount || !currency) {
      return res.status(400).json({
        error: 'Missing required fields: amount and currency',
      });
    }

    if (amount <= 0) {
      return res.status(400).json({
        error: 'Amount must be greater than 0',
      });
    }

    // Create payment object
    const paymentId = uuidv4();
    const payment = {
      id: paymentId,
      amount,
      currency,
      description: description || '',
      status: 'pending',
      createdAt: new Date().toISOString(),
    };

    // Store payment
    payments[paymentId] = payment;

    res.status(201).json({
      message: 'Payment created successfully',
      payment,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Internal server error',
      details: error.message,
    });
  }
});

/**
 * GET /payments/:id
 * Retrieve a payment by ID
 */
app.get('/payments/:id', (req, res) => {
  try {
    const { id } = req.params;

    const payment = payments[id];

    if (!payment) {
      return res.status(404).json({
        error: 'Payment not found',
      });
    }

    res.status(200).json({
      message: 'Payment retrieved successfully',
      payment,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Internal server error',
      details: error.message,
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Payment API server running on port ${PORT}`);
});

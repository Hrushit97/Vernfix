package com.banking.service;

import com.banking.dto.PaymentRequest;
import com.banking.dto.PaymentResponse;
import com.banking.exception.InvalidPaymentException;
import com.banking.exception.ResourceNotFoundException;
import com.banking.model.Payment;
import com.banking.model.Payment.PaymentStatus;
import com.banking.repository.PaymentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.UUID;

@Service
public class PaymentService {

    @Autowired
    private PaymentRepository paymentRepository;

    public PaymentResponse createPayment(PaymentRequest request) {
        // Validation
        if (request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new InvalidPaymentException("Amount must be greater than zero");
        }

        if (request.getFromAccount() == null || request.getFromAccount().isEmpty()) {
            throw new InvalidPaymentException("From account is required");
        }

        if (request.getToAccount() == null || request.getToAccount().isEmpty()) {
            throw new InvalidPaymentException("To account is required");
        }

        if (request.getFromAccount().equals(request.getToAccount())) {
            throw new InvalidPaymentException("From and To accounts cannot be the same");
        }

        // Create payment
        Payment payment = new Payment();
        payment.setTransactionId(UUID.randomUUID().toString());
        payment.setFromAccount(request.getFromAccount());
        payment.setToAccount(request.getToAccount());
        payment.setAmount(request.getAmount());
        payment.setDescription(request.getDescription());
        payment.setStatus(PaymentStatus.COMPLETED);

        Payment savedPayment = paymentRepository.save(payment);
        return PaymentResponse.fromEntity(savedPayment);
    }

    public PaymentResponse getPaymentById(Long id) {
        Payment payment = paymentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found with id: " + id));
        return PaymentResponse.fromEntity(payment);
    }

    public PaymentResponse getPaymentByTransactionId(String transactionId) {
        Payment payment = paymentRepository.findByTransactionId(transactionId)
                .orElseThrow(() -> new ResourceNotFoundException("Payment not found with transaction id: " + transactionId));
        return PaymentResponse.fromEntity(payment);
    }
}

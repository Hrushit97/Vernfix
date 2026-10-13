package com.banking.service;

import com.banking.dto.PaymentRequest;
import com.banking.dto.PaymentResponse;
import com.banking.exception.InvalidPaymentException;
import com.banking.exception.ResourceNotFoundException;
import com.banking.model.Payment;
import com.banking.model.Payment.PaymentStatus;
import com.banking.repository.PaymentRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

class PaymentServiceTest {

    @Mock
    private PaymentRepository paymentRepository;

    @InjectMocks
    private PaymentService paymentService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void testCreatePaymentSuccess() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount("ACC001");
        request.setToAccount("ACC002");
        request.setAmount(new BigDecimal("100.00"));
        request.setDescription("Test payment");

        Payment payment = new Payment();
        payment.setId(1L);
        payment.setTransactionId("test-uuid");
        payment.setFromAccount("ACC001");
        payment.setToAccount("ACC002");
        payment.setAmount(new BigDecimal("100.00"));
        payment.setStatus(PaymentStatus.COMPLETED);
        payment.setDescription("Test payment");

        when(paymentRepository.save(any(Payment.class))).thenReturn(payment);

        PaymentResponse response = paymentService.createPayment(request);

        assertNotNull(response);
        assertEquals("ACC001", response.getFromAccount());
        assertEquals("ACC002", response.getToAccount());
        assertEquals(new BigDecimal("100.00"), response.getAmount());
        verify(paymentRepository, times(1)).save(any(Payment.class));
    }

    @Test
    void testCreatePaymentInvalidAmount() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount("ACC001");
        request.setToAccount("ACC002");
        request.setAmount(BigDecimal.ZERO);
        request.setDescription("Test payment");

        assertThrows(InvalidPaymentException.class, () -> {
            paymentService.createPayment(request);
        });
    }

    @Test
    void testCreatePaymentNegativeAmount() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount("ACC001");
        request.setToAccount("ACC002");
        request.setAmount(new BigDecimal("-50.00"));
        request.setDescription("Test payment");

        assertThrows(InvalidPaymentException.class, () -> {
            paymentService.createPayment(request);
        });
    }

    @Test
    void testCreatePaymentMissingFromAccount() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount(null);
        request.setToAccount("ACC002");
        request.setAmount(new BigDecimal("100.00"));
        request.setDescription("Test payment");

        assertThrows(InvalidPaymentException.class, () -> {
            paymentService.createPayment(request);
        });
    }

    @Test
    void testCreatePaymentMissingToAccount() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount("ACC001");
        request.setToAccount(null);
        request.setAmount(new BigDecimal("100.00"));
        request.setDescription("Test payment");

        assertThrows(InvalidPaymentException.class, () -> {
            paymentService.createPayment(request);
        });
    }

    @Test
    void testCreatePaymentSameAccount() {
        PaymentRequest request = new PaymentRequest();
        request.setFromAccount("ACC001");
        request.setToAccount("ACC001");
        request.setAmount(new BigDecimal("100.00"));
        request.setDescription("Test payment");

        assertThrows(InvalidPaymentException.class, () -> {
            paymentService.createPayment(request);
        });
    }

    @Test
    void testGetPaymentByIdSuccess() {
        Payment payment = new Payment();
        payment.setId(1L);
        payment.setTransactionId("test-uuid");
        payment.setFromAccount("ACC001");
        payment.setToAccount("ACC002");
        payment.setAmount(new BigDecimal("100.00"));
        payment.setStatus(PaymentStatus.COMPLETED);

        when(paymentRepository.findById(1L)).thenReturn(Optional.of(payment));

        PaymentResponse response = paymentService.getPaymentById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
    }

    @Test
    void testGetPaymentByIdNotFound() {
        when(paymentRepository.findById(1L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> {
            paymentService.getPaymentById(1L);
        });
    }

    @Test
    void testGetPaymentByTransactionIdSuccess() {
        Payment payment = new Payment();
        payment.setId(1L);
        payment.setTransactionId("test-uuid-123");
        payment.setFromAccount("ACC001");
        payment.setToAccount("ACC002");
        payment.setAmount(new BigDecimal("100.00"));
        payment.setStatus(PaymentStatus.COMPLETED);

        when(paymentRepository.findByTransactionId("test-uuid-123"))
                .thenReturn(Optional.of(payment));

        PaymentResponse response = paymentService.getPaymentByTransactionId("test-uuid-123");

        assertNotNull(response);
        assertEquals("test-uuid-123", response.getTransactionId());
    }

    @Test
    void testGetPaymentByTransactionIdNotFound() {
        when(paymentRepository.findByTransactionId("invalid-uuid"))
                .thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> {
            paymentService.getPaymentByTransactionId("invalid-uuid");
        });
    }
}

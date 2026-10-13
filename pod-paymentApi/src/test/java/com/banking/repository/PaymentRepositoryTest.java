package com.banking.repository;

import com.banking.model.Payment;
import com.banking.model.Payment.PaymentStatus;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
public class PaymentRepositoryTest {

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private TestEntityManager entityManager;

    private Payment testPayment;

    @BeforeEach
    void setUp() {
        testPayment = new Payment();
        testPayment.setTransactionId("test-uuid-123");
        testPayment.setFromAccount("ACC001");
        testPayment.setToAccount("ACC002");
        testPayment.setAmount(new BigDecimal("100.00"));
        testPayment.setStatus(PaymentStatus.COMPLETED);
        testPayment.setDescription("Test payment");
        testPayment.setCreatedAt(LocalDateTime.now(ZoneId.systemDefault()));
    }

    @Test
    void testSavePayment() {
        Payment saved = paymentRepository.save(testPayment);

        assertNotNull(saved.getId());
        assertEquals("test-uuid-123", saved.getTransactionId());
        assertEquals("ACC001", saved.getFromAccount());
    }

    @Test
    void testFindByTransactionId() {
        paymentRepository.save(testPayment);
        entityManager.flush();

        Optional<Payment> found = paymentRepository.findByTransactionId("test-uuid-123");

        assertTrue(found.isPresent());
        assertEquals("ACC001", found.get().getFromAccount());
    }

    @Test
    void testFindByTransactionIdNotFound() {
        Optional<Payment> found = paymentRepository.findByTransactionId("invalid-uuid");

        assertFalse(found.isPresent());
    }

    @Test
    void testFindById() {
        Payment saved = paymentRepository.save(testPayment);
        entityManager.flush();

        Optional<Payment> found = paymentRepository.findById(saved.getId());

        assertTrue(found.isPresent());
        assertEquals("test-uuid-123", found.get().getTransactionId());
    }

    @Test
    void testPaymentAmount() {
        Payment saved = paymentRepository.save(testPayment);

        assertEquals(new BigDecimal("100.00"), saved.getAmount());
    }

    @Test
    void testPaymentStatus() {
        Payment saved = paymentRepository.save(testPayment);

        assertEquals(PaymentStatus.COMPLETED, saved.getStatus());
    }
}

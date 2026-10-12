package com.banking.repository;

import com.banking.model.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.List;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {

    Optional<Payment> findByTransactionId(String transactionId);

    List<Payment> findByFromAccount(String fromAccount);

    List<Payment> findByToAccount(String toAccount);

    List<Payment> findByFromAccountOrToAccount(String fromAccount, String toAccount);
}

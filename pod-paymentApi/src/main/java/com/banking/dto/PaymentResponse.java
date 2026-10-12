package com.banking.dto;

import com.banking.model.Payment;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PaymentResponse {

    private Long id;

    private String transactionId;

    private String fromAccount;

    private String toAccount;

    private BigDecimal amount;

    private String status;

    private String description;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    public static PaymentResponse fromEntity(Payment payment) {
        PaymentResponse response = new PaymentResponse();
        response.setId(payment.getId());
        response.setTransactionId(payment.getTransactionId());
        response.setFromAccount(payment.getFromAccount());
        response.setToAccount(payment.getToAccount());
        response.setAmount(payment.getAmount());
        response.setStatus(payment.getStatus().toString());
        response.setDescription(payment.getDescription());
        response.setCreatedAt(payment.getCreatedAt());
        response.setUpdatedAt(payment.getUpdatedAt());
        return response;
    }
}

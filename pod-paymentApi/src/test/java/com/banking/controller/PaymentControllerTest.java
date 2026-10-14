package com.banking.controller;

import com.banking.dto.PaymentRequest;
import com.banking.dto.PaymentResponse;
import com.banking.service.PaymentService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class PaymentControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PaymentService paymentService;

    @Autowired
    private ObjectMapper objectMapper;

    private PaymentRequest paymentRequest;
    private PaymentResponse paymentResponse;

    @BeforeEach
    void setUp() {
        paymentRequest = new PaymentRequest();
        paymentRequest.setFromAccount("ACC001");
        paymentRequest.setToAccount("ACC002");
        paymentRequest.setAmount(new BigDecimal("100.00"));
        paymentRequest.setDescription("Test payment");

        paymentResponse = new PaymentResponse();
        paymentResponse.setId(1L);
        paymentResponse.setTransactionId("test-uuid-123");
        paymentResponse.setFromAccount("ACC001");
        paymentResponse.setToAccount("ACC002");
        paymentResponse.setAmount(new BigDecimal("100.00"));
        paymentResponse.setStatus("COMPLETED");
        paymentResponse.setDescription("Test payment");
        paymentResponse.setCreatedAt(LocalDateTime.now());
    }

    @Test
    void testCreatePaymentSuccess() throws Exception {
        when(paymentService.createPayment(any(PaymentRequest.class)))
                .thenReturn(paymentResponse);

        mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(paymentRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.fromAccount").value("ACC001"))
                .andExpect(jsonPath("$.toAccount").value("ACC002"))
                .andExpect(jsonPath("$.amount").value(100.00));
    }

    @Test
    void testGetPaymentByIdSuccess() throws Exception {
        when(paymentService.getPaymentById(1L))
                .thenReturn(paymentResponse);

        mockMvc.perform(get("/api/payments/1")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.status").value("COMPLETED"));
    }

    @Test
    void testGetPaymentByTransactionIdSuccess() throws Exception {
        when(paymentService.getPaymentByTransactionId("test-uuid-123"))
                .thenReturn(paymentResponse);

        mockMvc.perform(get("/api/payments/transaction/test-uuid-123")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.transactionId").value("test-uuid-123"));
    }
}

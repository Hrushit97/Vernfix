package com.banking.integration;

import com.banking.dto.AuthRequest;
import com.banking.dto.PaymentRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = {
    "jwt.secret=MySecretKeyForTestingTheJWTTokenGenerationAndValidationProcess123",
    "jwt.expiration=3600000"
})
public class PaymentIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void testPaymentFlowIntegration() throws Exception {
        // Step 1: Login to get JWT token
        AuthRequest authRequest = new AuthRequest();
        authRequest.setUsername("user1");
        authRequest.setPassword("password123");

        MvcResult loginResult = mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(authRequest)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").exists())
                .andExpect(jsonPath("$.username").value("user1"))
                .andReturn();

        String token = objectMapper.readTree(loginResult.getResponse().getContentAsString())
                .get("token").asText();

        // Step 2: Create a payment with JWT token
        PaymentRequest paymentRequest = new PaymentRequest();
        paymentRequest.setFromAccount("ACC001");
        paymentRequest.setToAccount("ACC002");
        paymentRequest.setAmount(new BigDecimal("500.00"));
        paymentRequest.setDescription("Integration test payment");

        MvcResult paymentResult = mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", "Bearer " + token)
                .content(objectMapper.writeValueAsString(paymentRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists())
                .andExpect(jsonPath("$.fromAccount").value("ACC001"))
                .andReturn();

        String paymentId = objectMapper.readTree(paymentResult.getResponse().getContentAsString())
                .get("id").asText();

        // Step 3: Retrieve the created payment
        mockMvc.perform(get("/api/payments/" + paymentId)
                .contentType(MediaType.APPLICATION_JSON)
                .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(paymentId))
                .andExpect(jsonPath("$.amount").value(500.00))
                .andExpect(jsonPath("$.status").value("COMPLETED"));
    }

    @Test
    void testUnauthorizedAccessWithoutToken() throws Exception {
        PaymentRequest paymentRequest = new PaymentRequest();
        paymentRequest.setFromAccount("ACC001");
        paymentRequest.setToAccount("ACC002");
        paymentRequest.setAmount(new BigDecimal("100.00"));

        mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(paymentRequest)))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void testAuthenticationFailure() throws Exception {
        AuthRequest authRequest = new AuthRequest();
        authRequest.setUsername("invalid");
        authRequest.setPassword("invalid");

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(authRequest)))
                .andExpect(status().isUnauthorized());
    }
}

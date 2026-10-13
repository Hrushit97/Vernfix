package com.banking.exception;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@TestPropertySource(properties = {
    "jwt.secret=MySecretKeyForTestingTheJWTTokenGenerationAndValidationProcess123",
    "jwt.expiration=3600000"
})
public class GlobalExceptionHandlerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void testResourceNotFoundExceptionResponse() throws Exception {
        // Attempt to retrieve a non-existent payment
        mockMvc.perform(get("/api/payments/9999")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.message").exists())
                .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    void testUnauthorizedExceptionResponse() throws Exception {
        // Attempt login with invalid credentials
        String invalidLoginJson = "{\"username\":\"invalid\",\"password\":\"invalid\"}";

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidLoginJson))
                .andExpect(status().isUnauthorized())
                .andExpect(jsonPath("$.message").exists())
                .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    void testInvalidPaymentExceptionResponse() throws Exception {
        // Attempt to create payment with zero amount
        String invalidPaymentJson = "{" +
                "\"fromAccount\":\"ACC001\"," +
                "\"toAccount\":\"ACC002\"," +
                "\"amount\":0," +
                "\"description\":\"Invalid payment\"" +
                "}";

        mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidPaymentJson))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").exists());
    }

    @Test
    void testMissingRequestBodyException() throws Exception {
        // POST without body
        mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isBadRequest());
    }

    @Test
    void testMissingRequiredFieldException() throws Exception {
        // Missing required fields
        String incompletePaymentJson = "{" +
                "\"fromAccount\":\"ACC001\"" +
                "}";

        mockMvc.perform(post("/api/payments/create")
                .contentType(MediaType.APPLICATION_JSON)
                .content(incompletePaymentJson))
                .andExpect(status().isBadRequest());
    }
}

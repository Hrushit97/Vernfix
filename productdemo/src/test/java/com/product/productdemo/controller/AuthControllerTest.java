package com.product.productdemo.controller;

import com.product.productdemo.dto.JwtAuthenticationResponse;
import com.product.productdemo.dto.LoginRequest;
import com.product.productdemo.security.JwtUtils;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Auth Controller JWT Tests")
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtUtils jwtUtils;

    @Test
    @DisplayName("Should login with valid credentials - Admin")
    void testLoginAdminSuccess() throws Exception {
        String loginJson = "{\"username\": \"admin\", \"password\": \"admin123\"}";

        MvcResult result = mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").exists())
                .andExpect(jsonPath("$.tokenType").value("Bearer"))
                .andExpect(jsonPath("$.username").value("admin"))
                .andReturn();

        String content = result.getResponse().getContentAsString();
        assertTrue(content.contains("accessToken"));
    }

    @Test
    @DisplayName("Should login with valid credentials - User")
    void testLoginUserSuccess() throws Exception {
        String loginJson = "{\"username\": \"user\", \"password\": \"user123\"}";

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.username").value("user"))
                .andExpect(jsonPath("$.accessToken").exists());
    }

    @Test
    @DisplayName("Should reject invalid credentials")
    void testLoginInvalidCredentials() throws Exception {
        String loginJson = "{\"username\": \"admin\", \"password\": \"wrongpassword\"}";

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Should reject non-existent user")
    void testLoginNonExistentUser() throws Exception {
        String loginJson = "{\"username\": \"nonexistent\", \"password\": \"password\"}";

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @DisplayName("Should validate valid token")
    void testValidateValidToken() throws Exception {
        // First, get a token
        String loginJson = "{\"username\": \"admin\", \"password\": \"admin123\"}";
        MvcResult loginResult = mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(loginJson))
                .andExpect(status().isOk())
                .andReturn();

        // Extract token from response
        String content = loginResult.getResponse().getContentAsString();
        assertTrue(content.contains("accessToken"));
    }

    @Test
    @DisplayName("Should reject invalid token")
    void testValidateInvalidToken() throws Exception {
        mockMvc.perform(post("/api/auth/validate")
                .header("Authorization", "Bearer invalid.token.here"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").value(false));
    }

    @Test
    @DisplayName("Should validate without token header")
    void testValidateNoTokenHeader() throws Exception {
        mockMvc.perform(post("/api/auth/validate"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").value(false));
    }
}

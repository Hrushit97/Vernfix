package com.product.productdemo.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.test.util.ReflectionTestUtils;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("JWT Utils Tests")
class JwtUtilsTest {

    private JwtUtils jwtUtils;
    private UserDetails userDetails;

    @BeforeEach
    void setUp() {
        jwtUtils = new JwtUtils();
        ReflectionTestUtils.setField(jwtUtils, "jwtSecret", 
            "mySecretKeyForJWTAuthenticationProductDemoApplicationWithMoreThan256Bits");
        ReflectionTestUtils.setField(jwtUtils, "jwtExpirationMs", 86400000L);

        userDetails = User.builder()
            .username("testuser")
            .password("password")
            .roles("USER")
            .build();
    }

    @Test
    @DisplayName("Should generate valid JWT token")
    void testGenerateToken() {
        String token = jwtUtils.generateToken(userDetails);
        assertNotNull(token);
        assertTrue(token.contains("."));
    }

    @Test
    @DisplayName("Should extract username from token")
    void testGetUsernameFromToken() {
        String token = jwtUtils.generateToken(userDetails);
        String username = jwtUtils.getUsernameFromToken(token);
        assertEquals("testuser", username);
    }

    @Test
    @DisplayName("Should validate token syntax")
    void testValidateTokenSyntax() {
        String token = jwtUtils.generateToken(userDetails);
        assertTrue(jwtUtils.validateTokenSyntax(token));
    }

    @Test
    @DisplayName("Should reject invalid token syntax")
    void testInvalidTokenSyntax() {
        assertFalse(jwtUtils.validateTokenSyntax("invalid.token.here"));
    }

    @Test
    @DisplayName("Should validate token with user details")
    void testValidateToken() {
        String token = jwtUtils.generateToken(userDetails);
        assertTrue(jwtUtils.validateToken(token, userDetails));
    }
}

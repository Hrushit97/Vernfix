package com.banking.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@TestPropertySource(properties = {
    "jwt.secret=MySecretKeyForTestingTheJWTTokenGenerationAndValidationProcess123",
    "jwt.expiration=3600000"
})
public class JwtUtilTest {

    @Autowired
    private JwtUtil jwtUtil;

    private String testToken;
    private String testUsername = "testuser";
    private String testRole = "USER";
    private String testAccountNumber = "ACC001";

    @BeforeEach
    void setUp() {
        testToken = jwtUtil.generateToken(testUsername, testRole, testAccountNumber);
    }

    @Test
    void testGenerateToken() {
        assertNotNull(testToken);
        assertFalse(testToken.isEmpty());
    }

    @Test
    void testExtractUsername() {
        String username = jwtUtil.extractUsername(testToken);

        assertEquals(testUsername, username);
    }

    @Test
    void testExtractRole() {
        String role = jwtUtil.extractRole(testToken);

        assertEquals(testRole, role);
    }

    @Test
    void testExtractAccountNumber() {
        String accountNumber = jwtUtil.extractAccountNumber(testToken);

        assertEquals(testAccountNumber, accountNumber);
    }

    @Test
    void testIsTokenValid() {
        Boolean isValid = jwtUtil.isTokenValid(testToken);

        assertTrue(isValid);
    }

    @Test
    void testIsTokenInvalid() {
        String invalidToken = "invalid.token.here";

        Boolean isValid = jwtUtil.isTokenValid(invalidToken);

        assertFalse(isValid);
    }

    @Test
    void testIsTokenValidWithWrongSignature() {
        String malformedToken = testToken + "modified";

        Boolean isValid = jwtUtil.isTokenValid(malformedToken);

        assertFalse(isValid);
    }

    @Test
    void testGenerateMultipleTokens() {
        String token1 = jwtUtil.generateToken("user1", "USER", "ACC001");
        String token2 = jwtUtil.generateToken("user2", "ADMIN", "ACC002");

        assertNotEquals(token1, token2);
        assertEquals("user1", jwtUtil.extractUsername(token1));
        assertEquals("user2", jwtUtil.extractUsername(token2));
    }
}

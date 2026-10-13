package com.banking.service;

import com.banking.dto.AuthRequest;
import com.banking.dto.AuthResponse;
import com.banking.exception.UnauthorizedException;
import com.banking.model.User;
import com.banking.repository.UserRepository;
import com.banking.security.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

public class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private JwtUtil jwtUtil;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private AuthService authService;

    private User testUser;
    private AuthRequest authRequest;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);

        testUser = new User();
        testUser.setId(1L);
        testUser.setUsername("user1");
        testUser.setPassword("$2a$10$hashedPassword");
        testUser.setRole("USER");
        testUser.setAccountNumber("ACC001");
        testUser.setEnabled(true);

        authRequest = new AuthRequest();
        authRequest.setUsername("user1");
        authRequest.setPassword("password123");
    }

    @Test
    void testAuthenticateSuccess() {
        when(userRepository.findByUsername("user1")).thenReturn(Optional.of(testUser));
        when(passwordEncoder.matches("password123", testUser.getPassword())).thenReturn(true);
        when(jwtUtil.generateToken("user1", "USER", "ACC001")).thenReturn("valid-token");

        AuthResponse response = authService.authenticate(authRequest);

        assertNotNull(response);
        assertEquals("user1", response.getUsername());
        assertEquals("USER", response.getRole());
        assertEquals("ACC001", response.getAccountNumber());
        assertEquals("valid-token", response.getToken());
        verify(userRepository, times(1)).findByUsername("user1");
        verify(passwordEncoder, times(1)).matches("password123", testUser.getPassword());
        verify(jwtUtil, times(1)).generateToken("user1", "USER", "ACC001");
    }

    @Test
    void testAuthenticateUserNotFound() {
        when(userRepository.findByUsername("invalid")).thenReturn(Optional.empty());

        authRequest.setUsername("invalid");

        assertThrows(UnauthorizedException.class, () -> {
            authService.authenticate(authRequest);
        });

        verify(userRepository, times(1)).findByUsername("invalid");
        verify(passwordEncoder, never()).matches(anyString(), anyString());
    }

    @Test
    void testAuthenticateWrongPassword() {
        when(userRepository.findByUsername("user1")).thenReturn(Optional.of(testUser));
        when(passwordEncoder.matches("wrongPassword", testUser.getPassword())).thenReturn(false);

        authRequest.setPassword("wrongPassword");

        assertThrows(UnauthorizedException.class, () -> {
            authService.authenticate(authRequest);
        });

        verify(passwordEncoder, times(1)).matches("wrongPassword", testUser.getPassword());
        verify(jwtUtil, never()).generateToken(anyString(), anyString(), anyString());
    }

    @Test
    void testAuthenticateDisabledUser() {
        testUser.setEnabled(false);
        when(userRepository.findByUsername("user1")).thenReturn(Optional.of(testUser));
        when(passwordEncoder.matches("password123", testUser.getPassword())).thenReturn(true);

        assertThrows(UnauthorizedException.class, () -> {
            authService.authenticate(authRequest);
        });

        verify(jwtUtil, never()).generateToken(anyString(), anyString(), anyString());
    }
}

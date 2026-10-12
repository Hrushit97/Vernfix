package com.banking.service;

import com.banking.dto.AuthRequest;
import com.banking.dto.AuthResponse;
import com.banking.exception.UnauthorizedException;
import com.banking.model.User;
import com.banking.repository.UserRepository;
import com.banking.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public AuthResponse authenticate(AuthRequest request) {
        User user = userRepository.findByUsername(request.getUsername())
                .orElseThrow(() -> new UnauthorizedException("Invalid username or password"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new UnauthorizedException("Invalid username or password");
        }

        if (!user.getEnabled()) {
            throw new UnauthorizedException("User account is disabled");
        }

        String token = jwtUtil.generateToken(user.getUsername(), user.getRole(), user.getAccountNumber());

        AuthResponse response = new AuthResponse();
        response.setToken(token);
        response.setUsername(user.getUsername());
        response.setRole(user.getRole());
        response.setAccountNumber(user.getAccountNumber());

        return response;
    }
}

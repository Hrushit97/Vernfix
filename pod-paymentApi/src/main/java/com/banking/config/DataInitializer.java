package com.banking.config;

import com.banking.model.User;
import com.banking.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        // Check if users already exist
        if (userRepository.findByUsername("user1").isEmpty()) {
            User user1 = new User();
            user1.setUsername("user1");
            user1.setPassword(passwordEncoder.encode("password123"));
            user1.setEmail("user1@banking.com");
            user1.setRole("USER");
            user1.setEnabled(true);
            user1.setAccountNumber("ACC001");
            userRepository.save(user1);

            User user2 = new User();
            user2.setUsername("user2");
            user2.setPassword(passwordEncoder.encode("password456"));
            user2.setEmail("user2@banking.com");
            user2.setRole("USER");
            user2.setEnabled(true);
            user2.setAccountNumber("ACC002");
            userRepository.save(user2);

            User admin = new User();
            admin.setUsername("admin");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setEmail("admin@banking.com");
            admin.setRole("ADMIN");
            admin.setEnabled(true);
            admin.setAccountNumber("ADMIN001");
            userRepository.save(admin);

            System.out.println("✓ Test users initialized successfully");
        }
    }
}

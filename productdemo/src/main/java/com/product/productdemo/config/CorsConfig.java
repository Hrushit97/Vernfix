package com.product.productdemo.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

    /**
     * Configure CORS (Cross-Origin Resource Sharing)
     * Restricts which origins can access the API
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            // Allow only specified origins (change in production)
            .allowedOrigins(
                "http://localhost:3000",
                "http://localhost:8080",
                "http://127.0.0.1:3000"
            )
            // Allow specific HTTP methods
            .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
            // Allow credentials (cookies, authorization headers)
            .allowCredentials(true)
            // Allow these headers
            .allowedHeaders("*")
            // Cache preflight response for 1 hour
            .maxAge(3600);
    }
}

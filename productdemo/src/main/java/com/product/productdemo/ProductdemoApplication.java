package com.product.productdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;

@SpringBootApplication
@Configuration
@EnableMethodSecurity(prePostEnabled = true)
public class ProductdemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(ProductdemoApplication.class, args);
	}

}

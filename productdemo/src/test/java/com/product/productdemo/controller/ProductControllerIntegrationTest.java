package com.product.productdemo.controller;

import com.product.productdemo.entity.Product;
import com.product.productdemo.repository.ProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Product Controller Integration Tests")
class ProductControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    void setUp() {
        productRepository.deleteAll();
    }

    @Test
    @DisplayName("Should create product with valid data")
    void testCreateProductSuccess() throws Exception {
        String productJson = "{\"name\": \"Laptop\", \"price\": 999.99, \"quantity\": 5}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").exists())
                .andExpect(jsonPath("$.name").value("Laptop"))
                .andExpect(jsonPath("$.price").value(999.99))
                .andExpect(jsonPath("$.quantity").value(5));
    }

    @Test
    @DisplayName("Should get product by id successfully")
    void testGetProductSuccess() throws Exception {
        Product product = new Product("Mouse", 29.99, 50);
        Product savedProduct = productRepository.save(product);

        mockMvc.perform(get("/api/products/" + savedProduct.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(savedProduct.getId()))
                .andExpect(jsonPath("$.name").value("Mouse"))
                .andExpect(jsonPath("$.price").value(29.99))
                .andExpect(jsonPath("$.quantity").value(50));
    }

    @Test
    @DisplayName("Should return 404 when product not found")
    void testGetProductNotFound() throws Exception {
        mockMvc.perform(get("/api/products/999"))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("Should create multiple products")
    void testCreateMultipleProducts() throws Exception {
        String product1Json = "{\"name\": \"Laptop\", \"price\": 999.99, \"quantity\": 5}";
        String product2Json = "{\"name\": \"Mouse\", \"price\": 29.99, \"quantity\": 50}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(product1Json))
                .andExpect(status().isCreated());

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(product2Json))
                .andExpect(status().isCreated());

        assertEquals(2, productRepository.count());
    }

    @Test
    @DisplayName("Should create product with zero price")
    void testCreateProductWithZeroPrice() throws Exception {
        String productJson = "{\"name\": \"Free Item\", \"price\": 0.0, \"quantity\": 100}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.price").value(0.0));
    }

    @Test
    @DisplayName("Should create product with negative price")
    void testCreateProductWithNegativePrice() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": -100.0, \"quantity\": 5}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.price").value(-100.0));
    }

    @Test
    @DisplayName("Should create product with empty name")
    void testCreateProductWithEmptyName() throws Exception {
        String productJson = "{\"name\": \"\", \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should create product with null quantity")
    void testCreateProductWithNullQuantity() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 99.99, \"quantity\": null}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should get product after create")
    void testCreateAndThenGet() throws Exception {
        String productJson = "{\"name\": \"Keyboard\", \"price\": 79.99, \"quantity\": 20}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());

        // Create a new product and retrieve it
        Product product = new Product("Keyboard", 79.99, 20);
        Product savedProduct = productRepository.save(product);

        mockMvc.perform(get("/api/products/" + savedProduct.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Keyboard"));
    }

    @Test
    @DisplayName("Should handle invalid JSON")
    void testCreateProductWithInvalidJson() throws Exception {
        String invalidJson = "{invalid json}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidJson))
                .andExpect(status().isBadRequest());
    }

    private void assertEquals(long expected, long actual) {
        if (expected != actual) {
            throw new AssertionError("Expected: " + expected + ", Actual: " + actual);
        }
    }
}

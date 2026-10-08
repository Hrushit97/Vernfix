package com.product.productdemo;

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

@SpringBootTest
@AutoConfigureMockMvc
@DisplayName("Edge Case Tests")
class EdgeCaseTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ProductRepository productRepository;

    @BeforeEach
    void setUp() {
        productRepository.deleteAll();
    }

    @Test
    @DisplayName("Should handle very large product name")
    void testVeryLargeProductName() throws Exception {
        String largeName = "A".repeat(1000);
        String productJson = "{\"name\": \"" + largeName + "\", \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle decimal price with many decimal places")
    void testPriceWithManyDecimalPlaces() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 99.999999999, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle maximum integer quantity")
    void testMaxIntegerQuantity() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 99.99, \"quantity\": 2147483647}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle minimum integer quantity")
    void testMinIntegerQuantity() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 99.99, \"quantity\": -2147483648}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle product with special characters in name")
    void testProductNameWithSpecialCharacters() throws Exception {
        String productJson = "{\"name\": \"Item@#$%^&*()\", \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle product with unicode characters")
    void testProductNameWithUnicodeCharacters() throws Exception {
        String productJson = "{\"name\": \"商品名\", \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle very large price value")
    void testVeryLargePrice() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 999999999.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle very small price value")
    void testVerySmallPrice() throws Exception {
        String productJson = "{\"name\": \"Item\", \"price\": 0.01, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle whitespace in product name")
    void testProductNameWithWhitespace() throws Exception {
        String productJson = "{\"name\": \"   Product Name   \", \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should handle null product name")
    void testNullProductName() throws Exception {
        String productJson = "{\"name\": null, \"price\": 99.99, \"quantity\": 10}";

        mockMvc.perform(post("/api/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content(productJson))
                .andExpect(status().isCreated());
    }

    @Test
    @DisplayName("Should retrieve product by id 1")
    void testGetProductById1() throws Exception {
        Product product = new Product("Test", 99.99, 10);
        Product saved = productRepository.save(product);

        mockMvc.perform(get("/api/products/" + saved.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Test"));
    }

    @Test
    @DisplayName("Should return 404 for non-existent product id 0")
    void testGetProductByIdZero() throws Exception {
        mockMvc.perform(get("/api/products/0"))
                .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("Should return 404 for negative product id")
    void testGetProductByNegativeId() throws Exception {
        mockMvc.perform(get("/api/products/-1"))
                .andExpect(status().isNotFound());
    }
}

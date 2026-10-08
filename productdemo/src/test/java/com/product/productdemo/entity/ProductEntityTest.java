package com.product.productdemo.entity;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Product Entity Tests")
class ProductEntityTest {

    private Product product;

    @BeforeEach
    void setUp() {
        product = new Product();
    }

    @Test
    @DisplayName("Should create product with constructor")
    void testProductConstructor() {
        Product testProduct = new Product("Laptop", 999.99, 5);
        
        assertEquals("Laptop", testProduct.getName());
        assertEquals(999.99, testProduct.getPrice());
        assertEquals(5, testProduct.getQuantity());
    }

    @Test
    @DisplayName("Should set and get product id")
    void testSetGetId() {
        product.setId(1L);
        assertEquals(1L, product.getId());
    }

    @Test
    @DisplayName("Should set and get product name")
    void testSetGetName() {
        product.setName("Mouse");
        assertEquals("Mouse", product.getName());
    }

    @Test
    @DisplayName("Should set and get product price")
    void testSetGetPrice() {
        product.setPrice(29.99);
        assertEquals(29.99, product.getPrice());
    }

    @Test
    @DisplayName("Should set and get product quantity")
    void testSetGetQuantity() {
        product.setQuantity(50);
        assertEquals(50, product.getQuantity());
    }

    @Test
    @DisplayName("Should handle null values")
    void testNullValues() {
        product.setName(null);
        product.setPrice(null);
        product.setQuantity(null);
        
        assertNull(product.getName());
        assertNull(product.getPrice());
        assertNull(product.getQuantity());
    }

    @Test
    @DisplayName("Should handle zero price")
    void testZeroPrice() {
        product.setPrice(0.0);
        assertEquals(0.0, product.getPrice());
    }

    @Test
    @DisplayName("Should handle negative price")
    void testNegativePrice() {
        product.setPrice(-99.99);
        assertEquals(-99.99, product.getPrice());
    }

    @Test
    @DisplayName("Should handle negative quantity")
    void testNegativeQuantity() {
        product.setQuantity(-5);
        assertEquals(-5, product.getQuantity());
    }

    @Test
    @DisplayName("Should handle zero quantity")
    void testZeroQuantity() {
        product.setQuantity(0);
        assertEquals(0, product.getQuantity());
    }

    @Test
    @DisplayName("Should set multiple properties correctly")
    void testMultipleProperties() {
        product.setId(1L);
        product.setName("Keyboard");
        product.setPrice(79.99);
        product.setQuantity(20);
        
        assertEquals(1L, product.getId());
        assertEquals("Keyboard", product.getName());
        assertEquals(79.99, product.getPrice());
        assertEquals(20, product.getQuantity());
    }

    @Test
    @DisplayName("Should handle empty string name")
    void testEmptyStringName() {
        product.setName("");
        assertEquals("", product.getName());
    }

    @Test
    @DisplayName("Should create product with default constructor")
    void testDefaultConstructor() {
        Product newProduct = new Product();
        assertNull(newProduct.getId());
        assertNull(newProduct.getName());
        assertNull(newProduct.getPrice());
        assertNull(newProduct.getQuantity());
    }
}

package com.product.productdemo.repository;

import com.product.productdemo.entity.Product;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
@DisplayName("Product Repository Tests")
class ProductRepositoryTest {

    @Autowired
    private ProductRepository productRepository;

    private Product testProduct;

    @BeforeEach
    void setUp() {
        productRepository.deleteAll();
        testProduct = new Product("Laptop", 999.99, 5);
    }

    @Test
    @DisplayName("Should save product successfully")
    void testSaveProduct() {
        Product savedProduct = productRepository.save(testProduct);

        assertNotNull(savedProduct);
        assertNotNull(savedProduct.getId());
        assertEquals("Laptop", savedProduct.getName());
        assertEquals(999.99, savedProduct.getPrice());
        assertEquals(5, savedProduct.getQuantity());
    }

    @Test
    @DisplayName("Should find product by id")
    void testFindProductById() {
        Product savedProduct = productRepository.save(testProduct);

        Optional<Product> foundProduct = productRepository.findById(savedProduct.getId());

        assertTrue(foundProduct.isPresent());
        assertEquals("Laptop", foundProduct.get().getName());
    }

    @Test
    @DisplayName("Should return empty Optional when product not found")
    void testFindProductByIdNotFound() {
        Optional<Product> foundProduct = productRepository.findById(999L);

        assertFalse(foundProduct.isPresent());
    }

    @Test
    @DisplayName("Should update product successfully")
    void testUpdateProduct() {
        Product savedProduct = productRepository.save(testProduct);
        savedProduct.setName("Updated Laptop");
        savedProduct.setPrice(1299.99);

        Product updatedProduct = productRepository.save(savedProduct);

        assertEquals("Updated Laptop", updatedProduct.getName());
        assertEquals(1299.99, updatedProduct.getPrice());
    }

    @Test
    @DisplayName("Should delete product successfully")
    void testDeleteProduct() {
        Product savedProduct = productRepository.save(testProduct);
        productRepository.delete(savedProduct);

        Optional<Product> deletedProduct = productRepository.findById(savedProduct.getId());

        assertFalse(deletedProduct.isPresent());
    }

    @Test
    @DisplayName("Should save product with null name")
    void testSaveProductWithNullName() {
        Product nullNameProduct = new Product(null, 99.99, 10);
        Product savedProduct = productRepository.save(nullNameProduct);

        assertNotNull(savedProduct.getId());
        assertNull(savedProduct.getName());
    }

    @Test
    @DisplayName("Should save product with zero price")
    void testSaveProductWithZeroPrice() {
        Product zeroPriceProduct = new Product("Free Item", 0.0, 100);
        Product savedProduct = productRepository.save(zeroPriceProduct);

        assertEquals(0.0, savedProduct.getPrice());
    }

    @Test
    @DisplayName("Should save product with negative price")
    void testSaveProductWithNegativePrice() {
        Product negativePriceProduct = new Product("Item", -50.0, 5);
        Product savedProduct = productRepository.save(negativePriceProduct);

        assertEquals(-50.0, savedProduct.getPrice());
    }

    @Test
    @DisplayName("Should save product with zero quantity")
    void testSaveProductWithZeroQuantity() {
        Product zeroQtyProduct = new Product("Item", 99.99, 0);
        Product savedProduct = productRepository.save(zeroQtyProduct);

        assertEquals(0, savedProduct.getQuantity());
    }

    @Test
    @DisplayName("Should save product with negative quantity")
    void testSaveProductWithNegativeQuantity() {
        Product negativeQtyProduct = new Product("Item", 99.99, -5);
        Product savedProduct = productRepository.save(negativeQtyProduct);

        assertEquals(-5, savedProduct.getQuantity());
    }

    @Test
    @DisplayName("Should save multiple products")
    void testSaveMultipleProducts() {
        Product product1 = new Product("Laptop", 999.99, 5);
        Product product2 = new Product("Mouse", 29.99, 50);
        Product product3 = new Product("Keyboard", 79.99, 20);

        productRepository.save(product1);
        productRepository.save(product2);
        productRepository.save(product3);

        assertEquals(3, productRepository.count());
    }

    @Test
    @DisplayName("Should save and retrieve product with same data")
    void testSaveAndRetrieveProduct() {
        Product savedProduct = productRepository.save(testProduct);
        Optional<Product> retrievedProduct = productRepository.findById(savedProduct.getId());

        assertTrue(retrievedProduct.isPresent());
        assertEquals(savedProduct.getName(), retrievedProduct.get().getName());
        assertEquals(savedProduct.getPrice(), retrievedProduct.get().getPrice());
        assertEquals(savedProduct.getQuantity(), retrievedProduct.get().getQuantity());
    }

    @Test
    @DisplayName("Should delete all products")
    void testDeleteAllProducts() {
        productRepository.save(new Product("Product1", 10.0, 1));
        productRepository.save(new Product("Product2", 20.0, 2));

        productRepository.deleteAll();

        assertEquals(0, productRepository.count());
    }

    @Test
    @DisplayName("Should handle product with very large price")
    void testSaveProductWithLargePrice() {
        Product largeProduct = new Product("Expensive", 999999999.99, 1);
        Product savedProduct = productRepository.save(largeProduct);

        assertEquals(999999999.99, savedProduct.getPrice());
    }

    @Test
    @DisplayName("Should handle product with very large quantity")
    void testSaveProductWithLargeQuantity() {
        Product largeQtyProduct = new Product("Item", 99.99, 1000000);
        Product savedProduct = productRepository.save(largeQtyProduct);

        assertEquals(1000000, savedProduct.getQuantity());
    }

    @Test
    @DisplayName("Should save product with empty string name")
    void testSaveProductWithEmptyName() {
        Product emptyNameProduct = new Product("", 99.99, 10);
        Product savedProduct = productRepository.save(emptyNameProduct);

        assertEquals("", savedProduct.getName());
    }
}

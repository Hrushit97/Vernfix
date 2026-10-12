package com.product.productdemo.controller;

import com.product.productdemo.entity.Product;
import com.product.productdemo.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Product Controller Unit Tests")
class ProductControllerUnitTest {

    @Mock
    private ProductService productService;

    @InjectMocks
    private ProductController productController;

    private Product testProduct;

    @BeforeEach
    void setUp() {
        testProduct = new Product("Laptop", 999.99, 5);
        testProduct.setId(1L);
    }

    @Test
    @DisplayName("Should return 201 Created when product created successfully")
    void testCreateProductReturnsCreated() {
        when(productService.createProduct(any(Product.class))).thenReturn(testProduct);

        ResponseEntity<Product> response = productController.createProduct(testProduct);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Laptop", response.getBody().getName());
    }

    @Test
    @DisplayName("Should return created product with all fields")
    void testCreateProductReturnsAllFields() {
        when(productService.createProduct(any(Product.class))).thenReturn(testProduct);

        ResponseEntity<Product> response = productController.createProduct(testProduct);

        Product product = response.getBody();
        assertEquals(1L, product.getId());
        assertEquals("Laptop", product.getName());
        assertEquals(999.99, product.getPrice());
        assertEquals(5, product.getQuantity());
    }

    @Test
    @DisplayName("Should call service when creating product")
    void testCreateProductCallsService() {
        when(productService.createProduct(testProduct)).thenReturn(testProduct);

        productController.createProduct(testProduct);

        verify(productService, times(1)).createProduct(testProduct);
    }

    @Test
    @DisplayName("Should return 200 OK when product found")
    void testGetProductReturnsOk() {
        when(productService.getProductById(1L)).thenReturn(Optional.of(testProduct));

        ResponseEntity<Product> response = productController.getProduct(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
    }

    @Test
    @DisplayName("Should return product details when found")
    void testGetProductReturnsCorrectProduct() {
        when(productService.getProductById(1L)).thenReturn(Optional.of(testProduct));

        ResponseEntity<Product> response = productController.getProduct(1L);

        Product product = response.getBody();
        assertEquals("Laptop", product.getName());
        assertEquals(999.99, product.getPrice());
    }

    @Test
    @DisplayName("Should return 404 Not Found when product not found")
    void testGetProductReturnsNotFound() {
        when(productService.getProductById(999L)).thenReturn(Optional.empty());

        ResponseEntity<Product> response = productController.getProduct(999L);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    @DisplayName("Should call service when getting product")
    void testGetProductCallsService() {
        when(productService.getProductById(1L)).thenReturn(Optional.of(testProduct));

        productController.getProduct(1L);

        verify(productService, times(1)).getProductById(1L);
    }

    @Test
    @DisplayName("Should handle null response body in get request")
    void testGetProductNullBody() {
        when(productService.getProductById(999L)).thenReturn(Optional.empty());

        ResponseEntity<Product> response = productController.getProduct(999L);

        assertNull(response.getBody());
    }

    @Test
    @DisplayName("Should create product with minimum valid price")
    void testCreateProductWithMinimumPrice() {
        Product minPriceProduct = new Product("Budget Item", 0.01, 10);
        when(productService.createProduct(minPriceProduct)).thenReturn(minPriceProduct);

        ResponseEntity<Product> response = productController.createProduct(minPriceProduct);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals(0.01, response.getBody().getPrice());
    }

    @Test
    @DisplayName("Should create product with large price")
    void testCreateProductWithLargePrice() {
        Product largePriceProduct = new Product("Expensive", 999999.99, 1);
        when(productService.createProduct(largePriceProduct)).thenReturn(largePriceProduct);

        ResponseEntity<Product> response = productController.createProduct(largePriceProduct);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals(999999.99, response.getBody().getPrice());
    }

    @Test
    @DisplayName("Should create product with zero quantity")
    void testCreateProductWithZeroQuantity() {
        Product zeroQtyProduct = new Product("Out of Stock", 50.0, 0);
        when(productService.createProduct(zeroQtyProduct)).thenReturn(zeroQtyProduct);

        ResponseEntity<Product> response = productController.createProduct(zeroQtyProduct);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertEquals(0, response.getBody().getQuantity());
    }

    @Test
    @DisplayName("Should get product with id 1")
    void testGetProductWithIdOne() {
        when(productService.getProductById(1L)).thenReturn(Optional.of(testProduct));

        ResponseEntity<Product> response = productController.getProduct(1L);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(1L, response.getBody().getId());
    }

    @Test
    @DisplayName("Should get product with large id")
    void testGetProductWithLargeId() {
        Long largeId = 999999999L;
        Product largeIdProduct = new Product("Item", 99.99, 10);
        largeIdProduct.setId(largeId);

        when(productService.getProductById(largeId)).thenReturn(Optional.of(largeIdProduct));

        ResponseEntity<Product> response = productController.getProduct(largeId);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(largeId, response.getBody().getId());
    }
}

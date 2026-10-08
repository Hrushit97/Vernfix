package com.product.productdemo.service;

import com.product.productdemo.entity.Product;
import com.product.productdemo.repository.ProductRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("Product Service Unit Tests")
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @InjectMocks
    private ProductService productService;

    private Product testProduct;

    @BeforeEach
    void setUp() {
        testProduct = new Product("Laptop", 999.99, 5);
    }

    @Test
    @DisplayName("Should create product successfully")
    void testCreateProductSuccess() {
        when(productRepository.save(testProduct)).thenReturn(testProduct);

        Product result = productService.createProduct(testProduct);

        assertNotNull(result);
        assertEquals("Laptop", result.getName());
        assertEquals(999.99, result.getPrice());
        assertEquals(5, result.getQuantity());
        verify(productRepository, times(1)).save(testProduct);
    }

    @Test
    @DisplayName("Should call repository save method")
    void testCreateProductCallsRepository() {
        when(productRepository.save(any(Product.class))).thenReturn(testProduct);

        productService.createProduct(testProduct);

        verify(productRepository, times(1)).save(testProduct);
    }

    @Test
    @DisplayName("Should get product by id successfully")
    void testGetProductByIdSuccess() {
        testProduct.setId(1L);
        when(productRepository.findById(1L)).thenReturn(Optional.of(testProduct));

        Optional<Product> result = productService.getProductById(1L);

        assertTrue(result.isPresent());
        assertEquals("Laptop", result.get().getName());
        verify(productRepository, times(1)).findById(1L);
    }

    @Test
    @DisplayName("Should return empty Optional when product not found")
    void testGetProductByIdNotFound() {
        when(productRepository.findById(999L)).thenReturn(Optional.empty());

        Optional<Product> result = productService.getProductById(999L);

        assertFalse(result.isPresent());
        verify(productRepository, times(1)).findById(999L);
    }

    @Test
    @DisplayName("Should handle null product")
    void testCreateNullProduct() {
        when(productRepository.save(null)).thenReturn(null);

        Product result = productService.createProduct(null);

        assertNull(result);
    }

    @Test
    @DisplayName("Should create product with zero price")
    void testCreateProductWithZeroPrice() {
        Product zeroPriceProduct = new Product("Free Item", 0.0, 100);
        when(productRepository.save(zeroPriceProduct)).thenReturn(zeroPriceProduct);

        Product result = productService.createProduct(zeroPriceProduct);

        assertEquals(0.0, result.getPrice());
    }

    @Test
    @DisplayName("Should create product with negative price")
    void testCreateProductWithNegativePrice() {
        Product negativePriceProduct = new Product("Item", -50.0, 5);
        when(productRepository.save(negativePriceProduct))
            .thenReturn(negativePriceProduct);

        Product result = productService.createProduct(negativePriceProduct);

        assertEquals(-50.0, result.getPrice());
    }

    @Test
    @DisplayName("Should create product with null name")
    void testCreateProductWithNullName() {
        Product nullNameProduct = new Product(null, 99.99, 10);
        when(productRepository.save(nullNameProduct)).thenReturn(nullNameProduct);

        Product result = productService.createProduct(nullNameProduct);

        assertNull(result.getName());
    }

    @Test
    @DisplayName("Should handle multiple get requests")
    void testGetProductMultipleTimes() {
        testProduct.setId(1L);
        when(productRepository.findById(1L)).thenReturn(Optional.of(testProduct));

        Optional<Product> result1 = productService.getProductById(1L);
        Optional<Product> result2 = productService.getProductById(1L);

        assertTrue(result1.isPresent());
        assertTrue(result2.isPresent());
        verify(productRepository, times(2)).findById(1L);
    }

    @Test
    @DisplayName("Should verify repository interaction details")
    void testRepositoryInteractionDetails() {
        Product product = new Product("Mouse", 29.99, 50);
        when(productRepository.save(product)).thenReturn(product);

        productService.createProduct(product);

        verify(productRepository).save(product);
        verifyNoMoreInteractions(productRepository);
    }
}

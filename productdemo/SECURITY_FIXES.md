# Security Fixes and Recommendations

## Quick Fix Checklist

### 1️⃣ Disable H2 Console (IMMEDIATE)
**File**: `application-prod.yaml`
```yaml
spring:
  h2:
    console:
      enabled: false
```

### 2️⃣ Add Input Validation (HIGH PRIORITY)
**File**: `Product.java`
```java
import jakarta.validation.constraints.*;

public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Product name is required")
    private String name;

    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.0", inclusive = false)
    private Double price;

    @NotNull(message = "Quantity is required")
    @Min(value = 0)
    private Integer quantity;
}
```

### 3️⃣ Add Spring Security (CRITICAL)
**pom.xml** - Add dependency:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

**SecurityConfig.java**:
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeRequests()
            .requestMatchers("/api/products/**").authenticated()
            .anyRequest().permitAll()
            .and()
            .httpBasic();
        return http.build();
    }
}
```

### 4️⃣ Fix Configuration Files
**application.yaml**:
```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: validate  # was: update
    show-sql: false  # was: true
  datasource:
    username: ${DB_USER:sa}
    password: ${DB_PASSWORD:}
```

### 5️⃣ Add Request Validation in Controller
**ProductController.java**:
```java
import jakarta.validation.Valid;

@PostMapping
public ResponseEntity<Product> createProduct(@Valid @RequestBody Product product) {
    Product createdProduct = productService.createProduct(product);
    return ResponseEntity.status(HttpStatus.CREATED).body(createdProduct);
}
```

### 6️⃣ Add HTTPS/SSL Configuration
**application-prod.yaml**:
```yaml
server:
  ssl:
    key-store: ${SSL_KEYSTORE_PATH}
    key-store-password: ${SSL_KEYSTORE_PASSWORD}
    key-store-type: PKCS12
```

### 7️⃣ Add CORS Configuration
**CorsConfig.java**:
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("${ALLOWED_ORIGINS:http://localhost:3000}")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .maxAge(3600);
    }
}
```

### 8️⃣ Add Rate Limiting
**pom.xml**:
```xml
<dependency>
    <groupId>io.github.bucket4j</groupId>
    <artifactId>bucket4j-core</artifactId>
    <version>7.6.0</version>
</dependency>
```

### 9️⃣ Global Exception Handler
**GlobalExceptionHandler.java**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> handleValidation(...) {
        // Return proper error response
    }
}
```

### 🔟 Enable Logging Properly
**logback-spring.xml**:
```xml
<configuration>
    <springProperty name="LOG_FILE" source="logging.file.name"/>
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <file>${LOG_FILE}</file>
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
</configuration>
```

---

## Environment-Specific Configurations

### Development (application-dev.yaml)
```yaml
spring:
  h2:
    console:
      enabled: true
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: create-drop
```

### Production (application-prod.yaml)
```yaml
spring:
  h2:
    console:
      enabled: false
  jpa:
    show-sql: false
    hibernate:
      ddl-auto: validate
server:
  ssl:
    enabled: true
```

---

## Testing Security

- [ ] Test H2 console is disabled in prod
- [ ] Test all endpoints require authentication
- [ ] Test invalid inputs are rejected
- [ ] Test HTTPS redirects work
- [ ] Test CORS restrictions
- [ ] Test rate limiting works
- [ ] Run dependency check: `mvn org.owasp:dependency-check-maven:check`

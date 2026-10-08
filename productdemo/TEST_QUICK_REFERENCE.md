# 🧪 Test Quick Reference Card

## Run All Tests
```bash
mvn clean test
```
✅ 69 tests | ⏱️ ~15-20 seconds

---

## Run by Layer

| Layer | Command | Tests |
|-------|---------|-------|
| **Entity** | `mvn test -Dtest=ProductEntityTest` | 11 |
| **Repository** | `mvn test -Dtest=ProductRepositoryTest` | 14 |
| **Service** | `mvn test -Dtest=ProductServiceTest` | 11 |
| **Controller Unit** | `mvn test -Dtest=ProductControllerUnitTest` | 11 |
| **Controller Integration** | `mvn test -Dtest=ProductControllerIntegrationTest` | 11 |
| **Edge Cases** | `mvn test -Dtest=EdgeCaseTest` | 11 |

---

## Common Commands

### Run Specific Test Method
```bash
mvn test -Dtest=ProductRepositoryTest#testSaveProduct
```

### Run Tests Matching Pattern
```bash
mvn test -Dtest=*Repository*
```

### Generate Coverage Report
```bash
mvn clean test jacoco:report
# View: target/site/jacoco/index.html
```

### Run Tests in Parallel
```bash
mvn test -T 4
```

### Run with Detailed Output
```bash
mvn test -X
```

---

## Test File Structure

```
src/test/java/com/product/productdemo/
├── entity/
│   └── ProductEntityTest.java (11 tests)
├── repository/
│   └── ProductRepositoryTest.java (14 tests)
├── service/
│   └── ProductServiceTest.java (11 tests)
├── controller/
│   ├── ProductControllerUnitTest.java (11 tests)
│   └── ProductControllerIntegrationTest.java (11 tests)
├── EdgeCaseTest.java (11 tests)
└── ProductdemoApplicationTests.java
```

---

## Test Types at a Glance

| Test Type | Location | Mocks | Database | Speed |
|-----------|----------|-------|----------|-------|
| Entity | entity/ | No | No | ⚡⚡⚡ |
| Repository | repository/ | No | Yes | ⚡⚡ |
| Service | service/ | Yes | No | ⚡⚡⚡ |
| Controller Unit | controller/ | Yes | No | ⚡⚡⚡ |
| Controller Integration | controller/ | No | Yes | ⚡⚡ |
| Edge Case | root | No | Yes | ⚡⚡ |

---

## What Each Test Covers

### ProductEntityTest (11)
✅ Constructors  
✅ Getters/Setters  
✅ Null handling  
✅ Edge values  

### ProductRepositoryTest (14)
✅ Save operations  
✅ Find by ID  
✅ Update/Delete  
✅ Data persistence  
✅ Edge cases  

### ProductServiceTest (11)
✅ Create product  
✅ Get product  
✅ Mock interactions  
✅ Error scenarios  

### ProductControllerUnitTest (11)
✅ HTTP responses (201, 200, 404)  
✅ Request handling  
✅ Response bodies  
✅ Service calls  

### ProductControllerIntegrationTest (11)
✅ Full API flow  
✅ End-to-end testing  
✅ Database interactions  
✅ Multiple scenarios  

### EdgeCaseTest (11)
✅ Large values  
✅ Special characters  
✅ Boundary conditions  
✅ Unicode handling  

---

## Expected Results

```
✅ ProductEntityTest .............. 11/11
✅ ProductRepositoryTest .......... 14/14
✅ ProductServiceTest ............ 11/11
✅ ProductControllerUnitTest ...... 11/11
✅ ProductControllerIntegrationTest 11/11
✅ EdgeCaseTest .................. 11/11
────────────────────────────────────────
✅ TOTAL ....................... 69/69

Tests run: 69 | Failures: 0 | Errors: 0
Duration: ~15-20 seconds
BUILD SUCCESS ✅
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests not found | Check class name and location match |
| Database locked | Restart IDE/Maven |
| Port 8080 in use | `lsof -i :8080` and kill process |
| Compilation errors | `mvn clean compile` first |
| Timeout | Add `-DtimeoutInMinutes=5` |

---

## IDE Shortcuts

### IntelliJ IDEA
- **Run test class**: Right-click → Run 'ClassName'
- **Run test method**: Right-click → Run 'methodName'
- **Run all tests**: Ctrl+Shift+F10
- **Show coverage**: Ctrl+Shift+F2

### Eclipse
- **Run test class**: Right-click → Run As → JUnit Test
- **Run all tests**: Alt+Shift+X, T

### VS Code
- Install "Test Explorer UI"
- Click test in explorer panel

---

## Annotations Used

| Annotation | Purpose |
|-----------|---------|
| `@Test` | Mark as test method |
| `@DisplayName` | Readable test name |
| `@BeforeEach` | Setup before test |
| `@DataJpaTest` | DB testing context |
| `@SpringBootTest` | Full app context |
| `@ExtendWith(MockitoExtension)` | Enable Mockito |
| `@Mock` | Create mock object |
| `@InjectMocks` | Auto-inject mocks |

---

## Coverage Target

- **Entity**: 100%
- **Repository**: 95%+
- **Service**: 100%
- **Controller**: 90%+
- **Overall**: 90%+

---

## Test Data Examples

### Valid Product
```json
{"name": "Laptop", "price": 999.99, "quantity": 5}
```

### Zero Price
```json
{"name": "Free", "price": 0.0, "quantity": 100}
```

### Negative Price
```json
{"name": "Discount", "price": -50.0, "quantity": 10}
```

### Null Name
```json
{"name": null, "price": 99.99, "quantity": 10}
```

---

## Documentation Files

- **TEST_DOCUMENTATION.md** - Full details of all 69 tests
- **TEST_EXECUTION_GUIDE.md** - How to run tests (all methods)
- **TEST_SUMMARY.txt** - Overview and statistics
- **TEST_QUICK_REFERENCE.md** - This file!

---

## Next Steps

1. ✅ Run: `mvn clean test`
2. ✅ Verify all 69 tests pass
3. ✅ Review test output
4. ✅ Check coverage: `mvn jacoco:report`
5. ✅ Integrate into CI/CD

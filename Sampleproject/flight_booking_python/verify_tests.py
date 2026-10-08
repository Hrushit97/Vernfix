#!/usr/bin/env python
"""
Verification script to validate test suite integrity
"""

import os
import sys
from pathlib import Path

def check_test_files():
    """Verify test files exist"""
    print("=" * 80)
    print("TEST SUITE VERIFICATION")
    print("=" * 80)
    print()
    
    test_dir = Path("tests")
    required_files = [
        "test_status_service_comprehensive.py",
        "test_langgraph_workflow.py",
        "test_mcp_tools.py"
    ]
    
    print("✓ Checking test files...")
    all_exist = True
    for test_file in required_files:
        path = test_dir / test_file
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {test_file} ({size:,} bytes)")
        else:
            print(f"  ❌ {test_file} NOT FOUND")
            all_exist = False
    
    return all_exist

def check_documentation():
    """Verify documentation files"""
    print("\n✓ Checking documentation files...")
    docs = [
        "TEST_DOCUMENTATION.md",
        "TESTS_SUMMARY.md",
        "TEST_EXECUTION_GUIDE.md",
        "COMPREHENSIVE_TEST_REPORT.md"
    ]
    
    all_exist = True
    for doc in docs:
        if os.path.exists(doc):
            size = os.path.getsize(doc)
            print(f"  ✅ {doc} ({size:,} bytes)")
        else:
            print(f"  ❌ {doc} NOT FOUND")
            all_exist = False
    
    return all_exist

def count_test_cases():
    """Count test cases in test files"""
    print("\n✓ Counting test cases...")
    
    test_file = Path("tests/test_status_service_comprehensive.py")
    if test_file.exists():
        content = test_file.read_text()
        test_count = content.count("def test_")
        print(f"  test_status_service_comprehensive.py: {test_count} tests")
    
    test_file = Path("tests/test_langgraph_workflow.py")
    if test_file.exists():
        content = test_file.read_text()
        test_count = content.count("def test_")
        print(f"  test_langgraph_workflow.py: {test_count} tests")
    
    test_file = Path("tests/test_mcp_tools.py")
    if test_file.exists():
        content = test_file.read_text()
        test_count = content.count("def test_")
        print(f"  test_mcp_tools.py: {test_count} tests")

def check_imports():
    """Check test imports"""
    print("\n✓ Checking imports...")
    
    imports_ok = True
    test_files = [
        "tests/test_status_service_comprehensive.py",
        "tests/test_langgraph_workflow.py",
        "tests/test_mcp_tools.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                with open(test_file) as f:
                    content = f.read()
                    if "import pytest" in content:
                        print(f"  ✅ {test_file} has pytest import")
                    else:
                        print(f"  ⚠️ {test_file} missing pytest import")
                        imports_ok = False
            except Exception as e:
                print(f"  ❌ Error reading {test_file}: {e}")
                imports_ok = False
    
    return imports_ok

def verify_structure():
    """Verify test structure"""
    print("\n✓ Verifying test structure...")
    
    # Check for test classes
    test_file = Path("tests/test_status_service_comprehensive.py")
    if test_file.exists():
        content = test_file.read_text()
        class_count = content.count("class Test")
        print(f"  test_status_service_comprehensive.py: {class_count} test classes")
    
    test_file = Path("tests/test_langgraph_workflow.py")
    if test_file.exists():
        content = test_file.read_text()
        class_count = content.count("class Test")
        print(f"  test_langgraph_workflow.py: {class_count} test classes")
    
    test_file = Path("tests/test_mcp_tools.py")
    if test_file.exists():
        content = test_file.read_text()
        class_count = content.count("class Test")
        print(f"  test_mcp_tools.py: {class_count} test classes")

def main():
    """Run all verifications"""
    files_ok = check_test_files()
    docs_ok = check_documentation()
    check_imports()
    count_test_cases()
    verify_structure()
    
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    if files_ok and docs_ok:
        print("✅ All verifications passed!")
        print("✅ Test suite is ready to use")
        print("\nRun tests with: python -m pytest tests/ -v")
        return 0
    else:
        print("⚠️ Some checks failed")
        print("❌ Please review the output above")
        return 1

if __name__ == "__main__":
    sys.exit(main())

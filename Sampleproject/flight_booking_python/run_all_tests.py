#!/usr/bin/env python
"""
Test runner script for comprehensive test suites
"""

import subprocess
import sys

def run_tests():
    """Run all test suites and generate report"""
    
    test_files = [
        "tests/test_status_service_comprehensive.py",
        "tests/test_langgraph_workflow.py",
        "tests/test_mcp_tools.py"
    ]
    
    print("=" * 80)
    print("COMPREHENSIVE TEST SUITE EXECUTION")
    print("=" * 80)
    print()
    
    total_passed = 0
    total_failed = 0
    results = []
    
    for test_file in test_files:
        print(f"\n🧪 Running: {test_file}")
        print("-" * 80)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            output = result.stdout + result.stderr
            
            # Parse results
            lines = output.split('\n')
            for line in lines:
                if 'passed' in line and 'failed' not in line:
                    # Extract test count
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'passed' in part and i > 0:
                            try:
                                count = int(parts[i-1])
                                total_passed += count
                                results.append((test_file, count, 0))
                                print(f"✅ {count} tests passed")
                            except (ValueError, IndexError):
                                pass
                
                if 'failed' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if 'failed' in part and i > 0:
                            try:
                                count = int(parts[i-1])
                                total_failed += count
                                if results and results[-1][0] == test_file:
                                    results[-1] = (test_file, results[-1][1], count)
                                else:
                                    results.append((test_file, 0, count))
                                print(f"❌ {count} tests failed")
                            except (ValueError, IndexError):
                                pass
            
            if result.returncode != 0 and total_failed == 0:
                # Some other error - list failures
                for line in lines:
                    if 'FAILED' in line:
                        print(f"   {line}")
        
        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout running {test_file}")
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_file, passed, failed in results:
        print(f"\n{test_file}:")
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failed}")
        print(f"  Total: {passed + failed}")
    
    print(f"\n{'─' * 80}")
    print(f"TOTAL RESULTS:")
    print(f"  ✅ Total Passed: {total_passed}")
    print(f"  ❌ Total Failed: {total_failed}")
    print(f"  📊 Pass Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%" if (total_passed + total_failed) > 0 else "  📊 No tests found")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()

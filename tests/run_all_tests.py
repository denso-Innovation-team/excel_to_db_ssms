"""
tests/run_all_tests.py
Test Runner for All Components
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_all_tests():
    """Run all test suites"""

    print("🧪 DENSO888 Test Suite")
    print("=" * 50)
    print("Created by: Thammaphon Chittasuwanna (SDM)")
    print("เฮียตอมจัดหั้ย!!! - Testing Edition 🚀")
    print("=" * 50)
    print()

    # Discover and run tests
    loader = unittest.TestLoader()

    # Test directories
    test_dirs = ["tests", "tests/test_gui"]

    # Create test suite
    suite = unittest.TestSuite()

    # Add tests from all directories
    for test_dir in test_dirs:
        test_path = project_root / test_dir
        if test_path.exists():
            print(f"📁 Loading tests from: {test_dir}")
            discovered_tests = loader.discover(
                str(test_path), pattern="test_*.py", top_level_dir=str(project_root)
            )
            suite.addTests(discovered_tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True, failfast=False)

    print("\n🚀 Running tests...")
    print("-" * 50)

    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)

    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped) if hasattr(result, "skipped") else 0

    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {total_tests - failures - errors}")
    print(f"❌ Failed: {failures}")
    print(f"🔥 Errors: {errors}")
    print(f"⏭️ Skipped: {skipped}")

    if failures == 0 and errors == 0:
        print("\n🎉 All tests passed! เฮียตอมเก่งมาก!!! 🚀")
        return True
    else:
        print("\n⚠️ Some tests failed. Check output above for details.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

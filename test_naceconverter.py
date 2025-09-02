#!/usr/bin/env python3
"""
Test script for the NACE Converter package.
Run this to verify the package works correctly before publishing.
"""

import sys
from pathlib import Path

def test_direct_import():
    """Test importing the module directly."""
    print("=" * 60)
    print("Testing direct import of NACEConverter class...")
    print("-" * 60)
    
    try:
        from NACEConverter import NACEConverter
        converter = NACEConverter()
        print("✅ Direct import successful")
        return converter
    except Exception as e:
        print(f"❌ Direct import failed: {e}")
        return None

def test_package_import():
    """Test importing as a package (after installation)."""
    print("\n" + "=" * 60)
    print("Testing package import styles...")
    print("-" * 60)
    
    # Test direct import style
    try:
        from NACEConverter import NACEConverter
        print("✅ Direct import successful: from NACEConverter import NACEConverter")
    except ImportError as e:
        print(f"❌ Direct import failed: {e}")
        return None
    
    # Test module import with functions
    try:
        import NACEConverter
        if hasattr(NACEConverter, 'get_description'):
            print("✅ Module functions available: NACEConverter.get_description()")
            return NACEConverter
        else:
            print("⚠️  Module functions not available")
            return None
    except ImportError:
        print("⚠️  Module import failed")
        return None

def test_basic_functionality(converter):
    """Test basic converter functionality."""
    print("\n" + "=" * 60)
    print("Testing basic functionality...")
    print("-" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Get description with dots
    try:
        desc = converter.get_description("01.1")
        if desc:
            print(f"✅ get_description('01.1'): {desc[:50]}...")
            tests_passed += 1
        else:
            print("❌ get_description('01.1') returned None")
            tests_failed += 1
    except Exception as e:
        print(f"❌ get_description('01.1') failed: {e}")
        tests_failed += 1
    
    # Test 2: Get description without dots
    try:
        desc = converter.get_description("011")
        if desc:
            print(f"✅ get_description('011'): {desc[:50]}...")
            tests_passed += 1
        else:
            print("❌ get_description('011') returned None")
            tests_failed += 1
    except Exception as e:
        print(f"❌ get_description('011') failed: {e}")
        tests_failed += 1
    
    # Test 3: Search functionality
    try:
        results = converter.search_codes("farming")
        if results:
            print(f"✅ search_codes('farming'): Found {len(results)} results")
            print(f"   First result: {results[0]['code']} - {results[0]['description'][:40]}...")
            tests_passed += 1
        else:
            print("⚠️  search_codes('farming') returned no results")
            tests_passed += 1  # This might be valid
    except Exception as e:
        print(f"❌ search_codes('farming') failed: {e}")
        tests_failed += 1
    
    # Test 4: Get full info
    try:
        info = converter.get_full_info("01")
        if info:
            print(f"✅ get_full_info('01'): Level {info['level']}, Parent: '{info['parentCode']}'")
            tests_passed += 1
        else:
            print("❌ get_full_info('01') returned None")
            tests_failed += 1
    except Exception as e:
        print(f"❌ get_full_info('01') failed: {e}")
        tests_failed += 1
    
    # Test 5: Get all codes
    try:
        all_codes = converter.get_all_codes()
        print(f"✅ get_all_codes(): Found {len(all_codes)} total codes")
        tests_passed += 1
    except Exception as e:
        print(f"❌ get_all_codes() failed: {e}")
        tests_failed += 1
    
    # Test 6: Get codes by level
    try:
        level_2_codes = converter.get_codes_by_level(2)
        print(f"✅ get_codes_by_level(2): Found {len(level_2_codes)} level-2 codes")
        tests_passed += 1
    except Exception as e:
        print(f"❌ get_codes_by_level(2) failed: {e}")
        tests_failed += 1
    
    # Test 7: Get children
    try:
        children = converter.get_children("01")
        if children:
            print(f"✅ get_children('01'): Found {len(children)} child codes")
            tests_passed += 1
        else:
            print("⚠️  get_children('01') returned no children")
            tests_passed += 1  # Might be valid
    except Exception as e:
        print(f"❌ get_children('01') failed: {e}")
        tests_failed += 1
    
    print("\n" + "-" * 60)
    print(f"Results: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

def test_module_api():
    """Test the module-level API functions."""
    print("\n" + "=" * 60)
    print("Testing module-level API...")
    print("-" * 60)
    
    try:
        import NACEConverter
    except ImportError:
        print("⚠️  Module not installed, skipping module API tests")
        return False
    
    tests_passed = 0
    tests_failed = 0
    
    # Test module-level functions
    functions_to_test = [
        ("get_description", "01.1"),
        ("search_code", "painting"),
        ("search_codes", "agriculture"),
        ("get_full_info", "01"),
    ]
    
    for func_name, test_arg in functions_to_test:
        try:
            if hasattr(NACEConverter, func_name):
                func = getattr(NACEConverter, func_name)
                result = func(test_arg)
                if result is not None:
                    print(f"✅ NACEConverter.{func_name}('{test_arg}'): Success")
                    tests_passed += 1
                else:
                    print(f"⚠️  NACEConverter.{func_name}('{test_arg}'): Returned None")
                    tests_passed += 1  # Might be valid
            else:
                print(f"❌ NACEConverter.{func_name} not found")
                tests_failed += 1
        except Exception as e:
            print(f"❌ NACEConverter.{func_name}('{test_arg}'): {e}")
            tests_failed += 1
    
    print("\n" + "-" * 60)
    print(f"Module API Results: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

def test_edge_cases(converter):
    """Test edge cases and error handling."""
    print("\n" + "=" * 60)
    print("Testing edge cases...")
    print("-" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test non-existent code
    try:
        result = converter.get_description("XXXXX")
        if result is None:
            print("✅ Non-existent code returns None")
            tests_passed += 1
        else:
            print("❌ Non-existent code should return None")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Error handling non-existent code: {e}")
        tests_failed += 1
    
    # Test empty search
    try:
        results = converter.search_codes("")
        print(f"✅ Empty search handled: {len(results)} results")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Empty search failed: {e}")
        tests_failed += 1
    
    # Test search with max_results
    try:
        results = converter.search_codes("a", max_results=5)
        if len(results) <= 5:
            print(f"✅ max_results parameter works: {len(results)} results")
            tests_passed += 1
        else:
            print(f"❌ max_results not respected: got {len(results)} results")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Search with max_results failed: {e}")
        tests_failed += 1
    
    print("\n" + "-" * 60)
    print(f"Edge Cases Results: {tests_passed} passed, {tests_failed} failed")
    return tests_failed == 0

def main():
    """Run all tests."""
    print("\n" + "🧪 NACE Converter Test Suite " + "🧪")
    print("=" * 60)
    
    # Test direct import
    converter = test_direct_import()
    if not converter:
        print("\n❌ Cannot proceed without successful import")
        sys.exit(1)
    
    # Test basic functionality
    basic_ok = test_basic_functionality(converter)
    
    # Test edge cases
    edge_ok = test_edge_cases(converter)
    
    # Test package import (if installed)
    test_package_import()
    
    # Test module API (if installed)
    module_ok = test_module_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if basic_ok and edge_ok:
        print("✅ All core tests passed!")
        print("\nNext steps:")
        print("1. Install package locally: uv pip install -e .")
        print("2. Run tests again to verify package installation")
        print("3. Build package: python -m build")
        print("4. Upload to PyPI: twine upload dist/*")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before publishing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
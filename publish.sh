#!/bin/bash

# Publishing script for naceconverter package with comprehensive testing

set -e  # Exit on error

echo "🚀 Starting NACE Converter package publication process..."
echo "=" | tr "=" "$(printf '%.0s=' {1..60})"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Install it first:"
    echo ""
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or with Homebrew:"
    echo "  brew install uv"
    exit 1
fi

# Check if nacecodes.csv exists
if [ ! -f "nacecodes.csv" ]; then
    echo "❌ nacecodes.csv not found in current directory!"
    echo "Please ensure the CSV file is present before publishing."
    exit 1
fi

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/ __pycache__/ .pytest_cache/

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with uv..."
    uv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install build dependencies
echo "📚 Installing build dependencies..."
uv pip install --upgrade pip setuptools wheel build twine

# Run basic import test first
echo ""
echo "🧪 Running basic import test..."
python -c "
try:
    from NACEConverter import NACEConverter
    converter = NACEConverter()
    desc = converter.get_description('01.1')
    if desc:
        print('✅ Basic import test passed!')
        print(f'   Test result: 01.1 = {desc[:50]}...')
    else:
        print('❌ Basic test failed: Could not get description')
        exit(1)
except Exception as e:
    print(f'❌ Import test failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Basic tests failed. Please fix issues before continuing."
    exit 1
fi

# Install package in editable mode for testing
echo ""
echo "📦 Installing package in editable mode for testing..."
uv pip install -e .

# Run comprehensive tests if test file exists
if [ -f "test_naceconverter.py" ]; then
    echo ""
    echo "🧪 Running comprehensive test suite..."
    python test_naceconverter.py
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Tests failed. Please fix issues before publishing."
        exit 1
    fi
else
    echo ""
    echo "⚠️  test_naceconverter.py not found, running basic tests only..."
    
    # Run inline tests
    python -c "
import naceconverter as nc

print('Testing module-level API...')
tests_passed = 0
tests_failed = 0

# Test 1: get_description
try:
    desc = nc.get_description('01.1')
    if desc:
        print('✅ nc.get_description works')
        tests_passed += 1
    else:
        print('❌ nc.get_description returned None')
        tests_failed += 1
except Exception as e:
    print(f'❌ nc.get_description failed: {e}')
    tests_failed += 1

# Test 2: search_code
try:
    results = nc.search_code('farming')
    print(f'✅ nc.search_code works: {len(results)} results')
    tests_passed += 1
except Exception as e:
    print(f'❌ nc.search_code failed: {e}')
    tests_failed += 1

# Test 3: Dot-agnostic lookup
try:
    desc1 = nc.get_description('01.11')
    desc2 = nc.get_description('0111')
    if desc1 == desc2 and desc1 is not None:
        print('✅ Dot-agnostic lookup works')
        tests_passed += 1
    else:
        print('❌ Dot-agnostic lookup failed')
        tests_failed += 1
except Exception as e:
    print(f'❌ Dot-agnostic test failed: {e}')
    tests_failed += 1

print(f'\nTest Results: {tests_passed} passed, {tests_failed} failed')
if tests_failed > 0:
    exit(1)
"
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Module tests failed. Please fix issues before publishing."
        exit 1
    fi
fi

# Build the package
echo ""
echo "🔨 Building package..."
python -m build

# Check the distribution
echo ""
echo "🔍 Checking distribution files..."
twine check dist/*

if [ $? -ne 0 ]; then
    echo "❌ Distribution check failed. Please fix issues before publishing."
    exit 1
fi

# Display package contents
echo ""
echo "📋 Package contents:"
echo "-" | tr "-" "$(printf '%.0s-' {1..60})"
ls -lah dist/
echo "-" | tr "-" "$(printf '%.0s-' {1..60})"

# Verify wheel contents
echo ""
echo "📦 Verifying wheel contents..."
python -c "
import zipfile
import sys
from pathlib import Path

dist_files = list(Path('dist').glob('*.whl'))
if not dist_files:
    print('❌ No wheel file found')
    sys.exit(1)

wheel_file = dist_files[0]
print(f'Checking: {wheel_file.name}')
print('')

with zipfile.ZipFile(wheel_file, 'r') as zf:
    files = zf.namelist()
    
    # Check for required files
    required = ['NACEConverter.py', '__init__.py', 'nacecodes.csv']
    missing = []
    
    for req in required:
        if not any(req in f for f in files):
            missing.append(req)
    
    if missing:
        print(f'❌ Missing files in wheel: {missing}')
        sys.exit(1)
    else:
        print('✅ All required files present in wheel')
        
    # Check CSV file size
    csv_files = [f for f in files if 'nacecodes.csv' in f]
    if csv_files:
        info = zf.getinfo(csv_files[0])
        size_kb = info.file_size / 1024
        print(f'✅ CSV file included: {size_kb:.1f} KB')
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Wheel verification failed."
    exit 1
fi

# Final confirmation
echo ""
echo "=" | tr "=" "$(printf '%.0s=' {1..60})"
echo "✅ All checks passed! Package is ready for upload."
echo "=" | tr "=" "$(printf '%.0s=' {1..60})"
echo ""

# Ask for TestPyPI upload
read -p "📤 Upload to TestPyPI first? (recommended) [y/n]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📤 Uploading to TestPyPI..."
    twine upload --repository testpypi dist/*
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully uploaded to TestPyPI!"
        echo ""
        echo "Test installation with:"
        echo "  uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple naceconverter"
        echo ""
        
        read -p "Continue to upload to PyPI? [y/n]: " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "📌 Stopping here. You can upload to PyPI later with:"
            echo "  twine upload dist/*"
            exit 0
        fi
    else
        echo "❌ TestPyPI upload failed."
        exit 1
    fi
fi

# Upload to PyPI
echo ""
read -p "📤 Upload to PyPI? [y/n]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📤 Uploading to PyPI..."
    twine upload dist/*
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Package successfully published to PyPI!"
        echo ""
        echo "Install with:"
        echo "  uv pip install naceconverter"
        echo "  # or"
        echo "  pip install naceconverter"
        echo ""
        echo "View at: https://pypi.org/project/naceconverter/"
    else
        echo "❌ PyPI upload failed."
        exit 1
    fi
else
    echo "📌 Upload cancelled. You can upload later with:"
    echo "  twine upload dist/*"
fi
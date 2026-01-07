#!/bin/bash
set -e

cd /Users/dalebrubaker/Documents/GitHub/sourcegraph-mcp

# Activate virtual environment
source .venv/bin/activate

# Install build tools
pip install build twine

# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build

# Check
python -m twine check dist/*

# Show files
echo "📋 Files built:"
ls -lh dist/

echo ""
echo "✅ Package built successfully!"
echo ""
echo "Now run: python -m twine upload dist/*"
echo "Username: __token__"
echo "Password: (your PyPI token)"

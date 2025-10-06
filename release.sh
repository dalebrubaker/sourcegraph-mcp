#!/bin/bash
# Release script for publishing to PyPI

set -e  # Exit on error

echo "🚀 Releasing sourcegraph-mcp to PyPI"
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run this script from the project root."
    exit 1
fi

# Get version from pyproject.toml
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📦 Version: $VERSION"
echo ""

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf dist/ build/ *.egg-info
echo ""

# Build the package
echo "🔨 Building package..."
python3 -m build
echo ""

# Check the package
echo "🔍 Checking package..."
python3 -m twine check dist/*
echo ""

# Show what will be uploaded
echo "📋 Files to be uploaded:"
ls -lh dist/
echo ""

# Ask for confirmation
read -p "Upload to PyPI? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Upload cancelled"
    exit 1
fi

# Upload to PyPI
echo "⬆️  Uploading to PyPI..."
python3 -m twine upload dist/*

echo ""
echo "✅ Successfully released version $VERSION to PyPI!"
echo ""
echo "🏷️  Don't forget to:"
echo "  1. Commit and push changes: git add . && git commit -m 'Release v$VERSION' && git push"
echo "  2. Create a git tag: git tag v$VERSION && git push origin v$VERSION"
echo "  3. Create a GitHub release at: https://github.com/dalebrubaker/sourcegraph-mcp/releases/new"

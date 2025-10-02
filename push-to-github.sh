#!/bin/bash
# Quick commands to push to GitHub

cd /Users/dalebrubaker/Documents/GitHub/sourcegraph-mcp

# Initialize and commit
git init
git add .
git commit -m "Initial commit: SourceGraph MCP server"

# Connect to GitHub (you'll create the repo first)
echo ""
echo "Now go to: https://github.com/new"
echo "Create repo named: sourcegraph-mcp"
echo "Make it PUBLIC"
echo "Do NOT initialize with README"
echo ""
echo "Then run:"
echo "  git remote add origin https://github.com/dalebrubaker/sourcegraph-mcp.git"
echo "  git branch -M main"  
echo "  git push -u origin main"

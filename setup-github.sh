#!/bin/bash
# Complete GitHub setup script

cd "$(dirname "$0")"

echo "🚀 Setting up sourcegraph-mcp for GitHub..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📝 Adding files to git..."
git add .

echo ""
echo "📊 Git status:"
git status --short

echo ""
echo "💾 Creating initial commit..."
git commit -m "Initial commit: SourceGraph MCP server

Features:
- Full SourceGraph GraphQL API integration
- Three powerful search tools (literal, regex, config check)
- Support for local and cloud SourceGraph instances
- Comprehensive documentation (README, SETUP, QUICKSTART)
- Security best practices (config.json git-ignored)
- MIT License

Cost: 50-150x cheaper than loading full codebase into context"

echo ""
echo "✅ Local repository ready!"
echo ""
echo "=========================================="
echo "Next: Create GitHub repository"
echo "=========================================="
echo ""
echo "GitHub CLI method (if you have gh installed):"
echo ""
echo "  gh repo create sourcegraph-mcp --public --source=. --remote=origin"
echo "  git push -u origin main"
echo ""
echo "Manual method:"
echo ""
echo "1. Go to: https://github.com/new"
echo ""
echo "2. Fill in:"
echo "   Repository name: sourcegraph-mcp"
echo "   Description: Model Context Protocol server for SourceGraph code search"
echo "   Visibility: Public"
echo "   ⚠️  Do NOT check 'Add a README' (we have one)"
echo ""
echo "3. After creating, run these commands:"
echo ""
echo "   git remote add origin https://github.com/dalebrubaker/sourcegraph-mcp.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "=========================================="
echo "✨ Your repo will be live at:"
echo "https://github.com/dalebrubaker/sourcegraph-mcp"
echo "=========================================="

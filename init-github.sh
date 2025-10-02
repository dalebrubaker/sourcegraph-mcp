#!/bin/bash
# Initialize Git repository and prepare for GitHub

echo "🚀 Initializing SourceGraph MCP for GitHub..."
echo ""

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "ℹ️  Git repository already initialized"
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Show status
echo ""
echo "📊 Git status:"
git status

echo ""
echo "✅ Ready for first commit!"
echo ""
echo "Next steps:"
echo ""
echo "1. Create initial commit:"
echo "   git commit -m \"Initial commit: SourceGraph MCP server\""
echo ""
echo "2. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Name: sourcegraph-mcp"
echo "   - Description: Model Context Protocol server for SourceGraph code search"
echo "   - Visibility: Public"
echo "   - Do NOT initialize with README (we already have one)"
echo ""
echo "3. Connect to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/sourcegraph-mcp.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Update README.md and pyproject.toml with your GitHub username"
echo ""
echo "🎉 Then share your repository with the world!"

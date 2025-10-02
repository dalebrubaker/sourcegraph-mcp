# Quick Start

Get up and running with SourceGraph MCP in 5 minutes!

## Prerequisites

- Python 3.10+
- SourceGraph running (local or cloud)
- Claude Desktop

## Installation

```bash
# 1. Clone or download
git clone https://github.com/dalebrubaker/sourcegraph-mcp.git
cd sourcegraph-mcp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get your SourceGraph token
# Visit: http://localhost:3370/user/settings/tokens
# Create a new token and copy it

# 4. Configure (choose one)

# Option A: Environment variables
export SOURCEGRAPH_URL="http://localhost:3370"
export SOURCEGRAPH_TOKEN="your-token-here"

# Option B: Config file
cp config.example.json config.json
# Edit config.json with your token

# 5. Test it works
python test_connection.py

# 6. Add to Claude Desktop config
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Add this:
{
  "mcpServers": {
    "sourcegraph": {
      "command": "python",
      "args": ["/full/path/to/sourcegraph-mcp/server.py"],
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "your-token-here"
      }
    }
  }
}

# 7. Restart Claude Desktop (Cmd+Q, then reopen)

# 8. Try it!
# In Claude: "Search for TODO comments in my code"
```

## Usage Examples

```
"Find all usages of PlaceOrder"
"Search for Python functions that start with 'get_'"
"Find TODO comments in the backend repo"
"Search for classes ending with Service in C#"
```

## Need Help?

- **Full Guide:** See [SETUP.md](SETUP.md)
- **Troubleshooting:** See [README.md#troubleshooting](README.md#troubleshooting)
- **Issues:** [GitHub Issues](https://github.com/dalebrubaker/sourcegraph-mcp/issues)

## What This Does

- ✅ Search 500k+ lines of code instantly
- ✅ Works with C#, Python, and 40+ languages
- ✅ 50-150x cheaper than loading full codebase
- ✅ No local indexing needed
- ✅ One-time permission setup

Built with ❤️ for developers who want smarter code search.

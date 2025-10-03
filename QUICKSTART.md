# Quick Start

Get up and running with SourceGraph MCP in 5 minutes!

## Prerequisites

- Python 3.10+
- SourceGraph running (local or cloud)
- Claude Desktop or Claude Code

## Installation

```bash
# Recommended: Install with pipx
pipx install sourcegraph-mcp

# Alternative: From source
git clone https://github.com/dalebrubaker/sourcegraph-mcp.git
cd sourcegraph-mcp
pip install -e .
```

## Configuration

**IMPORTANT:** Replace the URL and token with your actual SourceGraph instance details.

```bash
# 1. Get your SourceGraph token
# Visit: http://localhost:3370/user/settings/tokens
# Create a new token and copy it

# 2. Set environment variables
export SOURCEGRAPH_URL="http://localhost:3370"
export SOURCEGRAPH_TOKEN="sgp_your_token_here"

# 3. Test it works
python test_connection.py
```

## Claude Desktop Setup

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "sgp_your_token_here"
      }
    }
  }
}
```

Restart Claude Desktop (Cmd+Q, then reopen).

## Claude Code Setup

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "sgp_your_token_here"
      }
    }
  },
  "permissions": {
    "allow": ["mcp__sourcegraph__*"]
  }
}
```
**IMPORTANT:** Replace the URL and token with your actual SourceGraph instance details.

Restart Claude Code and verify with `/mcp`.

**Note:** Permissions are Claude Code-specific. Other clients may not need them.

## Other MCP Clients (Cursor, Windsurf, Zed, Cline, etc.)

Most MCP clients follow a similar pattern:

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "sgp_your_token_here"
      }
    }
  }
}
```

Refer to your client's documentation for the config file location. See [README.md](README.md#other-mcp-clients-cursor-windsurf-zed-cline-etc) for details.

## Usage Examples

### Symbol Definitions (Go to Definition)
```
"Where is the ProcessOrder function defined?"
"Find the definition of CustomerService class"
"Show me where API_KEY is declared"
"Locate the HandleRequest method definition with line number"
```

### Symbol References (Find Usages)
```
"Find all calls to ProcessOrder"
"Where is CustomerService used in the codebase?"
"Show me all references to API_KEY"
"Find everywhere HandleRequest is invoked"
```

### General Code Search
```
"Search for TODO comments in the backend repo"
"Find error handling code in Python files"
"Search for classes ending with Service in C#"
"Find all functions that start with 'get_' in JavaScript"
```

### Regex Search
```
"Find all class definitions matching 'class \\w+Controller'"
"Search for TODO or FIXME comments"
"Find getter/setter methods using regex"
```

## What You Get

### ⚡ Fast Symbol Search
- **<100ms lookups** using SourceGraph's indexed symbols
- **Precise results**: Definition vs references clearly separated
- **Line numbers**: Exact file path, line, and column position

### 🔍 Powerful Code Search
- **Instant results** across millions of lines
- **Smart filtering**: By repo, file, language, and more
- **Regex support**: Complex pattern matching

### 💰 Cost Efficient
- **~400 tokens** per search vs 50k+ loading files
- **No file loading**: Pinpoint results without context bloat
- **Scales**: Works across entire codebase

## Features at a Glance

| Feature | What It Does | Example Query |
|---------|--------------|---------------|
| `find_symbol_definition` | Find where symbols are declared | "Where is ProcessOrder defined?" |
| `find_symbol_references` | Find where symbols are used | "Find all calls to ProcessOrder" |
| `search_sourcegraph` | General text search | "Search for authentication code" |
| `search_sourcegraph_regex` | Pattern matching | "Find TODO comments" |
| `get_sourcegraph_config` | View configuration | "Show my SourceGraph config" |

## Verification

After setup, ask Claude:
```
"Find the definition of any common function in my codebase"
```

You should see:
- ✅ File path
- ✅ Line number
- ✅ Symbol kind (function, class, etc.)
- ✅ Repository name

## Need Help?

- **Full Guide:** See [README.md](README.md)
- **Setup Details:** See [SETUP.md](SETUP.md)
- **Troubleshooting:** See [README.md#troubleshooting](README.md#troubleshooting)
- **Issues:** [GitHub Issues](https://github.com/dalebrubaker/sourcegraph-mcp/issues)

## What This Does

- ✅ Instant symbol lookups with SourceGraph's index
- ✅ Separate "definition" vs "usage" searches
- ✅ Search 500k+ lines instantly
- ✅ Works with C#, Python, and 75+ languages
- ✅ 50-150x cheaper than loading full codebase
- ✅ No local indexing needed
- ✅ One-time setup

Built with ❤️ for developers who want smarter, faster code navigation.

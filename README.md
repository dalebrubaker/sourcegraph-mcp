# SourceGraph MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides code search capabilities through SourceGraph's GraphQL API. Works with both self-hosted and cloud SourceGraph instances.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

🔍 **Powerful Code Search**
- Full SourceGraph query syntax support
- Literal and regex pattern matching  
- Filter by repository, file, language
- Cross-repository search

⚡ **Fast & Lightweight**
- Direct GraphQL API calls (no local indexing)
- Async operation for responsiveness
- Configurable timeouts

🌐 **Flexible Deployment**
- Works with local SourceGraph instances
- Supports cloud/hosted SourceGraph
- Environment variable or config file setup

🤖 **Claude Integration**
- Seamless integration with Claude Desktop
- Compatible with Claude Code CLI
- Works with any MCP-compatible client

## Quick Start

### 1. Install Dependencies

```bash
git clone https://github.com/dalebrubaker/sourcegraph-mcp.git
cd sourcegraph-mcp
pip install -r requirements.txt
```

### 2. Configure SourceGraph Access

**Option A: Environment Variables (Recommended)**

```bash
export SOURCEGRAPH_URL="http://localhost:3370"  # or your cloud URL
export SOURCEGRAPH_TOKEN="your-access-token"
```

**Option B: Config File**

```bash
cp config.example.json config.json
# Edit config.json with your settings
```

### 3. Generate SourceGraph Access Token

1. Navigate to your SourceGraph instance
2. Go to **Settings** → **Access tokens**
3. Click **Generate new token**
4. Copy the token and use it in your configuration

For local instances: `http://localhost:3370/user/settings/tokens`

### 4. Configure Claude Desktop

Add to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "python",
      "args": ["/path/to/sourcegraph-mcp/server.py"],
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "your-token-here"
      }
    }
  }
}
```

**For cloud SourceGraph:**

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "python",
      "args": ["/path/to/sourcegraph-mcp/server.py"],
      "env": {
        "SOURCEGRAPH_URL": "https://sourcegraph.yourcompany.com",
        "SOURCEGRAPH_TOKEN": "your-token-here"
      }
    }
  }
}
```

### 5. Restart Claude Desktop

Completely quit and restart Claude Desktop to load the MCP server.

## Usage Examples

Once configured, Claude can automatically search your codebase:

### Basic Search

```
"Find all usages of PlaceOrder in C# files"
```

Claude will use: `search_sourcegraph("PlaceOrder lang:csharp")`

### Repository-Specific Search

```
"Search for TODO comments in the trading-engine repository"
```

Claude will use: `search_sourcegraph("TODO repo:myorg/trading-engine")`

### Regex Search

```
"Find all class names that end with 'Service'"
```

Claude will use: `search_sourcegraph_regex("class \\w+Service")`

### Combined Filters

```
"Find Python functions that start with 'get_' or 'set_'"
```

Claude will use: `search_sourcegraph_regex("def (get|set)_\\w+", "lang:python")`

## Available Tools

### `search_sourcegraph`

Search code using SourceGraph's literal search.

**Parameters:**
- `query` (string, required): Search query using SourceGraph syntax
- `max_results` (integer, optional): Maximum results to return (default: 10)

**Query Syntax:**
- `repo:owner/name` - Filter by repository
- `file:pattern` - Filter by file path
- `lang:language` - Filter by programming language  
- `case:yes` - Case-sensitive search
- `-term` - Exclude term

**Examples:**
```
PlaceOrder lang:csharp
repo:myorg/myrepo TODO
file:\.py$ import pandas
repo:myorg/backend -file:test
```

### `search_sourcegraph_regex`

Search code using regular expressions.

**Parameters:**
- `pattern` (string, required): Regular expression pattern
- `filters` (string, optional): Additional SourceGraph filters
- `max_results` (integer, optional): Maximum results (default: 10)

**Examples:**
```
pattern: "class \w+Service"
pattern: "def (get|set)_\w+"
pattern: "TODO|FIXME|HACK", filters: "repo:myorg/backend"
```

### `get_sourcegraph_config`

Check current configuration and connection status.

## SourceGraph Query Syntax

SourceGraph supports powerful query syntax:

| Syntax | Description | Example |
|--------|-------------|---------|
| `repo:` | Filter by repository | `repo:myorg/myrepo` |
| `file:` | Filter by file pattern | `file:\.cs$` |
| `lang:` | Filter by language | `lang:python` |
| `case:yes` | Case-sensitive search | `case:yes MyClass` |
| `-term` | Exclude term | `-test` |
| `OR` | Boolean OR | `get OR set` |
| `AND` | Boolean AND | `class AND Service` |
| `count:N` | Limit results | `count:50` |

See [SourceGraph search syntax docs](https://docs.sourcegraph.com/code_search/reference/queries) for more.

## Configuration

### Environment Variables

- `SOURCEGRAPH_URL` - SourceGraph instance URL (default: `http://localhost:3370`)
- `SOURCEGRAPH_TOKEN` - Access token for authentication (required)

### Config File (`config.json`)

```json
{
  "sourcegraph_url": "http://localhost:3370",
  "access_token": "your-token",
  "timeout": 30
}
```

Environment variables take precedence over config file values.

## Troubleshooting

### "No access token configured"

Make sure you've set `SOURCEGRAPH_TOKEN` environment variable or added it to `config.json`.

### "Connection refused" or "HTTP 502"

- Verify SourceGraph is running: `curl http://localhost:3370`
- Check the URL in your configuration
- For cloud instances, ensure you have network access

### "Authentication failed" or "HTTP 401"

- Verify your access token is correct
- Regenerate the token in SourceGraph settings
- Check token hasn't expired

### MCP Server Not Showing in Claude

1. Verify the config file syntax is valid JSON
2. Check the path to `server.py` is absolute and correct
3. Completely quit and restart Claude Desktop (not just close window)
4. Check Claude logs: Help → View Logs

### No Results Found

- Test the same query in SourceGraph UI first
- Check if repositories are indexed in SourceGraph
- Try simpler queries to verify connection
- Use `get_sourcegraph_config` tool to check setup

## Development

### Testing Locally

```bash
# Test the server directly
python server.py

# With environment variables
SOURCEGRAPH_URL=http://localhost:3370 SOURCEGRAPH_TOKEN=your-token python server.py
```

### Project Structure

```
sourcegraph-mcp/
├── server.py              # Main MCP server
├── requirements.txt       # Python dependencies
├── config.example.json    # Example configuration
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore            # Git ignore rules
```

## Security Notes

- **Never commit `config.json` with real tokens** - it's in `.gitignore` by default
- Use environment variables in CI/CD pipelines
- Rotate access tokens regularly
- Use read-only tokens when possible

## Cost Comparison

| Method | Tokens per Query | Cost per Query (Sonnet 4.5) |
|--------|------------------|------------------------------|
| Load full codebase | 150,000 | $0.45-$0.56 |
| With prompt caching | 150,000 | $0.045 (after first) |
| **SourceGraph MCP** | **2,000-5,000** | **$0.006-$0.015** |

**50-150x cheaper than loading your entire codebase!**

## Requirements

- Python 3.10+
- SourceGraph instance (local or cloud)
- Claude Desktop or MCP-compatible client

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Issues:** [GitHub Issues](https://github.com/dalebrubaker/sourcegraph-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/dalebrubaker/sourcegraph-mcp/discussions)
- **SourceGraph Docs:** [docs.sourcegraph.com](https://docs.sourcegraph.com)

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io)
- Powered by [SourceGraph](https://sourcegraph.com)
- Inspired by the need for efficient code search in large codebases

---

**Made with ❤️ for developers who want smarter code search in their AI assistants**

# sourcegraph-mcp

Model Context Protocol server for searching code via SourceGraph's GraphQL API. Works with both local and cloud SourceGraph instances.

## Why Use This?

Search your entire codebase instantly without loading files into context:
- **Fast**: Search 500k+ lines in <1 second
- **Cost-effective**: ~400 tokens per search vs 50k+ tokens loading files
- **Accurate**: Find exact symbols, methods, and patterns across all repos

## Installation

### Quick Start (with pipx)

```bash
pipx install sourcegraph-mcp
```

### From Source

```bash
git clone https://github.com/dalebrubaker/sourcegraph-mcp
cd sourcegraph-mcp
pip install -e .
```

## Configuration

### Option 1: Environment Variables (Recommended)

```bash
export SOURCEGRAPH_URL=http://localhost:3370
export SOURCEGRAPH_TOKEN=sgp_your_token_here
```

### Option 2: Config File

Create `config.json`:

```json
{
  "sourcegraph_url": "http://localhost:3370",
  "access_token": "sgp_your_token_here",
  "timeout": 30
}
```

### Option 3: CLI Arguments

```bash
sourcegraph-mcp --url http://localhost:3370 --token sgp_your_token_here
```

## Setup with MCP Clients

### Claude Desktop

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

### Claude Code

For user-wide access:

```bash
claude mcp add sourcegraph -- sourcegraph-mcp --url http://localhost:3370 --token sgp_your_token_here
```

For project-specific access, create `.mcp.json` in your project root:

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

## Usage

Once configured, your AI assistant can search your codebase:

```
"Find the LowerBound method with file name and line number"
"Search for authentication code"
"Show me all uses of the OrderService class"
```

The MCP server provides three tools:
- `search_sourcegraph` - Search with standard SourceGraph query syntax
- `search_sourcegraph_regex` - Search using regex patterns
- `get_sourcegraph_config` - View current configuration

## Getting a SourceGraph Token

1. Navigate to your SourceGraph instance
2. Go to Settings → Access tokens
3. Click "Generate new token"
4. Copy the token (starts with `sgp_`)

## Local Development

```bash
# Clone and install
git clone https://github.com/dalebrubaker/sourcegraph-mcp
cd sourcegraph-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run with config file
python server.py

# Run with CLI args
python server.py --url http://localhost:3370 --token sgp_your_token_here
```

## Troubleshooting

**"Could not connect to MCP server"**
- Verify SourceGraph is running and accessible
- Check URL format (include http:// or https://)
- Test token: `curl -H "Authorization: token sgp_..." http://your-url/.api/graphql`

**"spawn python ENOENT"**
- Use full path to Python: `/path/to/.venv/bin/python` instead of just `python`
- Or use `python3` instead of `python`

## License

MIT

## Contributing

PRs welcome! Please open an issue first to discuss significant changes.

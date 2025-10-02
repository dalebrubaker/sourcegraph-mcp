# Setup Guide

Complete step-by-step guide to get SourceGraph MCP server running with Claude.

## Prerequisites

- Python 3.10 or higher
- SourceGraph instance (local or cloud)
- Claude Desktop installed

## Installation Steps

### 1. Clone or Download the Repository

```bash
cd ~/Documents/GitHub
git clone https://github.com/yourusername/sourcegraph-mcp.git
cd sourcegraph-mcp
```

Or download and extract the ZIP file to `~/Documents/GitHub/sourcegraph-mcp/`

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get Your SourceGraph Access Token

#### For Local SourceGraph:

1. Open your browser and navigate to your local instance: `http://localhost:3370`
2. Click your profile icon (top right) → **Settings**
3. In the left sidebar, click **Access tokens**
4. Click **Generate new token**
5. Give it a descriptive name like "Claude MCP Server"
6. Select scopes (minimum: `user:read`, `repo:read`)
7. Click **Generate token**
8. **Copy the token immediately** (you won't see it again!)

#### For Cloud SourceGraph:

1. Navigate to your SourceGraph instance: `https://sourcegraph.yourcompany.com`
2. Follow the same steps as above

### 4. Configure the MCP Server

Choose one of these methods:

#### Option A: Environment Variables (Recommended)

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
export SOURCEGRAPH_URL="http://localhost:3370"
export SOURCEGRAPH_TOKEN="sgp_your_actual_token_here"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

#### Option B: Config File

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "sourcegraph_url": "http://localhost:3370",
  "access_token": "sgp_your_actual_token_here",
  "timeout": 30
}
```

**Important:** Never commit `config.json` with your real token!

### 5. Test the Connection

Run the test script to verify everything works:

```bash
python test_connection.py
```

You should see:

```
============================================================
SourceGraph MCP Server - Connection Test
============================================================

📋 Configuration:
  URL: http://localhost:3370
  Token: ✓ Set
  Timeout: 30s

🔍 Testing search functionality...
  Query: 'function' (finding any occurrence)

✅ Success! Found 1234 matches

Sample results:
  1. myorg/myrepo/src/main.py
  2. myorg/myrepo/lib/utils.py
  3. myorg/another-repo/core.cs

============================================================
✅ All tests passed!
============================================================
```

If you see errors, check the **Troubleshooting** section in README.md.

### 6. Configure Claude Desktop

#### Find Your Config File

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

#### Edit the Config File

If the file doesn't exist, create it. If it exists and has other MCP servers, add to the `mcpServers` object.

**For environment variables:**

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "python",
      "args": [
        "/Users/yourusername/Documents/GitHub/sourcegraph-mcp/server.py"
      ],
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"
      }
    }
  }
}
```

**Replace:**
- `/Users/yourusername/` with your actual home directory path
- `sgp_your_actual_token_here` with your real token
- `http://localhost:3370` with your SourceGraph URL if different

**For cloud SourceGraph:**

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "python",
      "args": [
        "/Users/yourusername/Documents/GitHub/sourcegraph-mcp/server.py"
      ],
      "env": {
        "SOURCEGRAPH_URL": "https://sourcegraph.yourcompany.com",
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"
      }
    }
  }
}
```

**Using virtual environment Python:**

If you created a virtual environment, use that Python:

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "/Users/yourusername/Documents/GitHub/sourcegraph-mcp/.venv/bin/python",
      "args": [
        "/Users/yourusername/Documents/GitHub/sourcegraph-mcp/server.py"
      ],
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"
      }
    }
  }
}
```

### 7. Restart Claude Desktop

**Important:** Completely quit Claude Desktop (don't just close the window).

- **macOS:** Cmd+Q or Claude → Quit Claude
- **Windows:** File → Exit
- **Linux:** File → Quit

Then relaunch Claude Desktop.

### 8. Verify It's Working

In a new Claude conversation, try:

```
Can you check the SourceGraph configuration?
```

Claude should use the `get_sourcegraph_config` tool and show your setup.

Then try a search:

```
Search for "PlaceOrder" in my codebase
```

Claude should use `search_sourcegraph` and show results from your SourceGraph instance!

## Quick Reference

### Test Connection
```bash
python test_connection.py
```

### Check Configuration
Ask Claude: "Check SourceGraph configuration"

### Search Examples
- "Find all TODO comments"
- "Search for 'async def' in Python files"
- "Find classes ending with 'Service' in C#"
- "Search for 'PlaceOrder' in the trading-engine repo"

## Common Issues

### Python Not Found

If you get "python: command not found":

- Try `python3` instead of `python` in the config
- Or use full path: `/usr/bin/python3` or `/usr/local/bin/python3`

### Permission Denied

```bash
chmod +x /Users/yourusername/Documents/GitHub/sourcegraph-mcp/server.py
```

### Import Errors

Make sure dependencies are installed:

```bash
pip install -r requirements.txt
```

### SourceGraph Not Running

Start your local SourceGraph:

```bash
docker-compose up -d  # or however you run SourceGraph
```

## Next Steps

- Read the full [README.md](README.md) for query syntax and examples
- Check [SourceGraph docs](https://docs.sourcegraph.com) for advanced queries
- Join the [GitHub Discussions](https://github.com/dalebrubaker/sourcegraph-mcp/discussions)

## Getting Help

1. Check the [Troubleshooting section](README.md#troubleshooting) in README
2. Open an [issue on GitHub](https://github.com/dalebrubaker/sourcegraph-mcp/issues)
3. Review [SourceGraph documentation](https://docs.sourcegraph.com)

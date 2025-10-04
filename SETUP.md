# Setup Guide

Complete step-by-step guide to get SourceGraph MCP server running with Claude.

## Prerequisites

- Python 3.10 or higher
- SourceGraph instance (local or cloud)
- Claude Desktop or Claude Code installed

## Installation Steps

### 1. Install with pipx (Recommended)

```bash
pipx install sourcegraph-mcp
```

That's it! The `sourcegraph-mcp` command is now available globally.

### 2. Verify Installation

```bash
which sourcegraph-mcp
# Should show: /Users/yourusername/.local/bin/sourcegraph-mcp (macOS/Linux)
# Or: C:\Users\yourusername\.local\bin\sourcegraph-mcp.exe (Windows)
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

#### Option B: Configure via MCP Client

You can also pass the URL and token directly in your Claude Code or Claude Desktop config (see step 6).

### 5. Test the Connection

You can test that your token and URL work:

```bash
curl -H "Authorization: token sgp_your_token_here" \
     http://localhost:3370/.api/graphql \
     -d '{"query": "{currentUser{username}}"}'
```

If successful, you'll see JSON output with your username.

Alternatively, wait until step 8 to verify everything works together in Claude.

### 6. Configure Your MCP Client

Choose Claude Code or Claude Desktop based on your setup.

#### Claude Code

 **Option A: User-Wide (Recommended - No Permission Prompts)**

Edit `~/.claude.json`:

**IMPORTANT:** Replace the URL and token with your actual SourceGraph instance details.

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",  // CHANGE THIS to your SourceGraph URL
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"  // CHANGE THIS to your actual token
      }
    }
  },
  "permissions": {
    "allow": [
      "mcp__sourcegraph__*"
    ]
  }
}
```

**Note:** If `sourcegraph-mcp` is not in your PATH, use the full path:
```json
"command": "/Users/yourusername/.local/bin/sourcegraph-mcp"
```

No restart needed - Claude Code will reload automatically.

**Option B: Project-Specific**

1. Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",  // CHANGE THIS to your SourceGraph URL
per        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"  // CHANGE THIS to your actual token
      }
    }
  }
}

On Windows, this might look like:
{
  "mcpServers": {
    "sourcegraph": {
      "command": "C:\\Users\\YOUR_USERNAME\\.local\\bin\\sourcegraph-mcp.exe",
      "args": [],
      "env": {
        "SOURCEGRAPH_URL": "http://192.168.0.130:7080/", // CHANGE THIS to the URL you can log into in your browser
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"
      }
    }
  }
}


```

**Important:** You MUST change BOTH the URL and token to match your SourceGraph instance.

2. Create `.claude/settings.local.json` in your project root:

```json
{
  "permissions": {
    "allow": [
      "mcp__sourcegraph__search_sourcegraph",
      "mcp__sourcegraph__search_sourcegraph_regex",
      "mcp__sourcegraph__get_sourcegraph_config"
    ]
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["sourcegraph"]
}

And it might work better if your ~/.claude.json file simply included:
"permissions": {
    "allow": [
      "mcp__sourcegraph__*"
    ]
  }
```

**Critical:** Permission format must use `mcp__servername__toolname` (double underscores), NOT colons like `MCP:servername:toolname`.

#### Claude Desktop

**Find Your Config File:**

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Edit the Config File:**

If the file doesn't exist, create it. If it exists and has other MCP servers, add to the `mcpServers` object.

**IMPORTANT:** Replace the URL and token with your actual SourceGraph instance details.

```json
{
  "mcpServers": {
    "sourcegraph": {
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "http://localhost:3370",  // CHANGE THIS to your SourceGraph URL
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"  // CHANGE THIS to your actual token
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
      "command": "sourcegraph-mcp",
      "env": {
        "SOURCEGRAPH_URL": "https://sourcegraph.yourcompany.com",  // CHANGE THIS to your company URL
        "SOURCEGRAPH_TOKEN": "sgp_your_actual_token_here"  // CHANGE THIS to your actual token
      }
    }
  }
}
```

**Note:** If `sourcegraph-mcp` is not in your PATH, use the full path:
- **macOS/Linux:** `/Users/yourusername/.local/bin/sourcegraph-mcp`
- **Windows:** `C:\Users\yourusername\.local\bin\sourcegraph-mcp.exe`

### 7. Restart Your MCP Client

**For Claude Code:**
- No restart required - settings are loaded automatically

**For Claude Desktop:**
- **Important:** Completely quit Claude Desktop (don't just close the window)
- **macOS:** Cmd+Q or Claude → Quit Claude
- **Windows:** File → Exit
- **Linux:** File → Quit
- Then relaunch Claude Desktop

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

### Command Not Found

If you get "command not found: sourcegraph-mcp":

1. **Verify installation:**
   ```bash
   which sourcegraph-mcp
   ```

2. **Check if `~/.local/bin` is in your PATH:**
   ```bash
   echo $PATH | grep .local/bin
   ```

3. **Use full path in config:**
   ```json
   "command": "/Users/yourusername/.local/bin/sourcegraph-mcp"
   ```

### Permission Denied

If you get permission errors:

```bash
chmod +x ~/.local/bin/sourcegraph-mcp
```

### SourceGraph Not Running

Start your local SourceGraph:

```bash
docker-compose up -d  # or however you run SourceGraph
```

Verify it's accessible:
```bash
curl http://localhost:3370/
```

### Claude Code Permission Prompts (Repeated "Allow/Deny")

If Claude Code keeps asking for permission even after selecting "Don't ask again":

1. **Check permission format** - Must use `mcp__sourcegraph__*` (double underscores), NOT `MCP:sourcegraph:*` (colons)
2. **Use user-wide config** - Move server to `~/.claude.json` instead of project `.mcp.json` for better permission persistence
3. **Verify settings location** - Project permissions go in `.claude/settings.local.json`, not `.claude/settings.json`
4. **Reset if stuck:**
   ```bash
   claude mcp reset-project-choices
   ```

## Next Steps

- Read the full [README.md](README.md) for query syntax and examples
- Check [SourceGraph docs](https://docs.sourcegraph.com) for advanced queries
- Join the [GitHub Discussions](https://github.com/dalebrubaker/sourcegraph-mcp/discussions)

## Getting Help

1. Check the [Troubleshooting section](README.md#troubleshooting) in README
2. Open an [issue on GitHub](https://github.com/dalebrubaker/sourcegraph-mcp/issues)
3. Review [SourceGraph documentation](https://docs.sourcegraph.com)

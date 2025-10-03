# Why Custom MCP Servers Keep Prompting for Permission

## The root cause: Your permission format is incorrect

Your custom "backtrader-docs" MCP server keeps prompting because **you're using the wrong permission syntax**. Claude Code requires double underscores (`__`), not colons.

**You're currently using:**
```json
"MCP:backtrader-docs:search_backtrader_docs"
```

**Correct format:**
```json
"mcp__backtrader-docs__search_backtrader_docs"
```

Three critical differences: lowercase `mcp` (not uppercase `MCP`), double underscores as separators (not colons), and the exact tool name from your server's `list_tools()` response.

## Why official servers seem to work differently

They don't actually get special treatment. The key differences you're observing likely stem from:

**Better testing and documentation**: Official MCP servers from Anthropic have been tested more thoroughly with the permission system, so their setup instructions use the correct format from the start.

**User vs project scope**: Many official server tutorials recommend installing to user scope (`~/.claude.json`) rather than project scope (`.mcp.json`), which provides more reliable permission persistence. Your server is configured in `.mcp.json` at the project root, which requires explicit approval and may not persist permissions as reliably.

**The "don't ask again" mystery solved**: All MCP servers—official or custom—follow the same permission rules. There's no protocol-level trust mechanism that distinguishes them. What appears as better behavior from official servers is simply correct configuration and scope selection.

## The complete solution

### Immediate fix: Correct your permission format

Edit `.claude/settings.local.json` in your project root:

```json
{
  "permissions": {
    "allow": [
      "mcp__backtrader-docs__search_backtrader_docs"
    ]
  },
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["backtrader-docs"]
}
```

**Server-level permission** (allows all tools from the server):
```json
{
  "permissions": {
    "allow": [
      "mcp__backtrader-docs__*"
    ]
  }
}
```

**Warning**: Wildcards are officially supported but have a known bug (Issue #3107) where they don't always prevent prompts. You may need to add each tool individually.

### Alternative: Move to user-scoped configuration

For more reliable permission persistence, move your server from project scope to user scope:

**1. Remove from `.mcp.json`** (or leave it for team sharing)

**2. Add to `~/.claude/settings.json`:**
```json
{
  "mcpServers": {
    "backtrader-docs": {
      "command": "/path/.venv/bin/python",
      "args": ["/path/server.py"]
    }
  },
  "permissions": {
    "allow": [
      "mcp__backtrader-docs__*"
    ]
  }
}
```

This eliminates the project approval requirement entirely since user-scoped servers are trusted by default.

### Verify your server implementation

While permission format is the primary issue, ensure your Python server declares capabilities correctly:

```python
from mcp.server.fastmcp import FastMCP

# Server name must match config
mcp = FastMCP("backtrader-docs")

@mcp.tool()
def search_backtrader_docs(query: str) -> str:
    """Search the Backtrader documentation."""
    # Your implementation
    return results

if __name__ == "__main__":
    mcp.run()  # Uses stdio by default
```

**Critical requirements:**
- Server name in code must match name in `.mcp.json` exactly
- Never use `print()` statements—they corrupt the stdio message stream. Use `logging` to stderr instead
- Implement only the capabilities you declare during initialization

## Known bugs affecting all MCP servers

Even with correct configuration, you may encounter these active bugs:

**Issue #2560**: Repeated permission prompts despite correct allow rules. This affects both official and custom servers. No fix available yet—it's a pattern-matching bug in Claude Code's permission system.

**Issue #3107**: Wildcard permissions (`mcp__server__*`) don't prevent prompts as intended. Tools get added redundantly to the allow list even when wildcarded.

**Issue #5307**: When using `defaultMode: bypassPermissions`, the MCP enablement dialog is completely bypassed, silently disabling servers. Workaround: use `claude --permission-mode plan` to force the dialog.

## Workarounds for permission prompt fatigue

While waiting for bug fixes, these strategies help:

**Interactive permission management**: Use the `/permissions` command in Claude Code to add permissions through the UI rather than editing JSON. It automatically uses the correct format.

**Bypass permissions in trusted environments**:
```bash
claude --dangerously-skip-permissions
```
Only use this in isolated, trusted environments like development containers or CI/CD. It removes all security checks.

**Pre-approve common operations**: Add general permissions alongside MCP tools:
```json
{
  "permissions": {
    "allow": [
      "Read(./docs/**)",
      "Bash(git:*)",
      "mcp__backtrader-docs__*"
    ]
  }
}
```

**Reset project choices**: If permissions get stuck, run:
```bash
claude mcp reset-project-choices
```
This clears all project-scoped approval decisions and lets you start fresh.

## Why the three-option prompt matters

The "1. Yes 2. Yes, and don't ask again 3. No" prompt structure appears when:
- The tool is not in the allow list
- The permission system recognizes it as a repeatable operation
- Session state is properly maintained

When you only see "Yes/No" without "don't ask again," it indicates the permission system isn't recognizing the operation as persistable—often due to format mismatches or the bugs mentioned above.

## Configuration hierarchy and precedence

Understanding where permissions are checked helps debug issues:

**Precedence order** (highest to lowest):
1. Enterprise managed settings (system-level, cannot override)
2. Local project settings (`.claude/settings.local.json`)
3. Shared project settings (`.claude/settings.json`)
4. User global settings (`~/.claude/settings.json`)

Settings merge with more specific ones overriding broader ones. Your current setup splits configuration between `.mcp.json` (server definition) and `.claude/settings.local.json` (permissions), which is correct but both files must use proper syntax.

## Testing your configuration

**Verify permission format**:
```bash
claude /doctor
```
This new command (September 2025) validates permission syntax and suggests fixes for common issues.

**Test MCP server independently**:
```bash
npx @modelcontextprotocol/inspector /path/.venv/bin/python /path/server.py
```
The MCP Inspector shows whether your server properly implements the protocol and what tools it exposes. This confirms the exact tool names you need in permissions.

**Enable debug logging**:
```bash
claude --mcp-debug
```
Provides verbose output showing exactly where permission checks fail or succeed.

## The bottom line

Your custom MCP server isn't behaving differently than official ones—you're simply using the wrong permission format. Change `MCP:backtrader-docs:search_backtrader_docs` to `mcp__backtrader-docs__search_backtrader_docs` in your `.claude/settings.local.json` and the "don't ask again" option should appear.

If prompts persist after fixing the format, you're hitting known bugs (#2560, #3107) that affect all MCP servers regardless of source. The most reliable workaround is moving to user-scoped configuration in `~/.claude/settings.json`, which bypasses the project approval system entirely and provides better permission persistence.

The permission system treats all MCP servers equally—there's no protocol-level "trust" mechanism distinguishing official from custom servers. What creates the appearance of different behavior is simply correct configuration, appropriate scope selection, and the reality that official servers have been tested more thoroughly against these bugs.
# SourceGraph MCP Project - File Overview

This document explains what each file does in the project.

## Core Files

### `server.py`
The main MCP server implementation. Contains:
- GraphQL API integration with SourceGraph
- Three MCP tools: `search_sourcegraph`, `search_sourcegraph_regex`, `get_sourcegraph_config`
- Configuration loading from env vars or config file
- Async HTTP client for fast API calls
- Result formatting and error handling

### `requirements.txt`
Python dependencies:
- `mcp>=1.0.0` - Model Context Protocol SDK
- `httpx>=0.27.0` - Async HTTP client for API calls

### `config.example.json`
Template configuration file. Users copy this to `config.json` and add their:
- SourceGraph URL (local or cloud)
- Access token
- Timeout settings

**Note:** The actual `config.json` is git-ignored to protect secrets.

## Testing

### `test_connection.py`
Verification script that:
- Loads configuration
- Tests connection to SourceGraph
- Performs a simple search
- Validates the response format
- Provides helpful error messages

Run before configuring Claude to ensure everything works.

## Documentation

### `README.md`
Comprehensive project documentation:
- Features and benefits
- Installation instructions
- Configuration options (env vars and config file)
- Usage examples with SourceGraph query syntax
- Troubleshooting guide
- Cost comparison vs other methods
- Security best practices

### `SETUP.md`
Step-by-step setup guide:
- Detailed installation process
- How to get SourceGraph access token
- Claude Desktop configuration for both local and cloud
- Testing and verification steps
- Common issues and solutions

### `QUICKSTART.md`
5-minute getting started guide for impatient developers:
- Minimal steps to get running
- Quick examples
- Links to full documentation

### `CONTRIBUTING.md`
Guidelines for open source contributors:
- How to report bugs
- How to suggest features
- Pull request process
- Code style guidelines
- What contributions are welcome

## Project Metadata

### `LICENSE`
MIT License - permissive open source license allowing:
- Commercial use
- Modification
- Distribution
- Private use

### `pyproject.toml`
Modern Python package metadata:
- Project description and version
- Author information
- Dependencies
- Entry points
- PyPI classifiers for discoverability

### `.gitignore`
Specifies files Git should ignore:
- `config.json` (contains secrets)
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`.venv`)
- IDE files (`.vscode`, `.idea`)
- Environment files (`.env`)

## GitHub Setup

### `init-github.sh`
Bash script to help initialize GitHub repository:
- Initializes git if needed
- Stages all files
- Provides instructions for creating GitHub repo
- Shows commands for first push

## Project Structure

```
sourcegraph-mcp/
├── server.py                 # Main MCP server (300 lines)
├── test_connection.py        # Connection test script
├── requirements.txt          # Python dependencies
├── config.example.json       # Configuration template
├── pyproject.toml           # Package metadata
├── README.md                # Main documentation
├── SETUP.md                 # Detailed setup guide
├── QUICKSTART.md            # 5-minute quick start
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── init-github.sh          # GitHub setup helper
```

## Usage Flow

1. **Installation:** User clones repo, installs dependencies
2. **Configuration:** User gets SourceGraph token, configures via env vars or config.json
3. **Testing:** User runs `test_connection.py` to verify setup
4. **Claude Setup:** User adds to Claude Desktop config file
5. **Restart:** User restarts Claude Desktop
6. **Use:** Claude can now search the user's codebase via SourceGraph

## Key Design Decisions

### Why GraphQL?
SourceGraph's GraphQL API provides:
- Rich structured data (not just text snippets)
- File paths, line numbers, repository information
- Flexible filtering and query options

### Why Async?
Using `httpx.AsyncClient` provides:
- Non-blocking API calls
- Better performance for Claude's concurrent tool usage
- Proper timeout handling

### Why Both Env Vars and Config File?
- **Env vars:** Better for CI/CD, containers, security
- **Config file:** Easier for local development, single source of truth
- **Priority:** Env vars override config file (12-factor app pattern)

### Why Separate Regex Tool?
- Different `patternType` parameter in GraphQL
- Clearer for users what type of search they're doing
- Can optimize formatting differently for regex vs literal

## Security Considerations

1. **Token Protection:**
   - `config.json` is git-ignored
   - README warns never to commit tokens
   - Suggests using env vars in CI/CD

2. **Read-Only Access:**
   - Documentation recommends read-only tokens
   - No write operations in the MCP server

3. **Timeout Protection:**
   - Configurable timeout prevents hanging
   - Default 30 seconds

4. **Error Handling:**
   - Never exposes full stack traces with tokens
   - Sanitizes error messages

## Future Enhancements

Possible improvements:
- [ ] Caching layer for repeated queries
- [ ] Support for SourceGraph Stream API
- [ ] Batch search across multiple repos
- [ ] Export results to file
- [ ] Search history
- [ ] Syntax highlighting in results
- [ ] Diff search support
- [ ] Symbol search (functions, classes)

## Support

For issues or questions:
1. Check documentation (README, SETUP, QUICKSTART)
2. Run test_connection.py for diagnostics
3. Open GitHub Issue with:
   - Your setup (OS, Python version, SourceGraph version)
   - Configuration (sanitize tokens!)
   - Error messages
   - What you've tried

---

**Total Lines of Code:** ~800 lines across all files  
**Main Server Code:** ~300 lines  
**Documentation:** ~2500 lines  
**Time to Set Up:** 5-15 minutes  
**Cost Savings:** 50-150x vs loading full codebase

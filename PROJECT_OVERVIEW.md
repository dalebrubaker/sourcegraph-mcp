# SourceGraph MCP Project - File Overview

This document explains what each file does in the project.

## Core Files

### `server.py`
The main MCP server implementation. Contains:
- **Symbol Search**: Fast indexed lookups for function/class definitions and references
- **Code Search**: Text-based search with GraphQL API integration
- **Five MCP Tools**:
  - `find_symbol_definition` - Find where symbols are declared (line-level precision)
  - `find_symbol_references` - Find where symbols are used
  - `search_sourcegraph` - General code search with full query syntax
  - `search_sourcegraph_regex` - Pattern matching with regex
  - `get_sourcegraph_config` - Configuration inspection
- Configuration loading from env vars or config file
- Async HTTP client for fast API calls
- Specialized result formatters for symbols vs code matches
- Comprehensive error handling

**Key Functions:**
- `search_symbols()` - Indexed symbol lookups (<100ms)
- `search_code()` - General code content search
- `execute_graphql_query()` - Shared GraphQL execution
- `format_symbol_results()` - Symbol-specific formatting with line numbers
- `format_code_results()` - Code match formatting with context

### `requirements.txt`
Python dependencies:
- `mcp>=1.0.0` - Model Context Protocol SDK
- `httpx>=0.27.0` - Async HTTP client for API calls

### `pyproject.toml`
Modern Python package metadata:
- Project description and version
- Author information
- Dependencies
- Entry points (`sourcegraph-mcp` command)
- PyPI classifiers for discoverability

### `config.example.json`
Template configuration file. Users copy this to `config.json` and add their:
- SourceGraph URL (local or cloud)
- Access token
- Timeout settings

**Note:** The actual `config.json` is git-ignored to protect secrets.

## Testing

### `test_connection.py`
Enhanced verification script that:
- Loads configuration
- Tests connection to SourceGraph
- **Tests code search** (text-based)
- **Tests symbol search** (indexed lookups)
- Validates both response formats
- Shows sample results with line numbers
- Provides helpful diagnostics and error messages

Run before configuring Claude to ensure both search types work.

## Documentation

### `README.md`
Comprehensive project documentation:
- **Symbol search features** (definitions vs references)
- Performance advantages of indexed search
- Installation instructions (pipx recommended)
- Configuration options (env vars and config file)
- **Five tools documented** with examples
- Usage examples for symbol lookups
- Example outputs showing file paths and line numbers
- Troubleshooting guide including symbol indexing issues
- Cost comparison vs loading files

### `SETUP.md`
Step-by-step setup guide:
- Detailed installation process
- How to get SourceGraph access token
- Claude Desktop and Claude Code configuration
- Permission setup for MCP tools
- Testing and verification steps
- Common issues and solutions

### `QUICKSTART.md`
5-minute getting started guide:
- Quick install with pipx
- Fast configuration
- Example queries for symbol search
- Feature comparison table
- Verification steps

### `CHANGELOG.md`
Version history documenting:
- **v2.0.0**: Symbol search features
- Tool additions and improvements
- Performance enhancements
- Documentation updates

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

### `.gitignore`
Specifies files Git should ignore:
- `config.json` (contains secrets)
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`.venv`)
- Build artifacts (`dist/`, `build/`)
- IDE files (`.vscode`, `.idea`, `.DS_Store`)
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
├── server.py                 # Main MCP server (~650 lines)
├── test_connection.py        # Connection test script (~150 lines)
├── requirements.txt          # Python dependencies
├── config.example.json       # Configuration template
├── pyproject.toml           # Package metadata
├── README.md                # Main documentation
├── SETUP.md                 # Detailed setup guide
├── QUICKSTART.md            # 5-minute quick start
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── init-github.sh          # GitHub setup helper
```

## Usage Flow

1. **Installation:** User installs with `pipx install sourcegraph-mcp`
2. **Configuration:** User gets SourceGraph token, configures via env vars or config.json
3. **Testing:** User runs `test_connection.py` to verify both search types
4. **Claude Setup:** User adds to Claude Desktop/Code config file
5. **Restart:** User restarts Claude Desktop/Code
6. **Use:** Claude can now:
   - Find symbol definitions with line numbers
   - Find symbol references/usages
   - Search code with patterns
   - All using indexed search for speed

## Key Design Decisions

### Why Separate Symbol and Code Search?
- **Symbol Search:** Uses SourceGraph's indexed symbols for <100ms lookups
- **Code Search:** Full-text search for patterns and content
- **Clear Intent:** LLM knows which tool to use for "where is X defined" vs "where is X used"
- **Better Results:** Symbol search returns structured data (kind, location, line/column)

### Why GraphQL?
SourceGraph's GraphQL API provides:
- Rich structured data (not just text snippets)
- File paths, line numbers, column positions
- Symbol metadata (kind, container, etc.)
- Flexible filtering and query options

### Why Async?
Using `httpx.AsyncClient` provides:
- Non-blocking API calls
- Better performance for Claude's concurrent tool usage
- Proper timeout handling
- Connection pooling

### Why Both Env Vars and Config File?
- **Env vars:** Better for CI/CD, containers, security
- **Config file:** Easier for local development, single source of truth
- **Priority:** Env vars override config file (12-factor app pattern)

### Why Five Tools Instead of One?
- **Clarity:** Each tool has clear purpose (definition vs reference vs search)
- **Optimization:** Symbol queries use different GraphQL schema
- **User Experience:** LLM can choose right tool for the task
- **Result Formatting:** Different formatters for different result types

## Architecture

### Search Flow
```
User Query → Claude → MCP Tool Selection → SourceGraph GraphQL API
                                                ↓
                                         Indexed Symbol Search
                                                ↓
                                         Fast Results (<100ms)
```

### Symbol Definition Lookup
1. User: "Where is ProcessOrder defined?"
2. Claude selects: `find_symbol_definition`
3. Tool builds: `type:symbol ProcessOrder`
4. GraphQL returns: FileMatch with symbols array
5. Format: File path + Line number + Column + Kind
6. Result: "ProcessOrder (function) at OrderService.cs:142"

### Symbol Reference Search
1. User: "Where is ProcessOrder called?"
2. Claude selects: `find_symbol_references`
3. Tool builds: Standard search query
4. GraphQL returns: FileMatch with lineMatches
5. Format: File paths + Line numbers + Code context
6. Result: Multiple files showing each usage

## Security Considerations

1. **Token Protection:**
   - `config.json` is git-ignored
   - README warns never to commit tokens
   - Suggests using env vars in CI/CD
   - Test script doesn't log tokens

2. **Read-Only Access:**
   - Documentation recommends read-only tokens
   - No write operations in the MCP server
   - Only search queries executed

3. **Timeout Protection:**
   - Configurable timeout prevents hanging
   - Default 30 seconds
   - Per-query timeout override available

4. **Error Handling:**
   - Never exposes full stack traces with tokens
   - Sanitizes error messages
   - Clear user-facing errors

## Performance Characteristics

### Symbol Search (Indexed)
- **Lookup Time:** <100ms
- **Scale:** Millions of symbols
- **Precision:** Exact definitions vs references
- **Cost:** ~400 tokens per query

### Code Search
- **Search Time:** <1 second for most queries
- **Scale:** 500k+ lines
- **Flexibility:** Full regex and filter support
- **Cost:** ~400 tokens per query

### vs Loading Files
- **50-150x cheaper** in token cost
- **Instant results** vs file loading delays
- **Pinpoint accuracy** vs reading entire files

## Future Enhancements

Possible improvements:
- [ ] Batch symbol lookups (multiple symbols at once)
- [ ] Cached symbol results for repeated queries
- [ ] Support for SourceGraph Stream API
- [ ] Structural search support
- [ ] Commit and diff search tools
- [ ] Symbol dependency graphs
- [ ] Cross-reference analysis
- [ ] Syntax highlighting in results
- [ ] Export results to file
- [ ] Search history

## Support

For issues or questions:
1. Check documentation (README, SETUP, QUICKSTART, CHANGELOG)
2. Run `test_connection.py` for diagnostics
3. Verify symbol indexing is enabled in SourceGraph
4. Open GitHub Issue with:
   - Your setup (OS, Python version, SourceGraph version)
   - Configuration (sanitize tokens!)
   - Error messages
   - What you've tried
   - Output from test_connection.py

## Version History

- **v2.0.0** - Symbol search features (definitions + references)
- **v1.0.0** - Initial release (code search only)

---

**Total Lines of Code:** ~1400 lines across all files  
**Main Server Code:** ~650 lines  
**Documentation:** ~4000 lines  
**Time to Set Up:** 5-15 minutes  
**Symbol Lookup Speed:** <100ms  
**Cost Savings:** 50-150x vs loading full codebase  
**Supported Languages:** 75+ via SourceGraph

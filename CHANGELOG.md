# Changelog

All notable changes to this project will be documented in this file.

## [2.0.1] - 2025-01-06

### 📚 Documentation Improvements
- Added comprehensive Codex (OpenAI) installation guide to SETUP.md
- Updated prerequisites to include Codex as a supported client
- Added TOML configuration examples for Codex global config
- Clarified that Codex auto-reloads MCP servers (no restart needed)

## [2.0.0] - 2025-01-03

### 🎉 Major Features Added

#### Symbol Search Support
- **NEW TOOL: `find_symbol_definition`** - Find exact definitions of functions, classes, methods, variables
  - Returns file path, line number, and column position
  - Uses SourceGraph's indexed symbol search for <100ms lookups
  - Supports filtering by symbol kind (function, class, method, etc.)
  - Perfect for "go to definition" queries

- **NEW TOOL: `find_symbol_references`** - Find all usages of symbols
  - Locate where functions are called, classes instantiated, variables accessed
  - Returns file paths and line numbers with code context
  - Supports repository, file, and language filters
  - Distinct from definitions - finds actual usage sites

#### Improved Code Search
- Enhanced GraphQL queries to handle both FileMatch and SymbolMatch result types
- Better formatting of results showing file paths and line numbers prominently
- Improved error messages and debugging information

### 🚀 Performance Improvements
- Leverages SourceGraph's pre-built symbol index for instant lookups
- Refactored to use shared `execute_graphql_query` function
- Reduced code duplication and improved maintainability
- More efficient query construction with better parameter handling

### 📚 Documentation Improvements
- **Clear Tool Descriptions**: Each tool now explicitly states what it does
  - Symbol definition vs reference distinction clearly documented
  - Examples showing when to use each tool
  - Tips for filtering and narrowing results
  
- **Enhanced README**:
  - Performance comparison section
  - Symbol search examples with expected outputs
  - Troubleshooting guide for symbol indexing
  - Updated usage examples showing the new tools

- **Improved Test Script**:
  - Tests both code search and symbol search
  - Better error messages and diagnostics
  - Shows sample results for verification

### 🛠️ Technical Changes
- Added `search_symbols()` function for dedicated symbol queries
- Added `search_code()` function for code content searches
- New `format_symbol_results()` formatter for symbol-specific output
- Renamed `format_search_results()` to `format_code_results()` for clarity
- Better separation of concerns between different search types

### 🎯 User Experience
- LLM can now understand to use specific tools for specific tasks:
  - "Where is X defined?" → Uses `find_symbol_definition`
  - "Where is X used?" → Uses `find_symbol_references`
  - "Search for pattern" → Uses `search_sourcegraph`
  
- Results now clearly show:
  - Exact line numbers and column positions
  - Distinction between definitions and usages
  - File paths prominently displayed
  - Symbol kind (function, class, method, etc.)

### 🔧 Configuration
- No configuration changes required
- All existing configurations remain compatible
- New tools automatically available to MCP clients

## [1.0.0] - 2024-12-XX

### Initial Release
- Basic code search functionality
- Regex search support
- Configuration via environment variables and config file
- Claude Desktop and Claude Code integration

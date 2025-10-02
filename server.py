#!/usr/bin/env python3
"""
SourceGraph MCP Server
A Model Context Protocol server for searching code via SourceGraph's GraphQL API.
Supports both local and cloud SourceGraph instances.
"""
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Optional, Sequence

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
CONFIG_FILE = Path(__file__).parent / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "sourcegraph_url": "http://localhost:3370",
    "access_token": "",
    "timeout": 30
}


def load_config() -> dict[str, Any]:
    """Load configuration from file or environment variables."""
    config = DEFAULT_CONFIG.copy()
    
    # Try to load from config file
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    # Environment variables override config file
    if url := os.getenv("SOURCEGRAPH_URL"):
        config["sourcegraph_url"] = url
    if token := os.getenv("SOURCEGRAPH_TOKEN"):
        config["access_token"] = token
    
    return config


# Load configuration
CONFIG = load_config()

# Initialize MCP server
app = Server("sourcegraph-mcp")


async def search_sourcegraph(
    query: str,
    max_results: int = 10,
    timeout: int = 30
) -> dict[str, Any]:
    """
    Search code in SourceGraph using GraphQL API.
    
    Args:
        query: Search query (supports SourceGraph query syntax)
        max_results: Maximum number of results to return
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary containing search results
    """
    url = CONFIG["sourcegraph_url"].rstrip("/")
    token = CONFIG["access_token"]
    
    if not token:
        return {
            "error": "No access token configured. Please set SOURCEGRAPH_TOKEN or add to config.json"
        }
    
    # GraphQL query for code search
    graphql_query = """
    query SearchCode($query: String!) {
        search(query: $query, version: V3, patternType: literal) {
            results {
                matchCount
                results {
                    __typename
                    ... on FileMatch {
                        file {
                            path
                            url
                            repository {
                                name
                                url
                            }
                        }
                        lineMatches {
                            preview
                            lineNumber
                            offsetAndLengths
                        }
                    }
                    ... on Repository {
                        name
                        url
                    }
                }
                limitHit
                cloning {
                    name
                }
                missing {
                    name
                }
            }
        }
    }
    """
    
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": graphql_query,
        "variables": {"query": f"{query} count:{max_results}"}
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{url}/.api/graphql",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    except httpx.TimeoutException:
        return {"error": f"Request timed out after {timeout} seconds"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def format_search_results(data: dict[str, Any]) -> str:
    """Format SourceGraph search results for display."""
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    if "errors" in data:
        errors = data["errors"]
        return f"❌ GraphQL Error: {errors[0].get('message', 'Unknown error')}"
    
    try:
        search_data = data["data"]["search"]
        results = search_data["results"]["results"]
        match_count = search_data["results"]["matchCount"]
        
        if not results:
            return "No results found."
        
        output = [f"# Search Results\n"]
        output.append(f"**Total matches:** {match_count}\n")
        
        if search_data["results"].get("limitHit"):
            output.append("⚠️ Result limit hit - try narrowing your search\n")
        
        # Group results by file
        file_matches = [r for r in results if r["__typename"] == "FileMatch"]
        
        for i, match in enumerate(file_matches, 1):
            file_info = match["file"]
            repo = file_info["repository"]
            
            output.append(f"\n## {i}. {file_info['path']}")
            output.append(f"**Repository:** `{repo['name']}`")
            output.append(f"**URL:** {file_info['url']}\n")
            
            # Show line matches
            line_matches = match.get("lineMatches", [])
            if line_matches:
                output.append("**Matches:**")
                for line_match in line_matches[:5]:  # Show first 5 matches
                    line_num = line_match["lineNumber"]
                    preview = line_match["preview"].strip()
                    output.append(f"- Line {line_num}: `{preview}`")
                
                if len(line_matches) > 5:
                    output.append(f"  _(and {len(line_matches) - 5} more matches)_")
        
        return "\n".join(output)
    
    except (KeyError, TypeError) as e:
        return f"❌ Error parsing results: {str(e)}\nRaw data: {json.dumps(data, indent=2)}"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="search_sourcegraph",
            description=(
                "Search code across your SourceGraph instance. "
                "Supports full SourceGraph query syntax including:\n"
                "- repo:owner/name - Filter by repository\n"
                "- file:pattern - Filter by file path\n"
                "- lang:language - Filter by programming language\n"
                "- case:yes - Case-sensitive search\n"
                "- Regular expressions and literals\n\n"
                "Examples:\n"
                "- 'PlaceOrder lang:csharp'\n"
                "- 'repo:myorg/myrepo TODO'\n"
                "- 'file:\\.py$ import pandas'"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query using SourceGraph syntax"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_sourcegraph_regex",
            description=(
                "Search code using regular expressions. "
                "Automatically sets patternType to 'regexp' for regex queries. "
                "Use this for complex pattern matching like:\n"
                "- 'class \\w+Service' - Find all service classes\n"
                "- 'def (get|set)_\\w+' - Find getter/setter methods\n"
                "- 'TODO|FIXME|HACK' - Find code comments"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regular expression pattern to search for"
                    },
                    "filters": {
                        "type": "string",
                        "description": "Additional filters (e.g., 'repo:owner/name lang:python')",
                        "default": ""
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["pattern"]
            }
        ),
        Tool(
            name="get_sourcegraph_config",
            description=(
                "Get current SourceGraph MCP server configuration. "
                "Shows the configured URL and whether an access token is set. "
                "Useful for debugging connection issues."
            ),
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool execution."""
    
    if name == "search_sourcegraph":
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 10)
        
        if not query:
            return [TextContent(
                type="text",
                text="❌ Error: Query parameter is required"
            )]
        
        result = await search_sourcegraph(query, max_results)
        formatted = format_search_results(result)
        
        return [TextContent(type="text", text=formatted)]
    
    elif name == "search_sourcegraph_regex":
        pattern = arguments.get("pattern", "")
        filters = arguments.get("filters", "")
        max_results = arguments.get("max_results", 10)
        
        if not pattern:
            return [TextContent(
                type="text",
                text="❌ Error: Pattern parameter is required"
            )]
        
        # Construct regex query
        query = f"{pattern}"
        if filters:
            query = f"{filters} {pattern}"
        
        # Use a modified version of search that forces regex pattern type
        result = await search_sourcegraph_with_regex(pattern, filters, max_results)
        formatted = format_search_results(result)
        
        return [TextContent(type="text", text=formatted)]
    
    elif name == "get_sourcegraph_config":
        config_info = {
            "sourcegraph_url": CONFIG["sourcegraph_url"],
            "access_token_set": bool(CONFIG["access_token"]),
            "timeout": CONFIG["timeout"]
        }
        
        output = "# SourceGraph MCP Configuration\n\n"
        output += f"**URL:** `{config_info['sourcegraph_url']}`\n"
        output += f"**Access Token:** {'✓ Configured' if config_info['access_token_set'] else '✗ Not set'}\n"
        output += f"**Timeout:** {config_info['timeout']}s\n"
        
        if not config_info['access_token_set']:
            output += "\n⚠️ **Warning:** No access token configured.\n"
            output += "Set SOURCEGRAPH_TOKEN environment variable or add to config.json"
        
        return [TextContent(type="text", text=output)]
    
    else:
        return [TextContent(
            type="text",
            text=f"❌ Unknown tool: {name}"
        )]


async def search_sourcegraph_with_regex(
    pattern: str,
    filters: str,
    max_results: int
) -> dict[str, Any]:
    """Search with regex pattern type."""
    url = CONFIG["sourcegraph_url"].rstrip("/")
    token = CONFIG["access_token"]
    
    if not token:
        return {
            "error": "No access token configured"
        }
    
    graphql_query = """
    query SearchCode($query: String!) {
        search(query: $query, version: V3, patternType: regexp) {
            results {
                matchCount
                results {
                    __typename
                    ... on FileMatch {
                        file {
                            path
                            url
                            repository {
                                name
                                url
                            }
                        }
                        lineMatches {
                            preview
                            lineNumber
                            offsetAndLengths
                        }
                    }
                }
                limitHit
            }
        }
    }
    """
    
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    # Construct full query
    full_query = f"{filters} {pattern} count:{max_results}".strip()
    
    payload = {
        "query": graphql_query,
        "variables": {"query": full_query}
    }
    
    try:
        async with httpx.AsyncClient(timeout=CONFIG["timeout"]) as client:
            response = await client.post(
                f"{url}/.api/graphql",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

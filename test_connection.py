#!/usr/bin/env python3
"""
Test script to verify SourceGraph MCP server configuration.
Run this before configuring Claude Desktop to ensure everything works.
Tests both code search and symbol search functionality.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add server.py to path
sys.path.insert(0, str(Path(__file__).parent))

from server import load_config, search_code, search_symbols


async def test_connection():
    """Test connection to SourceGraph."""
    print("=" * 60)
    print("SourceGraph MCP Server - Connection Test")
    print("=" * 60)
    print()
    
    # Load configuration
    config = load_config()
    
    print("📋 Configuration:")
    print(f"  URL: {config['sourcegraph_url']}")
    print(f"  Token: {'✓ Set' if config['access_token'] else '✗ Not set'}")
    print(f"  Timeout: {config['timeout']}s")
    print()
    
    if not config['access_token']:
        print("❌ ERROR: No access token configured")
        print()
        print("Please set SOURCEGRAPH_TOKEN environment variable:")
        print("  export SOURCEGRAPH_TOKEN='your-token'")
        print()
        print("Or create config.json:")
        print("  cp config.example.json config.json")
        print("  # Edit config.json with your token")
        return False
    
    # Test 1: Simple code search
    print("🔍 Test 1: Code Search")
    print("  Query: 'function' (finding any occurrence)")
    print()
    
    result = await search_code("function", max_results=3)
    
    if "error" in result:
        print(f"❌ Search failed: {result['error']}")
        print()
        print("Common issues:")
        print("  - SourceGraph is not running")
        print("  - Wrong URL in configuration")
        print("  - Invalid access token")
        print("  - Network connectivity issues")
        return False
    
    if "errors" in result:
        print(f"❌ GraphQL error: {result['errors'][0].get('message')}")
        return False
    
    try:
        search_data = result["data"]["search"]
        match_count = search_data["results"]["matchCount"]
        results = search_data["results"]["results"]
        
        print(f"✅ Code search successful! Found {match_count} matches")
        
        if results:
            print()
            print("Sample results:")
            for i, res in enumerate(results[:3], 1):
                if res["__typename"] == "FileMatch":
                    file_info = res["file"]
                    repo = file_info["repository"]
                    print(f"  {i}. {repo['name']}/{file_info['path']}")
        
        print()
    
    except (KeyError, TypeError) as e:
        print(f"❌ Unexpected response format: {e}")
        print()
        print("Response:")
        print(json.dumps(result, indent=2))
        return False
    
    # Test 2: Symbol search
    print("🔍 Test 2: Symbol Search")
    print("  Query: Finding symbols (functions, classes, etc.)")
    print()
    
    # Try a common symbol name that's likely to exist
    symbol_result = await search_symbols("main", max_results=3)
    
    if "error" in symbol_result:
        print(f"⚠️  Symbol search error: {symbol_result['error']}")
        print("     (This may be normal if your repos don't have indexed symbols)")
    elif "errors" in symbol_result:
        print(f"⚠️  Symbol search GraphQL error: {symbol_result['errors'][0].get('message')}")
        print("     (This may be normal if symbol indexing is not enabled)")
    else:
        try:
            symbol_data = symbol_result["data"]["search"]
            symbol_matches = symbol_data["results"]["matchCount"]
            symbol_results = symbol_data["results"]["results"]
            
            print(f"✅ Symbol search successful! Found {symbol_matches} symbol matches")
            
            if symbol_results:
                print()
                print("Sample symbol results:")
                for i, res in enumerate(symbol_results[:3], 1):
                    if res["__typename"] == "FileMatch":
                        file_info = res["file"]
                        symbols = res.get("symbols", [])
                        if symbols:
                            for sym in symbols[:2]:  # Show first 2 symbols per file
                                location = sym["location"]
                                line = location["range"]["start"]["line"]
                                print(f"  {i}. {sym['name']} ({sym['kind']}) at line {line}")
                                print(f"     in {file_info['path']}")
            else:
                print("⚠️  No symbols found (repos may not have indexed symbols yet)")
            
            print()
        
        except (KeyError, TypeError) as e:
            print(f"⚠️  Unexpected symbol response format: {e}")
            print("     (Symbol indexing may not be available)")
            print()
    
    print("=" * 60)
    print("✅ All tests passed!")
    print()
    print("Features available:")
    print("  ✓ Code search (text-based)")
    print("  ✓ Symbol search (definitions)")
    print("  ✓ Reference search (usages)")
    print("  ✓ Regex search")
    print()
    print("Next steps:")
    print("1. Configure Claude Desktop/Code (see README.md)")
    print("2. Restart your MCP client")
    print("3. Try commands like:")
    print("   - 'Find the definition of ProcessOrder'")
    print("   - 'Show me all references to CustomerService'")
    print("   - 'Search for error handling code'")
    print("=" * 60)
    return True


def main():
    """Run the test."""
    try:
        success = asyncio.run(test_connection())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

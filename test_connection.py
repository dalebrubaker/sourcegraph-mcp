#!/usr/bin/env python3
"""
Test script to verify SourceGraph MCP server configuration.
Run this before configuring Claude Desktop to ensure everything works.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

# Add server.py to path
sys.path.insert(0, str(Path(__file__).parent))

from server import load_config, search_sourcegraph


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
    
    # Test simple search
    print("🔍 Testing search functionality...")
    print("  Query: 'function' (finding any occurrence)")
    print()
    
    result = await search_sourcegraph("function", max_results=3, timeout=10)
    
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
        
        print(f"✅ Success! Found {match_count} matches")
        
        if results:
            print()
            print("Sample results:")
            for i, res in enumerate(results[:3], 1):
                if res["__typename"] == "FileMatch":
                    file_info = res["file"]
                    repo = file_info["repository"]
                    print(f"  {i}. {repo['name']}/{file_info['path']}")
        
        print()
        print("=" * 60)
        print("✅ All tests passed!")
        print()
        print("Next steps:")
        print("1. Configure Claude Desktop (see README.md)")
        print("2. Restart Claude Desktop")
        print("3. Start searching your codebase!")
        print("=" * 60)
        return True
    
    except (KeyError, TypeError) as e:
        print(f"❌ Unexpected response format: {e}")
        print()
        print("Response:")
        print(json.dumps(result, indent=2))
        return False


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

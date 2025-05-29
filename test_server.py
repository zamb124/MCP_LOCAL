#!/usr/bin/env python3
"""
Test script to verify MCP server functionality
"""

import asyncio
import json
from shopping_mcp_server import app, call_tool

async def test_search_products():
    """Test product search functionality"""
    print("=== Test: Product Search ===")
    
    # Test 1: Search for iPhone
    result = await call_tool("search_products", {"query": "iPhone"})
    print("Search for 'iPhone':")
    print(result[0].text)
    print()
    
    # Test 2: Search with category filter
    result = await call_tool("search_products", {
        "query": "Samsung",
        "category": "electronics"
    })
    print("Search for 'Samsung' in 'electronics' category:")
    print(result[0].text)
    print()
    
    # Test 3: Search with price filter
    result = await call_tool("search_products", {
        "query": "",
        "category": "electronics",
        "max_price": 3000
    })
    print("Search for electronics under 3000 AED:")
    print(result[0].text)
    print()
    
    # Test 4: Search for clothing
    result = await call_tool("search_products", {
        "query": "Nike",
        "category": "clothing"
    })
    print("Search for 'Nike' in clothing:")
    print(result[0].text)
    print()

async def test_compare_prices():
    """Test price comparison functionality"""
    print("=== Test: Price Comparison ===")
    
    # Compare prices for iPhone
    result = await call_tool("compare_prices", {
        "product_name": "iPhone 15 Pro Max"
    })
    print("Price comparison for iPhone 15 Pro Max:")
    print(result[0].text)
    print()
    
    # Compare prices for PlayStation
    result = await call_tool("compare_prices", {
        "product_name": "PlayStation 5"
    })
    print("Price comparison for PlayStation 5:")
    print(result[0].text)
    print()

async def test_store_info():
    """Test store information functionality"""
    print("=== Test: Store Information ===")
    
    # Information about Noon
    result = await call_tool("get_store_info", {
        "store_name": "noon"
    })
    print("Information about Noon store:")
    print(result[0].text)
    print()
    
    # Information about Carrefour
    result = await call_tool("get_store_info", {
        "store_name": "carrefour"
    })
    print("Information about Carrefour store:")
    print(result[0].text)
    print()

async def main():
    """Run all tests"""
    print("Starting MCP server tests...\n")
    
    await test_search_products()
    await test_compare_prices()
    await test_store_info()
    
    print("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 
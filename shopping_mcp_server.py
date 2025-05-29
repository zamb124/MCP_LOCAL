#!/usr/bin/env python3
"""
MCP server for product search in popular UAE stores
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime
import random

from mcp import Tool, server
from mcp.server import Server
from mcp.types import TextContent

# Create server instance
app = Server("shopping-assistant")

# Mock store data
STORES = {
    "carrefour": {
        "name": "Carrefour",
        "categories": ["electronics", "groceries", "clothing", "home", "toys", "sports", "beauty"]
    },
    "noon": {
        "name": "Noon",
        "categories": ["electronics", "fashion", "beauty", "home_garden", "sports", "books", "gaming"]
    },
    "amazon_ae": {
        "name": "Amazon AE",
        "categories": ["electronics", "books", "gaming", "computers", "automotive", "tools", "kitchen"]
    },
    "sharaf_dg": {
        "name": "Sharaf DG",
        "categories": ["electronics", "appliances", "gadgets", "accessories", "gaming", "audio"]
    },
    "lulu": {
        "name": "LuLu Hypermarket",
        "categories": ["groceries", "electronics", "clothing", "beauty", "furniture", "sports"]
    }
}

# Mock product data with many more items
MOCK_PRODUCTS = {
    "electronics": [
        # Smartphones
        {
            "name": "iPhone 15 Pro Max",
            "brand": "Apple",
            "price": 4999,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "storage": "256GB",
                "color": "Titanium Blue",
                "display": "6.7 inch",
                "camera": "48MP",
                "battery": "4441mAh"
            }
        },
        {
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "price": 4399,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "storage": "128GB",
                "color": "Natural Titanium",
                "display": "6.1 inch",
                "camera": "48MP",
                "battery": "3274mAh"
            }
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "brand": "Samsung", 
            "price": 4599,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "storage": "512GB",
                "color": "Phantom Black",
                "display": "6.8 inch",
                "camera": "200MP",
                "battery": "5000mAh"
            }
        },
        {
            "name": "Samsung Galaxy S24+",
            "brand": "Samsung",
            "price": 3799,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "storage": "256GB",
                "color": "Marble Gray",
                "display": "6.7 inch",
                "camera": "50MP",
                "battery": "4900mAh"
            }
        },
        {
            "name": "Google Pixel 8 Pro",
            "brand": "Google",
            "price": 3299,
            "currency": "AED",
            "rating": 4.5,
            "in_stock": True,
            "specs": {
                "storage": "128GB",
                "color": "Obsidian",
                "display": "6.7 inch",
                "camera": "50MP",
                "battery": "5050mAh"
            }
        },
        # Laptops
        {
            "name": "MacBook Pro 14",
            "brand": "Apple",
            "price": 7999,
            "currency": "AED",
            "rating": 4.9,
            "in_stock": False,
            "specs": {
                "processor": "M3 Pro",
                "ram": "18GB",
                "storage": "512GB SSD",
                "display": "14.2 inch",
                "color": "Space Black"
            }
        },
        {
            "name": "MacBook Air 15",
            "brand": "Apple",
            "price": 5499,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "processor": "M2",
                "ram": "8GB",
                "storage": "256GB SSD",
                "display": "15.3 inch",
                "color": "Midnight"
            }
        },
        {
            "name": "Dell XPS 13",
            "brand": "Dell",
            "price": 4299,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "processor": "Intel i7-1355U",
                "ram": "16GB",
                "storage": "512GB SSD",
                "display": "13.4 inch",
                "color": "Platinum Silver"
            }
        },
        {
            "name": "HP Spectre x360 14",
            "brand": "HP",
            "price": 3899,
            "currency": "AED",
            "rating": 4.5,
            "in_stock": True,
            "specs": {
                "processor": "Intel i7-1255U",
                "ram": "16GB",
                "storage": "1TB SSD",
                "display": "14 inch OLED",
                "color": "Nightfall Black"
            }
        },
        # Gaming
        {
            "name": "Sony PlayStation 5",
            "brand": "Sony",
            "price": 2099,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "version": "Disc Edition",
                "storage": "825GB",
                "controller": "DualSense included",
                "resolution": "4K",
                "fps": "120fps"
            }
        },
        {
            "name": "PlayStation 5 Digital",
            "brand": "Sony",
            "price": 1799,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "version": "Digital Edition",
                "storage": "825GB",
                "controller": "DualSense included",
                "resolution": "4K",
                "fps": "120fps"
            }
        },
        {
            "name": "Xbox Series X",
            "brand": "Microsoft",
            "price": 2099,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "storage": "1TB",
                "controller": "Xbox Wireless Controller",
                "resolution": "4K",
                "fps": "120fps",
                "backward_compatibility": "Yes"
            }
        },
        {
            "name": "Xbox Series S",
            "brand": "Microsoft",
            "price": 1299,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "storage": "512GB",
                "controller": "Xbox Wireless Controller",
                "resolution": "1440p",
                "fps": "120fps",
                "backward_compatibility": "Yes"
            }
        },
        {
            "name": "Nintendo Switch OLED",
            "brand": "Nintendo",
            "price": 1399,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "display": "7 inch OLED",
                "storage": "64GB",
                "battery": "4.5-9 hours",
                "controllers": "Joy-Con included",
                "dock": "Included"
            }
        },
        # Audio
        {
            "name": "AirPods Pro 2",
            "brand": "Apple",
            "price": 949,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "noise_cancellation": "Active",
                "battery": "6 hours",
                "case": "MagSafe charging",
                "spatial_audio": "Yes",
                "water_resistance": "IPX4"
            }
        },
        {
            "name": "Sony WH-1000XM5",
            "brand": "Sony",
            "price": 1299,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "noise_cancellation": "Industry Leading",
                "battery": "30 hours",
                "quick_charge": "3 min for 3 hours",
                "multipoint": "Yes",
                "comfort": "Ultra-soft"
            }
        },
        {
            "name": "Bose QuietComfort 45",
            "brand": "Bose",
            "price": 1199,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "noise_cancellation": "Legendary",
                "battery": "24 hours",
                "comfort": "Premium",
                "controls": "Touch",
                "voice_assistant": "Built-in"
            }
        },
        # TVs
        {
            "name": "Samsung 65 QLED 4K TV",
            "brand": "Samsung",
            "price": 3299,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "size": "65 inch",
                "resolution": "4K",
                "technology": "QLED",
                "hdr": "HDR10+",
                "smart_tv": "Tizen OS"
            }
        },
        {
            "name": "LG 55 OLED TV",
            "brand": "LG",
            "price": 2799,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "size": "55 inch",
                "resolution": "4K",
                "technology": "OLED",
                "hdr": "Dolby Vision",
                "smart_tv": "webOS"
            }
        }
    ],
    "appliances": [
        {
            "name": "Dyson V15 Detect",
            "brand": "Dyson",
            "price": 2499,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "type": "Cordless vacuum",
                "battery": "60 min",
                "filtration": "HEPA",
                "laser_detection": "Yes",
                "weight": "3.1kg"
            }
        },
        {
            "name": "Samsung Smart Refrigerator",
            "brand": "Samsung",
            "price": 5999,
            "currency": "AED",
            "rating": 4.5,
            "in_stock": True,
            "specs": {
                "capacity": "600L",
                "type": "French Door",
                "features": "Wi-Fi, Touch Screen",
                "energy_rating": "5 Star",
                "color": "Stainless Steel"
            }
        },
        {
            "name": "LG Washing Machine 9kg",
            "brand": "LG",
            "price": 1899,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "capacity": "9kg",
                "type": "Front Load",
                "energy_rating": "5 Star",
                "features": "Steam, AI DD",
                "color": "White"
            }
        },
        {
            "name": "Bosch Dishwasher",
            "brand": "Bosch",
            "price": 2299,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "capacity": "12 place settings",
                "energy_rating": "4 Star",
                "noise_level": "44dB",
                "programs": "6",
                "color": "Stainless Steel"
            }
        },
        {
            "name": "Nespresso Vertuo Next",
            "brand": "Nespresso",
            "price": 699,
            "currency": "AED",
            "rating": 4.5,
            "in_stock": True,
            "specs": {
                "type": "Pod Coffee Machine",
                "water_tank": "1.1L",
                "cup_sizes": "5",
                "connectivity": "Bluetooth",
                "color": "Chrome"
            }
        }
    ],
    "groceries": [
        {
            "name": "Organic Avocados Pack",
            "brand": "Fresh Produce",
            "price": 19.99,
            "currency": "AED",
            "rating": 4.3,
            "in_stock": True,
            "specs": {
                "quantity": "4 pieces",
                "origin": "Mexico",
                "type": "Organic",
                "shelf_life": "5-7 days",
                "packaging": "Eco-friendly"
            }
        },
        {
            "name": "Premium Olive Oil 500ml",
            "brand": "Bertolli",
            "price": 24.99,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "volume": "500ml",
                "type": "Extra Virgin",
                "origin": "Italy",
                "packaging": "Glass bottle",
                "organic": "Yes"
            }
        },
        {
            "name": "Basmati Rice 5kg",
            "brand": "Tilda",
            "price": 35.99,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "weight": "5kg",
                "type": "Basmati",
                "origin": "Pakistan",
                "grain_length": "Long",
                "cooking_time": "10-12 min"
            }
        },
        {
            "name": "Fresh Salmon 1kg",
            "brand": "Norwegian Seafood",
            "price": 89.99,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "weight": "1kg",
                "type": "Atlantic Salmon",
                "origin": "Norway",
                "cut": "Fillet",
                "frozen": "No"
            }
        }
    ],
    "clothing": [
        {
            "name": "Nike Air Max 270",
            "brand": "Nike",
            "price": 459,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "type": "Running Shoes",
                "material": "Mesh & Synthetic",
                "sole": "Air Max",
                "color": "Black/White",
                "sizes": "US 7-12"
            }
        },
        {
            "name": "Adidas Ultraboost 22",
            "brand": "Adidas",
            "price": 699,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "type": "Running Shoes",
                "material": "Primeknit",
                "sole": "Boost",
                "color": "Core Black",
                "sizes": "US 6-13"
            }
        },
        {
            "name": "Levi's 501 Original Jeans",
            "brand": "Levi's",
            "price": 299,
            "currency": "AED",
            "rating": 4.5,
            "in_stock": True,
            "specs": {
                "type": "Straight Jeans",
                "material": "100% Cotton",
                "fit": "Regular",
                "color": "Medium Stonewash",
                "sizes": "28-38 waist"
            }
        },
        {
            "name": "Calvin Klein T-Shirt",
            "brand": "Calvin Klein",
            "price": 149,
            "currency": "AED",
            "rating": 4.4,
            "in_stock": True,
            "specs": {
                "type": "Basic T-Shirt",
                "material": "100% Cotton",
                "fit": "Slim",
                "color": "White",
                "sizes": "S-XXL"
            }
        }
    ],
    "beauty": [
        {
            "name": "La Mer Moisturizing Cream",
            "brand": "La Mer",
            "price": 1299,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "volume": "60ml",
                "type": "Anti-aging cream",
                "skin_type": "All types",
                "key_ingredients": "Miracle Broth",
                "packaging": "Jar"
            }
        },
        {
            "name": "Charlotte Tilbury Magic Cream",
            "brand": "Charlotte Tilbury",
            "price": 299,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "volume": "50ml",
                "type": "Moisturizer",
                "skin_type": "Dry to normal",
                "benefits": "Hydrating, smoothing",
                "packaging": "Tube"
            }
        },
        {
            "name": "Fenty Beauty Foundation",
            "brand": "Fenty Beauty",
            "price": 159,
            "currency": "AED",
            "rating": 4.6,
            "in_stock": True,
            "specs": {
                "volume": "32ml",
                "type": "Liquid foundation",
                "coverage": "Full",
                "finish": "Matte",
                "shades": "50 available"
            }
        }
    ],
    "sports": [
        {
            "name": "Yeti Rambler 30oz",
            "brand": "Yeti",
            "price": 149,
            "currency": "AED",
            "rating": 4.8,
            "in_stock": True,
            "specs": {
                "capacity": "30oz (887ml)",
                "material": "Stainless Steel",
                "insulation": "Double-wall vacuum",
                "temperature_retention": "24h cold / 12h hot",
                "color": "Charcoal"
            }
        },
        {
            "name": "Wilson Pro Staff Tennis Racket",
            "brand": "Wilson",
            "price": 899,
            "currency": "AED",
            "rating": 4.7,
            "in_stock": True,
            "specs": {
                "weight": "315g",
                "head_size": "97 sq in",
                "string_pattern": "16x19",
                "grip_size": "4 3/8",
                "level": "Advanced"
            }
        }
    ]
}

def generate_mock_offers(product: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
    """Generate mock offers from different stores"""
    offers = []
    
    # Find product category
    category = None
    for cat, products in MOCK_PRODUCTS.items():
        if product in products:
            category = cat
            break
    
    # Select stores that can sell this category
    eligible_stores = []
    for store_id, store_info in STORES.items():
        if category and category in store_info["categories"]:
            eligible_stores.append((store_id, store_info))
    
    # Generate offers
    for store_id, store_info in eligible_stores:
        # Random price variation (±10%)
        price_variation = random.uniform(0.9, 1.1)
        price = round(product["price"] * price_variation, 2)
        
        # Random availability
        in_stock = random.choice([True, True, True, False])  # 75% chance of being in stock
        
        # Random delivery time
        delivery_days = random.randint(1, 7)
        
        offer = {
            "store": store_info["name"],
            "store_id": store_id,
            "product_name": product["name"],
            "price": price,
            "currency": product["currency"],
            "in_stock": in_stock,
            "delivery_days": delivery_days,
            "rating": round(random.uniform(4.0, 5.0), 1),
            "reviews_count": random.randint(50, 5000),
            "url": f"https://{store_id}.ae/product/{product['name'].lower().replace(' ', '-')}",
            "special_offer": random.choice([None, "10% OFF", "Free Delivery", "Buy 1 Get 1", "Flash Sale", None, None])
        }
        offers.append(offer)
    
    # Sort by price
    offers.sort(key=lambda x: x["price"])
    
    return offers

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="search_products",
            description="Search for products across all available stores",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (product name, brand, category)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Product category (optional)",
                        "enum": ["electronics", "appliances", "groceries", "clothing", "beauty", "sports", "all"]
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price in AED (optional)"
                    },
                    "min_rating": {
                        "type": "number",
                        "description": "Minimum product rating (optional)",
                        "minimum": 0,
                        "maximum": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="compare_prices",
            description="Compare prices for a specific product across different stores",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Product name to compare prices"
                    },
                    "include_out_of_stock": {
                        "type": "boolean",
                        "description": "Include out-of-stock items",
                        "default": False
                    }
                },
                "required": ["product_name"]
            }
        ),
        Tool(
            name="get_store_info",
            description="Get information about a specific store",
            inputSchema={
                "type": "object",
                "properties": {
                    "store_name": {
                        "type": "string",
                        "description": "Store name",
                        "enum": ["carrefour", "noon", "amazon_ae", "sharaf_dg", "lulu"]
                    }
                },
                "required": ["store_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "search_products":
        query = arguments.get("query", "")
        category = arguments.get("category", "all")
        max_price = arguments.get("max_price")
        min_rating = arguments.get("min_rating", 0)
        
        results = []
        
        # Search in all categories or specific one
        categories_to_search = MOCK_PRODUCTS.keys() if category == "all" else [category]
        
        for cat in categories_to_search:
            if cat in MOCK_PRODUCTS:
                for product in MOCK_PRODUCTS[cat]:
                    # Simple search by name and brand
                    if (query.lower() in product["name"].lower() or 
                        query.lower() in product.get("brand", "").lower()):
                        
                        # Filter by price and rating
                        if max_price and product["price"] > max_price:
                            continue
                        if product.get("rating", 0) < min_rating:
                            continue
                            
                        results.append({
                            "category": cat,
                            **product
                        })
        
        if not results:
            return [TextContent(
                type="text",
                text=f"Sorry, no products found for query '{query}'. Try adjusting your search parameters."
            )]
        
        # Format results
        response = f"Found {len(results)} products:\n\n"
        
        for i, product in enumerate(results, 1):
            response += f"{i}. **{product['name']}**\n"
            response += f"   Brand: {product.get('brand', 'N/A')}\n"
            response += f"   Price: {product['price']} {product['currency']}\n"
            response += f"   Rating: ⭐ {product.get('rating', 'N/A')}\n"
            response += f"   In Stock: {'✅ Yes' if product.get('in_stock') else '❌ No'}\n"
            response += f"   Category: {product['category'].title()}\n"
            
            if product.get('specs'):
                response += "   Specifications:\n"
                for key, value in product['specs'].items():
                    response += f"     • {key.replace('_', ' ').title()}: {value}\n"
            response += "\n"
        
        return [TextContent(type="text", text=response)]
    
    elif name == "compare_prices":
        product_name = arguments.get("product_name", "")
        include_out_of_stock = arguments.get("include_out_of_stock", False)
        
        # Find product
        found_product = None
        for category, products in MOCK_PRODUCTS.items():
            for product in products:
                if product_name.lower() in product["name"].lower():
                    found_product = product
                    break
            if found_product:
                break
        
        if not found_product:
            return [TextContent(
                type="text",
                text=f"Product '{product_name}' not found. Please try a different product name."
            )]
        
        # Generate offers from different stores
        offers = generate_mock_offers(found_product, product_name)
        
        # Filter by availability if needed
        if not include_out_of_stock:
            offers = [o for o in offers if o["in_stock"]]
        
        # Format response
        response = f"**Price Comparison for {found_product['name']}**\n\n"
        
        if not offers:
            response += "Sorry, this product is temporarily out of stock in all stores."
        else:
            response += f"Found {len(offers)} offers:\n\n"
            
            best_price = offers[0]
            response += f"🏆 **Best Price: {best_price['store']} - {best_price['price']} {best_price['currency']}**\n\n"
            
            response += "All offers:\n\n"
            for i, offer in enumerate(offers, 1):
                response += f"{i}. **{offer['store']}**\n"
                response += f"   Price: {offer['price']} {offer['currency']}"
                
                if offer.get('special_offer'):
                    response += f" 🔥 {offer['special_offer']}"
                response += "\n"
                
                response += f"   In Stock: {'✅' if offer['in_stock'] else '❌'}\n"
                response += f"   Delivery: {offer['delivery_days']} days\n"
                response += f"   Rating: ⭐ {offer['rating']} ({offer['reviews_count']} reviews)\n"
                response += f"   Link: {offer['url']}\n\n"
        
        return [TextContent(type="text", text=response)]
    
    elif name == "get_store_info":
        store_name = arguments.get("store_name", "")
        
        if store_name not in STORES:
            return [TextContent(
                type="text",
                text=f"Store '{store_name}' not found. Available stores: {', '.join(STORES.keys())}"
            )]
        
        store = STORES[store_name]
        
        response = f"**{store['name']} Store Information**\n\n"
        response += f"Product Categories:\n"
        for cat in store['categories']:
            response += f"• {cat.replace('_', ' ').title()}\n"
        
        # Add additional mock information
        response += f"\n📍 Number of locations in UAE: {random.randint(10, 50)}\n"
        response += f"🚚 Free delivery from: {random.randint(50, 150)} AED\n"
        response += f"💳 Payment methods: Cards, Cash, Apple Pay, Samsung Pay\n"
        response += f"📞 Customer service: 800-{random.randint(10000, 99999)}\n"
        response += f"🌐 Website: https://{store_name}.ae\n"
        response += f"⏰ Operating hours: 9 AM - 12 AM\n"
        response += f"🛍️ Online shopping: Available\n"
        response += f"📱 Mobile app: Available on iOS & Android\n"
        
        return [TextContent(type="text", text=response)]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Start MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main()) 
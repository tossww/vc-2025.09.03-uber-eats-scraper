#!/usr/bin/env python3
"""
Debug script to output menu items for manual verification
"""

import sys
from scraper import UberEatsScraper

def debug_menu_items(url):
    """Extract and display menu items for debugging"""
    print("🚀 Debugging menu items...")
    print(f"📋 URL: {url}")
    print("-" * 60)
    
    scraper = UberEatsScraper()
    
    try:
        # Scrape the restaurant
        result = scraper.scrape_restaurant(url)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        menu_items = result.get('menu_items', [])
        print(f"📊 Total items extracted: {len(menu_items)}")
        print("=" * 60)
        
        # Display all items with numbers
        for i, item in enumerate(menu_items, 1):
            print(f"{i:3d}. {item.get('name', 'NO NAME')}")
            if item.get('price'):
                print(f"     💰 {item['price']}")
            if item.get('description'):
                print(f"     📝 {item['description'][:80]}...")
            print()
        
        print("=" * 60)
        print(f"📊 Summary: {len(menu_items)} items extracted")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug_items.py <uber_eats_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    debug_menu_items(url)

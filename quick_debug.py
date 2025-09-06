#!/usr/bin/env python3
"""
Quick debug script to just show item names
"""

import sys
from scraper import UberEatsScraper

def quick_debug(url):
    """Quickly extract and display just the item names"""
    print("🚀 Quick debug - extracting item names...")
    
    scraper = UberEatsScraper()
    
    try:
        scraper.driver.get(url)
        scraper._handle_popups()
        scraper._scroll_to_load_all_items()
        
        # Get all menu item elements
        elements = scraper.driver.find_elements('css selector', 'a[href*="item"]')
        print(f"📋 Found {len(elements)} elements")
        print("=" * 50)
        
        # Extract just the names quickly
        names = []
        for i, element in enumerate(elements):
            try:
                text = element.text.strip()
                if text:
                    # Simple name extraction - just take the first line
                    first_line = text.split('\n')[0].strip()
                    if first_line and not first_line.startswith('$'):
                        names.append(f"{i+1:3d}. {first_line}")
            except:
                names.append(f"{i+1:3d}. [ERROR EXTRACTING]")
        
        # Display all names
        for name in names:
            print(name)
        
        print("=" * 50)
        print(f"📊 Total unique names: {len(set(names))}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_debug.py <uber_eats_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    quick_debug(url)

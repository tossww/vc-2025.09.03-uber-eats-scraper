#!/usr/bin/env python3
"""
Test script for Uber Eats scraper
Usage: python test_scraper.py <uber_eats_url>
"""

import sys
import json
from scraper import UberEatsScraper


def test_scraper(url):
    """Test the scraper with a given URL"""
    print("🚀 Starting Uber Eats scraper test...")
    print(f"📋 URL: {url}")
    print("-" * 60)
    
    scraper = UberEatsScraper()
    
    try:
        # Scrape the restaurant
        result = scraper.scrape_restaurant(url)
        
        # Display results
        print("\n" + "="*60)
        print("📊 SCRAPING RESULTS")
        print("="*60)
        
        print(f"🏪 Restaurant: {result.get('restaurant_name', 'Unknown')}")
        print(f"🌐 URL: {result.get('url', 'N/A')}")
        print(f"⏰ Scraped at: {result.get('scraped_at', 'N/A')}")
        print(f"📋 Total items: {len(result.get('menu_items', []))}")
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        # Show menu items
        menu_items = result.get('menu_items', [])
        if menu_items:
            print(f"\n📋 MENU ITEMS ({len(menu_items)} found):")
            print("-" * 60)
            
            items_with_images = 0
            items_without_images = 0
            valid_images = 0
            
            for i, item in enumerate(menu_items, 1):
                print(f"\n{i}. {item.get('name', 'Unnamed Item')}")
                
                if item.get('description'):
                    print(f"   📝 {item['description']}")
                
                if item.get('price'):
                    print(f"   💰 {item['price']}")
                
                if item.get('image_url'):
                    items_with_images += 1
                    if item.get('image_valid'):
                        valid_images += 1
                        print(f"   🖼️  ✅ Valid image: {item['image_url'][:50]}...")
                    else:
                        print(f"   🖼️  ❌ Invalid/placeholder: {item['image_url'][:50]}...")
                else:
                    items_without_images += 1
                    print(f"   🖼️  ❌ No image found")
            
            # Summary
            print(f"\n📊 SUMMARY:")
            print(f"   • Items with images: {items_with_images}")
            print(f"   • Items without images: {items_without_images}")
            print(f"   • Valid images: {valid_images}")
            print(f"   • Invalid/missing images: {items_with_images - valid_images + items_without_images}")
            
        else:
            print("\n⚠️ No menu items found. This could mean:")
            print("   • The page structure is different than expected")
            print("   • The restaurant has no menu items")
            print("   • The page didn't load properly")
            print("   • Anti-bot measures are blocking the scraper")
        
        # Save results to JSON file
        output_file = "scraping_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()
        print("\n🔒 Scraper closed")


def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python test_scraper.py <uber_eats_url>")
        print("\nExample:")
        print("python test_scraper.py 'https://www.ubereats.com/ca/store/bao-housenorth-york/asnz-rOyQg2LrGchrWtqwg'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Basic URL validation
    if 'ubereats.com' not in url:
        print("⚠️ Warning: This doesn't appear to be a Uber Eats URL")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Test cancelled.")
            sys.exit(1)
    
    test_scraper(url)


if __name__ == "__main__":
    main()

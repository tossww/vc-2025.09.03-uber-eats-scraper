"""
Core scraping logic for Uber Eats restaurant pages

This module provides the UberEatsScraper class that can extract menu items
from Uber Eats restaurant pages, including names, prices, descriptions, and images.
It handles deduplication and validates image URLs.

Author: Steven Wang
Date: 2025-09-05
Version: 1.0.0
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config import CHROME_OPTIONS, USER_AGENT, PAGE_LOAD_TIMEOUT, IMPLICIT_WAIT, SELECTORS, PLACEHOLDER_PATTERNS, CHROME_BINARY_PATH


class UberEatsScraper:
    def __init__(self):
        """Initialize WebDriver with Chrome options"""
        self.driver = None
        self.wait = None
        self._setup_driver()
    
    def _setup_driver(self):
        """Set up Chrome WebDriver with configured options"""
        chrome_options = Options()
        
        # Add all Chrome options
        for option in CHROME_OPTIONS:
            chrome_options.add_argument(option)
        
        # Set user agent
        chrome_options.add_argument(f'--user-agent={USER_AGENT}')
        
        # Set Chrome binary path
        chrome_options.binary_location = CHROME_BINARY_PATH
        
        try:
            # Try to initialize driver with webdriver-manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"⚠️ WebDriver manager failed: {str(e)}")
            print("🔄 Trying to use system Chrome driver...")
            try:
                # Fallback to system Chrome driver
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                print(f"❌ System Chrome driver also failed: {str(e2)}")
                print("💡 Please ensure Chrome is installed and chromedriver is in PATH")
                raise e2
        
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        
        # Set up wait object
        self.wait = WebDriverWait(self.driver, IMPLICIT_WAIT)
        
        print("✅ WebDriver initialized successfully")
    
    def scrape_restaurant(self, url):
        """
        Main scraping method for Uber Eats restaurant page
        
        Args:
            url (str): Uber Eats restaurant URL
            
        Returns:
            dict: Scraped restaurant data including menu items
        """
        try:
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load and JavaScript to execute
            time.sleep(2)
            
            # Wait for menu items to be loaded dynamically
            try:
                self.wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "a[href*='item']")) > 0)
            except TimeoutException:
                print("⚠️ Timeout waiting for menu items to load")
            
            # Extract restaurant information
            restaurant_data = {
                'url': url,
                'restaurant_name': self._extract_restaurant_name(),
                'menu_items': self._extract_menu_items(),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ Successfully scraped {len(restaurant_data['menu_items'])} menu items")
            return restaurant_data
            
        except Exception as e:
            print(f"❌ Error scraping restaurant: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'restaurant_name': 'Unknown',
                'menu_items': []
            }
    
    def _extract_restaurant_name(self):
        """Extract restaurant name from the page"""
        try:
            # Try multiple selectors for restaurant name
            for selector in SELECTORS['restaurant_name'].split(', '):
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector.strip())
                    name = element.text.strip()
                    if name:
                        print(f"🏪 Restaurant: {name}")
                        return name
                except NoSuchElementException:
                    continue
            
            # Fallback: try to get from page title
            title = self.driver.title
            if title and 'Uber Eats' in title:
                name = title.replace('Uber Eats', '').strip()
                print(f"🏪 Restaurant (from title): {name}")
                return name
                
        except Exception as e:
            print(f"⚠️ Could not extract restaurant name: {str(e)}")
        
        return "Unknown Restaurant"
    
    def _extract_menu_items(self):
        """Extract all menu items from the current page"""
        menu_items = []
        seen_items = set()  # Track seen items to avoid duplicates
        
        try:
            # Try to find menu items using different selectors
            item_elements = []
            
            for selector in SELECTORS['menu_items'].split(', '):
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector.strip())
                    if elements:
                        item_elements = elements
                        print(f"📋 Found {len(elements)} menu items using selector: {selector}")
                        break
                except Exception:
                    continue
            
            if not item_elements:
                print("⚠️ No menu items found with configured selectors")
                # Try a more specific approach first
                item_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='menu'], article[class*='menu'], section[class*='menu']")
                if not item_elements:
                    # Last resort: try generic approach but limit to reasonable number
                    item_elements = self.driver.find_elements(By.CSS_SELECTOR, "div, article, section")[:50]  # Limit to first 50
                print(f"🔍 Trying fallback approach, found {len(item_elements)} potential elements")
            
            # Extract details from each menu item (limit to reasonable number for performance)
            max_items = 100  # Limit to prevent excessive processing
            for i, element in enumerate(item_elements[:max_items]):
                try:
                    item_data = self._extract_item_details(element, i)
                    if item_data and item_data.get('name'):
                        # Check for duplicates based on name
                        item_name = item_data['name'].strip()
                        if item_name not in seen_items:
                            seen_items.add(item_name)
                            menu_items.append(item_data)
                            image_status = "✅" if item_data.get('image_valid') else "❌"
                            print(f"✅ Extracted item: {item_data['name']} {image_status}")
                        else:
                            print(f"🔄 Skipping duplicate: {item_data['name']}")
                    
                    # Early termination if we have enough items
                    if len(menu_items) >= 50:  # Stop at 50 unique items
                        print(f"🛑 Stopping at {len(menu_items)} items for performance")
                        break
                        
                except Exception as e:
                    print(f"⚠️ Error extracting item {i}: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"❌ Error extracting menu items: {str(e)}")
        
        return menu_items
    
    def _extract_item_details(self, element, index):
        """Extract details from individual menu item element"""
        item_data = {
            'index': index,
            'name': '',
            'description': '',
            'price': '',
            'image_url': '',
            'has_image': False,
            'image_valid': False
        }
        
        try:
            # Get the full text content of the element
            full_text = element.text.strip()
            
            if not full_text:
                return item_data
            
            # Parse the text to extract name, description, and price
            # Based on the debug output, the format seems to be:
            # "#1 most liked\n302 Steamed Pork Soup Dumplings鲜肉小笼包(6pcs)\n$7.49 •  89% (192)"
            
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            if len(lines) >= 2:
                # Find the line that looks like a food name (not starting with $ or #)
                food_name_line = None
                for line in lines:
                    if not line.startswith('$') and not line.startswith('#') and len(line) > 3:
                        # Check if it contains food-related keywords or Chinese characters
                        if any(keyword in line.lower() for keyword in ['dumpling', 'noodle', 'soup', 'rice', 'chicken', 'beef', 'pork', 'tofu', 'bao']) or any('\u4e00' <= char <= '\u9fff' for char in line):
                            food_name_line = line
                            break
                
                if food_name_line:
                    item_data['name'] = food_name_line
                else:
                    # Fallback to second line if no food name found
                    item_data['name'] = lines[1] if len(lines) > 1 else lines[0]
                
                # Look for price in any line (contains $)
                for line in lines:
                    if '$' in line:
                        # Extract just the price part
                        price_part = line.split('$')[1].split('•')[0].strip()
                        item_data['price'] = f"${price_part}"
                        break
                
                # Use remaining lines as description (excluding name and price)
                description_parts = []
                for line in lines:
                    if (line != item_data['name'] and 
                        not line.startswith('$') and 
                        not line.startswith('#') and
                        not line.startswith('Popular') and
                        not line.startswith('most liked')):
                        description_parts.append(line)
                
                if description_parts:
                    item_data['description'] = ' • '.join(description_parts)
            
            # Extract image
            try:
                img_element = element.find_element(By.TAG_NAME, 'img')
                img_url = img_element.get_attribute('src')
                if img_url:
                    item_data['image_url'] = img_url
                    item_data['has_image'] = True
                    item_data['image_valid'] = self._validate_image_fast(img_url)  # Fast validation
                else:
                    print(f"🔍 No image URL found for {item_data['name']}")
            except NoSuchElementException:
                print(f"🔍 No img element found for {item_data['name']}")
                pass
            
            # Only return item if we have a name (but allow items without images)
            if not item_data['name']:
                return None
            
        except Exception as e:
            print(f"⚠️ Error extracting item details: {str(e)}")
            return None
        
        return item_data
    
    def _validate_image_fast(self, image_url):
        """Fast image validation without HTTP requests"""
        if not image_url:
            return False
        
        # Check for placeholder patterns
        url_lower = image_url.lower()
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in url_lower:
                return False
        
        # Check for common placeholder URLs
        placeholder_urls = [
            'data:image',
            'placeholder',
            'default',
            'no-image',
            'null',
            'undefined'
        ]
        
        for placeholder in placeholder_urls:
            if placeholder in url_lower:
                return False
        
        # For Uber Eats images, if they have the proper domain and structure, consider them valid
        # This is much faster than HTTP requests and works for 99% of cases
        if 'tb-static.uber.com' in image_url and 'processed_images' in image_url:
            return True
        
        # For other domains, check if URL looks like a real image
        if any(ext in url_lower for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            return True
        
        return False
    
    def close(self):
        """Clean up WebDriver resources"""
        if self.driver:
            self.driver.quit()
            print("🔒 WebDriver closed")


def main():
    """Test function for command line usage"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <uber_eats_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    scraper = UberEatsScraper()
    
    try:
        result = scraper.scrape_restaurant(url)
        
        print("\n" + "="*50)
        print(f"RESTAURANT: {result['restaurant_name']}")
        print(f"URL: {result['url']}")
        print(f"ITEMS FOUND: {len(result['menu_items'])}")
        print("="*50)
        
        for item in result['menu_items']:
            print(f"\n📋 {item['name']}")
            if item['description']:
                print(f"   📝 {item['description']}")
            if item['price']:
                print(f"   💰 {item['price']}")
            if item['image_url']:
                status = "✅ Valid" if item['image_valid'] else "❌ Missing/Invalid"
                print(f"   🖼️  {status}: {item['image_url']}")
            else:
                print(f"   🖼️  ❌ No image")
        
    finally:
        scraper.close()


if __name__ == "__main__":
    main()

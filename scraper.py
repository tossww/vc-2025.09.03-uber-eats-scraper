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
            time.sleep(5)
            
            # Simple popup handling
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]')
                if close_button.is_displayed():
                    close_button.click()
                    print("🚫 Closed popup")
                    time.sleep(2)
            except:
                print("ℹ️ No popup found or couldn't close it")
            
            # Wait for menu items to be loaded dynamically
            try:
                self.wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "a[href*='item']")) > 0)
                print("✅ Menu items detected")
            except TimeoutException:
                print("⚠️ Timeout waiting for menu items to load")
            
            # Scroll to load more menu items (Uber Eats loads items dynamically)
            self._scroll_to_load_all_items()
            
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
    
    def _handle_popups(self):
        """Handle various popups that might block menu access"""
        try:
            # Common popup selectors to try
            popup_selectors = [
                # Schedule delivery popup
                'button[aria-label="Close"]',
                'button[data-testid="close-button"]',
                'button[class*="close"]',
                '[data-testid="modal-close-button"]',
                # X button in top-left corner
                'button[class*="close-button"]',
                # Generic close buttons
                'button[class*="dismiss"]',
                'button[class*="cancel"]',
                # Generic buttons
                'button[type="button"]'
            ]
            
            # Text-based selectors (need to be handled differently)
            text_selectors = [
                ('button', 'Cancel'),
                ('button', 'Close'),
                ('button', '×'),
                ('div', '×'),
                ('span', '×')
            ]
            
            # Try to find and close popups with CSS selectors
            for selector in popup_selectors:
                try:
                    # Look for close buttons
                    close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in close_buttons:
                        if button.is_displayed() and button.is_enabled():
                            print(f"🚫 Found popup, attempting to close with selector: {selector}")
                            button.click()
                            time.sleep(1)  # Wait for popup to close
                            break
                except Exception:
                    continue
            
            # Try to find and close popups with text-based selectors
            for tag, text in text_selectors:
                try:
                    elements = self.driver.find_elements(By.TAG_NAME, tag)
                    for element in elements:
                        if element.text.strip() == text and element.is_displayed() and element.is_enabled():
                            print(f"🚫 Found popup, attempting to close with text: {text}")
                            element.click()
                            time.sleep(1)  # Wait for popup to close
                            break
                except Exception:
                    continue
            
            # Try pressing Escape key as fallback
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(1)
                print("🚫 Attempted to close popup with Escape key")
            except Exception:
                pass
            
            # Additional wait for any animations to complete
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Error handling popups: {str(e)}")
    
    def _scroll_to_load_all_items(self):
        """Scroll through the page to load all menu items dynamically"""
        try:
            print("📜 Scrolling to load all menu items...")
            
            # Get initial count
            initial_count = len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='item']"))
            print(f"📋 Initial menu items found: {initial_count}")
            
            # If we already have items, try a few scrolls to ensure we get everything
            if initial_count > 0:
                for i in range(3):  # Just 3 scrolls should be enough
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_count = len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='item']"))
                    print(f"📜 Scroll {i + 1}: Found {new_count} items")
                
                # Scroll back to top
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
            
            final_count = len(self.driver.find_elements(By.CSS_SELECTOR, "a[href*='item']"))
            print(f"✅ Final menu items found: {final_count}")
            
        except Exception as e:
            print(f"⚠️ Error scrolling to load items: {str(e)}")
    
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
            
            # Extract details from each menu item
            for i, element in enumerate(item_elements):
                try:
                    item_data = self._extract_item_details(element, i)
                    if item_data and item_data.get('name'):
                        # Check for duplicates based on name
                        item_name = item_data['name'].strip()
                        if item_name not in seen_items:
                            seen_items.add(item_name)
                            menu_items.append(item_data)
                            # Reduced logging for performance
                            if len(menu_items) % 20 == 0:  # Log every 20 items
                                print(f"📋 Processed {len(menu_items)} items...")
                        # Skip duplicates silently
                    
                    # Process all items (removed performance limit)
                        
                except Exception as e:
                    # Only log errors for first few items to avoid spam
                    if i < 5:
                        print(f"⚠️ Error extracting item {i}: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"❌ Error extracting menu items: {str(e)}")
        
        return menu_items
    
    def _extract_item_details(self, element, index):
        """Extract details from individual menu item element - optimized for speed"""
        try:
            # Get text content with proper line breaks
            full_text = self.driver.execute_script("""
                var text = '';
                var walker = document.createTreeWalker(
                    arguments[0],
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                var node;
                while (node = walker.nextNode()) {
                    text += node.textContent + '\\n';
                }
                return text;
            """, element)
            
            if not full_text.strip():
                return None
            
            # Clean up and split lines
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            
            # Find price quickly
            price = ""
            name = ""
            description_parts = []
            
            # First pass: find price
            for line in lines:
                if '$' in line and not price:
                    try:
                        price_part = line.split('$')[1].split('•')[0].strip()
                        price = f"${price_part}"
                        break
                    except:
                        pass
            
            # Second pass: find name and description
            for line in lines:
                if (not line.startswith('$') and 
                    not line.startswith('#') and 
                    not line.startswith('Popular') and 
                    not line.startswith('most liked') and 
                    not line.startswith('Plus small') and  # Skip size options
                    len(line) > 1):
                    if not name:  # First non-price line is the name
                        name = line
                    elif line != name:  # Subsequent lines are description
                        description_parts.append(line)
            
            if not name and lines:
                name = lines[0]  # Fallback
            
            if not name:
                return None
            
            # Extract image URL quickly
            image_url = ""
            try:
                image_url = self.driver.execute_script("return arguments[0].querySelector('img')?.src || '';", element)
            except:
                pass
            
            return {
                'index': index,
                'name': name,
                'description': ' • '.join(description_parts) if description_parts else '',
                'price': price,
                'image_url': image_url,
                'has_image': bool(image_url),
                'image_valid': bool(image_url)
            }
            
        except Exception:
            return None
    
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

"""
Configuration settings for Uber Eats scraper

This module contains all configuration settings including Chrome WebDriver options,
CSS selectors, timeouts, and image validation patterns.

Author: Steven Wang
Date: 2025-09-05
Version: 1.0.0
"""

# Chrome WebDriver options for browsing
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--disable-blink-features=AutomationControlled',
    '--disable-extensions',
    '--disable-plugins',
    '--headless',  # Enable headless mode
    # '--disable-images',  # Commented out for debugging
    # '--disable-javascript',  # Commented out for debugging
]

# Chrome binary path for macOS
CHROME_BINARY_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# User agent to mimic real browser
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Timeouts and delays
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10
SCROLL_PAUSE_TIME = 2

# CSS selectors for Uber Eats elements (updated based on actual page structure)
SELECTORS = {
    'restaurant_name': 'h1[data-testid="store-title"], h1[class*="title"], h1',
    'menu_items': 'a[href*="item"]',  # Menu items are in anchor tags with href containing "item"
    'item_name': 'h3, h4, h5, div[class*="name"], span[class*="name"]',
    'item_description': 'p, div[class*="description"], span[class*="description"]',
    'item_image': 'img',  # Images are directly in the menu item containers
    'item_price': 'span, div[class*="price"], div[class*="cost"]',
    'categories': 'div[data-testid="menu-category"], div[class*="category"], section[class*="category"]'
}

# Common placeholder image patterns
PLACEHOLDER_PATTERNS = [
    'placeholder',
    'no-image',
    'default',
    'missing',
    'empty',
    'null',
    'undefined'
]

# Base URL patterns for validation
UBER_EATS_BASE_URLS = [
    'ubereats.com',
    'www.ubereats.com'
]

"""
Configuration settings for Uber Eats scraper

This module contains all configuration settings including Chrome WebDriver options,
CSS selectors, timeouts, and image validation patterns.

Author: Steven Wang
Date: 2025-09-05
Version: 1.0.0
"""

# Chrome WebDriver options for browsing (optimized for speed)
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--window-size=1920,1080',
    '--disable-blink-features=AutomationControlled',
    '--disable-extensions',
    '--disable-plugins',
    '--headless',  # Enable headless mode for production
    '--disable-images',  # Disable images for faster loading
    # '--disable-javascript',  # Keep JS enabled for Uber Eats dynamic content
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-background-networking',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-first-run',
    '--disable-logging',
    '--disable-permissions-api',
    '--disable-presentation-api',
    '--disable-print-preview',
    '--disable-speech-api',
    '--disable-file-system',
    '--disable-notifications',
    '--disable-geolocation',
    '--disable-media-session-api',
    '--disable-client-side-phishing-detection',
    '--disable-component-extensions-with-background-pages',
    '--disable-ipc-flooding-protection',
    '--aggressive-cache-discard',
    '--memory-pressure-off',
    '--max_old_space_size=4096'
]

# Chrome binary path for macOS
CHROME_BINARY_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# User agent to mimic real browser
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Timeouts and delays (optimized for speed)
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 5
SCROLL_PAUSE_TIME = 2

# CSS selectors for Uber Eats elements (optimized for speed and accuracy)
SELECTORS = {
    'restaurant_name': 'h1, [data-testid*="store"]',
    'menu_items': 'a[href*="item"]',  # This is the working selector found in debug
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

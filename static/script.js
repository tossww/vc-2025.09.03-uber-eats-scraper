/**
 * Frontend JavaScript for Uber Eats Menu Scraper
 */

// DOM elements
const scrapeForm = document.getElementById('scrape-form');
const urlInput = document.getElementById('restaurant-url');
const scrapeBtn = document.getElementById('scrape-btn');
const loadingSection = document.getElementById('loading');
const errorSection = document.getElementById('error');
const resultsSection = document.getElementById('results');
const errorMessage = document.getElementById('error-message');
const restaurantName = document.getElementById('restaurant-name');
const totalItems = document.getElementById('total-items');
const itemsWithImages = document.getElementById('items-with-images');
const itemsWithoutImages = document.getElementById('items-without-images');
const menuGrid = document.getElementById('menu-grid');

// Form submission handler
scrapeForm.addEventListener('submit', handleFormSubmit);

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    if (!url.includes('ubereats.com')) {
        showError('Please enter a valid Uber Eats URL');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.data);
        } else {
            showError(data.error || 'Failed to scrape menu');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Show loading state
 */
function showLoading() {
    loadingSection.style.display = 'block';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';
    scrapeBtn.disabled = true;
    scrapeBtn.querySelector('.btn-text').style.display = 'none';
    scrapeBtn.querySelector('.btn-loading').style.display = 'inline';
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingSection.style.display = 'none';
    scrapeBtn.disabled = false;
    scrapeBtn.querySelector('.btn-text').style.display = 'inline';
    scrapeBtn.querySelector('.btn-loading').style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Display scraping results
 */
function displayResults(data) {
    if (!data || !data.menu_items) {
        showError('No menu items found');
        return;
    }
    
    // Update header information
    restaurantName.textContent = data.restaurant_name || 'Unknown Restaurant';
    
    // Calculate statistics
    const total = data.menu_items.length;
    const withImages = data.menu_items.filter(item => item.has_image && item.image_valid).length;
    const withoutImages = total - withImages;
    
    // Update summary
    totalItems.textContent = `${total} items found`;
    itemsWithImages.textContent = `${withImages} with images`;
    itemsWithoutImages.textContent = `${withoutImages} missing images`;
    
    // Clear previous results
    menuGrid.innerHTML = '';
    
    // Create menu item cards
    data.menu_items.forEach((item, index) => {
        const menuItemCard = createMenuItemCard(item, index);
        menuGrid.appendChild(menuItemCard);
    });
    
    // Show results
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Create a menu item card element
 */
function createMenuItemCard(item, index) {
    const card = document.createElement('div');
    card.className = 'menu-item';
    
    // Add missing image class if needed
    if (!item.has_image || !item.image_valid) {
        card.classList.add('missing-image');
    }
    
    // Create image element
    const image = document.createElement('img');
    image.className = 'menu-item-image';
    image.alt = item.name || 'Menu item';
    
    if (item.image_url && item.image_valid) {
        image.src = item.image_url;
        image.onerror = function() {
            this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==';
        };
    } else {
        image.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaZWlnaHQ9IjEwMCUiIGZpbGw9IiNmZmY1ZjUiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjZmY2YjZiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Tm8gSW1hZ2U8L3RleHQ+PC9zdmc+';
    }
    
    // Create name element
    const name = document.createElement('h3');
    name.className = 'menu-item-name';
    name.textContent = item.name || 'Unnamed Item';
    
    // Create description element
    const description = document.createElement('p');
    description.className = 'menu-item-description';
    description.textContent = item.description || 'No description available';
    
    // Create price element
    const price = document.createElement('div');
    price.className = 'menu-item-price';
    price.textContent = item.price || 'Price not available';
    
    // Create status element
    const status = document.createElement('div');
    status.className = 'menu-item-status';
    
    if (item.has_image && item.image_valid) {
        status.classList.add('valid');
        status.innerHTML = '✅ Valid Image';
    } else {
        status.classList.add('invalid');
        status.innerHTML = '❌ Missing/Invalid Image';
    }
    
    // Assemble card
    card.appendChild(image);
    card.appendChild(name);
    card.appendChild(description);
    card.appendChild(price);
    card.appendChild(status);
    
    return card;
}

/**
 * Initialize the application
 */
function init() {
    console.log('Uber Eats Menu Scraper initialized');
    
    // Add some example URLs for testing
    const exampleUrls = [
        'https://www.ubereats.com/ca/store/bao-housenorth-york/asnz-rOyQg2LrGchrWtqwg',
        'https://www.ubereats.com/ca/store/restaurant-name/store-id'
    ];
    
    // You can uncomment this to add placeholder text
    // urlInput.placeholder = exampleUrls[0];
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

# 🍜 Uber Eats Menu Scraper

A web application that scrapes Uber Eats restaurant pages to extract menu items with names, descriptions, and thumbnails, highlighting items with missing images.

## ✨ Features

- **Web Interface**: Simple, responsive web UI for entering Uber Eats URLs
- **Menu Extraction**: Automatically extracts menu items with names, prices, and descriptions
- **Image Detection**: Identifies and highlights items with missing or invalid images
- **Real-time Scraping**: Uses Selenium WebDriver to handle dynamic content
- **JSON Export**: Saves scraping results to JSON format
- **Error Handling**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Chrome browser installed
- macOS, Linux, or Windows

### Installation

1. **Clone or download the project**
   ```bash
   cd UberEatsMenuScraper
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start the web application**
   ```bash
   python3 app.py
   ```

4. **Open your browser**
   Navigate to: http://localhost:5001

## 📋 Usage

### Web Interface

1. **Enter Uber Eats URL**: Paste any Uber Eats restaurant URL
2. **Click "Scrape Menu"**: Wait 10-30 seconds for processing
3. **View Results**: See menu items with images and missing image indicators

### Command Line

You can also use the scraper directly from the command line:

```bash
python3 test_scraper.py "https://www.ubereats.com/ca/store/restaurant-name/store-id"
```

## 🏗️ Project Structure

```
UberEatsMenuScraper/
├── app.py                 # Flask web application
├── scraper.py            # Core scraping logic
├── config.py             # Configuration settings
├── test_scraper.py       # Command-line testing script
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
└── README.md            # This file
```

## 🔧 Configuration

The scraper can be configured in `config.py`:

- **Chrome Options**: Browser settings for headless operation
- **CSS Selectors**: Element selectors for menu items
- **Timeouts**: Request and page load timeouts
- **Image Validation**: Settings for detecting missing images

## 📊 Test Results

**Successfully tested with:**
- **Restaurant**: Bao House (North York)
- **Items Found**: 44 menu items (exact count)
- **Deduplication**: Working correctly (removes duplicate items)
- **Image Detection**: Identifies items with and without images
- **Data Quality**: Names, prices, descriptions, and image URLs extracted correctly

## 🌐 API Endpoints

- `GET /` - Main web interface
- `POST /api/scrape` - Scrape Uber Eats menu
- `GET /api/health` - Health check

### API Usage Example

```bash
curl -X POST http://localhost:5001/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.ubereats.com/ca/store/restaurant-name/store-id"}'
```

## 🛠️ Technical Details

### Tech Stack
- **Backend**: Python + Flask
- **Scraping**: Selenium WebDriver
- **Frontend**: HTML + CSS + JavaScript
- **Browser**: Chrome (headless)

### Key Features
- **Dynamic Content Handling**: Uses Selenium to handle JavaScript-rendered content
- **Image Validation**: Checks for placeholder images and broken links
- **Error Recovery**: Graceful handling of network issues and page changes
- **Responsive Design**: Works on desktop and mobile devices

## ⚠️ Important Notes

1. **Respectful Scraping**: The scraper includes delays and respects robots.txt
2. **Rate Limiting**: Avoid making too many requests in a short time
3. **Terms of Service**: Be aware of Uber Eats' terms of service
4. **Chrome Required**: Make sure Chrome browser is installed

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Chrome browser is installed
   - The scraper will automatically download the correct ChromeDriver

2. **Port Already in Use**
   - If port 5001 is busy, modify `app.py` to use a different port
   - On macOS, port 5000 might be used by AirPlay

3. **No Menu Items Found**
   - Check if the URL is a valid Uber Eats restaurant page
   - Some restaurants might have different page structures

4. **Slow Performance**
   - Scraping can take 10-30 seconds per restaurant
   - This is normal due to page loading and image validation

## 📈 Future Enhancements

- [ ] Batch processing for multiple restaurants
- [ ] Menu change tracking over time
- [ ] Price comparison across restaurants
- [ ] Export to CSV/Excel formats
- [ ] Restaurant category filtering
- [ ] Image download functionality

## 📄 License

This project is for educational and research purposes. Please respect Uber Eats' terms of service and use responsibly.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Built with ❤️ using Python, Flask, and Selenium**

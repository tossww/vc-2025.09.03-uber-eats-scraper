"""
Flask web application for Uber Eats menu scraper

This module provides a REST API and web interface for scraping Uber Eats
restaurant menus. It includes endpoints for scraping, health checks, and
serving the web interface.

Author: Steven Wang
Date: 2025-09-05
Version: 1.0.0
"""

from flask import Flask, render_template, request, jsonify, url_for
from flask_cors import CORS
import json
import logging
from datetime import datetime
from scraper import UberEatsScraper

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global scraper instance (will be initialized per request)
scraper = None


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/scrape', methods=['POST'])
def scrape_menu():
    """
    API endpoint for scraping Uber Eats menu
    
    Expected JSON payload:
    {
        "url": "https://www.ubereats.com/ca/store/..."
    }
    
    Returns:
    {
        "success": true/false,
        "data": {...} or null,
        "error": "error message" or null,
        "timestamp": "2025-01-01 12:00:00"
    }
    """
    global scraper
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'No JSON data provided',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'URL is required',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        # Validate URL format
        if 'ubereats.com' not in url:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'Please provide a valid Uber Eats URL',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }), 400
        
        logger.info(f"Starting scrape for URL: {url}")
        
        # Initialize scraper
        scraper = UberEatsScraper()
        
        try:
            # Scrape the restaurant
            result = scraper.scrape_restaurant(url)
            
            # Check if scraping was successful
            if 'error' in result:
                return jsonify({
                    'success': False,
                    'data': None,
                    'error': result['error'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }), 500
            
            # Return successful result
            return jsonify({
                'success': True,
                'data': result,
                'error': None,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
        finally:
            # Always clean up scraper
            if scraper:
                scraper.close()
                scraper = None
    
    except Exception as e:
        logger.error(f"Error in scrape_menu: {str(e)}")
        
        # Clean up scraper on error
        if scraper:
            try:
                scraper.close()
            except:
                pass
            scraper = None
        
        return jsonify({
            'success': False,
            'data': None,
            'error': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 500


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 405


if __name__ == '__main__':
    print("🚀 Starting Uber Eats Menu Scraper Web App...")
    print("📋 Available endpoints:")
    print("   • GET  / - Main web interface")
    print("   • POST /api/scrape - Scrape Uber Eats menu")
    print("   • GET  /api/health - Health check")
    print("🌐 Server will be available at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

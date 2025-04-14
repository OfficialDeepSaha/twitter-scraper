import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from twitter_scraper import TwitterScraper
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "twitter-scraper-secret-key")

# Initialize the scraper
scraper = TwitterScraper()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle the search form submission"""
    search_type = request.form.get('search_type')
    query = request.form.get('query', '').strip()
    limit = int(request.form.get('limit', 100))
    start_date = request.form.get('start_date', '') or None
    end_date = request.form.get('end_date', '') or None
    lang = request.form.get('lang', '') or None
    file_format = request.form.get('file_format', 'csv')
    
    if not query:
        flash('Please enter a search query', 'danger')
        return redirect(url_for('index'))
    
    try:
        # Perform search based on search type
        if search_type == 'keyword':
            df = scraper.search_by_keyword(query, limit, start_date, end_date, lang)
        elif search_type == 'hashtag':
            df = scraper.search_by_hashtag(query, limit, start_date, end_date, lang)
        elif search_type == 'user':
            df = scraper.search_by_user(query, limit, start_date, end_date)
        else:
            flash('Invalid search type', 'danger')
            return redirect(url_for('index'))
        
        # Get statistics
        stats = scraper.get_statistics()
        
        # Store data in session for download
        session['last_query'] = {
            'search_type': search_type,
            'query': query,
            'limit': limit,
            'start_date': start_date,
            'end_date': end_date,
            'lang': lang,
            'file_format': file_format
        }
        
        # Convert DataFrame to list of dicts for template
        tweets = df.to_dict('records')
        for tweet in tweets:
            if 'date' in tweet and hasattr(tweet['date'], 'isoformat'):
                tweet['date'] = tweet['date'].isoformat()
        
        # Render results page
        return render_template('results.html', 
                               tweets=tweets, 
                               stats=stats, 
                               query=query, 
                               search_type=search_type,
                               count=len(tweets))
    
    except Exception as e:
        logging.error(f"Error during search: {str(e)}")
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/download')
def download():
    """Download scraped tweets as a file"""
    file_format = request.args.get('format', 'csv')
    
    # Check if we have data to download
    if 'last_query' not in session:
        flash('No data to download. Please perform a search first.', 'warning')
        return redirect(url_for('index'))
    
    try:
        # Generate filename
        filename = None
        
        # Save data to file
        if file_format == 'csv':
            filename = scraper.save_to_csv(filename)
        else:
            filename = scraper.save_to_json(filename)
        
        if not filename:
            flash('Error generating file for download', 'danger')
            return redirect(url_for('index'))
        
        # Send file for download
        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        logging.error(f"Error during download: {str(e)}")
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('index.html', error="Server error, please try again later"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

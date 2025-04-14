# Twitter Scraper

A Python tool for scraping Twitter data using the snscrape package with both a command-line interface and a web interface.

## Features

- Search Twitter by keywords, hashtags, or usernames
- Filter results by date range and language
- Download results as CSV or JSON
- View tweet statistics and metrics
- User-friendly web interface
- Command-line interface for batch processing

## Requirements

See `packages_requirements.txt` for the required packages.

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r packages_requirements.txt
   ```

## Usage

### Web Interface

Run the web application:
```
python app.py
```

Then open your browser to http://localhost:5000/

### Command Line

Examples:

```
# Search by keyword
python twitter_scraper.py keyword "climate change" --limit 100 --start-date 2023-01-01 --end-date 2023-06-30 --lang en --format csv

# Search by hashtag
python twitter_scraper.py hashtag "AI" --limit 50 --format json

# Search by user
python twitter_scraper.py user "elonmusk" --limit 200
```

For more examples, see `twitter_scraper_cli_examples.txt`.

## File Structure

- **app.py**: Flask web application
- **twitter_scraper.py**: Core scraper functionality and CLI
- **main.py**: Entry point for the web application
- **templates/**: HTML templates for the web interface
- **static/**: CSS and JavaScript files for the web interface

## License

MIT

## Disclaimer

This tool is for educational purposes only. Please respect Twitter's terms of service.
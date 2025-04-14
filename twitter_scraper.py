import os
import snscrape.modules.twitter as sntwitter
import pandas as pd
import json
import csv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TwitterScraper:
    def __init__(self):
        """
        Initialize the TwitterScraper with default values
        """
        self.tweets_list = []
        self.df = None
    
    def search_by_keyword(self, keyword, limit=100, start_date=None, end_date=None, lang=None):
        """
        Search tweets by keyword
        
        Args:
            keyword (str): Keyword to search for
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            lang (str): Language filter (e.g., 'en' for English)
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        query = f"{keyword}"
        
        if start_date and end_date:
            query += f" since:{start_date} until:{end_date}"
        
        if lang:
            query += f" lang:{lang}"
            
        logging.info(f"Searching for tweets with query: {query}")
        
        try:
            self.tweets_list = []
            
            # Using Twitter Search to get tweets
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                
                self.tweets_list.append({
                    'date': tweet.date,
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'user': tweet.user.username,
                    'reply_count': tweet.replyCount,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'quote_count': tweet.quoteCount
                })
            
            # Creating a dataframe
            self.df = pd.DataFrame(self.tweets_list)
            logging.info(f"Successfully retrieved {len(self.tweets_list)} tweets")
            return self.df
            
        except Exception as e:
            logging.error(f"Error searching for tweets: {str(e)}")
            raise
    
    def search_by_hashtag(self, hashtag, limit=100, start_date=None, end_date=None, lang=None):
        """
        Search tweets by hashtag
        
        Args:
            hashtag (str): Hashtag to search for (with or without the # symbol)
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            lang (str): Language filter (e.g., 'en' for English)
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        # Add the # symbol if it's not already there
        if not hashtag.startswith('#'):
            hashtag = f"#{hashtag}"
            
        return self.search_by_keyword(hashtag, limit, start_date, end_date, lang)
    
    def search_by_user(self, username, limit=100, start_date=None, end_date=None):
        """
        Search tweets by Twitter user
        
        Args:
            username (str): Twitter username (with or without the @ symbol)
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        # Remove the @ symbol if it's present
        if username.startswith('@'):
            username = username[1:]
            
        query = f"from:{username}"
        
        if start_date and end_date:
            query += f" since:{start_date} until:{end_date}"
            
        logging.info(f"Searching for tweets with query: {query}")
        
        try:
            self.tweets_list = []
            
            # Using Twitter Search to get tweets
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                
                self.tweets_list.append({
                    'date': tweet.date,
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'user': tweet.user.username,
                    'reply_count': tweet.replyCount,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'quote_count': tweet.quoteCount
                })
            
            # Creating a dataframe
            self.df = pd.DataFrame(self.tweets_list)
            logging.info(f"Successfully retrieved {len(self.tweets_list)} tweets")
            return self.df
            
        except Exception as e:
            logging.error(f"Error searching for tweets: {str(e)}")
            raise
    
    def save_to_csv(self, filename=None):
        """
        Save the scraped tweets to a CSV file
        
        Args:
            filename (str, optional): Filename to save the CSV. If none provided, 
                                      a default name with timestamp will be used.
                                      
        Returns:
            str: Path to the saved file
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to save. Run a search method first.")
            return None
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.csv"
        
        try:
            self.df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)
            logging.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")
            return None
    
    def save_to_json(self, filename=None):
        """
        Save the scraped tweets to a JSON file
        
        Args:
            filename (str, optional): Filename to save the JSON. If none provided, 
                                      a default name with timestamp will be used.
                                      
        Returns:
            str: Path to the saved file
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to save. Run a search method first.")
            return None
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.json"
        
        try:
            # Convert datetime objects to strings for JSON serialization
            json_df = self.df.copy()
            if 'date' in json_df.columns:
                json_df['date'] = json_df['date'].astype(str)
                
            json_df.to_json(filename, orient='records', indent=4)
            logging.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving to JSON: {str(e)}")
            return None
    
    def get_statistics(self):
        """
        Get basic statistics about the scraped tweets
        
        Returns:
            dict: Dictionary containing statistics
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to analyze. Run a search method first.")
            return None
            
        try:
            stats = {
                'total_tweets': len(self.df),
                'average_likes': self.df['like_count'].mean(),
                'average_retweets': self.df['retweet_count'].mean(),
                'average_replies': self.df['reply_count'].mean(),
                'most_liked_tweet': self.df.loc[self.df['like_count'].idxmax()]['content'] if 'like_count' in self.df.columns else None,
                'most_retweeted_tweet': self.df.loc[self.df['retweet_count'].idxmax()]['content'] if 'retweet_count' in self.df.columns else None,
                'date_range': {
                    'earliest': self.df['date'].min(),
                    'latest': self.df['date'].max()
                }
            }
            return stats
        except Exception as e:
            logging.error(f"Error calculating statistics: {str(e)}")
            return None


if __name__ == "__main__":
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Twitter Scraping Tool using snscrape')
    
    # Define subparsers for different search types
    subparsers = parser.add_subparsers(dest='command', help='Search command')
    
    # Keyword search parser
    keyword_parser = subparsers.add_parser('keyword', help='Search by keyword')
    keyword_parser.add_argument('query', type=str, help='Keyword to search for')
    
    # Hashtag search parser
    hashtag_parser = subparsers.add_parser('hashtag', help='Search by hashtag')
    hashtag_parser.add_argument('query', type=str, help='Hashtag to search for (with or without #)')
    
    # User search parser
    user_parser = subparsers.add_parser('user', help='Search by user')
    user_parser.add_argument('query', type=str, help='Twitter username (with or without @)')
    
    # Common arguments for all search types
    for subparser in [keyword_parser, hashtag_parser, user_parser]:
        subparser.add_argument('--limit', '-l', type=int, default=100, help='Maximum number of tweets to retrieve')
        subparser.add_argument('--start-date', '-s', type=str, help='Start date (YYYY-MM-DD)')
        subparser.add_argument('--end-date', '-e', type=str, help='End date (YYYY-MM-DD)')
        subparser.add_argument('--lang', type=str, help='Language filter (e.g., en for English)')
        subparser.add_argument('--output', '-o', type=str, help='Output file path')
        subparser.add_argument('--format', '-f', choices=['csv', 'json'], default='csv', help='Output format (csv or json)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        exit(1)
    
    # Initialize scraper
    scraper = TwitterScraper()
    
    # Perform search based on command
    try:
        if args.command == 'keyword':
            df = scraper.search_by_keyword(args.query, args.limit, args.start_date, args.end_date, args.lang)
        elif args.command == 'hashtag':
            df = scraper.search_by_hashtag(args.query, args.limit, args.start_date, args.end_date, args.lang)
        elif args.command == 'user':
            df = scraper.search_by_user(args.query, args.limit, args.start_date, args.end_date)
        
        # Print basic statistics
        stats = scraper.get_statistics()
        print(f"\nFound {stats['total_tweets']} tweets")
        print(f"Average likes: {stats['average_likes']:.2f}")
        print(f"Average retweets: {stats['average_retweets']:.2f}")
        print(f"Average replies: {stats['average_replies']:.2f}")
        
        # Save to file
        if args.format == 'csv':
            filename = scraper.save_to_csv(args.output)
        else:
            filename = scraper.save_to_json(args.output)
            
        if filename:
            print(f"\nData saved to {filename}")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        exit(1)
